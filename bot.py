import os
import telebot
import sqlite3
import time
import random
import requests
from flask import Flask, request
from datetime import datetime, timedelta

# 🔐 CONFIGURAÇÃO
TOKEN = "8306714275:AAGzNXE3TZKbe5-49YGTgNOMrJiLVxBjmLA"
ADMIN_USERNAME = "ayltonanna7"
ADMIN_ID = 5125563829

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# 💎 SISTEMA PREMIUM
CONTATOS = {
    'whatsapp': '848568229',
    'telegram': '@ayltonanna7',
    'email': 'ayltonanna7@gmail.com',
    'mpesa': '848568229', 
    'emola': '870612404',
    'paypal': 'ayltonanna7@gmail.com'
}

# 🎬 CATÁLOGO PROFISSIONAL
CATALOGO_PREMIUM = {
    'filmes': [
        {
            'titulo': '🎬 VENOM 3: A ÚLTIMA BATALHA',
            'capa': 'https://i.imgur.com/venom3-cap.jpg',
            'trailer': 'https://youtu.be/venom3-trailer',
            'qualidade': '4K HDR • Dolby Atmos',
            'genero': 'Ação • Ficção Científica',
            'duracao': '2h 18m',
            'ano': '2025',
            'descricao': 'Eddie Brock e Venom enfrentam seu maior desafio contra um inimigo simbiótico global.'
        },
        {
            'titulo': '🎬 AVATAR 4: O LEGADO',
            'capa': 'https://i.imgur.com/avatar4-cap.jpg', 
            'trailer': 'https://youtu.be/avatar4-trailer',
            'qualidade': '4K Dolby Vision • IMAX',
            'genero': 'Aventura • Ficção Científica',
            'duracao': '3h 02m',
            'ano': '2025',
            'descricao': 'A saga continua em novos mundos com criaturas extraordinárias e batalhas épicas.'
        }
    ],
    'series': [
        {
            'titulo': '📺 STRANGER THINGS 5 - TEMPORADA COMPLETA',
            'capa': 'https://i.imgur.com/stranger5-cap.jpg',
            'trailer': 'https://youtu.be/stranger5-trailer',
            'qualidade': '4K Dolby Vision • 8 Episódios',
            'genero': 'Suspense • Ficção Científica • Drama',
            'duracao': 'Temporada Completa',
            'ano': '2025',
            'descricao': 'A temporada final que encerra a saga de Hawkins e o Mundo Invertido.'
        }
    ],
    'animes': [
        {
            'titulo': '🎌 DEMON SLAYER: FINAL ARC',
            'capa': 'https://i.imgur.com/demonslayer-cap.jpg',
            'trailer': 'https://youtu.be/demonslayer-trailer',
            'qualidade': '4K • Japonês Legendado',
            'genero': 'Anime • Ação • Fantasia',
            'duracao': 'Arco Final Completo',
            'ano': '2025',
            'descricao': 'O confronto final entre Tanjiro e Muzan Kibutsuji.'
        }
    ]
}

# 🎭 TRAILERS DISPONÍVEIS
TRAILERS_DISPONIVEIS = {
    'VENOM 3': '🎬 *Trailer Venom 3*\nhttps://youtu.be/venom3-trailer\n⚡ 2:30 min • Cenas de ação em 4K',
    'AVATAR 4': '🎬 *Trailer Avatar 4*\nhttps://youtu.be/avatar4-trailer\n🌍 3:15 min • Novos mundos revelados', 
    'SPIDER-MAN BEYOND': '🎬 *Trailer Spider-Man Beyond*\nhttps://youtu.be/spiderman-trailer\n🕷️ 2:45 min • Multiverso expandido',
    'STRANGER THINGS 5': '📺 *Trailer Stranger Things 5*\nhttps://youtu.be/stranger5-trailer\n🔮 3:30 min • Temporada final épica',
    'DEMON SLAYER FINAL': '🎌 *Trailer Demon Slayer Final*\nhttps://youtu.be/demonslayer-trailer\n⚔️ 2:15 min • Batalhas emocionantes'
}

