import telebot
from telebot import types
import sqlite3
import json
import hashlib
from datetime import datetime, timedelta
import threading
import time
import schedule
import requests
import random
import string
from typing import Dict, List, Tuple
import logging
import pytz
from decimal import Decimal

# ================= CONFIGURAÇÃO =================
TOKEN = "8306714275:AAGzNXE3TZKbe5-49YGTgNOMrJiLVxBjmLA"
ADMIN_ID = 5125563829  # 
ADMIN_USERNAME = '@ayltonanna7'
BOT_USERNAME = '@cinetobot'

# Preços dos planos VIP (em MT)
PRECOS = {
    'daily': {'nome': 'VIP Diário', 'preco': 150, 'dias': 1, 'codigos_dia': 10},
    'weekly': {'nome': 'VIP Semanal', 'preco': 800, 'dias': 7, 'codigos_dia': 15},
    'monthly': {'nome': 'VIP Mensal', 'preco': 2500, 'dias': 30, 'codigos_dia': 20},
    'premium': {'nome': 'VIP Premium', 'preco': 5000, 'dias': 90, 'codigos_dia': 30}
}

# Informações de pagamento
PAYMENT_INFO = {
    'emola': '870612404 - Ailton Armindo',
    'mpesa': '848568229 - Ailton Armindo',
    'paypal': 'ayltonanna@gmail.com',
    'whatsapp': '+258 84 856 8229'
}

bot = telebot.TeleBot(TOKEN, parse_mode='HTML')
logging.basicConfig(level=logging.INFO)

# ================= BANCO DE DADOS =================
conn = sqlite3.connect('betmaster.db', check_same_thread=False)
cursor = conn.cursor()

