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
ADMIN_ID =5125563829   # Atualize com seu ID

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

# 🎬 CATÁLOGO PROFISSIONAL COM CAPAS
CATALOGO_PREMIUM = {
    'lancamentos_4k': [
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
        },
        {
            'titulo': '🎬 SPIDER-MAN: BEYOND THE SPIDER-VERSE',
            'capa': 'https://i.imgur.com/spiderman-cap.jpg',
            'trailer': 'https://youtu.be/spiderman-trailer',
            'qualidade': '4K HDR • Animação',
            'genero': 'Ação • Animação • Super-herói',
            'duracao': '2h 28m',
            'ano': '2025',
            'descricao': 'Miles Morales enfrenta o multiverso em uma aventura visualmente deslumbrante.'
        }
    ],
    'series_premium': [
        {
            'titulo': '📺 STRANGER THINGS 5 - TEMPORADA COMPLETA',
            'capa': 'https://i.imgur.com/stranger5-cap.jpg',
            'trailer': 'https://youtu.be/stranger5-trailer',
            'qualidade': '4K Dolby Vision • 8 Episódios',
            'genero': 'Suspense • Ficção Científica • Drama',
            'duracao': 'Temporada Completa',
            'ano': '2025',
            'descricao': 'A temporada final que encerra a saga de Hawkins e o Mundo Invertido.'
        },
        {
            'titulo': '📺 THE LAST OF US 3 - TODOS OS EPISÓDIOS',
            'capa': 'https://i.imgur.com/lastofus3-cap.jpg',
            'trailer': 'https://youtu.be/lastofus3-trailer',
            'qualidade': '4K HDR • 10 Episódios',
            'genero': 'Drama • Ação • Pós-apocalíptico',
            'duracao': 'Temporada Completa',
            'ano': '2025',
            'descricao': 'Continua a jornada emocionante em um mundo devastado por infecção.'
        }
    ],
    'animes_exclusivos': [
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

# 🎭 TRAILERS E AMOSTRAS
TRAILERS_DISPONIVEIS = {
    'VENOM 3': '🎬 *Trailer Venom 3*\nhttps://youtu.be/venom3-trailer\n⚡ 2:30 min • Cenas de ação em 4K',
    'AVATAR 4': '🎬 *Trailer Avatar 4*\nhttps://youtu.be/avatar4-trailer\n🌍 3:15 min • Novos mundos revelados', 
    'SPIDER-MAN BEYOND': '🎬 *Trailer Spider-Man Beyond*\nhttps://youtu.be/spiderman-trailer\n🕷️ 2:45 min • Multiverso expandido',
    'STRANGER THINGS 5': '📺 *Trailer Stranger Things 5*\nhttps://youtu.be/stranger5-trailer\n🔮 3:30 min • Temporada final épica',
    'DEMON SLAYER FINAL': '🎌 *Trailer Demon Slayer Final*\nhttps://youtu.be/demonslayer-trailer\n⚔️ 2:15 min • Batalhas emocionantes'
}

# 🎯 RECOMENDAÇÕES DIÁRIAS
RECOMENDACOES_DIARIAS = {
    'segunda': {
        'titulo': '🚀 INÍCIO DE SEMANA ENERGÉTICO!',
        'filme': 'VENOM 3: A ÚLTIMA BATALHA',
        'descricao': 'Comece a semana com ação intensa e cenas espetaculares em 4K!',
        'hashtag': '#SegundaDeAção'
    },
    'terca': {
        'titulo': '🎭 DRAMA E EMOÇÃO!',
        'filme': 'THE LAST OF US 3', 
        'descricao': 'Uma jornada emocional em um mundo pós-apocalíptico.',
        'hashtag': '#TerçaDramática'
    },
    'quarta': {
        'titulo': '🌍 AVENTURA ÉPICA!',
        'filme': 'AVATAR 4: O LEGADO',
        'descricao': 'Meio da semana perfeito para uma aventura em novos mundos!',
        'hashtag': '#QuartaAventura'
    },
    'quinta': {
        'titulo': '🕷️ MULTIVERSO SURPREENDENTE!',
        'filme': 'SPIDER-MAN: BEYOND',
        'descricao': 'Prepare-se para o fim de semana com esta animação incrível!',
        'hashtag': '#QuintaAnimada'
    },
    'sexta': {
        'titulo': '🔮 FIM DE SEMANA MISTERIOSO!', 
        'filme': 'STRANGER THINGS 5',
        'descricao': 'Sexta-feira perfeita para maratonar esta série emocionante!',
        'hashtag': '#SextaMisteriosa'
    },
    'sabado': {
        'titulo': '⚔️ ANIME ÉPICO!',
        'filme': 'DEMON SLAYER: FINAL ARC',
        'descricao': 'Sábado ideal para uma maratona de anime em 4K!',
        'hashtag': '#SábadoAnime'
    },
    'domingo': {
        'titulo': '🎬 CLÁSSICO DO DIA!',
        'filme': 'VENOM 3: A ÚLTIMA BATALHA',
        'descricao': 'Domingão perfeito com o filme mais popular da semana!',
        'hashtag': '#Domingão'
    }
}

# 🗄️ BANCO DE DADOS
def get_db():
    conn = sqlite3.connect('cinema_premium.db', check_same_thread=False)
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
    return (str(username) == ADMIN_USERNAME.replace('@', '') or 
            user_id == ADMIN_ID)

# 🎁 SISTEMA DE 3 CRÉDITOS PARA PRIMEIROS 10 USUÁRIOS
def verificar_primeiros_usuarios(user_id, username):
    conn = get_db()
    c = conn.cursor()
    
    # Contar usuários totais
    total_usuarios = c.execute("SELECT COUNT(*) FROM usuarios").fetchone()[0]
    
    # Verificar se é um dos primeiros 10 e ainda não recebeu
    c.execute("SELECT primeiro_usuario FROM usuarios WHERE user_id = ?", (user_id,))
    usuario = c.fetchone()
    
    if total_usuarios <= 10 and (not usuario or usuario[0] == 0):
        # Adicionar 3 créditos e marcar como premiado
        c.execute("UPDATE usuarios SET creditos = creditos + 3, primeiro_usuario = 1 WHERE user_id = ?", (user_id,))
        c.execute("INSERT INTO transacoes (user_id, tipo, valor, admin) VALUES (?, ?, ?, ?)",
                 (user_id, "bonus_boas_vindas", 3, "sistema"))
        conn.commit()
        conn.close()
        
        # Enviar mensagem de boas-vindas com bônus
        try:
            bot.send_message(user_id, f"""
🎉 *BOAS-VINDAS PREMIUM!* 🎉

Bem-vindo ao *CINEMA PRO*! Como você é um dos nossos primeiros 10 usuários, recebeu:

💎 *+3 CRÉDITOS GRÁTIS!*

🎬 Agora você pode pedir 3 filmes/séries gratuitamente!

⚡ *Como usar:*
`/pedir Nome do Filme` - Para fazer seu primeiro pedido
`/catalogo` - Ver catálogo completo
`/trailer` - Ver trailers antes de pedir

📞 *Dúvidas?* @{ADMIN_USERNAME}

Obrigado por fazer parte do CINEMA PRO! 🚀
            """, parse_mode='Markdown')
        except:
            pass
        return True
    
    conn.close()
    return False

# 👋 MENSAGEM DE BOAS-VINDAS EM GRUPOS
@bot.message_handler(content_types=['new_chat_members'])
def welcome_group(message):
    for member in message.new_chat_members:
        if member.username == bot.get_me().username:
            # Bot adicionado no grupo
            group_id = message.chat.id
            group_title = message.chat.title
            
            conn = get_db()
            c = conn.cursor()
            c.execute("INSERT OR REPLACE INTO grupos (group_id, group_title) VALUES (?, ?)",
                     (group_id, group_title))
            conn.commit()
            conn.close()
            
            # Mensagem de boas-vindas profissional
            welcome_msg = f"""
🎬 *CINEMA PRO - SISTEMA PREMIUM ADICIONADO!* 🎬

Olá *{group_title}*! 🤖

É uma honra fazer parte desta comunidade! Trago o melhor do entretenimento em qualidade premium:

⚡ *SERVIÇOS EXCLUSIVOS:*
• 🎥 *Filmes em 4K HDR/Dolby Vision*
• 📺 *Séries completas ULTRA HD*  
• 🎌 *Animes legendados em alta qualidade*
• 🚀 *Lançamentos em primeira mão*

💎 *SISTEMA AUTOMÁTICO:*
• Recomendações diárias personalizadas
• Trailers exclusivos
• Catálogo sempre atualizado
• Entrega em 15-30 minutos

🎯 *COMANDOS NO GRUPO:*
`/recomendacao` - Filme do dia
`/lancamentos` - Novidades da semana  
`/catalogo` - Catálogo completo
`/trailer` - Ver trailers

📞 *ATENDIMENTO PERSONALIZADO:*
💬 WhatsApp: {CONTATOS['whatsapp']}
👤 Telegram: @{ADMIN_USERNAME}

*Sejam bem-vindos ao mundo do entretenimento premium!* 🎉
            """
            
            bot.send_message(group_id, welcome_msg, parse_mode='Markdown')
            
            # Primeira recomendação automática
            time.sleep(5)
            enviar_recomendacao_diaria(group_id)
            
        else:
            # Novo membro no grupo
            welcome_user = f"""
👋 *BEM-VINDO(A) AO GRUPO!*

Olá *{member.first_name}*! 🎉

Que bom ter você aqui no grupo! 🎬

💡 *DICA EXCLUSIVA:* Use `/start` no privado comigo para acessar nosso catálogo premium de filmes e séries!

⚡ *VANTAGENS:*
• Qualidade 4K garantida
• Entrega super rápida  
• Preços acessíveis
• Atendimento 24/7

🎁 *OFERTA ESPECIAL PARA MEMBROS DO GRUPO!*
            """
            
            bot.send_message(message.chat.id, welcome_user, parse_mode='Markdown')

# 🎯 RECOMENDAÇÃO DIÁRIA AUTOMÁTICA
def enviar_recomendacao_diaria(group_id):
    dia_semana = datetime.now().strftime('%A').lower()
    dias_pt = {
        'monday': 'segunda',
        'tuesday': 'terca', 
        'wednesday': 'quarta',
        'thursday': 'quinta',
        'friday': 'sexta',
        'saturday': 'sabado',
        'sunday': 'domingo'
    }
    
    dia = dias_pt.get(dia_semana, 'segunda')
    recomendacao = RECOMENDACOES_DIARIAS.get(dia, RECOMENDACOES_DIARIAS['segunda'])
    
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row(
        telebot.types.InlineKeyboardButton("🎬 Ver Trailer", callback_data=f"trailer:{recomendacao['filme']}"),
        telebot.types.InlineKeyboardButton("📦 Pedir Agora", callback_data=f"pedir:{recomendacao['filme']}")
    )
    markup.row(
        telebot.types.InlineKeyboardButton("📞 Comprar Créditos", url=f"https://t.me/{ADMIN_USERNAME}"),
        telebot.types.InlineKeyboardButton("🎯 Catálogo Completo", callback_data="catalogo_completo")
    )
    
    recomendacao_msg = f"""
🎬 *RECOMENDAÇÃO DO DIA* 🎬
{recomendacao['hashtag']}

{recomendacao['titulo']}

⚡ *FILME SUGERIDO:*
*{recomendacao['filme']}*

📖 *Sinopse:*
{recomendacao['descricao']}

💎 *Por que assistir hoje?*
• Perfeito para o clima do {dia}
• Qualidade 4K garantida  
• Entrega em 15-30 minutos
• Aprovação de 95% dos usuários

🎯 *Não perca esta experiência cinematográfica!*
    """
    
    try:
        bot.send_message(group_id, recomendacao_msg, parse_mode='Markdown', reply_markup=markup)
    except:
        pass

# 🎬 COMANDO RECOMENDAÇÃO
@bot.message_handler(commands=['recomendacao', 'filmedodia'])
def recomendacao_cmd(message):
    enviar_recomendacao_diaria(message.chat.id)

# 🎥 SISTEMA DE TRAILERS
@bot.message_handler(commands=['trailer'])
def trailer_cmd(message):
    args = message.text.split()[1:]
    
    if not args:
        markup = telebot.types.InlineKeyboardMarkup()
        
        trailers = list(TRAILERS_DISPONIVEIS.keys())[:6]
        for i in range(0, len(trailers), 2):
            row = []
            for j in range(2):
                if i + j < len(trailers):
                    filme = trailers[i + j]
                    row.append(telebot.types.InlineKeyboardButton(
                        f"🎬 {filme.split(':')[0]}", 
                        callback_data=f"trailer:{filme}"
                    ))
            markup.add(*row)
        
        bot.reply_to(message, """
🎬 *TRAILERS EXCLUSIVOS* 🎬

⚠️ *ASSISTA ANTES DE PEDIR!*

Escolha um trailer para ver:

*🎯 VANTAGENS:*
• Veja a qualidade do conteúdo
• Conheça a história antes de comprar
• Cenas exclusivas em alta definição
• Tome a melhor decisão

*💡 APÓS O TRAILER:*
• Pedido completo por 1 crédito
• Filme/série completo em 4K
• Download direto via Google Drive
• Entrega rápida

*🚀 EXPERIÊNCIA COMPLETA!*
        """, parse_mode='Markdown', reply_markup=markup)
        return
    
    filme = ' '.join(args).upper()
    trailer_info = None
    
    for key, value in TRAILERS_DISPONIVEIS.items():
        if filme in key:
            trailer_info = value
            break
    
    if trailer_info:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(
            telebot.types.InlineKeyboardButton("📦 Pedir Completo", callback_data=f"pedir:{key}"),
            telebot.types.InlineKeyboardButton("💎 Comprar Créditos", callback_data="comprar_creditos")
        )
        
        bot.reply_to(message, f"""
{trailer_info}

💫 *VERSÃO COMPLETA INCLUI:*
• Conteúdo integral em 4K HDR
• Download direto via Google Drive/Mega
• Áudio original + legendas PT/EN
• Qualidade cinema garantida
• Entrega em 15-30 minutos

💎 *PREÇO: 1 CRÉDITO*
        """, parse_mode='Markdown', reply_markup=markup)
    else:
        bot.reply_to(message, f"""
❌ *TRAILER NÃO ENCONTRADO*

Não temos trailer disponível para *{filme}*.

💡 *TRAILERS DISPONÍVEIS:*
`/trailer` - Ver lista completa
`/catalogo` - Ver catálogo
        """, parse_mode='Markdown')

# 🎨 CATÁLOGO PROFISSIONAL COM CAPAS
@bot.message_handler(commands=['catalogo', 'lancamentos'])
def catalogo_premium(message):
    markup = telebot.types.InlineKeyboardMarkup()
    
    # Categorias
    markup.row(
        telebot.types.InlineKeyboardButton("🎬 FILMES 4K", callback_data="categoria_filmes"),
        telebot.types.InlineKeyboardButton("📺 SÉRIES", callback_data="categoria_series")
    )
    markup.row(
        telebot.types.InlineKeyboardButton("🎌 ANIMES", callback_data="categoria_animes"),
        telebot.types.InlineKeyboardButton("🚀 LANÇAMENTOS", callback_data="categoria_lancamentos")
    )
    markup.row(
        telebot.types.InlineKeyboardButton("🎥 VER TRAILERS", callback_data="ver_trailers"),
        telebot.types.InlineKeyboardButton("📞 ATENDIMENTO", url=f"https://t.me/{ADMIN_USERNAME}")
    )
    
    bot.reply_to(message, f"""
🎬 *CATÁLOGO PREMIUM 2025* 🎬

💫 *EXPERIÊNCIA CINEMATOGRÁFICA COMPLETA*

⚡ *CATEGORIAS EXCLUSIVAS:*

🎬 *FILMES 4K ULTRA HD*
• Qualidade HDR/Dolby Vision
• Áudio Dolby Atmos
• Lançamentos mundiais

📺 *SÉRIES COMPLETAS*  
• Temporadas íntegras
• Qualidade streaming
• Conteúdo exclusivo

🎌 *ANIMES LEGENDADOS*
• Japonês original
• Legendas profissionais
• Lançamentos simultâneos

🚀 *LANÇAMENTOS 2025*
• Primeira exibição
• Conteúdo inédito
• Qualidade garantida

💎 *SISTEMA PROFISSIONAL:*
• Entrega automática
• Suporte 24/7
• Qualidade verificada

📞 *ATENDIMENTO:* @{ADMIN_USERNAME}
    """, parse_mode='Markdown', reply_markup=markup)

# 👑 SISTEMA ADMIN COMPLETO (mantenha todos os comandos admin anteriores)
@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if not is_admin(message.from_user.id, message.from_user.username):
        bot.reply_to(message, "❌ *Acesso negado!* Apenas administradores.", parse_mode='Markdown')
        return
    
    conn = get_db()
    c = conn.cursor()
    
    total_usuarios = c.execute("SELECT COUNT(*) FROM usuarios").fetchone()[0]
    total_pedidos = c.execute("SELECT COUNT(*) FROM pedidos").fetchone()[0]
    pedidos_pendentes = c.execute("SELECT COUNT(*) FROM pedidos WHERE status = 'pendente'").fetchone()[0]
    total_creditos = c.execute("SELECT SUM(creditos) FROM usuarios").fetchone()[0] or 0
    vip_count = c.execute("SELECT COUNT(*) FROM usuarios WHERE vip = 1").fetchone()[0]
    total_grupos = c.execute("SELECT COUNT(*) FROM grupos").fetchone()[0]
    
    conn.close()
    
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row(
        telebot.types.InlineKeyboardButton("📊 Estatísticas", callback_data="admin_stats"),
        telebot.types.InlineKeyboardButton("👥 Usuários", callback_data="admin_users")
    )
    markup.row(
        telebot.types.InlineKeyboardButton("💰 Créditos", callback_data="admin_creditos"),
        telebot.types.InlineKeyboardButton("📨 Pedidos", callback_data="admin_pedidos")
    )
    markup.row(
        telebot.types.InlineKeyboardButton("👑 VIP", callback_data="admin_vip"),
        telebot.types.InlineKeyboardButton("👥 Grupos", callback_data="admin_grupos")
    )
    markup.row(
        telebot.types.InlineKeyboardButton("📢 Anúncio", callback_data="admin_anuncio"),
        telebot.types.InlineKeyboardButton("⚙️ Sistema", callback_data="admin_sistema")
    )
    
    bot.reply_to(message, f"""
👑 *PAINEL ADMIN - CINEMA PRO PREMIUM*

📊 *ESTATÍSTICAS GERAIS:*
• 👥 Total Usuários: `{total_usuarios}`
• 💎 Créditos em Circulação: `{total_creditos}`
• 👑 VIPs Ativos: `{vip_count}`
• 📨 Total Pedidos: `{total_pedidos}`
• ⏳ Pedidos Pendentes: `{pedidos_pendentes}`
• 👥 Grupos Ativos: `{total_grupos}`

⚡ *SISTEMA ATIVO COM:*
• 🎬 Catálogo Profissional
• 🎥 Sistema de Trailers  
• 🎯 Recomendações Diárias
• 👋 Boas-vindas Automáticas
• 🎁 Bônus Primeiros Usuários

🎯 *ESCOLHA UMA OPÇÃO:*
    """, parse_mode='Markdown', reply_markup=markup)

# 🎯 COMANDO START PREMIUM
@bot.message_handler(commands=['start'])
def start_premium(message):
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name
    
    conn = get_db()
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO usuarios (user_id, username) VALUES (?, ?)", (user_id, username))
    conn.commit()
    
    # Verificar bônus primeiros usuários
    bonus_recebido = verificar_primeiros_usuarios(user_id, username)
    
    # Verificar se é admin
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
        telebot.types.InlineKeyboardButton("🎬 Catálogo Premium", callback_data="catalogo_premium"),
        telebot.types.InlineKeyboardButton("🎥 Ver Trailers", callback_data="ver_trailers"),
        telebot.types.InlineKeyboardButton("💰 Planos VIP", callback_data="planos_vip"),
        telebot.types.InlineKeyboardButton("🌎 PayPal", callback_data="paypal_premium"),
        telebot.types.InlineKeyboardButton("📞 Atendimento", url=f"https://t.me/{ADMIN_USERNAME}")
    ]
    
    if is_admin(user_id, username):
        botoes.append(telebot.types.InlineKeyboardButton("👑 Painel Admin", callback_data="admin_panel"))
    
    markup.add(*botoes[:2])
    markup.add(*botoes[2:4])
    markup.add(botoes[4])
    if len(botoes) > 5:
        markup.add(botoes[5])
    
    bot.reply_to(message, f"""
🎬 *CINEMA PRO PREMIUM 2025* 🎬

💎 *SEU STATUS:*
• Créditos: *{creditos}* {bonus_text}
• VIP: *{vip_status}* {admin_status}

⚡ *SERVIÇOS EXCLUSIVOS:*
• 🎥 Filmes em 4K HDR/Dolby Vision
• 📺 Séries completas ULTRA HD
• 🎌 Animes legendados profissionalmente
• 🚀 Lançamentos em primeira mão

💫 *VANTAGENS:*
• Entrega em 15-30 minutos
• Qualidade cinema garantida
• Suporte 24/7 prioritário
• Sistema automático profissional

🎯 *ESCOLHA UMA OPÇÃO:*
    """, parse_mode='Markdown', reply_markup=markup)

