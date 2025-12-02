"""
🎬 CINEMA PRO PREMIUM BOT v4.5
Sistema profissional de distribuição de conteúdo audiovisual
Configurado para: @ayltonanna7 (Admin)
Versão: 4.5.0 | Python 3.10+
"""

import os
import logging
import telebot
import sqlite3
import time
import random
import hashlib
import threading
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from telebot.types import (
    InlineKeyboardMarkup, 
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton
)

# ======================
# 🔧 CONFIGURAÇÃO PERSONALIZADA
# ======================
TOKEN = "8306714275:AAGzNXE3TZKbe5-49YGTgNOMrJiLVxBjmLA"
ADMIN_USERNAME = "ayltonanna7"
ADMIN_ID = 5125563829

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('cinema_pro.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

bot = telebot.TeleBot(TOKEN, parse_mode='HTML')
app = Flask(__name__)

# ======================
# 💎 SISTEMA PREMIUM
# ======================
CONTATOS = {
    'whatsapp': '848568229',
    'telegram': '@ayltonanna7',
    'email': 'ayltonanna7@gmail.com',
    'mpesa': '848568229',
    'emola': '870612404',
    'paypal': 'ayltonanna7@gmail.com'
}

# ======================
# 🗄️ SISTEMA DE BANCO DE DADOS
# ======================
class DatabaseManager:
    """Gerenciador avançado do banco de dados"""
    
    def __init__(self, db_name='cinema_premium.db'):
        self.db_name = db_name
        self.init_database()
    
    def get_connection(self):
        """Cria conexão com o banco de dados"""
        conn = sqlite3.connect(self.db_name, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """Inicializa todas as tabelas do sistema"""
        tables = [
            """
            CREATE TABLE IF NOT EXISTS usuarios (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                creditos INTEGER DEFAULT 0,
                vip INTEGER DEFAULT 0,
                vip_expira TIMESTAMP,
                data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ultimo_acesso TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                total_pedidos INTEGER DEFAULT 0,
                indicacoes INTEGER DEFAULT 0,
                status TEXT DEFAULT 'ativo',
                is_admin INTEGER DEFAULT 0
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS pedidos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                username TEXT,
                conteudo TEXT,
                categoria TEXT,
                status TEXT DEFAULT 'pendente',
                data_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                data_entrega TIMESTAMP,
                moderador TEXT,
                FOREIGN KEY (user_id) REFERENCES usuarios (user_id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS transacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                tipo TEXT,
                valor INTEGER,
                descricao TEXT,
                referencia TEXT UNIQUE,
                data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'completo',
                FOREIGN KEY (user_id) REFERENCES usuarios (user_id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS grupos (
                group_id INTEGER PRIMARY KEY,
                group_title TEXT,
                ativo INTEGER DEFAULT 1,
                data_adicao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ultima_recomendacao TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT,
                user_id INTEGER,
                descricao TEXT,
                data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS catalogo_acessos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                categoria TEXT,
                data_acesso TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS suporte_tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                assunto TEXT,
                mensagem TEXT,
                status TEXT DEFAULT 'aberto',
                data_abertura TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                data_resolucao TIMESTAMP,
                admin_resposta TEXT
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS anuncios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT,
                mensagem TEXT,
                enviado_para TEXT,
                total_enviados INTEGER DEFAULT 0,
                data_envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                admin_enviou TEXT
            )
            """
        ]
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        for table_sql in tables:
            cursor.execute(table_sql)
        
        # Criar índices para performance
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_usuarios_status ON usuarios(status)",
            "CREATE INDEX IF NOT EXISTS idx_pedidos_status ON pedidos(status)",
            "CREATE INDEX IF NOT EXISTS idx_pedidos_user ON pedidos(user_id)",
            "CREATE INDEX IF NOT EXISTS idx_transacoes_user ON transacoes(user_id)",
            "CREATE INDEX IF NOT EXISTS idx_transacoes_ref ON transacoes(referencia)"
        ]
        
        for index_sql in indexes:
            try:
                cursor.execute(index_sql)
            except:
                pass
        
        # Garantir que o admin exista na tabela
        cursor.execute(
            "INSERT OR IGNORE INTO usuarios (user_id, username, is_admin) VALUES (?, ?, ?)",
            (ADMIN_ID, ADMIN_USERNAME, 1)
        )
        
        conn.commit()
        conn.close()
        logger.info("Banco de dados inicializado com sucesso")
    
    def log_event(self, tipo, user_id=None, descricao=""):
        """Registra evento no sistema de logs"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO logs (tipo, user_id, descricao) VALUES (?, ?, ?)",
            (tipo, user_id, descricao)
        )
        conn.commit()
        conn.close()

db = DatabaseManager()

# ======================
# 🎬 SISTEMA DE CATÁLOGO COMPLETO
# ======================
class CatalogoManager:
    """Gerenciador do catálogo de conteúdo"""
    
    CATEGORIAS = {
        'acao': '🎬 AÇÃO',
        'aventura': '🌍 AVENTURA',
        'animacao': '🎥 ANIMAÇÃO',
        'series': '📺 SÉRIES',
        'animes': '🎌 ANIMES',
        'lancamentos': '🚀 LANÇAMENTOS',
        'drama': '🎭 DRAMA',
        'comedia': '😂 COMÉDIA',
        'terror': '👻 TERROR',
        'documentario': '📚 DOCUMENTÁRIO'
    }
    
    CONTEUDO = {
        'acao': [
            {
                'id': 'venom3',
                'titulo': 'VENOM 3: A ÚLTIMA BATALHA',
                'ano': '2025',
                'duracao': '2h 18m',
                'qualidade': '4K HDR • Dolby Atmos',
                'genero': 'Ação • Ficção Científica',
                'descricao': 'Eddie Brock e Venom enfrentam seu maior desafio contra um inimigo simbiótico global que ameaça destruir a humanidade.',
                'trailer': 'https://youtu.be/venom3-trailer',
                'disponivel': True,
                'popularidade': 95
            },
            {
                'id': 'johnwick5',
                'titulo': 'JOHN WICK 5: LEGADO',
                'ano': '2025',
                'duracao': '2h 35m',
                'qualidade': '4K HDR • Dolby Vision',
                'genero': 'Ação • Thriller',
                'descricao': 'John Wick retorna para seu confronto mais perigoso contra a Alta Câmara em uma batalha global.',
                'trailer': 'https://youtu.be/johnwick5-trailer',
                'disponivel': True,
                'popularidade': 92
            },
            {
                'id': 'mission9',
                'titulo': 'MISSION: IMPOSSIBLE 9',
                'ano': '2025',
                'duracao': '2h 48m',
                'qualidade': '4K IMAX • Dolby Atmos',
                'genero': 'Ação • Espionagem',
                'descricao': 'Ethan Hunt enfrenta sua missão mais impossível contra uma IA global que ameaça o mundo.',
                'trailer': 'https://youtu.be/mission9-trailer',
                'disponivel': True,
                'popularidade': 90
            }
        ],
        'aventura': [
            {
                'id': 'avatar4',
                'titulo': 'AVATAR 4: O LEGADO',
                'ano': '2025',
                'duracao': '3h 02m',
                'qualidade': '4K Dolby Vision • IMAX',
                'genero': 'Aventura • Ficção Científica',
                'descricao': 'A saga continua em novos mundos com criaturas extraordinárias e batalhas épicas por Pandora.',
                'trailer': 'https://youtu.be/avatar4-trailer',
                'disponivel': True,
                'popularidade': 94
            },
            {
                'id': 'indiana6',
                'titulo': 'INDIANA JONES 6',
                'ano': '2025',
                'duracao': '2h 25m',
                'qualidade': '4K HDR • Atmos',
                'genero': 'Aventura • Ação',
                'descricao': 'A última aventura do arqueólogo mais famoso em busca de um artefato ancestral perdido.',
                'trailer': 'https://youtu.be/indiana6-trailer',
                'disponivel': True,
                'popularidade': 88
            }
        ],
        'animacao': [
            {
                'id': 'spiderman',
                'titulo': 'SPIDER-MAN: BEYOND THE SPIDER-VERSE',
                'ano': '2025',
                'duracao': '2h 28m',
                'qualidade': '4K HDR • Animação',
                'genero': 'Ação • Animação • Super-herói',
                'descricao': 'Miles Morales enfrenta o multiverso em uma aventura visualmente deslumbrante.',
                'trailer': 'https://youtu.be/spiderman-trailer',
                'disponivel': True,
                'popularidade': 96
            },
            {
                'id': 'frozen3',
                'titulo': 'FROZEN 3: O REINO DE GELO',
                'ano': '2025',
                'duracao': '1h 55m',
                'qualidade': '4K HDR • Animação',
                'genero': 'Animação • Aventura • Musical',
                'descricao': 'Elsa e Anna descobrem um reino ancestral de gelo com segredos familiares.',
                'trailer': 'https://youtu.be/frozen3-trailer',
                'disponivel': True,
                'popularidade': 89
            }
        ],
        'series': [
            {
                'id': 'stranger5',
                'titulo': 'STRANGER THINGS 5 - TEMPORADA COMPLETA',
                'ano': '2025',
                'duracao': '8 Episódios',
                'qualidade': '4K Dolby Vision',
                'genero': 'Suspense • Ficção Científica • Drama',
                'descricao': 'A temporada final que encerra a saga de Hawkins e o Mundo Invertido.',
                'trailer': 'https://youtu.be/stranger5-trailer',
                'disponivel': True,
                'popularidade': 97
            },
            {
                'id': 'lastofus3',
                'titulo': 'THE LAST OF US 3 - TODOS OS EPISÓDIOS',
                'ano': '2025',
                'duracao': '10 Episódios',
                'qualidade': '4K HDR',
                'genero': 'Drama • Ação • Pós-apocalíptico',
                'descricao': 'Continua a jornada emocionante em um mundo devastado por infecção.',
                'trailer': 'https://youtu.be/lastofus3-trailer',
                'disponivel': True,
                'popularidade': 93
            }
        ],
        'animes': [
            {
                'id': 'demonslayer',
                'titulo': 'DEMON SLAYER: FINAL ARC',
                'ano': '2025',
                'duracao': 'Arco Final Completo',
                'qualidade': '4K • Japonês Legendado',
                'genero': 'Anime • Ação • Fantasia',
                'descricao': 'O confronto final entre Tanjiro e Muzan Kibutsuji.',
                'trailer': 'https://youtu.be/demonslayer-trailer',
                'disponivel': True,
                'popularidade': 98
            },
            {
                'id': 'attacktitan',
                'titulo': 'ATTACK ON TITAN: FINAL CHAPTERS',
                'ano': '2025',
                'duracao': 'Capítulos Finais',
                'qualidade': '4K HDR • Legendado PT-BR',
                'genero': 'Anime • Ação • Drama',
                'descricao': 'O épico final da batalha pela humanidade.',
                'trailer': 'https://youtu.be/aot-final-trailer',
                'disponivel': True,
                'popularidade': 99
            }
        ],
        'lancamentos': [
            {
                'id': 'deadpool4',
                'titulo': 'DEADPOOL 4: WOLVERINE RETURNS',
                'ano': '2025',
                'duracao': '2h 15m',
                'qualidade': '4K HDR • Ação',
                'genero': 'Ação • Comédia • Super-herói',
                'descricao': 'Deadpool e Wolverine se unem em uma aventura multiversal cheia de humor.',
                'trailer': 'https://youtu.be/deadpool4-trailer',
                'disponivel': True,
                'popularidade': 96
            },
            {
                'id': 'blackpanther3',
                'titulo': 'BLACK PANTHER 3: WAKANDA FOREVER 2',
                'ano': '2025',
                'duracao': '2h 45m',
                'qualidade': '4K IMAX • Dolby Vision',
                'genero': 'Ação • Ficção Científica',
                'descricao': 'O novo protetor de Wakanda enfrenta ameaças globais e conflitos internos.',
                'trailer': 'https://youtu.be/blackpanther3-trailer',
                'disponivel': True,
                'popularidade': 94
            }
        ]
    }
    
    @staticmethod
    def get_categoria(categoria_id):
        """Retorna conteúdo de uma categoria específica"""
        return CatalogoManager.CONTEUDO.get(categoria_id, [])
    
    @staticmethod
    def buscar_conteudo(termo):
        """Busca conteúdo por termo"""
        resultados = []
        termo = termo.lower()
        
        for categoria, conteudos in CatalogoManager.CONTEUDO.items():
            for conteudo in conteudos:
                if (termo in conteudo['titulo'].lower() or 
                    termo in conteudo['genero'].lower() or
                    termo in str(conteudo['ano'])):
                    conteudo['categoria'] = categoria
                    resultados.append(conteudo)
        
        return resultados[:10]

# ======================
# 🔐 SISTEMA DE SEGURANÇA E ADMIN
# ======================
class SecurityManager:
    """Gerenciador de segurança e permissões"""
    
    @staticmethod
    def is_admin(user_id, username=None):
        """Verifica se usuário é administrador"""
        if user_id == ADMIN_ID:
            return True
        
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT is_admin FROM usuarios WHERE user_id = ?",
            (user_id,)
        )
        result = cursor.fetchone()
        conn.close()
        
        return result and result['is_admin'] == 1
    
    @staticmethod
    def is_vip(user_id):
        """Verifica se usuário tem VIP ativo"""
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT vip, vip_expira FROM usuarios WHERE user_id = ?",
            (user_id,)
        )
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            return False
        
        vip, vip_expira = result['vip'], result['vip_expira']
        if vip == 1 and vip_expira:
            try:
                return datetime.now() < datetime.fromisoformat(vip_expira)
            except:
                return False
        
        return vip == 1
    
    @staticmethod
    def gerar_referencia():
        """Gera referência única para transações"""
        timestamp = str(time.time())
        rand = str(random.randint(1000, 9999))
        hash_obj = hashlib.md5((timestamp + rand).encode())
        return hash_obj.hexdigest()[:8].upper()

# ======================
# 💰 SISTEMA DE PAGAMENTOS
# ======================
class PaymentManager:
    """Gerenciador de sistema de pagamentos"""
    
    PLANOS_VIP = {
        'mensal': {
            'nome': '💎 VIP MENSAL',
            'preco': 50,
            'moeda': 'MZN',
            'creditos': 10,
            'dias': 30,
            'vantagens': [
                '10 créditos mensais',
                'Suporte prioritário',
                'Acesso antecipado'
            ]
        },
        'trimestral': {
            'nome': '🔥 VIP TRIMESTRAL',
            'preco': 120,
            'moeda': 'MZN',
            'creditos': 35,
            'dias': 90,
            'vantagens': [
                '35 créditos (5 bônus)',
                'Economia de 30 MZN',
                'Todos benefícios VIP'
            ]
        },
        'semestral': {
            'nome': '👑 VIP SEMESTRAL',
            'preco': 200,
            'moeda': 'MZN',
            'creditos': 80,
            'dias': 180,
            'vantagens': [
                '80 créditos (20 bônus)',
                'Melhor custo-benefício',
                'Status exclusivo'
            ]
        }
    }
    
    @staticmethod
    def get_planos_markup():
        """Retorna markup com botões para planos VIP"""
        markup = InlineKeyboardMarkup(row_width=1)
        
        for plano_id, plano in PaymentManager.PLANOS_VIP.items():
            markup.add(InlineKeyboardButton(
                f"{plano['nome']} - {plano['preco']} {plano['moeda']}",
                callback_data=f"vip_{plano_id}"
            ))
        
        markup.add(
            InlineKeyboardButton("💎 Créditos Avulsos", callback_data="comprar_creditos"),
            InlineKeyboardButton("🔙 Voltar", callback_data="menu_principal")
        )
        
        return markup

# ======================
# 👑 SISTEMA ADMIN COMPLETO
# ======================
class AdminManager:
    """Gerenciador de funções administrativas"""
    
    @staticmethod
    def get_admin_panel_markup():
        """Retorna markup do painel administrativo"""
        markup = InlineKeyboardMarkup(row_width=2)
        
        botoes_admin = [
            InlineKeyboardButton("📊 Estatísticas", callback_data="admin_stats"),
            InlineKeyboardButton("👥 Usuários", callback_data="admin_users"),
            InlineKeyboardButton("📨 Pedidos", callback_data="admin_pedidos"),
            InlineKeyboardButton("💰 Transações", callback_data="admin_transacoes"),
            InlineKeyboardButton("📢 Enviar Anúncio", callback_data="admin_broadcast"),
            InlineKeyboardButton("⚙️ Configurações", callback_data="admin_config"),
            InlineKeyboardButton("📞 Tickets Suporte", callback_data="admin_tickets"),
            InlineKeyboardButton("🔄 Atualizar", callback_data="admin_refresh"),
            InlineKeyboardButton("❌ Fechar", callback_data="admin_close")
        ]
        
        # Organizar em linhas de 2 botões
        for i in range(0, len(botoes_admin) - 1, 2):
            markup.row(botoes_admin[i], botoes_admin[i + 1])
        
        # Último botão sozinho
        markup.row(botoes_admin[-1])
        
        return markup
    
    @staticmethod
    def get_admin_stats():
        """Retorna estatísticas do sistema"""
        conn = db.get_connection()
        cursor = conn.cursor()
        
        stats = {}
        
        # Total de usuários
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        stats['total_usuarios'] = cursor.fetchone()[0]
        
        # Novos usuários hoje
        cursor.execute("""
            SELECT COUNT(*) FROM usuarios 
            WHERE date(data_cadastro) = date('now')
        """)
        stats['novos_hoje'] = cursor.fetchone()[0]
        
        # Total de pedidos
        cursor.execute("SELECT COUNT(*) FROM pedidos")
        stats['total_pedidos'] = cursor.fetchone()[0]
        
        # Pedidos pendentes
        cursor.execute("SELECT COUNT(*) FROM pedidos WHERE status = 'pendente'")
        stats['pedidos_pendentes'] = cursor.fetchone()[0]
        
        # Pedidos hoje
        cursor.execute("""
            SELECT COUNT(*) FROM pedidos 
            WHERE date(data_pedido) = date('now')
        """)
        stats['pedidos_hoje'] = cursor.fetchone()[0]
        
        # Total de créditos
        cursor.execute("SELECT SUM(creditos) FROM usuarios")
        stats['total_creditos'] = cursor.fetchone()[0] or 0
        
        # VIPs ativos
        cursor.execute("SELECT COUNT(*) FROM usuarios WHERE vip = 1")
        stats['vips_ativos'] = cursor.fetchone()[0]
        
        # Grupos ativos
        cursor.execute("SELECT COUNT(*) FROM grupos WHERE ativo = 1")
        stats['grupos_ativos'] = cursor.fetchone()[0]
        
        # Transações hoje
        cursor.execute("""
            SELECT COUNT(*) FROM transacoes 
            WHERE date(data) = date('now')
        """)
        stats['transacoes_hoje'] = cursor.fetchone()[0]
        
        conn.close()
        
        return stats

# ======================
# 🤖 HANDLERS PRINCIPAIS
# ======================
@bot.message_handler(commands=['start', 'inicio'])
def start_command(message):
    """Comando inicial do bot"""
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name
    first_name = message.from_user.first_name
    
    # Registrar/Atualizar usuário
    conn = db.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT OR REPLACE INTO usuarios 
        (user_id, username, first_name, ultimo_acesso)
        VALUES (?, ?, ?, CURRENT_TIMESTAMP)
    """, (user_id, username, first_name))
    
    # Verificar se é novo usuário
    cursor.execute("SELECT data_cadastro FROM usuarios WHERE user_id = ?", (user_id,))
    user_data = cursor.fetchone()
    
    is_novo = False
    if user_data and datetime.now().date() == datetime.fromisoformat(user_data['data_cadastro']).date():
        is_novo = True
        # Dar créditos iniciais para novos usuários
        cursor.execute("""
            UPDATE usuarios 
            SET creditos = creditos + 3 
            WHERE user_id = ?
        """, (user_id,))
        
        cursor.execute("""
            INSERT INTO transacoes 
            (user_id, tipo, valor, descricao, referencia)
            VALUES (?, ?, ?, ?, ?)
        """, (
            user_id,
            'bonus_boas_vindas',
            3,
            'Créditos iniciais para novo usuário',
            SecurityManager.gerar_referencia()
        ))
    
    # Obter informações do usuário
    cursor.execute("""
        SELECT creditos, vip, vip_expira, total_pedidos 
        FROM usuarios 
        WHERE user_id = ?
    """, (user_id,))
    usuario = cursor.fetchone()
    
    creditos = usuario['creditos'] if usuario else 0
    vip = usuario['vip'] if usuario else 0
    vip_expira = usuario['vip_expira'] if usuario else None
    total_pedidos = usuario['total_pedidos'] if usuario else 0
    
    # Determinar status VIP
    if vip == 1 and vip_expira:
        try:
            expira_date = datetime.fromisoformat(vip_expira)
            if datetime.now() < expira_date:
                vip_status = f"✅ ATIVO (até {expira_date.strftime('%d/%m/%Y')})"
            else:
                vip_status = "❌ EXPIRADO"
        except:
            vip_status = "✅ ATIVO"
    elif vip == 1:
        vip_status = "✅ ATIVO"
    else:
        vip_status = "❌ INATIVO"
    
    conn.commit()
    conn.close()
    
    # Log do evento
    db.log_event('start', user_id, f"Usuário {username} acessou o bot")
    
    # Criar teclado de resposta
    markup = InlineKeyboardMarkup(row_width=2)
    
    botoes = [
        InlineKeyboardButton("🎬 Catálogo", callback_data="catalogo"),
        InlineKeyboardButton("🎥 Trailers", callback_data="trailers"),
        InlineKeyboardButton("💎 Comprar Créditos", callback_data="comprar_creditos"),
        InlineKeyboardButton("👑 Planos VIP", callback_data="planos_vip"),
        InlineKeyboardButton("📦 Meus Pedidos", callback_data="meus_pedidos"),
        InlineKeyboardButton("📊 Meu Perfil", callback_data="meu_perfil"),
        InlineKeyboardButton("🆘 Suporte", callback_data="suporte"),
        InlineKeyboardButton("📋 Comandos", callback_data="comandos")
    ]
    
    # Organizar botões em linhas
    for i in range(0, len(botoes), 2):
        markup.row(botoes[i], botoes[i + 1])
    
    # Adicionar botão admin se for administrador
    if SecurityManager.is_admin(user_id, username):
        markup.row(InlineKeyboardButton("👑 Painel Admin", callback_data="admin_panel"))
    
    mensagem_boas_vindas = f"""
🎬 <b>CINEMA PRO PREMIUM</b> 🎬

👋 <b>Olá, {first_name}!</b>

💎 <b>SEU STATUS:</b>
├─ Créditos: <code>{creditos}</code>
├─ VIP: <b>{vip_status}</b>
├─ Pedidos realizados: <code>{total_pedidos}</code>
└─ Status: <b>Ativo</b>

{f'🎁 <b>BÔNUS DE BOAS-VINDAS:</b> +3 créditos gratuitos!' if is_novo else ''}

⚡ <b>O QUE VOCÊ PODE FAZER:</b>
• Assistir trailers exclusivos
• Solicitar filmes/séries em 4K
• Acompanhar seus pedidos
• Comprar créditos ou VIP
• Receber recomendações diárias

💫 <b>QUALIDADE GARANTIDA:</b>
• Conteúdo em 4K HDR
• Entrega em 15-30 minutos
• Suporte 24/7
• Sistema automatizado

👇 <b>ESCOLHA UMA OPÇÃO:</b>
    """
    
    bot.send_message(
        chat_id=message.chat.id,
        text=mensagem_boas_vindas,
        reply_markup=markup,
        parse_mode='HTML'
    )