# Criar tabelas
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    full_name TEXT,
    is_vip INTEGER DEFAULT 0,
    vip_type TEXT,
    vip_until TEXT,
    daily_codes_used INTEGER DEFAULT 0,
    daily_codes_limit INTEGER DEFAULT 2,
    total_codes_created INTEGER DEFAULT 0,
    credits DECIMAL(10,2) DEFAULT 0.00,
    balance DECIMAL(10,2) DEFAULT 0.00,
    total_spent DECIMAL(10,2) DEFAULT 0.00,
    referral_code TEXT UNIQUE,
    referred_by INTEGER,
    referral_count INTEGER DEFAULT 0,
    created_at TEXT,
    last_active TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS codes (
    code_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    code TEXT UNIQUE,
    bet_type TEXT,
    event TEXT,
    prediction TEXT,
    odds DECIMAL(5,2),
    stake DECIMAL(10,2),
    potential_win DECIMAL(10,2),
    status TEXT DEFAULT 'pending',
    result TEXT,
    created_at TEXT,
    won_amount DECIMAL(10,2) DEFAULT 0.00,
    is_free INTEGER DEFAULT 1,
    casa_aposta TEXT,
    FOREIGN KEY (user_id) REFERENCES users (user_id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS payments (
    payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    amount DECIMAL(10,2),
    payment_method TEXT,
    transaction_id TEXT,
    status TEXT DEFAULT 'pending',
    created_at TEXT,
    approved_at TEXT,
    approved_by INTEGER,
    plan_type TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS predictions (
    prediction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    event TEXT,
    league TEXT,
    prediction TEXT,
    odds DECIMAL(5,2),
    confidence INTEGER,
    analysis TEXT,
    status TEXT DEFAULT 'upcoming',
    result TEXT,
    created_at TEXT,
    created_by INTEGER DEFAULT 0
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS statistics (
    stat_date TEXT PRIMARY KEY,
    total_users INTEGER DEFAULT 0,
    new_users INTEGER DEFAULT 0,
    active_users INTEGER DEFAULT 0,
    vip_users INTEGER DEFAULT 0,
    total_codes INTEGER DEFAULT 0,
    total_predictions INTEGER DEFAULT 0,
    total_revenue DECIMAL(10,2) DEFAULT 0.00,
    created_at TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS admin_logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    admin_id INTEGER,
    action TEXT,
    target_user_id INTEGER,
    details TEXT,
    created_at TEXT
)
''')

conn.commit()

# ================= SISTEMA DE CÓDIGOS =================
class CodeSystem:
    @staticmethod
    def generate_code(user_id: int, bet_type: str = "normal") -> str:
        """Gera um código único para aposta"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return f"BM{user_id:04d}{timestamp[-6:]}{random_str}"
    
    @staticmethod
    def can_generate_free_code(user_id: int) -> Tuple[bool, str]:
        """Verifica se usuário pode gerar código grátis"""
        cursor.execute('SELECT daily_codes_used, daily_codes_limit, is_vip FROM users WHERE user_id = ?', (user_id,))
        user = cursor.fetchone()
        
        if not user:
            return False, "Usuário não encontrado"
        
        daily_used, daily_limit, is_vip = user
        
        if daily_used >= daily_limit:
            if is_vip:
                return False, f"❌ Limite VIP atingido! Use /comprar para mais códigos"
            else:
                return False, f"❌ Limite diário grátis atingido! (2/2)\n💎 Torne-se VIP para mais códigos!"
        
        return True, f"✅ Pode gerar código ({daily_used + 1}/{daily_limit})"

# ================= SISTEMA VIP =================
class VIPSystem:
    @staticmethod
    def check_vip_status(user_id: int) -> Dict:
        """Verifica status VIP do usuário"""
        cursor.execute('''
            SELECT is_vip, vip_type, vip_until, daily_codes_limit 
            FROM users WHERE user_id = ?
        ''', (user_id,))
        
        result = cursor.fetchone()
        if not result:
            return {'is_vip': False}
        
        is_vip, vip_type, vip_until, codes_limit = result
        
        if is_vip and vip_until:
            vip_until_date = datetime.strptime(vip_until, '%Y-%m-%d %H:%M:%S')
            if vip_until_date < datetime.now():
                # VIP expirado
                cursor.execute('UPDATE users SET is_vip = 0, vip_type = NULL, vip_until = NULL WHERE user_id = ?', (user_id,))
                conn.commit()
                return {'is_vip': False}
        
        return {
            'is_vip': bool(is_vip),
            'vip_type': vip_type,
            'vip_until': vip_until,
            'daily_codes_limit': codes_limit
        }

# ================= PREDIÇÕES ESPORTIVAS =================
class PredictionEngine:
    def __init__(self):
        self.leagues = {
            'premier': 'Premier League',
            'laliga': 'La Liga',
            'seriea': 'Serie A',
            'bundesliga': 'Bundesliga',
            'liganos': 'Liga NOS',
            'champions': 'Champions League',
            'europa': 'Europa League'
        }
    
    def generate_prediction(self, league: str = None) -> Dict:
        """Gera uma previsão esportiva"""
        if not league:
            league = random.choice(list(self.leagues.keys()))
        
        teams = self.get_teams(league)
        team_home, team_away = random.sample(teams, 2)
        
        predictions = [
            {"type": "1X2", "pred": "1", "odds": random.uniform(1.5, 2.5)},
            {"type": "1X2", "pred": "X", "odds": random.uniform(3.0, 4.0)},
            {"type": "1X2", "pred": "2", "odds": random.uniform(2.0, 3.5)},
            {"type": "Over/Under", "pred": "Over 2.5", "odds": random.uniform(1.8, 2.2)},
            {"type": "Over/Under", "pred": "Under 2.5", "odds": random.uniform(1.7, 2.0)},
            {"type": "BTTS", "pred": "Sim", "odds": random.uniform(1.6, 2.1)},
            {"type": "BTTS", "pred": "Não", "odds": random.uniform(1.8, 2.4)}
        ]
        
        pred = random.choice(predictions)
        
        return {
            'event': f"{team_home} vs {team_away}",
            'league': self.leagues[league],
            'prediction': pred['pred'],
            'type': pred['type'],
            'odds': round(pred['odds'], 2),
            'confidence': random.randint(65, 92),
            'analysis': self.generate_analysis(team_home, team_away, pred['pred'])
        }
    
    def get_teams(self, league: str) -> List[str]:
        """Retorna times da liga"""
        teams_db = {
            'premier': ['Manchester City', 'Liverpool', 'Chelsea', 'Arsenal', 'Manchester Utd', 'Tottenham'],
            'laliga': ['Real Madrid', 'Barcelona', 'Atlético Madrid', 'Sevilla', 'Valencia', 'Villarreal'],
            'seriea': ['Juventus', 'Inter Milan', 'AC Milan', 'Napoli', 'Roma', 'Lazio'],
            'bundesliga': ['Bayern Munich', 'Borussia Dortmund', 'RB Leipzig', 'Bayer Leverkusen', 'Wolfsburg']
        }
        return teams_db.get(league, ['Time A', 'Time B'])
    
    def generate_analysis(self, team_home: str, team_away: str, prediction: str) -> str:
        """Gera análise para a previsão"""
        analyses = [
            f"📊 <b>Análise:</b> {team_home} tem vantagem em casa. Estatísticas mostram bom desempenho ofensivo.",
            f"📈 <b>Forma:</b> {team_away} vem de boa sequência. Defesa sólida nas últimas partidas.",
            f"⚽ <b>Confronto Direto:</b> Histórico equilibrado. Ambos times marcam frequentemente.",
            f"🎯 <b>Momento:</b> {team_home} precisa da vitória. Motivação extra para este jogo.",
            f"🛡️ <b>Defesas:</b> Ambas defesas têm mostrado fragilidades. Expectativa de gols."
        ]
        return random.choice(analyses)

# ================= HANDLERS PRINCIPAIS =================
@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name
    full_name = f"{message.from_user.first_name} {message.from_user.last_name or ''}".strip()
    
    # Registrar usuário
    cursor.execute('''
        INSERT OR IGNORE INTO users 
        (user_id, username, full_name, created_at, last_active, referral_code) 
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, username, full_name, datetime.now(), datetime.now(), 
          f"REF{user_id:06d}"))
    
    cursor.execute('UPDATE users SET last_active = ? WHERE user_id = ?', 
                  (datetime.now(), user_id))
    conn.commit()
    
    # Verificar status VIP
    vip_status = VIPSystem.check_vip_status(user_id)
    
    welcome_text = f"""
🏆 <b>BEM-VINDO AO BET MASTER PRO!</b>

👤 <b>Usuário:</b> {full_name}
🆔 <b>ID:</b> <code>{user_id}</code>
📅 <b>Cadastro:</b> {datetime.now().strftime('%d/%m/%Y')}

💎 <b>Status:</b> {'<b>VIP 🎖️</b>' if vip_status['is_vip'] else 'Grátis ⭐'}
🔢 <b>Códigos/dia:</b> {vip_status.get('daily_codes_limit', 2)}
📊 <b>VIP até:</b> {vip_status.get('vip_until', 'Não VIP')}

<b>🎯 FUNCIONALIDADES:</b>
• Gerar códigos de aposta
• Previsões especializadas
• Sistema VIP Premium
• Histórico completo
• Comparador de odds

<b>💰 PLANOS VIP:</b>
/diario - 150MT (10 códigos/dia)
/semanal - 800MT (15 códigos/dia)
/mensal - 2500MT (20 códigos/dia)
/premium - 5000MT (30 códigos/dia)

<b>⚡ COMANDOS RÁPIDOS:</b>
/gerar - Criar código de aposta
/palpites - Ver previsões
/vip - Info planos VIP
/saldo - Meu saldo
/ajuda - Ajuda completa

💡 <i>Você tem 2 códigos GRÁTIS por dia!</i>
"""
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🎯 GERAR CÓDIGO", callback_data="generate_code"),
        types.InlineKeyboardButton("💎 VER VIP", callback_data="view_vip")
    )
    markup.add(
        types.InlineKeyboardButton("📊 PALPITES", callback_data="view_predictions"),
        types.InlineKeyboardButton("💰 PAGAMENTOS", callback_data="payment_info")
    )
    markup.add(
        types.InlineKeyboardButton("👤 MEU PERFIL", callback_data="my_profile"),
        types.InlineKeyboardButton("📞 SUPORTE", url=f"https://t.me/{ADMIN_USERNAME[1:]}")
    )
    
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

@bot.message_handler(commands=['gerar'])
def generate_code_command(message):
    user_id = message.from_user.id
    
    # Verificar se pode gerar código grátis
    can_generate, msg = CodeSystem.can_generate_free_code(user_id)
    
    if not can_generate:
        bot.send_message(message.chat.id, msg)
        return
    
    # Gerar código
    code = CodeSystem.generate_code(user_id)
    
    # Registrar código
    cursor.execute('''
        INSERT INTO codes (user_id, code, created_at, is_free)
        VALUES (?, ?, ?, 1)
    ''', (user_id, code, datetime.now()))
    
    # Atualizar contador do usuário
    cursor.execute('''
        UPDATE users 
        SET daily_codes_used = daily_codes_used + 1, 
            total_codes_created = total_codes_created + 1,
            last_active = ?
        WHERE user_id = ?
    ''', (datetime.now(), user_id))
    
    conn.commit()
    
    # Verificar novo status
    cursor.execute('SELECT daily_codes_used, daily_codes_limit FROM users WHERE user_id = ?', (user_id,))
    used, limit = cursor.fetchone()
    
    # Gerar previsão
    predictor = PredictionEngine()
    prediction = predictor.generate_prediction()
    
    # Criar mensagem
    response = f"""
✅ <b>CÓDIGO GERADO COM SUCESSO!</b>

🔢 <b>Código:</b> <code>{code}</code>
📅 <b>Data:</b> {datetime.now().strftime('%d/%m/%Y %H:%M')}
🎫 <b>Tipo:</b> {'VIP 🎖️' if limit > 2 else 'Grátis ⭐'}
📊 <b>Uso:</b> {used}/{limit} códigos hoje

<b>🎯 PALPITE RECOMENDADO:</b>
⚽ <b>Jogo:</b> {prediction['event']}
🏆 <b>Liga:</b> {prediction['league']}
🔮 <b>Previsão:</b> {prediction['prediction']}
📈 <b>Odds:</b> {prediction['odds']}
💯 <b>Confiança:</b> {prediction['confidence']}%
{prediction['analysis']}

<b>🏠 CASAS RECOMENDADAS:</b>
• Betway - Melhores odds
• 1xBet - Bônus 100%
• PremierBet - Cashout rápido
• ElephantBet - Promoções diárias

<b>💡 COMO USAR:</b>
1. Acesse sua casa de apostas
2. Insira o código {code}
3. Siga o palpite recomendado
4. Ajuste o valor da aposta
5. Confirme e boa sorte!

⚠️ <i>Jogue com responsabilidade</i>
"""
    
    # Adicionar botões de ação
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("💎 COMPRAR MAIS CÓDIGOS", callback_data="buy_more_codes"),
        types.InlineKeyboardButton("📊 VER HISTÓRICO", callback_data="view_history")
    )
    markup.add(
        types.InlineKeyboardButton("🎯 NOVO PALPITE", callback_data="new_prediction"),
        types.InlineKeyboardButton("📞 SUPORTE", url=f"https://t.me/{ADMIN_USERNAME[1:]}")
    )
    
    bot.send_message(message.chat.id, response, reply_markup=markup)