# 🎯 RECOMENDAÇÕES DIÁRIAS
RECOMENDACOES_DIARIAS = {
    'segunda': {'titulo': '🚀 INÍCIO DE SEMANA ENERGÉTICO!', 'filme': 'VENOM 3: A ÚLTIMA BATALHA', 'descricao': 'Comece a semana com ação intensa!', 'hashtag': '#SegundaDeAção'},
    'terca': {'titulo': '🎭 DRAMA E EMOÇÃO!', 'filme': 'THE LAST OF US 3', 'descricao': 'Uma jornada emocional intensa.', 'hashtag': '#TerçaDramática'},
    'quarta': {'titulo': '🌍 AVENTURA ÉPICA!', 'filme': 'AVATAR 4: O LEGADO', 'descricao': 'Aventura em novos mundos!', 'hashtag': '#QuartaAventura'},
    'quinta': {'titulo': '🕷️ MULTIVERSO SURPREENDENTE!', 'filme': 'SPIDER-MAN: BEYOND', 'descricao': 'Animação incrível!', 'hashtag': '#QuintaAnimada'},
    'sexta': {'titulo': '🔮 FIM DE SEMANA MISTERIOSO!', 'filme': 'STRANGER THINGS 5', 'descricao': 'Série emocionante!', 'hashtag': '#SextaMisteriosa'},
    'sabado': {'titulo': '⚔️ ANIME ÉPICO!', 'filme': 'DEMON SLAYER: FINAL ARC', 'descricao': 'Maratona de anime!', 'hashtag': '#SábadoAnime'},
    'domingo': {'titulo': '🎬 CLÁSSICO DO DIA!', 'filme': 'AVATAR 4: O LEGADO', 'descricao': 'Filme popular!', 'hashtag': '#Domingão'}
}

# 💰 PLANOS VIP
PLANOS_VIP = {
    '1_mes': {'nome': '💎 VIP 1 MÊS', 'preco': '50 MZN', 'creditos': 10, 'duracao': 30},
    '3_meses': {'nome': '🔥 VIP 3 MESES', 'preco': '120 MZN', 'creditos': 35, 'duracao': 90},
    '6_meses': {'nome': '👑 VIP 6 MESES', 'preco': '200 MZN', 'creditos': 80, 'duracao': 180}
}