# 📨 SISTEMA DE CALLBACKS COMPLETO
@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    
    try:
        if call.data.startswith('trailer:'):
            filme = call.data.split(':', 1)[1]
            trailer_info = TRAILERS_DISPONIVEIS.get(filme)
            
            if trailer_info:
                markup = telebot.types.InlineKeyboardMarkup()
                markup.row(
                    telebot.types.InlineKeyboardButton("📦 Pedir Completo", callback_data=f"pedir:{filme}"),
                    telebot.types.InlineKeyboardButton("💎 Comprar Créditos", callback_data="comprar_creditos")
                )
                
                bot.send_message(chat_id, f"""
{trailer_info}

💫 *VERSÃO COMPLETA INCLUI:*
• Conteúdo integral em 4K HDR
• Download direto via Google Drive/Mega
• Áudio original + legendas PT/EN
• Qualidade cinema garantida
• Entrega em 15-30 minutos

💎 *PREÇO: 1 CRÉDITO*
                """, parse_mode='Markdown', reply_markup=markup)
        
        elif call.data.startswith('pedir:'):
            filme = call.data.split(':', 1)[1]
            fake_msg = type('Msg', (), {'chat': type('Chat', (), {'id': chat_id}), 'text': f'/pedir {filme}', 'from_user': type('User', (), {'id': user_id, 'username': call.from_user.username})})()
            pedir_cmd(fake_msg)
        
        elif call.data == 'catalogo_premium':
            catalogo_premium(call.message)
        
        elif call.data == 'ver_trailers':
            trailer_cmd(call.message)
        
        elif call.data == 'admin_panel':
            admin_panel(call.message)
            
        bot.answer_callback_query(call.id)
        
    except Exception as e:
        bot.answer_callback_query(call.id, "❌ Erro, tente novamente")
        print(f"Erro callback: {e}")

# 🌐 WEBHOOK E INICIALIZAÇÃO (mantenha igual)
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
    print("🎬 Sistema Profissional Ativo!")
    
    bot.remove_webhook()
    time.sleep(1)
    
    try:
        bot.set_webhook(url="https://cinema-pro-bot-production.up.railway.app/webhook")
        print("✅ Webhook configurado")
    except:
        print("⚠️ Usando polling")
        bot.polling(none_stop=True)
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