@bot.message_handler(commands=['vip'])
def vip_info_command(message):
    vip_text = f"""
💎 <b>PLANOS VIP BET MASTER PRO</b>

<b>⭐ PLANO DIÁRIO - 150MT</b>
• 10 códigos por dia
• Acesso a palpites
• Suporte prioritário
• Validade: 24 horas

<b>🏆 PLANO SEMANAL - 800MT</b>
• 15 códigos por dia
• Todos benefícios Diário
• Análises exclusivas
• Validade: 7 dias

<b>👑 PLANO MENSAL - 2.500MT</b>
• 20 códigos por dia
• Todos benefícios Semanal
• Conteúdo premium
• Validade: 30 dias

<b>🚀 PLANO PREMIUM - 5.000MT</b>
• 30 códigos por dia
• Todos benefícios Mensal
• Mentoria pessoal
• Validade: 90 dias

<b>📲 FORMAS DE PAGAMENTO:</b>
• Emola: {PAYMENT_INFO['emola']}
• M-Pesa: {PAYMENT_INFO['mpesa']}
• PayPal: {PAYMENT_INFO['paypal']}
• WhatsApp: {PAYMENT_INFO['whatsapp']}

<b>⚡ COMO COMPRAR:</b>
1. Escolha seu plano
2. Faça o pagamento
3. Envie comprovante
4. Ativação em 5 minutos

💡 <i>Use /comprar para iniciar</i>
"""
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    for plan_id, plan in PRECOS.items():
        markup.add(
            types.InlineKeyboardButton(
                f"💰 {plan['nome']} - {plan['preco']}MT", 
                callback_data=f"buy_{plan_id}"
            )
        )
    markup.add(
        types.InlineKeyboardButton("📞 FALAR COM SUPORTE", url=f"https://t.me/{ADMIN_USERNAME[1:]}")
    )
    
    bot.send_message(message.chat.id, vip_text, reply_markup=markup)