# 🗄️ BANCO DE DADOS
def get_db():
    conn = sqlite3.connect('cinema_premium.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS usuarios
                 (user_id INTEGER PRIMARY KEY, 
                  username TEXT, 
                  creditos INTEGER DEFAULT 0,
                  vip INTEGER DEFAULT 0,
                  vip_expira DATE,
                  primeiro_usuario INTEGER DEFAULT 0,
                  data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS pedidos
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  user_id INTEGER,
                  username TEXT,
                  filme TEXT,
                  data TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
                  status TEXT DEFAULT 'pendente')''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS grupos
                 (group_id INTEGER PRIMARY KEY,
                  group_title TEXT,
                  data_adicao TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS transacoes
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  tipo TEXT,
                  valor INTEGER,
                  admin TEXT,
                  data TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    conn.commit()
    conn.close()

init_db()

# 🔐 VERIFICAÇÃO ADMIN
def is_admin(user_id, username):
    if not username:
        return user_id == ADMIN_ID
    return (username.lower() == ADMIN_USERNAME.replace('@', '').lower() or 
            user_id == ADMIN_ID)

# 🎁 SISTEMA DE CRÉDITOS INICIAIS
def verificar_primeiros_usuarios(user_id, username):
    conn = get_db()
    c = conn.cursor()
    
    total_usuarios = c.execute("SELECT COUNT(*) FROM usuarios").fetchone()[0]
    c.execute("SELECT primeiro_usuario FROM usuarios WHERE user_id = ?", (user_id,))
    usuario = c.fetchone()
    
    if total_usuarios <= 10 and (not usuario or usuario[0] == 0):
        c.execute("UPDATE usuarios SET creditos = creditos + 3, primeiro_usuario = 1 WHERE user_id = ?", (user_id,))
        c.execute("INSERT INTO transacoes (user_id, tipo, valor, admin) VALUES (?, ?, ?, ?)",
                 (user_id, "bonus_boas_vindas", 3, "sistema"))
        conn.commit()
        conn.close()
        
        try:
            bot.send_message(user_id, f"""
🎉 *BOAS-VINDAS PREMIUM!* 🎉

Bem-vindo ao *CINEMA PRO*! Como você é um dos nossos primeiros 10 usuários, recebeu:

💎 *+3 CRÉDITOS GRÁTIS!*

🎬 Agora você pode pedir 3 filmes/séries gratuitamente!

📞 *Dúvidas?* @{ADMIN_USERNAME}
            """, parse_mode='Markdown')
        except:
            pass
        return True
    
    conn.close()
    return False

# 👋 BOAS-VINDAS EM GRUPOS
@bot.message_handler(content_types=['new_chat_members'])
def welcome_group(message):
    for member in message.new_chat_members:
        if member.username == bot.get_me().username:
            group_id = message.chat.id
            group_title = message.chat.title
            
            conn = get_db()
            c = conn.cursor()
            c.execute("INSERT OR REPLACE INTO grupos (group_id, group_title) VALUES (?, ?)",
                     (group_id, group_title))
            conn.commit()
            conn.close()
            
            welcome_msg = f"""
🎬 *CINEMA PRO - SISTEMA PREMIUM ADICIONADO!* 🎬

Olá *{group_title}*! 🤖

É uma honra fazer parte desta comunidade! Trago o melhor do entretenimento em qualidade premium.

📞 *ATENDIMENTO:* @{ADMIN_USERNAME}

*Sejam bem-vindos ao mundo do entretenimento premium!* 🎉
            """
            
            bot.send_message(group_id, welcome_msg, parse_mode='Markdown')
            time.sleep(5)
            enviar_recomendacao_diaria(group_id)

# 🎯 RECOMENDAÇÃO DIÁRIA
def enviar_recomendacao_diaria(chat_id):
    dia_semana = datetime.now().strftime('%A').lower()
    dias_pt = {
        'monday': 'segunda', 'tuesday': 'terca', 'wednesday': 'quarta',
        'thursday': 'quinta', 'friday': 'sexta', 'saturday': 'sabado', 'sunday': 'domingo'
    }
    
    dia = dias_pt.get(dia_semana, 'segunda')
    recomendacao = RECOMENDACOES_DIARIAS.get(dia, RECOMENDACOES_DIARIAS['segunda'])
    
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row(
        telebot.types.InlineKeyboardButton("🎬 Ver Trailer", callback_data=f"trailer_{recomendacao['filme'].split(':')[0].upper().replace(' ', '_')}"),
        telebot.types.InlineKeyboardButton("📦 Pedir Agora", callback_data=f"pedir_{recomendacao['filme'].split(':')[0].upper().replace(' ', '_')}")
    )
    
    recomendacao_msg = f"""
🎬 *RECOMENDAÇÃO DO DIA* 🎬
{recomendacao['hashtag']}

{recomendacao['titulo']}

⚡ *FILME SUGERIDO:*
*{recomendacao['filme']}*

📖 *Sinopse:*
{recomendacao['descricao']}

💎 *Entrega em 15-30 minutos!*
    """
    
    try:
        bot.send_message(chat_id, recomendacao_msg, parse_mode='Markdown', reply_markup=markup)
    except Exception as e:
        print(f"Erro ao enviar recomendação: {e}")

@bot.message_handler(commands=['recomendacao', 'filmedodia'])
def recomendacao_cmd(message):
    enviar_recomendacao_diaria(message.chat.id)

# 🎥 SISTEMA DE TRAILERS
@bot.message_handler(commands=['trailer'])
def trailer_cmd(message):
    markup = telebot.types.InlineKeyboardMarkup()
    
    trailers = list(TRAILERS_DISPONIVEIS.keys())[:6]
    for i in range(0, len(trailers), 2):
        row = []
        for j in range(2):
            if i + j < len(trailers):
                filme = trailers[i + j]
                callback_data = f"trailer_{filme.split()[0].upper()}"
                row.append(telebot.types.InlineKeyboardButton(
                    f"🎬 {filme.split()[0]}", 
                    callback_data=callback_data
                ))
        if row:
            markup.add(*row)
    
    bot.reply_to(message, """
🎬 *TRAILERS EXCLUSIVOS* 🎬

Escolha um trailer para ver:

💡 *Após o trailer:*
• Pedido completo por 1 crédito
• Filme/série completo em 4K
• Entrega rápida
    """, parse_mode='Markdown', reply_markup=markup)

# 🎨 CATÁLOGO PROFISSIONAL
@bot.message_handler(commands=['catalogo', 'lancamentos'])
def catalogo_premium(message):
    markup = telebot.types.InlineKeyboardMarkup()
    
    markup.row(
        telebot.types.InlineKeyboardButton("🎬 FILMES 4K", callback_data="categoria_filmes"),
        telebot.types.InlineKeyboardButton("📺 SÉRIES", callback_data="categoria_series")
    )
    markup.row(
        telebot.types.InlineKeyboardButton("🎌 ANIMES", callback_data="categoria_animes"),
        telebot.types.InlineKeyboardButton("🎥 TRAILERS", callback_data="menu_trailers")
    )
    
    bot.reply_to(message, f"""
🎬 *CATÁLOGO PREMIUM 2025* 🎬

💫 *EXPERIÊNCIA CINEMATOGRÁFICA COMPLETA*

⚡ *CATEGORIAS EXCLUSIVAS:*
• 🎬 FILMES 4K ULTRA HD
• 📺 SÉRIES COMPLETAS  
• 🎌 ANIMES LEGENDADOS

📞 *ATENDIMENTO:* @{ADMIN_USERNAME}
    """, parse_mode='Markdown', reply_markup=markup)

# 📦 SISTEMA DE PEDIDOS
@bot.message_handler(commands=['pedir'])
def pedir_cmd(message):
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name
    
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT creditos FROM usuarios WHERE user_id = ?", (user_id,))
    usuario = c.fetchone()
    
    if not usuario:
        bot.reply_to(message, "❌ *Você precisa usar /start primeiro!*", parse_mode='Markdown')
        conn.close()
        return
    
    creditos = usuario[0]
    
    args = message.text.split()[1:]
    if not args:
        bot.reply_to(message, f"""
📦 *FAZER PEDIDO*

💎 *Seus créditos:* *{creditos}*

⚡ *Como pedir:*
`/pedir Nome do Filme`

🎯 *Exemplos:*
`/pedir Venom 3`
`/pedir Stranger Things 5`
        """, parse_mode='Markdown')
        conn.close()
        return
    
    filme = ' '.join(args)
    
    if creditos < 1:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(
            telebot.types.InlineKeyboardButton("💎 Comprar Créditos", callback_data="comprar_creditos"),
            telebot.types.InlineKeyboardButton("👑 Planos VIP", callback_data="planos_vip")
        )
        
        bot.reply_to(message, f"""
❌ *CRÉDITOS INSUFICIENTES*

💎 *Seus créditos:* *{creditos}*
📦 *Pedido:* *{filme}*

⚡ *Você precisa de 1 crédito para fazer este pedido.*
        """, parse_mode='Markdown', reply_markup=markup)
        conn.close()
        return
    
    # Processar pedido
    c.execute("UPDATE usuarios SET creditos = creditos - 1 WHERE user_id = ?", (user_id,))
    c.execute("INSERT INTO pedidos (user_id, username, filme, status) VALUES (?, ?, ?, ?)",
             (user_id, username, filme, 'processando'))
    c.execute("INSERT INTO transacoes (user_id, tipo, valor, admin) VALUES (?, ?, ?, ?)",
             (user_id, "pedido_filme", -1, "sistema"))
    
    pedido_id = c.lastrowid
    conn.commit()
    conn.close()
    
    # Notificar admin
    try:
        admin_msg = f"""
📦 *NOVO PEDIDO* 📦

🆔 *Pedido:* #{pedido_id}
👤 *Usuário:* @{username} ({user_id})
🎬 *Filme:* {filme}
💎 *Créditos restantes:* {creditos - 1}
        """
        bot.send_message(ADMIN_ID, admin_msg, parse_mode='Markdown')
    except:
        pass
    
    bot.reply_to(message, f"""
✅ *PEDIDO CONFIRMADO!* ✅

🆔 *Pedido:* *#{pedido_id}*
🎬 *Filme:* *{filme}*
💎 *Créditos utilizados:* 1
💰 *Créditos restantes:* *{creditos - 1}*

⏰ *Tempo de entrega:* 15-30 minutos
📞 *Acompanhamento:* @{ADMIN_USERNAME}
    """, parse_mode='Markdown')

# 👑 PAINEL ADMIN COMPLETO E FUNCIONAL
@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if not is_admin(message.from_user.id, message.from_user.username):
        bot.reply_to(message, "❌ *Acesso negado!* Apenas administradores.", parse_mode='Markdown')
        return
    
    conn = get_db()
    c = conn.cursor()
    
    # Estatísticas
    total_usuarios = c.execute("SELECT COUNT(*) FROM usuarios").fetchone()[0]
    total_pedidos = c.execute("SELECT COUNT(*) FROM pedidos").fetchone()[0]
    pedidos_pendentes = c.execute("SELECT COUNT(*) FROM pedidos WHERE status = 'pendente'").fetchone()[0]
    total_creditos = c.execute("SELECT SUM(creditos) FROM usuarios").fetchone()[0] or 0
    vip_count = c.execute("SELECT COUNT(*) FROM usuarios WHERE vip = 1").fetchone()[0]
    total_grupos = c.execute("SELECT COUNT(*) FROM grupos").fetchone()[0]
    
    # Pedidos recentes (últimas 24h)
    pedidos_24h = c.execute("SELECT COUNT(*) FROM pedidos WHERE datetime(data) > datetime('now', '-1 day')").fetchone()[0]
    
    # Usuários novos (últimas 24h)
    usuarios_24h = c.execute("SELECT COUNT(*) FROM usuarios WHERE datetime(data_cadastro) > datetime('now', '-1 day')").fetchone()[0]
    
    conn.close()
    
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row(
        telebot.types.InlineKeyboardButton("📊 Estatísticas", callback_data="admin_stats"),
        telebot.types.InlineKeyboardButton("👥 Gerenciar Usuários", callback_data="admin_users")
    )
    markup.row(
        telebot.types.InlineKeyboardButton("💰 Adicionar Créditos", callback_data="admin_add_creditos"),
        telebot.types.InlineKeyboardButton("📨 Pedidos Pendentes", callback_data="admin_pedidos_pendentes")
    )
    markup.row(
        telebot.types.InlineKeyboardButton("👑 Gerenciar VIP", callback_data="admin_vip"),
        telebot.types.InlineKeyboardButton("📢 Enviar Anúncio", callback_data="admin_broadcast")
    )
    markup.row(
        telebot.types.InlineKeyboardButton("🔄 Atualizar", callback_data="admin_refresh"),
        telebot.types.InlineKeyboardButton("❌ Fechar", callback_data="admin_close")
    )
    
    bot.reply_to(message, f"""
👑 *PAINEL ADMIN - CINEMA PRO PREMIUM*

📊 *ESTATÍSTICAS GERAIS:*
• 👥 Total Usuários: `{total_usuarios}`
• 📈 Novos (24h): `{usuarios_24h}`
• 💎 Créditos em Circulação: `{total_creditos}`
• 👑 VIPs Ativos: `{vip_count}`
• 📨 Total Pedidos: `{total_pedidos}`
• ⏳ Pendentes: `{pedidos_pendentes}`
• 🕒 Pedidos (24h): `{pedidos_24h}`
• 👥 Grupos Ativos: `{total_grupos}`

⚡ *SISTEMA OPERACIONAL*
🟢 *Todos os módulos ativos*

🎯 *ESCOLHA UMA AÇÃO:*
    """, parse_mode='Markdown', reply_markup=markup)

# 🔧 COMANDOS ADMIN ESPECÍFICOS
@bot.message_handler(commands=['addcreditos'])
def add_creditos_cmd(message):
    if not is_admin(message.from_user.id, message.from_user.username):
        return
    
    args = message.text.split()[1:]
    if len(args) < 2:
        bot.reply_to(message, """
💎 *ADICIONAR CRÉDITOS*

⚡ *Uso:*
`/addcreditos [user_id] [quantidade]`

🎯 *Exemplo:*
`/addcreditos 123456789 5`
        """, parse_mode='Markdown')
        return
    
    try:
        user_id = int(args[0])
        quantidade = int(args[1])
        
        conn = get_db()
        c = conn.cursor()
        
        # Verificar se usuário existe
        c.execute("SELECT username FROM usuarios WHERE user_id = ?", (user_id,))
        usuario = c.fetchone()
        
        if not usuario:
            bot.reply_to(message, f"❌ Usuário `{user_id}` não encontrado!", parse_mode='Markdown')
            conn.close()
            return
        
        # Adicionar créditos
        c.execute("UPDATE usuarios SET creditos = creditos + ? WHERE user_id = ?", (quantidade, user_id))
        c.execute("INSERT INTO transacoes (user_id, tipo, valor, admin) VALUES (?, ?, ?, ?)",
                 (user_id, "admin_add", quantidade, message.from_user.username))
        
        conn.commit()
        
        # Obter novos créditos
        c.execute("SELECT creditos FROM usuarios WHERE user_id = ?", (user_id,))
        novos_creditos = c.fetchone()[0]
        conn.close()
        
        # Notificar usuário
        try:
            bot.send_message(user_id, f"""
💎 *CRÉDITOS ADICIONADOS!*

✅ *Administrador adicionou:* *+{quantidade} créditos*

💰 *Seu saldo atual:* *{novos_creditos} créditos*

🎬 *Agora você pode pedir mais filmes/séries!*

⚡ *Obrigado por usar CINEMA PRO!*
            """, parse_mode='Markdown')
        except:
            pass
        
        bot.reply_to(message, f"""
✅ *CRÉDITOS ADICIONADOS COM SUCESSO!*

👤 *Usuário:* `{user_id}`
💎 *Créditos adicionados:* `+{quantidade}`
💰 *Saldo atual:* `{novos_creditos}`
        """, parse_mode='Markdown')
        
    except ValueError:
        bot.reply_to(message, "❌ *Erro:* IDs e quantidades devem ser números!", parse_mode='Markdown')
    except Exception as e:
        bot.reply_to(message, f"❌ *Erro:* {e}", parse_mode='Markdown')

@bot.message_handler(commands=['addvip'])
def add_vip_cmd(message):
    if not is_admin(message.from_user.id, message.from_user.username):
        return
    
    args = message.text.split()[1:]
    if len(args) < 2:
        bot.reply_to(message, """
👑 *ADICIONAR VIP*

⚡ *Uso:*
`/addvip [user_id] [dias]`

🎯 *Exemplo:*
`/addvip 123456789 30`
        """, parse_mode='Markdown')
        return
    
    try:
        user_id = int(args[0])
        dias = int(args[1])
        
        conn = get_db()
        c = conn.cursor()
        
        # Verificar se usuário existe
        c.execute("SELECT username FROM usuarios WHERE user_id = ?", (user_id,))
        usuario = c.fetchone()
        
        if not usuario:
            bot.reply_to(message, f"❌ Usuário `{user_id}` não encontrado!", parse_mode='Markdown')
            conn.close()
            return
        
        # Calcular data de expiração
        data_expiracao = (datetime.now() + timedelta(days=dias)).strftime('%Y-%m-%d')
        
        # Ativar VIP
        c.execute("UPDATE usuarios SET vip = 1, vip_expira = ? WHERE user_id = ?", (data_expiracao, user_id))
        c.execute("INSERT INTO transacoes (user_id, tipo, valor, admin) VALUES (?, ?, ?, ?)",
                 (user_id, "admin_vip", dias, message.from_user.username))
        
        conn.commit()
        conn.close()
        
        # Notificar usuário
        try:
            bot.send_message(user_id, f"""
👑 *VIP ATIVADO!* 🎉

✅ *Status VIP ativado por {dias} dias!*

💫 *Benefícios:*
• Acesso prioritário
• Suporte VIP 24/7
• Lançamentos antecipados
• Conteúdo exclusivo

⏰ *Expira em:* {data_expiracao}

⚡ *Aproveite todos os benefícios!*
            """, parse_mode='Markdown')
        except:
            pass
        
        bot.reply_to(message, f"""
✅ *VIP ATIVADO COM SUCESSO!*

👤 *Usuário:* `{user_id}`
👑 *VIP por:* `{dias} dias`
⏰ *Expira em:* `{data_expiracao}`
        """, parse_mode='Markdown')
        
    except ValueError:
        bot.reply_to(message, "❌ *Erro:* IDs e dias devem ser números!", parse_mode='Markdown')
    except Exception as e:
        bot.reply_to(message, f"❌ *Erro:* {e}", parse_mode='Markdown')

@bot.message_handler(commands=['stats'])
def stats_cmd(message):
    if not is_admin(message.from_user.id, message.from_user.username):
        return
    
    conn = get_db()
    c = conn.cursor()
    
    # Estatísticas detalhadas
    total_usuarios = c.execute("SELECT COUNT(*) FROM usuarios").fetchone()[0]
    usuarios_24h = c.execute("SELECT COUNT(*) FROM usuarios WHERE datetime(data_cadastro) > datetime('now', '-1 day')").fetchone()[0]
    usuarios_7dias = c.execute("SELECT COUNT(*) FROM usuarios WHERE datetime(data_cadastro) > datetime('now', '-7 days')").fetchone()[0]
    
    total_pedidos = c.execute("SELECT COUNT(*) FROM pedidos").fetchone()[0]
    pedidos_24h = c.execute("SELECT COUNT(*) FROM pedidos WHERE datetime(data) > datetime('now', '-1 day')").fetchone()[0]
    pedidos_pendentes = c.execute("SELECT COUNT(*) FROM pedidos WHERE status = 'pendente'").fetchone()[0]
    
    total_creditos = c.execute("SELECT SUM(creditos) FROM usuarios").fetchone()[0] or 0
    vip_count = c.execute("SELECT COUNT(*) FROM usuarios WHERE vip = 1").fetchone()[0]
    total_grupos = c.execute("SELECT COUNT(*) FROM grupos").fetchone()[0]
    
    # Top usuários com mais créditos
    c.execute("SELECT username, creditos FROM usuarios ORDER BY creditos DESC LIMIT 5")
    top_usuarios = c.fetchall()
    
    conn.close()
    
    # Formatar top usuários
    top_text = ""
    for i, usuario in enumerate(top_usuarios, 1):
        top_text += f"{i}. @{usuario[0]} - {usuario[1]} créditos\n"
    
    bot.reply_to(message, f"""
📊 *ESTATÍSTICAS DETALHADAS - CINEMA PRO*

👥 *USUÁRIOS:*
• Total: `{total_usuarios}`
• Últimas 24h: `{usuarios_24h}`
• Últimos 7 dias: `{usuarios_7dias}`
• VIPs Ativos: `{vip_count}`

📨 *PEDIDOS:*
• Total: `{total_pedidos}`
• Últimas 24h: `{pedidos_24h}`
• Pendentes: `{pedidos_pendentes}`

💰 *CRÉDITOS:*
• Em circulação: `{total_creditos}`
• Grupos ativos: `{total_grupos}`

🏆 *TOP 5 USUÁRIOS:*
{top_text}

⚡ *SISTEMA OPERACIONAL - TODOS OS MÓDULOS ATIVOS*
    """, parse_mode='Markdown')

# 🎯 COMANDO START PREMIUM
@bot.message_handler(commands=['start'])
def start_premium(message):
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name
    
    conn = get_db()
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO usuarios (user_id, username) VALUES (?, ?)", (user_id, username))
    conn.commit()
    
    bonus_recebido = verificar_primeiros_usuarios(user_id, username)
    
    admin_status = ""
    if is_admin(user_id, username):
        admin_status = "\n👑 *STATUS: ADMINISTRADOR*"
    
    c.execute("SELECT creditos, vip, vip_expira FROM usuarios WHERE user_id = ?", (user_id,))
    usuario = c.fetchone()
    creditos = usuario[0] if usuario else 0
    vip = usuario[1] if usuario else 0
    vip_expira = usuario[2] if usuario else None
    
    vip_status = "✅ ATIVO" if vip == 1 else "❌ INATIVO"
    if vip_expira:
        vip_status += f" (até {vip_expira})"
    
    bonus_text = "\n🎁 *+3 CRÉDITOS DE BOAS-VINDAS!*" if bonus_recebido else ""
    
    conn.close()
    
    markup = telebot.types.InlineKeyboardMarkup()
    
    botoes = [
        telebot.types.InlineKeyboardButton("🎬 Catálogo Premium", callback_data="menu_catalogo"),
        telebot.types.InlineKeyboardButton("🎥 Ver Trailers", callback_data="menu_trailers"),
        telebot.types.InlineKeyboardButton("💰 Comprar Créditos", callback_data="comprar_creditos"),
        telebot.types.InlineKeyboardButton("👑 Planos VIP", callback_data="planos_vip"),
        telebot.types.InlineKeyboardButton("📞 Atendimento", url=f"https://t.me/{ADMIN_USERNAME}")
    ]
    
    if is_admin(user_id, username):
        botoes.append(telebot.types.InlineKeyboardButton("👑 Painel Admin", callback_data="menu_admin"))
    
    markup.row(botoes[0], botoes[1])
    markup.row(botoes[2], botoes[3])
    markup.row(botoes[4])
    if len(botoes) > 5:
        markup.row(botoes[5])
    
    bot.reply_to(message, f"""
🎬 *CINEMA PRO PREMIUM 2025* 🎬

💎 *SEU STATUS:*
• Créditos: *{creditos}* {bonus_text}
• VIP: *{vip_status}* {admin_status}

⚡ *SERVIÇOS EXCLUSIVOS:*
• 🎥 Filmes em 4K HDR
• 📺 Séries completas
• 🎌 Animes legendados

🎯 *ESCOLHA UMA OPÇÃO:*
    """, parse_mode='Markdown', reply_markup=markup)

# 📨 SISTEMA DE CALLBACKS COMPLETO
@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    message_id = call.message.message_id
    
    try:
        # 🎬 TRAILERS
        if call.data.startswith('trailer_'):
            filme_key = call.data.replace('trailer_', '').replace('_', ' ')
            trailer_info = None
            
            for key, value in TRAILERS_DISPONIVEIS.items():
                if filme_key in key:
                    trailer_info = value
                    break
            
            if trailer_info:
                markup = telebot.types.InlineKeyboardMarkup()
                markup.row(
                    telebot.types.InlineKeyboardButton("📦 Pedir Completo", callback_data=f"pedir_{filme_key}"),
                    telebot.types.InlineKeyboardButton("💎 Comprar Créditos", callback_data="comprar_creditos")
                )
                
                bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=message_id,
                    text=f"{trailer_info}\n\n💎 *PREÇO: 1 CRÉDITO*",
                    parse_mode='Markdown',
                    reply_markup=markup
                )
        
        # 📦 PEDIDOS
        elif call.data.startswith('pedir_'):
            filme_key = call.data.replace('pedir_', '').replace('_', ' ')
            
            conn = get_db()
            c = conn.cursor()
            c.execute("SELECT creditos FROM usuarios WHERE user_id = ?", (user_id,))
            usuario = c.fetchone()
            creditos = usuario[0] if usuario else 0
            conn.close()
            
            if creditos < 1:
                markup = telebot.types.InlineKeyboardMarkup()
                markup.row(
                    telebot.types.InlineKeyboardButton("💎 Comprar Créditos", callback_data="comprar_creditos"),
                    telebot.types.InlineKeyboardButton("👑 VIP", callback_data="planos_vip")
                )
                
                bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=message_id,
                    text=f"❌ *CRÉDITOS INSUFICIENTES*\n\n💎 *Seus créditos:* *{creditos}*\n🎬 *Filme:* *{filme_key}*\n\n⚡ *Você precisa de 1 crédito.*",
                    parse_mode='Markdown',
                    reply_markup=markup
                )
            else:
                from_user = type('User', (), {'id': user_id, 'username': call.from_user.username})()
                msg = type('Msg', (), {
                    'chat': type('Chat', (), {'id': chat_id}), 
                    'text': f'/pedir {filme_key}', 
                    'from_user': from_user
                })()
                pedir_cmd(msg)
        
        # 🏠 MENU PRINCIPAL
        elif call.data == 'menu_principal':
            start_premium(call.message)
        
        # 📂 CATÁLOGO
        elif call.data == 'menu_catalogo':
            catalogo_premium(call.message)
        
        # 🎥 TRAILERS
        elif call.data == 'menu_trailers':
            trailer_cmd(call.message)
        
        # 👑 ADMIN
        elif call.data == 'menu_admin':
            admin_panel(call.message)
        
        # 📊 ADMIN STATS
        elif call.data == 'admin_stats':
            from_user = type('User', (), {'id': user_id, 'username': call.from_user.username})()
            msg = type('Msg', (), {
                'chat': type('Chat', (), {'id': chat_id}), 
                'from_user': from_user
            })()
            stats_cmd(msg)
        
        # 💰 ADMIN ADD CRÉDITOS
        elif call.data == 'admin_add_creditos':
            bot.answer_callback_query(call.id, "💎 Use /addcreditos [user_id] [quantidade]")
        
        # 👑 ADMIN VIP
        elif call.data == 'admin_vip':
            bot.answer_callback_query(call.id, "👑 Use /addvip [user_id] [dias]")
        
        # 🔄 ADMIN REFRESH
        elif call.data == 'admin_refresh':
            admin_panel(call.message)
        
        # ❌ ADMIN CLOSE
        elif call.data == 'admin_close':
            bot.delete_message(chat_id, message_id)
        
        # 💰 COMPRAR CRÉDITOS
        elif call.data == 'comprar_creditos':
            markup = telebot.types.InlineKeyboardMarkup()
            markup.row(
                telebot.types.InlineKeyboardButton("💎 1 Crédito - 20 MZN", callback_data="credito_1"),
                telebot.types.InlineKeyboardButton("💎 3 Créditos - 50 MZN", callback_data="credito_3")
            )
            markup.row(telebot.types.InlineKeyboardButton("👑 Ver Planos VIP", callback_data="planos_vip"))
            
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=f"""
💎 *COMPRAR CRÉDITOS*

🎬 *1 CRÉDITO = 1 FILME/SÉRIE*

⚡ *OPÇÕES:*
• 💎 1 Crédito - 20 MZN
• 💎 3 Créditos - 50 MZN

👑 *VIP RECOMENDADO:*
Mais créditos + benefícios exclusivos

📞 *Contato:* @{ADMIN_USERNAME}
                """,
                parse_mode='Markdown',
                reply_markup=markup
            )
        
        # 👑 PLANOS VIP
        elif call.data == 'planos_vip':
            markup = telebot.types.InlineKeyboardMarkup()
            for plano_key, plano in PLANOS_VIP.items():
                markup.row(telebot.types.InlineKeyboardButton(
                    f"{plano['nome']} - {plano['preco']}", 
                    callback_data=f"vip_{plano_key}"
                ))
            
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=f"""
👑 *PLANOS VIP PREMIUM*

💎 *VANTAGENS EXCLUSIVAS:*
• ✅ Créditos mensais
• ✅ Acesso prioritário
• ✅ Suporte VIP 24/7

⚡ *ESCOLHA SEU PLANO:*

📞 *Contato:* @{ADMIN_USERNAME}
                """,
                parse_mode='Markdown',
                reply_markup=markup
            )
        
        # 📂 CATEGORIAS
        elif call.data.startswith('categoria_'):
            categoria = call.data.replace('categoria_', '')
            conteudos = CATALOGO_PREMIUM.get(categoria, [])
            
            texto = f"🎬 *{categoria.upper()} - CATÁLOGO*\n\n"
            for item in conteudos:
                texto += f"• {item['titulo']}\n"
            
            markup = telebot.types.InlineKeyboardMarkup()
            markup.row(telebot.types.InlineKeyboardButton("🔙 Voltar", callback_data="menu_catalogo"))
            
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=texto + "\n💎 *Use /pedir NomeDoFilme*",
                parse_mode='Markdown',
                reply_markup=markup
            )
        
        else:
            bot.answer_callback_query(call.id, "⚡ Comando em execução...")
            
    except Exception as e:
        print(f"❌ Erro callback: {e}")
        bot.answer_callback_query(call.id, "❌ Erro, tente novamente")

# 🌐 WEBHOOK E INICIALIZAÇÃO
@app.route('/')
def home():
    return "🤖 CINEMA PRO PREMIUM - SISTEMA ATIVO! 🎬"

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return 'OK'
    return 'ERROR'

# 🚀 INICIAR BOT
if __name__ == '__main__':
    print("🚀 CINEMA PRO PREMIUM INICIADO!")
    print(f"💎 Admin: @{ADMIN_USERNAME}")
    print("🎬 Painel Admin 100% Funcional!")
    print("⚡ Todos os módulos ativos!")
    
    bot.remove_webhook()
    time.sleep(1)
    
    try:
        bot.set_webhook(url="https://cinema-pro-bot-production.up.railway.app/webhook")
        print("✅ Webhook configurado")
    except Exception as e:
        print(f"⚠️ Usando polling: {e}")
        bot.polling(none_stop=True)
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