@bot.message_handler(commands=['admin'])
def admin_command(message):
    """Painel administrativo"""
    user_id = message.from_user.id
    username = message.from_user.username
    
    if not SecurityManager.is_admin(user_id, username):
        bot.reply_to(message, "❌ <b>Acesso negado!</b> Apenas administradores podem usar este comando.", parse_mode='HTML')
        return
    
    stats = AdminManager.get_admin_stats()
    
    mensagem_admin = f"""
👑 <b>PAINEL ADMINISTRATIVO</b> 👑
👤 <i>Administrador: @{ADMIN_USERNAME}</i>

📊 <b>ESTATÍSTICAS DO SISTEMA:</b>
├─ 👥 Total Usuários: <code>{stats['total_usuarios']}</code>
├─ 🆕 Novos Hoje: <code>{stats['novos_hoje']}</code>
├─ 📨 Total Pedidos: <code>{stats['total_pedidos']}</code>
├─ ⏳ Pendentes: <code>{stats['pedidos_pendentes']}</code>
├─ 📅 Pedidos Hoje: <code>{stats['pedidos_hoje']}</code>
├─ 💎 Créditos em Circulação: <code>{stats['total_creditos']}</code>
├─ 👑 VIPs Ativos: <code>{stats['vips_ativos']}</code>
├─ 👥 Grupos Ativos: <code>{stats['grupos_ativos']}</code>
└─ 💰 Transações Hoje: <code>{stats['transacoes_hoje']}</code>

⚡ <b>SISTEMA:</b> <code>🟢 OPERACIONAL</code>

🎯 <b>FERRAMENTAS DISPONÍVEIS:</b>
    """
    
    bot.send_message(
        chat_id=message.chat.id,
        text=mensagem_admin,
        reply_markup=AdminManager.get_admin_panel_markup(),
        parse_mode='HTML'
    )