@bot.message_handler(commands=['palpites'])
def predictions_command(message):
    predictor = PredictionEngine()
    
    predictions_text = """
🔮 <b>PALPITES DO DIA</b>
⏰ Atualizado: {time}

<b>⚽ JOGOS SELECIONADOS:</b>
""".format(time=datetime.now().strftime('%d/%m %H:%M'))
    
    # Gerar 3 previsões
    for i in range(3):
        pred = predictor.generate_prediction()
        predictions_text += f"""
<b>{i+1}. {pred['event']}</b>
🏆 {pred['league']}
🎯 <b>Palpite:</b> {pred['prediction']}
📈 <b>Odds:</b> {pred['odds']}
💯 <b>Confiança:</b> {pred['confidence']}%
📊 {pred['analysis']}
➖➖➖➖➖➖➖
"""
    
    predictions_text += """
<b>🏠 CASAS RECOMENDADAS:</b>
1. Betway - Odds altas
2. 1xBet - Mercados variados
3. PremierBet - App estável

<b>⚠️ AVISO LEGAL:</b>
<i>Palpites são sugestões baseadas em análise.
Não garantimos lucros. Jogue com responsabilidade.</i>
"""
    
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("🎯 GERAR CÓDIGO", callback_data="generate_code"),
        types.InlineKeyboardButton("💎 TORNAR-SE VIP", callback_data="view_vip")
    )
    
    bot.send_message(message.chat.id, predictions_text, reply_markup=markup)