@bot.message_handler(commands=['catalogo'])
def catalogo_command(message):
    """Exibe o catálogo de conteúdos"""
    markup = InlineKeyboardMarkup(row_width=2)
    
    for categoria_id, categoria_nome in CatalogoManager.CATEGORIAS.items():
        markup.add(
            InlineKeyboardButton(
                categoria_nome,
                callback_data=f"categoria_{categoria_id}"
            )
        )
    
    markup.add(
        InlineKeyboardButton("🔍 Buscar Conteúdo", callback_data="buscar_conteudo"),
        InlineKeyboardButton("🎬 Lançamentos", callback_data="categoria_lancamentos")
    )
    markup.add(InlineKeyboardButton("🔙 Voltar", callback_data="menu_principal"))
    
    bot.send_message(
        chat_id=message.chat.id,
        text="""
🎬 <b>CATÁLOGO PREMIUM 2025</b> 🎬

📂 <b>CATEGORIAS DISPONÍVEIS:</b>

🎬 <b>AÇÃO</b> - Filmes com cenas intensas
🌍 <b>AVENTURA</b> - Explore novos mundos
🎥 <b>ANIMAÇÃO</b> - Para toda família
📺 <b>SÉRIES</b> - Temporadas completas
🎌 <b>ANIMES</b> - Legendados em português
🚀 <b>LANÇAMENTOS</b> - Novidades em primeira mão
🎭 <b>DRAMA</b> - Histórias emocionantes
😂 <b>COMÉDIA</b> - Risadas garantidas
👻 <b>TERROR</b> - Prepare-se para sustos
📚 <b>DOCUMENTÁRIO</b> - Conhecimento e cultura

💎 <b>1 CRÉDITO = 1 CONTEÚDO</b>

👇 <b>ESCOLHA UMA CATEGORIA:</b>
        """,
        reply_markup=markup,
        parse_mode='HTML'
    )

@bot.message_handler(commands=['pedir'])
def pedir_command(message):
    """Processa pedidos de conteúdo"""
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name
    
    args = message.text.split()[1:]
    if not args:
        bot.reply_to(
            message,
            """
📦 <b>COMO FAZER UM PEDIDO:</b>

⚡ <b>Formato:</b>
<code>/pedir Nome do Filme</code>

🎯 <b>Exemplos:</b>
• <code>/pedir Venom 3</code>
• <code>/pedir Stranger Things 5</code>
• <code>/pedir Demon Slayer Final</code>

💡 <b>Dica:</b> Use <code>/catalogo</code> para ver todo o conteúdo disponível.

❓ <b>Dúvidas?</b> Use <code>/suporte</code>
            """,
            parse_mode='HTML'
        )
        return
    
    conteudo = ' '.join(args)
    
    # Verificar créditos
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT creditos FROM usuarios WHERE user_id = ?",
        (user_id,)
    )
    usuario = cursor.fetchone()
    
    if not usuario:
        bot.reply_to(message, "❌ <b>Você precisa usar /start primeiro!</b>", parse_mode='HTML')
        conn.close()
        return
    
    creditos = usuario['creditos']
    
    if creditos < 1:
        markup = InlineKeyboardMarkup()
        markup.row(
            InlineKeyboardButton("💎 Comprar Créditos", callback_data="comprar_creditos"),
            InlineKeyboardButton("👑 Ver Planos VIP", callback_data="planos_vip")
        )
        
        bot.reply_to(
            message,
            f"""
❌ <b>CRÉDITOS INSUFICIENTES</b>

💎 <b>Seus créditos:</b> <code>{creditos}</code>
🎬 <b>Conteúdo:</b> <b>{conteudo}</b>

⚡ <b>Você precisa de 1 crédito para este pedido.</b>

💫 <b>OPÇÕES:</b>
• Comprar créditos avulsos
• Assinar plano VIP
• Ganhar créditos indicando amigos

👇 <b>ESCOLHA UMA OPÇÃO:</b>
            """,
            parse_mode='HTML',
            reply_markup=markup
        )
        conn.close()
        return
    
    # Processar pedido
    pedido_id = None
    try:
        cursor.execute("""
            UPDATE usuarios 
            SET creditos = creditos - 1, 
                total_pedidos = total_pedidos + 1 
            WHERE user_id = ?
        """, (user_id,))
        
        cursor.execute("""
            INSERT INTO pedidos 
            (user_id, username, conteudo, status, data_pedido)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (user_id, username, conteudo, 'processando'))
        
        pedido_id = cursor.lastrowid
        
        cursor.execute("""
            INSERT INTO transacoes 
            (user_id, tipo, valor, descricao, referencia)
            VALUES (?, ?, ?, ?, ?)
        """, (
            user_id,
            'pedido_conteudo',
            -1,
            f'Pedido: {conteudo}',
            SecurityManager.gerar_referencia()
        ))
        
        conn.commit()
        
    except Exception as e:
        logger.error(f"Erro ao processar pedido: {e}")
        bot.reply_to(message, "❌ <b>Erro ao processar pedido. Tente novamente.</b>", parse_mode='HTML')
        conn.close()
        return
    
    conn.close()
    
    # Notificar administrador
    try:
        admin_msg = f"""
📦 <b>NOVO PEDIDO REGISTRADO</b> 📦

🆔 <b>ID:</b> <code>#{pedido_id}</code>
👤 <b>Usuário:</b> @{username} (<code>{user_id}</code>)
🎬 <b>Conteúdo:</b> {conteudo}
💎 <b>Créditos Restantes:</b> {creditos - 1}
⏰ <b>Data:</b> {datetime.now().strftime('%d/%m/%Y %H:%M')}
⚡ <b>Status:</b> Processando

📊 <b>AÇÕES:</b>
• Use /admin para gerenciar
• Entre em contato: @{ADMIN_USERNAME}
        """
        bot.send_message(ADMIN_ID, admin_msg, parse_mode='HTML')
    except Exception as e:
        logger.error(f"Erro ao notificar admin: {e}")
    
    # Confirmar pedido ao usuário
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("📞 Acompanhar Pedido", url=f"https://t.me/{ADMIN_USERNAME}"),
        InlineKeyboardButton("🎬 Novo Pedido", callback_data="catalogo")
    )
    
    bot.reply_to(
        message,
        f"""
✅ <b>PEDIDO CONFIRMADO!</b> ✅

🆔 <b>Pedido ID:</b> <code>#{pedido_id}</code>
🎬 <b>Conteúdo:</b> <b>{conteudo}</b>
💎 <b>Créditos utilizados:</b> 1
💰 <b>Créditos restantes:</b> <code>{creditos - 1}</code>

⏰ <b>Tempo estimado:</b> 15-30 minutos
📦 <b>Formato:</b> Google Drive / Mega
🎯 <b>Qualidade:</b> 4K HDR Garantida

📞 <b>ACOMPANHAMENTO:</b>
Entre em contato com @{ADMIN_USERNAME} para atualizações.

⚡ <b>Obrigado pela preferência!</b>
        """,
        parse_mode='HTML',
        reply_markup=markup
    )
    
    db.log_event('pedido', user_id, f"Pedido #{pedido_id}: {conteudo}")

@bot.message_handler(commands=['creditos'])
def creditos_command(message):
    """Mostra créditos do usuário"""
    user_id = message.from_user.id
    
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT creditos, vip FROM usuarios WHERE user_id = ?",
        (user_id,)
    )
    usuario = cursor.fetchone()
    conn.close()
    
    if not usuario:
        bot.reply_to(message, "❌ <b>Você precisa usar /start primeiro!</b>", parse_mode='HTML')
        return
    
    creditos = usuario['creditos']
    vip = usuario['vip']
    
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("💎 Comprar Créditos", callback_data="comprar_creditos"),
        InlineKeyboardButton("👑 Planos VIP", callback_data="planos_vip")
    )
    
    bot.reply_to(
        message,
        f"""
💰 <b>SEUS CRÉDITOS</b> 💰

💎 <b>Créditos disponíveis:</b> <code>{creditos}</code>
👑 <b>Status VIP:</b> {'✅ ATIVO' if vip == 1 else '❌ INATIVO'}

⚡ <b>O QUE VOCÊ PODE FAZER:</b>
• <b>1 crédito</b> = 1 filme/série
• Compre mais créditos quando precisar
• Assine VIP para receber créditos mensais

📦 <b>FAÇA UM PEDIDO:</b>
Use <code>/pedir NomeDoFilme</code>

👇 <b>ESCOLHA UMA OPÇÃO:</b>
        """,
        parse_mode='HTML',
        reply_markup=markup
    )

# ======================
# 🎯 HANDLERS DE CALLBACK
# ======================
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    """Gerencia todos os callbacks do sistema"""
    try:
        chat_id = call.message.chat.id
        message_id = call.message.message_id
        user_id = call.from_user.id
        username = call.from_user.username
        data = call.data
        
        # Menu Principal
        if data == 'menu_principal':
            start_command(call.message)
        
        # Catálogo
        elif data == 'catalogo':
            catalogo_command(call.message)
        
        # Comprar Créditos
        elif data == 'comprar_creditos':
            markup = InlineKeyboardMarkup(row_width=2)
            markup.add(
                InlineKeyboardButton(
                    "💎 1 Crédito - 20 MZN",
                    url=f"https://t.me/{ADMIN_USERNAME}?text=Quero+comprar+1+crédito"
                ),
                InlineKeyboardButton(
                    "💎 3 Créditos - 50 MZN", 
                    url=f"https://t.me/{ADMIN_USERNAME}?text=Quero+comprar+3+créditos"
                )
            )
            markup.add(
                InlineKeyboardButton(
                    "💎 5 Créditos - 80 MZN",
                    url=f"https://t.me/{ADMIN_USERNAME}?text=Quero+comprar+5+créditos"
                ),
                InlineKeyboardButton(
                    "👑 Ver VIP", 
                    callback_data="planos_vip"
                )
            )
            markup.add(InlineKeyboardButton("🔙 Voltar", callback_data="menu_principal"))
            
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=f"""
💎 <b>COMPRAR CRÉDITOS</b> 💎

🎬 <b>1 CRÉDITO = 1 FILME/SÉRIE</b>

💰 <b>OPÇÕES:</b>
• 💎 <b>1 Crédito</b> - 20 MZN
• 💎 <b>3 Créditos</b> - 50 MZN (economize 10 MZN)
• 💎 <b>5 Créditos</b> - 80 MZN (economize 20 MZN)

💳 <b>FORMAS DE PAGAMENTO:</b>
• M-Pesa: <code>{CONTATOS['mpesa']}</code>
• e-Mola: <code>{CONTATOS['emola']}</code>
• PayPal: {CONTATOS['paypal']}

📋 <b>PROCEDIMENTO:</b>
1. Clique no pacote desejado
2. Será aberto chat com @{ADMIN_USERNAME}
3. Faça o pagamento
4. Envie o comprovante
5. Receba os créditos em 2-5 minutos

👇 <b>SELECIONE UMA OPÇÃO:</b>
                """,
                parse_mode='HTML',
                reply_markup=markup
            )
        
        # Planos VIP
        elif data == 'planos_vip':
            markup = PaymentManager.get_planos_markup()
            
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=f"""
👑 <b>PLANOS VIP PREMIUM</b> 👑

⭐ <b>VANTAGENS EXCLUSIVAS:</b>
• ✅ Créditos mensais automáticos
• ✅ Acesso prioritário a lançamentos
• ✅ Suporte VIP 24/7
• ✅ Catálogo exclusivo
• ✅ Descontos especiais

💎 <b>PLANOS DISPONÍVEIS:</b>

<b>VIP MENSAL</b> - 50 MZN
├─ 10 créditos mensais
├─ Todos benefícios VIP
└─ Renovação automática

<b>VIP TRIMESTRAL</b> - 120 MZN
├─ 35 créditos (5 bônus)
├─ Economia de 30 MZN
└─ 3 meses de benefícios

<b>VIP SEMESTRAL</b> - 200 MZN  
├─ 80 créditos (20 bônus)
├─ Melhor custo-benefício
└─ Status exclusivo

💳 <b>FORMAS DE PAGAMENTO:</b>
• M-Pesa: <code>{CONTATOS['mpesa']}</code>
• e-Mola: <code>{CONTATOS['emola']}</code>
• PayPal: {CONTATOS['paypal']}

📞 <b>ATENDIMENTO:</b> @{ADMIN_USERNAME}

👇 <b>ESCOLHA SEU PLANO:</b>
                """,
                parse_mode='HTML',
                reply_markup=markup
            )
        
        # Selecionar plano VIP específico
        elif data.startswith('vip_'):
            plano_id = data.replace('vip_', '')
            plano = PaymentManager.PLANOS_VIP.get(plano_id)
            
            if plano:
                markup = InlineKeyboardMarkup()
                markup.add(
                    InlineKeyboardButton(
                        f"💳 Assinar {plano['nome']}",
                        url=f"https://t.me/{ADMIN_USERNAME}?text=Quero+assinar+{plano['nome'].replace(' ', '+')}"
                    )
                )
                markup.add(InlineKeyboardButton("🔙 Voltar", callback_data="planos_vip"))
                
                bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=message_id,
                    text=f"""
👑 <b>{plano['nome']}</b> 👑

💰 <b>Preço:</b> {plano['preco']} {plano['moeda']}
💎 <b>Créditos incluídos:</b> {plano['creditos']}
📅 <b>Duração:</b> {plano['dias']} dias

⭐ <b>VANTAGENS:</b>
{chr(10).join(f'• {vantagem}' for vantagem in plano['vantagens'])}

💳 <b>FORMAS DE PAGAMENTO:</b>
• M-Pesa: <code>{CONTATOS['mpesa']}</code>
• e-Mola: <code>{CONTATOS['emola']}</code>
• PayPal: {CONTATOS['paypal']}

📋 <b>PROCEDIMENTO:</b>
1. Clique em "Assinar" abaixo
2. Será aberto chat com @{ADMIN_USERNAME}
3. Faça o pagamento
4. Envie comprovante
5. Seu VIP será ativado em 2-5 minutos

⚡ <b>Clique no botão abaixo para assinar:</b>
                    """,
                    parse_mode='HTML',
                    reply_markup=markup
                )
        
        # Categorias do catálogo
        elif data.startswith('categoria_'):
            categoria_id = data.replace('categoria_', '')
            conteudos = CatalogoManager.get_categoria(categoria_id)
            
            if not conteudos:
                bot.answer_callback_query(call.id, "📂 Catálogo em desenvolvimento!")
                return
            
            texto = f"<b>{CatalogoManager.CATEGORIAS.get(categoria_id, 'CATEGORIA').upper()}</b>\n\n"
            
            for i, conteudo in enumerate(conteudos[:5], 1):
                texto += f"<b>{i}. {conteudo['titulo']}</b>\n"
                texto += f"   🎬 {conteudo['qualidade']}\n"
                texto += f"   ⏰ {conteudo['duracao']} • {conteudo['ano']}\n"
                texto += f"   🎭 {conteudo['genero']}\n"
                texto += f"   📖 {conteudo['descricao'][:80]}...\n\n"
            
            markup = InlineKeyboardMarkup(row_width=2)
            
            # Botões para cada conteúdo
            for conteudo in conteudos[:3]:
                markup.add(InlineKeyboardButton(
                    f"🎬 {conteudo['titulo'][:15]}...",
                    callback_data=f"info_{conteudo['id']}"
                ))
            
            markup.add(
                InlineKeyboardButton("🎥 Ver Trailer", callback_data=f"trailers_cat_{categoria_id}"),
                InlineKeyboardButton("💎 Comprar Créditos", callback_data="comprar_creditos")
            )
            markup.add(InlineKeyboardButton("🔙 Voltar ao Catálogo", callback_data="catalogo"))
            
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=texto + "<b>💎 Use /pedir NomeDoFilme para solicitar</b>",
                parse_mode='HTML',
                reply_markup=markup
            )
        
        # Informações do conteúdo
        elif data.startswith('info_'):
            conteudo_id = data.replace('info_', '')
            
            # Buscar conteúdo em todas as categorias
            conteudo = None
            for categoria in CatalogoManager.CONTEUDO.values():
                for item in categoria:
                    if item['id'] == conteudo_id:
                        conteudo = item
                        break
                if conteudo:
                    break
            
            if conteudo:
                markup = InlineKeyboardMarkup(row_width=2)
                markup.add(
                    InlineKeyboardButton("🎬 Pedir Agora", callback_data=f"pedir_{conteudo_id}"),
                    InlineKeyboardButton("🎥 Ver Trailer", url=conteudo['trailer'])
                )
                markup.add(
                    InlineKeyboardButton("💎 Comprar Créditos", callback_data="comprar_creditos"),
                    InlineKeyboardButton("🔙 Voltar", callback_data="catalogo")
                )
                
                texto = f"""
<b>{conteudo['titulo']}</b>

🎯 <b>INFORMAÇÕES:</b>
├─ 🎬 Qualidade: <code>{conteudo['qualidade']}</code>
├─ ⏰ Duração: <code>{conteudo['duracao']}</code>
├─ 📅 Ano: <code>{conteudo['ano']}</code>
├─ 🎭 Gênero: <code>{conteudo['genero']}</code>
└─ ⭐ Popularidade: <code>{conteudo['popularidade']}%</code>

📖 <b>SINOPSE:</b>
{conteudo['descricao']}

💎 <b>PREÇO: 1 CRÉDITO</b>

👇 <b>ESCOLHA UMA AÇÃO:</b>
                """
                
                bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=message_id,
                    text=texto,
                    parse_mode='HTML',
                    reply_markup=markup
                )
        
        # Pedir conteúdo específico via callback
        elif data.startswith('pedir_'):
            conteudo_id = data.replace('pedir_', '')
            
            # Buscar conteúdo
            conteudo = None
            for categoria in CatalogoManager.CONTEUDO.values():
                for item in categoria:
                    if item['id'] == conteudo_id:
                        conteudo = item
                        break
                if conteudo:
                    break
            
            if conteudo:
                # Simular comando de pedido
                class FakeUser:
                    def __init__(self, user_id, username, first_name):
                        self.id = user_id
                        self.username = username
                        self.first_name = first_name
                
                class FakeChat:
                    def __init__(self, chat_id):
                        self.id = chat_id
                
                class FakeMessage:
                    def __init__(self, user_id, username, first_name, chat_id, conteudo_titulo):
                        self.from_user = FakeUser(user_id, username, first_name)
                        self.chat = FakeChat(chat_id)
                        self.text = f"/pedir {conteudo_titulo}"
                
                fake_msg = FakeMessage(
                    user_id,
                    username,
                    call.from_user.first_name,
                    chat_id,
                    conteudo['titulo']
                )
                
                pedir_command(fake_msg)
        
        # Admin Panel
        elif data == 'admin_panel' and SecurityManager.is_admin(user_id, username):
            admin_command(call.message)
        
        # Admin Statistics
        elif data == 'admin_stats' and SecurityManager.is_admin(user_id, username):
            stats = AdminManager.get_admin_stats()
            
            markup = InlineKeyboardMarkup()
            markup.add(
                InlineKeyboardButton("🔄 Atualizar", callback_data="admin_stats"),
                InlineKeyboardButton("🔙 Voltar", callback_data="admin_panel")
            )
            
            texto = f"""
📊 <b>ESTATÍSTICAS DETALHADAS</b> 📊

👥 <b>USUÁRIOS:</b>
├─ Total: <code>{stats['total_usuarios']}</code>
└─ Novos Hoje: <code>{stats['novos_hoje']}</code>

📨 <b>PEDIDOS:</b>
├─ Total: <code>{stats['total_pedidos']}</code>
├─ Pendentes: <code>{stats['pedidos_pendentes']}</code>
└─ Hoje: <code>{stats['pedidos_hoje']}</code>

💰 <b>FINANCEIRO:</b>
├─ Créditos em Circulação: <code>{stats['total_creditos']}</code>
├─ VIPs Ativos: <code>{stats['vips_ativos']}</code>
└─ Transações Hoje: <code>{stats['transacoes_hoje']}</code>

👥 <b>GRUPOS:</b>
└─ Ativos: <code>{stats['grupos_ativos']}</code>

⏰ <b>ÚLTIMA ATUALIZAÇÃO:</b>
{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
            """
            
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=texto,
                parse_mode='HTML',
                reply_markup=markup
            )
        
        # Admin Refresh
        elif data == 'admin_refresh' and SecurityManager.is_admin(user_id, username):
            admin_command(call.message)
            bot.answer_callback_query(call.id, "🔄 Painel atualizado!")
        
        # Admin Close
        elif data == 'admin_close' and SecurityManager.is_admin(user_id, username):
            bot.delete_message(chat_id, message_id)
        
        # Suporte
        elif data == 'suporte':
            markup = InlineKeyboardMarkup()
            markup.add(
                InlineKeyboardButton("📞 Falar com Suporte", url=f"https://t.me/{ADMIN_USERNAME}"),
                InlineKeyboardButton("🔙 Voltar", callback_data="menu_principal")
            )
            
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=f"""
🆘 <b>SUPORTE & AJUDA</b> 🆘

📞 <b>CONTATOS:</b>
• Telegram: @{ADMIN_USERNAME}
• WhatsApp: {CONTATOS['whatsapp']}
• Email: {CONTATOS['email']}

🕒 <b>HORÁRIO DE ATENDIMENTO:</b>
24 horas por dia, 7 dias por semana

❓ <b>PROBLEMAS COMUNS:</b>
• Créditos não aparecem? Aguarde 5 minutos
• Pedido não entregue? Contate o suporte
• Dúvidas sobre VIP? Consulte os planos

⚡ <b>RESPOSTA RÁPIDA GARANTIDA!</b>

👇 <b>Clique abaixo para falar com o suporte:</b>
                """,
                parse_mode='HTML',
                reply_markup=markup
            )
        
        # Comandos
        elif data == 'comandos':
            markup = InlineKeyboardMarkup(row_width=2)
            markup.add(
                InlineKeyboardButton("🎬 Catálogo", callback_data="catalogo"),
                InlineKeyboardButton("💰 Créditos", callback_data="comprar_creditos")
            )
            markup.add(
                InlineKeyboardButton("👑 VIP", callback_data="planos_vip"),
                InlineKeyboardButton("📞 Suporte", callback_data="suporte")
            )
            markup.add(InlineKeyboardButton("🔙 Voltar", callback_data="menu_principal"))
            
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=f"""
📋 <b>LISTA DE COMANDOS</b> 📋

🎬 <b>COMANDOS PRINCIPAIS:</b>
• <code>/start</code> - Menu inicial
• <code>/catalogo</code> - Ver catálogo completo
• <code>/pedir [nome]</code> - Fazer pedido
• <code>/creditos</code> - Ver seus créditos
• <code>/suporte</code> - Falar com atendimento

💰 <b>COMPRAS:</b>
• <code>/comprar</code> - Comprar créditos
• <code>/vip</code> - Ver planos VIP

🎯 <b>EXEMPLOS:</b>
• <code>/pedir Venom 3</code>
• <code>/pedir Stranger Things 5</code>
• <code>/pedir Demon Slayer</code>

💡 <b>DICAS:</b>
• 1 crédito = 1 filme/série
• Qualidade 4K garantida
• Entrega em 15-30 minutos

📞 <b>ATENDIMENTO:</b> @{ADMIN_USERNAME}
                """,
                parse_mode='HTML',
                reply_markup=markup
            )
        
        # Meu Perfil
        elif data == 'meu_perfil':
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT creditos, vip, vip_expira, total_pedidos, data_cadastro 
                FROM usuarios 
                WHERE user_id = ?
            """, (user_id,))
            usuario = cursor.fetchone()
            conn.close()
            
            if usuario:
                creditos = usuario['creditos']
                vip = usuario['vip']
                vip_expira = usuario['vip_expira']
                total_pedidos = usuario['total_pedidos']
                data_cadastro = usuario['data_cadastro']
                
                # Formatar data
                try:
                    data_cadastro_fmt = datetime.fromisoformat(data_cadastro).strftime('%d/%m/%Y')
                except:
                    data_cadastro_fmt = data_cadastro
                
                # Status VIP
                if vip == 1 and vip_expira:
                    try:
                        expira_date = datetime.fromisoformat(vip_expira)
                        if datetime.now() < expira_date:
                            vip_status = f"✅ ATIVO (até {expira_date.strftime('%d/%m/%Y')})"
                        else:
                            vip_status = "❌ EXPIRADO"
                    except:
                        vip_status = "✅ ATIVO"
                elif vip == 1:
                    vip_status = "✅ ATIVO"
                else:
                    vip_status = "❌ INATIVO"
                
                markup = InlineKeyboardMarkup()
                markup.row(
                    InlineKeyboardButton("💎 Comprar Créditos", callback_data="comprar_creditos"),
                    InlineKeyboardButton("👑 Ver VIP", callback_data="planos_vip")
                )
                markup.add(InlineKeyboardButton("🔙 Voltar", callback_data="menu_principal"))
                
                texto = f"""
📊 <b>MEU PERFIL</b> 📊

👤 <b>INFORMAÇÕES:</b>
├─ ID: <code>{user_id}</code>
├─ Usuário: @{username if username else 'Não definido'}
├─ Data de Cadastro: {data_cadastro_fmt}
└─ Status: ✅ Ativo

💰 <b>CRÉDITOS:</b>
└─ Disponíveis: <code>{creditos}</code>

👑 <b>VIP:</b>
└─ Status: {vip_status}

📦 <b>HISTÓRICO:</b>
└─ Pedidos Realizados: <code>{total_pedidos}</code>

⚡ <b>OPÇÕES:</b>
                """
                
                bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=message_id,
                    text=texto,
                    parse_mode='HTML',
                    reply_markup=markup
                )
        
        # Responder a outros callbacks
        else:
            bot.answer_callback_query(call.id, "⚡ Ação processada!")
            
    except Exception as e:
        logger.error(f"Erro no callback handler: {e}")
        bot.answer_callback_query(call.id, "❌ Erro ao processar ação!")