# ================= ADMIN PANEL =================
@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, "❌ Acesso negado!")
        return
    
    admin_text = f"""
👑 <b>PAINEL ADMINISTRATIVO</b>

<b>📊 ESTATÍSTICAS:</b>
• Total usuários: {get_total_users()}
• Usuários VIP: {get_vip_users_count()}
• Códigos gerados: {get_total_codes()}
• Receita total: {get_total_revenue()}MT

<b>⚙️ FUNÇÕES:</b>
/estatisticas - Estatísticas detalhadas
/usuarios - Gerenciar usuários
/vipmanual - Ativar VIP manual
/pagamentos - Gerenciar pagamentos
/broadcast - Enviar mensagem a todos

<b>📈 HOJE:</b>
• Novos usuários: {get_today_users()}
• Códigos gerados: {get_today_codes()}
• Pagamentos: {get_today_payments()}MT
"""
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("📊 ESTATÍSTICAS", callback_data="admin_stats"),
        types.InlineKeyboardButton("👤 USUÁRIOS", callback_data="admin_users")
    )
    markup.add(
        types.InlineKeyboardButton("💰 PAGAMENTOS", callback_data="admin_payments"),
        types.InlineKeyboardButton("🎫 CÓDIGOS", callback_data="admin_codes")
    )
    markup.add(
        types.InlineKeyboardButton("📢 BROADCAST", callback_data="admin_broadcast"),
        types.InlineKeyboardButton("⚙️ CONFIGURAÇÕES", callback_data="admin_config")
    )
    
    bot.send_message(message.chat.id, admin_text, reply_markup=markup)