# ======================
# 🌐 WEBHOOK E SERVER
# ======================
@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>🎬 Cinema Pro Premium</title>
        <style>
            body {
                font-family: 'Arial', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                text-align: center;
                padding: 50px;
            }
            .container {
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                padding: 40px;
                max-width: 800px;
                margin: 0 auto;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            }
            h1 {
                font-size: 3em;
                margin-bottom: 20px;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
            }
            .status {
                background: rgba(76, 175, 80, 0.2);
                border: 2px solid #4CAF50;
                border-radius: 10px;
                padding: 15px;
                margin: 20px 0;
                font-size: 1.2em;
            }
            .stats {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-top: 30px;
            }
            .stat-card {
                background: rgba(255, 255, 255, 0.15);
                border-radius: 10px;
                padding: 20px;
                transition: transform 0.3s;
            }
            .stat-card:hover {
                transform: translateY(-5px);
            }
            .stat-value {
                font-size: 2em;
                font-weight: bold;
                margin: 10px 0;
            }
            .telegram-btn {
                display: inline-block;
                background: #0088cc;
                color: white;
                padding: 15px 30px;
                border-radius: 50px;
                text-decoration: none;
                font-weight: bold;
                margin-top: 30px;
                transition: all 0.3s;
            }
            .telegram-btn:hover {
                background: #006699;
                transform: scale(1.05);
            }
            .admin-info {
                background: rgba(255, 193, 7, 0.2);
                border: 2px solid #FFC107;
                border-radius: 10px;
                padding: 15px;
                margin: 20px 0;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎬 CINEMA PRO PREMIUM</h1>
            <p>Sistema profissional de distribuição de conteúdo audiovisual</p>
            
            <div class="admin-info">
                <h3>👑 ADMINISTRADOR</h3>
                <p>Usuário: <strong>@{ADMIN_USERNAME}</strong></p>
                <p>ID: <code>{ADMIN_ID}</code></p>
            </div>
            
            <div class="status">
                ✅ SISTEMA OPERACIONAL - Status: <strong>ONLINE</strong>
            </div>
            
            <div class="stats">
                <div class="stat-card">
                    <div>👥 Usuários</div>
                    <div class="stat-value" id="userCount">Carregando...</div>
                </div>
                <div class="stat-card">
                    <div>📨 Pedidos Hoje</div>
                    <div class="stat-value" id="ordersToday">Carregando...</div>
                </div>
                <div class="stat-card">
                    <div>💎 Créditos</div>
                    <div class="stat-value" id="totalCredits">Carregando...</div>
                </div>
                <div class="stat-card">
                    <div>👑 VIPs</div>
                    <div class="stat-value" id="vipCount">Carregando...</div>
                </div>
            </div>
            
            <a href="https://t.me/{ADMIN_USERNAME}" class="telegram-btn" target="_blank">
                📞 CONTATAR ADMINISTRADOR
            </a>
            
            <p style="margin-top: 30px; opacity: 0.8;">
                Versão 4.5.0 | Sistema Premium | Admin: @{ADMIN_USERNAME} | © 2024
            </p>
        </div>
        
        <script>
            async function loadStats() {
                try {
                    const response = await fetch('/api/stats');
                    const data = await response.json();
                    
                    document.getElementById('userCount').textContent = data.total_usuarios;
                    document.getElementById('ordersToday').textContent = data.pedidos_hoje;
                    document.getElementById('totalCredits').textContent = data.total_creditos;
                    document.getElementById('vipCount').textContent = data.vip_count;
                } catch (error) {
                    console.error('Erro ao carregar estatísticas:', error);
                }
            }
            
            loadStats();
            setInterval(loadStats, 30000);
        </script>
    </body>
    </html>
    """.format(ADMIN_USERNAME=ADMIN_USERNAME, ADMIN_ID=ADMIN_ID)

@app.route('/api/stats')
def api_stats():
    """API para estatísticas do sistema"""
    conn = db.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    total_usuarios = cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT COUNT(*) FROM pedidos 
        WHERE date(data_pedido) = date('now')
    """)
    pedidos_hoje = cursor.fetchone()[0]
    
    cursor.execute("SELECT SUM(creditos) FROM usuarios")
    total_creditos = cursor.fetchone()[0] or 0
    
    cursor.execute("SELECT COUNT(*) FROM usuarios WHERE vip = 1")
    vip_count = cursor.fetchone()[0]
    
    conn.close()
    
    return jsonify({
        'status': 'success',
        'total_usuarios': total_usuarios,
        'pedidos_hoje': pedidos_hoje,
        'total_creditos': total_creditos,
        'vip_count': vip_count,
        'admin_username': ADMIN_USERNAME,
        'admin_id': ADMIN_ID,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/webhook', methods=['POST'])
def webhook():
    """Endpoint para webhook do Telegram"""
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return 'OK', 200
    return 'ERROR', 400

# ======================
# 🚀 COMANDOS ADICIONAIS DO ADMIN
# ======================
@bot.message_handler(commands=['addcreditos'])
def add_creditos_command(message):
    """Adicionar créditos a um usuário (admin only)"""
    user_id = message.from_user.id
    username = message.from_user.username
    
    if not SecurityManager.is_admin(user_id, username):
        bot.reply_to(message, "❌ <b>Acesso negado!</b>", parse_mode='HTML')
        return
    
    args = message.text.split()[1:]
    if len(args) != 2:
        bot.reply_to(
            message,
            """
💎 <b>ADICIONAR CRÉDITOS</b> 💎

⚡ <b>Formato:</b>
<code>/addcreditos ID_Usuario Quantidade</code>

🎯 <b>Exemplo:</b>
<code>/addcreditos 5125563829 10</code>

📝 <b>Nota:</b> Use /admin para ver IDs dos usuários
            """,
            parse_mode='HTML'
        )
        return
    
    try:
        target_user_id = int(args[0])
        quantidade = int(args[1])
        
        if quantidade <= 0:
            bot.reply_to(message, "❌ <b>A quantidade deve ser positiva!</b>", parse_mode='HTML')
            return
        
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # Verificar se usuário existe
        cursor.execute("SELECT username FROM usuarios WHERE user_id = ?", (target_user_id,))
        target_user = cursor.fetchone()
        
        if not target_user:
            bot.reply_to(message, f"❌ <b>Usuário com ID {target_user_id} não encontrado!</b>", parse_mode='HTML')
            conn.close()
            return
        
        # Adicionar créditos
        cursor.execute("""
            UPDATE usuarios 
            SET creditos = creditos + ? 
            WHERE user_id = ?
        """, (quantidade, target_user_id))
        
        cursor.execute("""
            INSERT INTO transacoes 
            (user_id, tipo, valor, descricao, referencia, admin)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            target_user_id,
            'creditos_adicionados',
            quantidade,
            f'Créditos adicionados por admin',
            SecurityManager.gerar_referencia(),
            username
        ))
        
        conn.commit()
        
        # Notificar usuário
        try:
            bot.send_message(
                target_user_id,
                f"""
🎉 <b>CRÉDITOS ADICIONADOS!</b> 🎉

💎 <b>Quantidade:</b> +{quantidade} créditos
👤 <b>Administrador:</b> @{username}
📝 <b>Motivo:</b> Adição manual pelo administrador

💰 <b>Seus novos créditos:</b> 
Verifique com <code>/creditos</code>

⚡ <b>Obrigado por usar Cinema Pro Premium!</b>
                """,
                parse_mode='HTML'
            )
        except:
            pass
        
        conn.close()
        
        bot.reply_to(
            message,
            f"""
✅ <b>CRÉDITOS ADICIONADOS COM SUCESSO!</b> ✅

👤 <b>Usuário:</b> ID {target_user_id}
💎 <b>Quantidade:</b> +{quantidade} créditos
👑 <b>Admin:</b> @{username}

📊 <b>Ação registrada no sistema.</b>
            """,
            parse_mode='HTML'
        )
        
        db.log_event('admin_add_creditos', user_id, f"Adicionou {quantidade} créditos para usuário {target_user_id}")
        
    except ValueError:
        bot.reply_to(message, "❌ <b>ID e quantidade devem ser números!</b>", parse_mode='HTML')
    except Exception as e:
        logger.error(f"Erro ao adicionar créditos: {e}")
        bot.reply_to(message, "❌ <b>Erro ao adicionar créditos!</b>", parse_mode='HTML')

@bot.message_handler(commands=['broadcast'])
def broadcast_command(message):
    """Enviar mensagem para todos os usuários (admin only)"""
    user_id = message.from_user.id
    username = message.from_user.username
    
    if not SecurityManager.is_admin(user_id, username):
        bot.reply_to(message, "❌ <b>Acesso negado!</b>", parse_mode='HTML')
        return
    
    args = message.text.split()[1:]
    if not args:
        bot.reply_to(
            message,
            """
📢 <b>ENVIAR BROADCAST</b> 📢

⚡ <b>Formato:</b>
<code>/broadcast Sua mensagem aqui</code>

🎯 <b>Exemplo:</b>
<code>/broadcast 🎉 Nova promoção! 50% de desconto em créditos!</code>

⚠️ <b>Atenção:</b> Esta mensagem será enviada para TODOS os usuários!
            """,
            parse_mode='HTML'
        )
        return
    
    mensagem = ' '.join(args)
    
    # Pedir confirmação
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("✅ Confirmar", callback_data=f"confirm_broadcast_{hashlib.md5(mensagem.encode()).hexdigest()[:8]}"),
        InlineKeyboardButton("❌ Cancelar", callback_data="cancel_broadcast")
    )
    
    bot.reply_to(
        message,
        f"""
⚠️ <b>CONFIRMAR BROADCAST</b> ⚠️

📝 <b>Mensagem:</b>
{mensagem}

👥 <b>Será enviado para:</b>
Todos os usuários registrados

⚠️ <b>Esta ação não pode ser desfeita!</b>

👇 <b>Confirme ou cancele:</b>
        """,
        parse_mode='HTML',
        reply_markup=markup
    )

@bot.message_handler(commands=['stats'])
def stats_command(message):
    """Estatísticas do sistema (admin only)"""
    user_id = message.from_user.id
    username = message.from_user.username
    
    if not SecurityManager.is_admin(user_id, username):
        bot.reply_to(message, "❌ <b>Acesso negado!</b>", parse_mode='HTML')
        return
    
    stats = AdminManager.get_admin_stats()
    
    texto = f"""
📊 <b>ESTATÍSTICAS DO SISTEMA</b> 📊
👑 <i>Admin: @{ADMIN_USERNAME}</i>

👥 <b>USUÁRIOS:</b>
├─ Total: <code>{stats['total_usuarios']}</code>
└─ Novos Hoje: <code>{stats['novos_hoje']}</code>

📨 <b>PEDIDOS:</b>
├─ Total: <code>{stats['total_pedidos']}</code>
├─ Pendentes: <code>{stats['pedidos_pendentes']}</code>
└─ Hoje: <code>{stats['pedidos_hoje']}</code>

💰 <b>FINANCEIRO:</b>
├─ Créditos em Circulação: <code>{stats['total_creditos']}</code>
├─ VIPs Ativos: <code>{stats['vips_ativos']}</code>
└─ Transações Hoje: <code>{stats['transacoes_hoje']}</code>

👥 <b>GRUPOS:</b>
└─ Ativos: <code>{stats['grupos_ativos']}</code>

⏰ <b>ÚLTIMA ATUALIZAÇÃO:</b>
{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

⚡ <b>SISTEMA:</b> <code>🟢 OPERACIONAL</code>
    """
    
    bot.reply_to(message, texto, parse_mode='HTML')

# ======================
# 🚀 INICIALIZAÇÃO
# ======================
def setup_webhook():
    """Configura webhook para produção"""
    try:
        webhook_url = f"https://cinema-pro-bot-production.up.railway.app/webhook"
        bot.remove_webhook()
        time.sleep(1)
        bot.set_webhook(url=webhook_url)
        logger.info(f"✅ Webhook configurado: {webhook_url}")
    except Exception as e:
        logger.warning(f"⚠️ Usando polling: {e}")
        # Inicia polling em thread separada
        polling_thread = threading.Thread(target=bot.polling, kwargs={'none_stop': True})
        polling_thread.daemon = True
        polling_thread.start()

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🎬 CINEMA PRO PREMIUM BOT - SISTEMA INICIADO")
    print("="*60)
    print(f"🤖 Token: {TOKEN[:10]}...")
    print(f"👑 Admin: @{ADMIN_USERNAME} (ID: {ADMIN_ID})")
    print(f"📊 Database: cinema_premium.db")
    print(f"🌐 Webhook: Ativo")
    print("="*60)
    print("✅ Sistema configurado e pronto para uso!")
    print("✅ Painel Admin disponível em /admin")
    print("✅ Dashboard web: https://cinema-pro-bot-production.up.railway.app")
    print("="*60 + "\n")
    
    logger.info(f"Sistema iniciado para admin @{ADMIN_USERNAME}")
    
    # Configurar webhook
    setup_webhook()
    
    # Iniciar servidor Flask
    port = int(os.environ.get('PORT', 5000))
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False,
        threaded=True
    )