@bot.message_handler(commands=['vipmanual'])
def manual_vip_activation(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    msg = bot.send_message(message.chat.id, "Digite o ID do usuário para ativar VIP:")
    bot.register_next_step_handler(msg, process_vip_activation)

def process_vip_activation(message):
    try:
        user_id = int(message.text)
        
        markup = types.InlineKeyboardMarkup(row_width=2)
        for plan_id, plan in PRECOS.items():
            markup.add(
                types.InlineKeyboardButton(
                    plan['nome'], 
                    callback_data=f"admin_activate_{plan_id}_{user_id}"
                )
            )
        
        bot.send_message(message.chat.id, f"Escolha o plano para o usuário {user_id}:", reply_markup=markup)
    except:
        bot.send_message(message.chat.id, "❌ ID inválido!")

@bot.message_handler(commands=['estatisticas'])
def statistics_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    stats_text = f"""
📈 <b>ESTATÍSTICAS COMPLETAS</b>

<b>👥 USUÁRIOS:</b>
• Total: {get_total_users()}
• VIPs: {get_vip_users_count()}
• Novos hoje: {get_today_users()}
• Ativos hoje: {get_active_today()}

<b>🎫 CÓDIGOS:</b>
• Total: {get_total_codes()}
• Hoje: {get_today_codes()}
• Grátis: {get_free_codes_count()}
• VIP: {get_vip_codes_count()}

<b>💰 FINANCEIRO:</b>
• Receita total: {get_total_revenue()}MT
• Hoje: {get_today_payments()}MT
• VIP Diário: {get_plan_revenue('daily')}MT
• VIP Semanal: {get_plan_revenue('weekly')}MT
• VIP Mensal: {get_plan_revenue('monthly')}MT
• VIP Premium: {get_plan_revenue('premium')}MT

<b>📅 ÚLTIMOS 7 DIAS:</b>
• Novos usuários: {get_last_7_days_users()}
• Receita: {get_last_7_days_revenue()}MT

<b>🏆 TOP USUÁRIOS:</b>
"""
    
    # Top usuários por códigos gerados
    cursor.execute('''
        SELECT username, total_codes_created 
        FROM users 
        ORDER BY total_codes_created DESC 
        LIMIT 5
    ''')
    
    for i, (username, codes) in enumerate(cursor.fetchall(), 1):
        stats_text += f"{i}. @{username}: {codes} códigos\n"
    
    bot.send_message(message.chat.id, stats_text)

# ================= FUNÇÕES DE SUPORTE =================
def get_total_users():
    cursor.execute('SELECT COUNT(*) FROM users')
    return cursor.fetchone()[0]

def get_vip_users_count():
    cursor.execute('SELECT COUNT(*) FROM users WHERE is_vip = 1')
    return cursor.fetchone()[0]

def get_total_codes():
    cursor.execute('SELECT COUNT(*) FROM codes')
    return cursor.fetchone()[0]

def get_total_revenue():
    cursor.execute('SELECT SUM(amount) FROM payments WHERE status = "approved"')
    result = cursor.fetchone()[0]
    return result if result else 0.00

def get_today_users():
    today = datetime.now().strftime('%Y-%m-%d')
    cursor.execute('SELECT COUNT(*) FROM users WHERE DATE(created_at) = ?', (today,))
    return cursor.fetchone()[0]

def get_today_codes():
    today = datetime.now().strftime('%Y-%m-%d')
    cursor.execute('SELECT COUNT(*) FROM codes WHERE DATE(created_at) = ?', (today,))
    return cursor.fetchone()[0]

def get_today_payments():
    today = datetime.now().strftime('%Y-%m-%d')
    cursor.execute('SELECT SUM(amount) FROM payments WHERE DATE(created_at) = ? AND status = "approved"', (today,))
    result = cursor.fetchone()[0]
    return result if result else 0.00

def get_plan_revenue(plan_type):
    cursor.execute('SELECT SUM(amount) FROM payments WHERE plan_type = ? AND status = "approved"', (plan_type,))
    result = cursor.fetchone()[0]
    return result if result else 0.00

def get_free_codes_count():
    cursor.execute('SELECT COUNT(*) FROM codes WHERE is_free = 1')
    return cursor.fetchone()[0]

def get_vip_codes_count():
    cursor.execute('SELECT COUNT(*) FROM codes WHERE is_free = 0')
    return cursor.fetchone()[0]

def get_active_today():
    today = datetime.now().strftime('%Y-%m-%d')
    cursor.execute('SELECT COUNT(*) FROM users WHERE DATE(last_active) = ?', (today,))
    return cursor.fetchone()[0]

def get_last_7_days_users():
    week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    cursor.execute('SELECT COUNT(*) FROM users WHERE DATE(created_at) >= ?', (week_ago,))
    return cursor.fetchone()[0]

def get_last_7_days_revenue():
    week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    cursor.execute('SELECT SUM(amount) FROM payments WHERE DATE(created_at) >= ? AND status = "approved"', (week_ago,))
    result = cursor.fetchone()[0]
    return result if result else 0.00

# ================= CALLBACK HANDLERS =================
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.from_user.id
    
    if call.data == "generate_code":
        generate_code_command(call.message)
    
    elif call.data == "view_vip":
        vip_info_command(call.message)
    
    elif call.data == "view_predictions":
        predictions_command(call.message)
    
    elif call.data == "my_profile":
        # Mostrar perfil do usuário
        cursor.execute('''
            SELECT username, is_vip, vip_type, daily_codes_used, daily_codes_limit, 
                   total_codes_created, balance, total_spent, created_at
            FROM users WHERE user_id = ?
        ''', (user_id,))
        
        user = cursor.fetchone()
        if user:
            profile_text = f"""
👤 <b>MEU PERFIL</b>

📛 <b>Usuário:</b> @{user[0]}
💎 <b>VIP:</b> {'Sim (' + user[2] + ')' if user[1] else 'Não'}
🔢 <b>Códigos hoje:</b> {user[3]}/{user[4]}
📊 <b>Total códigos:</b> {user[5]}
💰 <b>Saldo:</b> {user[6]}MT
💸 <b>Total gasto:</b> {user[7]}MT
📅 <b>Membro desde:</b> {user[8][:10] if user[8] else 'N/A'}

<b>🏆 CONQUISTAS:</b>
• Gerador de códigos
• Usuário ativo
{f'• VIP {user[2]}' if user[1] else ''}
"""
            bot.send_message(call.message.chat.id, profile_text)
    
    elif call.data.startswith("buy_"):
        plan_id = call.data[4:]
        plan = PRECOS.get(plan_id)
        
        if plan:
            payment_text = f"""
💰 <b>COMPRA DO PLANO {plan['nome'].upper()}</b>

<b>📋 DETALHES:</b>
• Plano: {plan['nome']}
• Preço: {plan['preco']}MT
• Códigos/dia: {plan['codigos_dia']}
• Validade: {plan['dias']} dias

<b>💳 FORMAS DE PAGAMENTO:</b>
1. <b>Emola:</b> {PAYMENT_INFO['emola']}
2. <b>M-Pesa:</b> {PAYMENT_INFO['mpesa']}
3. <b>PayPal:</b> {PAYMENT_INFO['paypal']}

<b>📲 WHATSAPP:</b> {PAYMENT_INFO['whatsapp']}

<b>⚡ PROCEDIMENTO:</b>
1. Faça o pagamento de {plan['preco']}MT
2. Envie comprovante para @{ADMIN_USERNAME[1:]}
3. Aguarde ativação (5-10 minutos)
4. Receba confirmação aqui

<b>⚠️ IMPORTANTE:</b>
• Inclua seu ID: <code>{user_id}</code>
• Mantenha o comprovante
• Ativação manual pelo admin

🎉 <i>Obrigado por escolher Bet Master Pro!</i>
"""
            bot.send_message(call.message.chat.id, payment_text)

# ================= FUNÇÕES DE MANUTENÇÃO =================
def reset_daily_counts():
    """Reseta contadores diários dos usuários"""
    cursor.execute('UPDATE users SET daily_codes_used = 0')
    conn.commit()
    logging.info("Contadores diários resetados")

def check_expired_vips():
    """Verifica e remove VIPs expirados"""
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
        UPDATE users 
        SET is_vip = 0, vip_type = NULL, vip_until = NULL, daily_codes_limit = 2
        WHERE vip_until < ? AND is_vip = 1
    ''', (now,))
    conn.commit()
    
    expired_count = cursor.rowcount
    if expired_count:
        logging.info(f"{expired_count} VIPs expirados removidos")

# Agendar tarefas
schedule.every().day.at("00:00").do(reset_daily_counts)
schedule.every().hour.do(check_expired_vips)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

# ================= INICIAR BOT =================
if __name__ == '__main__':
    print("""
    ╔══════════════════════════════════════╗
    ║      🏆 BET MASTER PRO BOT          ║
    ║      Iniciando sistema...           ║
    ╚══════════════════════════════════════╝
    """)
    
    # Iniciar scheduler em thread separada
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    
    print("✅ Scheduler iniciado")
    print(f"🤖 Bot iniciado como: {BOT_USERNAME}")
    print(f"👑 Admin: {ADMIN_USERNAME}")
    print("🔧 Sistema pronto para uso!")
    
    try:
        bot.polling(none_stop=True, interval=0)
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        conn.close()

