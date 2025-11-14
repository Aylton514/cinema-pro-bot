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
        },
        {
            'titulo': '🎌 ATTACK ON TITAN: FINAL CHAPTERS',
            'capa': 'https://i.imgur.com/aot-final.jpg',
            'trailer': 'https://youtu.be/aot-final-trailer',
            'qualidade': '4K HDR • Legendado PT-BR',
            'genero': 'Anime • Ação • Drama',
            'duracao': 'Capítulos Finais',
            'ano': '2025',
            'descricao': 'O épico final da batalha pela humanidade.'
        }
    ]
}

# 🎭 TRAILERS DISPONÍVEIS
TRAILERS_DISPONIVEIS = {
    'VENOM 3': '🎬 *Trailer Venom 3*\nhttps://youtu.be/venom3-trailer\n⚡ 2:30 min • Cenas de ação em 4K',
    'AVATAR 4': '🎬 *Trailer Avatar 4*\nhttps://youtu.be/avatar4-trailer\n🌍 3:15 min • Novos mundos revelados', 
    'SPIDER-MAN BEYOND': '🎬 *Trailer Spider-Man Beyond*\nhttps://youtu.be/spiderman-trailer\n🕷️ 2:45 min • Multiverso expandido',
    'STRANGER THINGS 5': '📺 *Trailer Stranger Things 5*\nhttps://youtu.be/stranger5-trailer\n🔮 3:30 min • Temporada final épica',
    'DEMON SLAYER FINAL': '🎌 *Trailer Demon Slayer Final*\nhttps://youtu.be/demonslayer-trailer\n⚔️ 2:15 min • Batalhas emocionantes',
    'THE LAST OF US 3': '📺 *Trailer The Last of Us 3*\nhttps://youtu.be/lastofus3-trailer\n🧟 3:10 min • Drama intenso'
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
        'filme': 'AVATAR 4: O LEGADO',
        'descricao': 'Domingão perfeito com o filme mais popular da semana!',
        'hashtag': '#Domingão'
    }
}

# 💰 PLANOS VIP
PLANOS_VIP = {
    '1_mes': {
        'nome': '💎 VIP 1 MÊS',
        'preco': '50 MZN',
        'beneficios': [
            '✅ 10 Créditos Mensais',
            '✅ Acesso Prioritário',
            '✅ Suporte VIP 24/7',
            '✅ Lançamentos Antecipados',
            '✅ Catálogo Exclusivo'
        ]
    },
    '3_meses': {
        'nome': '🔥 VIP 3 MESES', 
        'preco': '120 MZN',
        'beneficios': [
            '✅ 35 Créditos (5 bônus)',
            '✅ Todos benefícios VIP',
            '✅ Acesso Ilimitado',
            '✅ Pedidos Ilimitados',
            '✅ Presentes Exclusivos'
        ]
    },
    '6_meses': {
        'nome': '👑 VIP 6 MESES',
        'preco': '200 MZN', 
        'beneficios': [
            '✅ 80 Créditos (20 bônus)',
            '✅ Status Premium',
            '✅ Conteúdo Exclusivo',
            '✅ Suporte Personalizado',
            '✅ Vantagens Únicas'
        ]
    }
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
            bot.send_message(user_id, """
🎉 *BOAS-VINDAS PREMIUM!* 🎉

Bem-vindo ao *CINEMA PRO*! Como você é um dos nossos primeiros 10 usuários, recebeu:

💎 *+3 CRÉDITOS GRÁTIS!*

🎬 Agora você pode pedir 3 filmes/séries gratuitamente!

⚡ *Como usar:*
`/pedir Nome do Filme` - Para fazer seu primeiro pedido
`/catalogo` - Ver catálogo completo
`/trailer` - Ver trailers antes de pedir

📞 *Dúvidas?* @{}
            """.format(ADMIN_USERNAME), parse_mode='Markdown')
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
            
            welcome_msg = """
🎬 *CINEMA PRO - SISTEMA PREMIUM ADICIONADO!* 🎬

Olá *{}*! 🤖

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
💬 WhatsApp: {}
👤 Telegram: @{}

*Sejam bem-vindos ao mundo do entretenimento premium!* 🎉
            """.format(group_title, CONTATOS['whatsapp'], ADMIN_USERNAME)
            
            bot.send_message(group_id, welcome_msg, parse_mode='Markdown')
            time.sleep(5)
            enviar_recomendacao_diaria(group_id)
            
        else:
            welcome_user = """
👋 *BEM-VINDO(A) AO GRUPO!*

Olá *{}*! 🎉

Que bom ter você aqui no grupo! 🎬

💡 *DICA EXCLUSIVA:* Use `/start` no privado comigo para acessar nosso catálogo premium de filmes e séries!

⚡ *VANTAGENS:*
• Qualidade 4K garantida
• Entrega super rápida  
• Preços acessíveis
• Atendimento 24/7

🎁 *OFERTA ESPECIAL PARA MEMBROS DO GRUPO!*
            """.format(member.first_name)
            
            bot.send_message(message.chat.id, welcome_user, parse_mode='Markdown')

# 🎯 RECOMENDAÇÃO DIÁRIA
def enviar_recomendacao_diaria(chat_id):
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
        telebot.types.InlineKeyboardButton("🎬 Ver Trailer", callback_data=f"trailer_{recomendacao['filme'].split(':')[0].upper().replace(' ', '_')}"),
        telebot.types.InlineKeyboardButton("📦 Pedir Agora", callback_data=f"pedir_{recomendacao['filme'].split(':')[0].upper().replace(' ', '_')}")
    )
    markup.row(
        telebot.types.InlineKeyboardButton("📞 Comprar Créditos", callback_data="comprar_creditos"),
        telebot.types.InlineKeyboardButton("🎯 Catálogo", callback_data="menu_catalogo")
    )
    
    recomendacao_msg = """
🎬 *RECOMENDAÇÃO DO DIA* 🎬
{}

{}

⚡ *FILME SUGERIDO:*
*{}*

📖 *Sinopse:*
{}

💎 *Por que assistir hoje?*
• Perfeito para o clima do {}
• Qualidade 4K garantida  
• Entrega em 15-30 minutos
• Aprovação de 95% dos usuários

🎯 *Não perca esta experiência cinematográfica!*
    """.format(recomendacao['hashtag'], recomendacao['titulo'], recomendacao['filme'], 
               recomendacao['descricao'], dia)
    
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
    args = message.text.split()[1:]
    
    if not args:
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
        
        markup.add(telebot.types.InlineKeyboardButton("🔙 Voltar", callback_data="menu_principal"))
        
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
            telebot.types.InlineKeyboardButton("📦 Pedir Completo", callback_data=f"pedir_{filme.split()[0]}"),
            telebot.types.InlineKeyboardButton("💎 Comprar Créditos", callback_data="comprar_creditos")
        )
        markup.row(telebot.types.InlineKeyboardButton("🔙 Voltar", callback_data="menu_trailers"))
        
        bot.reply_to(message, """
{}

💫 *VERSÃO COMPLETA INCLUI:*
• Conteúdo integral em 4K HDR
• Download direto via Google Drive/Mega
• Áudio original + legendas PT/EN
• Qualidade cinema garantida
• Entrega em 15-30 minutos

💎 *PREÇO: 1 CRÉDITO*
        """.format(trailer_info), parse_mode='Markdown', reply_markup=markup)
    else:
        bot.reply_to(message, f"""
❌ *TRAILER NÃO ENCONTRADO*

Não temos trailer disponível para *{filme}*.

💡 *TRAILERS DISPONÍVEIS:*
`/trailer` - Ver lista completa
`/catalogo` - Ver catálogo
        """, parse_mode='Markdown')

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
        telebot.types.InlineKeyboardButton("🚀 TODOS", callback_data="categoria_todos")
    )
    markup.row(
        telebot.types.InlineKeyboardButton("🎥 TRAILERS", callback_data="menu_trailers"),
        telebot.types.InlineKeyboardButton("📞 ATENDIMENTO", url=f"https://t.me/{ADMIN_USERNAME}")
    )
    markup.row(telebot.types.InlineKeyboardButton("🔙 INÍCIO", callback_data="menu_principal"))
    
    bot.reply_to(message, """
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

📞 *ATENDIMENTO:* @{}
    """.format(ADMIN_USERNAME), parse_mode='Markdown', reply_markup=markup)

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
        bot.reply_to(message, """
📦 *FAZER PEDIDO*

💎 *Seus créditos:* *{}*

⚡ *Como pedir:*
`/pedir Nome do Filme`

🎯 *Exemplos:*
`/pedir Venom 3`
`/pedir Stranger Things 5`
`/pedir Demon Slayer`

💡 *Dica:* Use `/catalogo` para ver o catálogo completo!
        """.format(creditos), parse_mode='Markdown')
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

💫 *Opções:*
• Comprar créditos avulsos
• Assinar plano VIP
• Ganhar créditos indicando amigos

🎁 *Promoção:* Primeiros 10 usuários ganham 3 créditos grátis!
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
⏰ *Data:* {datetime.now().strftime('%d/%m/%Y %H:%M')}

⚡ *Status:* Processando
        """
        bot.send_message(ADMIN_ID, admin_msg, parse_mode='Markdown')
    except:
        pass
    
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row(
        telebot.types.InlineKeyboardButton("📞 Acompanhar Pedido", url=f"https://t.me/{ADMIN_USERNAME}"),
        telebot.types.InlineKeyboardButton("🎬 Novo Pedido", callback_data="menu_catalogo")
    )
    
    bot.reply_to(message, f"""
✅ *PEDIDO CONFIRMADO!* ✅

🆔 *Pedido:* *#{pedido_id}*
🎬 *Filme:* *{filme}*
💎 *Créditos utilizados:* 1
💰 *Créditos restantes:* *{creditos - 1}*

⏰ *Tempo de entrega:* 15-30 minutos
📦 *Formato:* Google Drive/Mega
🎯 *Qualidade:* 4K HDR Garantida

📞 *Acompanhamento:*
Entre em contato com @{ADMIN_USERNAME} para acompanhar seu pedido.

⚡ *Obrigado pela preferência!*
    """, parse_mode='Markdown', reply_markup=markup)

# 👑 PAINEL ADMIN
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
                markup.row(telebot.types.InlineKeyboardButton("🔙 Voltar", callback_data="menu_trailers"))
                
                bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=message_id,
                    text=f"{trailer_info}\n\n💫 *VERSÃO COMPLETA INCLUI:*\n• Conteúdo integral em 4K HDR\n• Download direto via Google Drive/Mega\n• Áudio original + legendas PT/EN\n• Qualidade cinema garantida\n• Entrega em 15-30 minutos\n\n💎 *PREÇO: 1 CRÉDITO*",
                    parse_mode='Markdown',
                    reply_markup=markup
                )
            else:
                bot.answer_callback_query(call.id, "❌ Trailer não encontrado")
        
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
                    text=f"❌ *CRÉDITOS INSUFICIENTES*\n\n💎 *Seus créditos:* *{creditos}*\n🎬 *Filme:* *{filme_key}*\n\n⚡ *Você precisa de 1 crédito.*\n💫 *Compre créditos ou assine VIP!*",
                    parse_mode='Markdown',
                    reply_markup=markup
                )
            else:
                # Simular comando /pedir
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
        
        # 💰 COMPRAR CRÉDITOS
        elif call.data == 'comprar_creditos':
            markup = telebot.types.InlineKeyboardMarkup()
            markup.row(
                telebot.types.InlineKeyboardButton("💎 1 Crédito - 20 MZN", callback_data="credito_1"),
                telebot.types.InlineKeyboardButton("💎 3 Créditos - 50 MZN", callback_data="credito_3")
            )
            markup.row(
                telebot.types.InlineKeyboardButton("💎 5 Créditos - 80 MZN", callback_data="credito_5"),
                telebot.types.InlineKeyboardButton("👑 VIP (Melhor Oferta)", callback_data="planos_vip")
            )
            markup.row(telebot.types.InlineKeyboardButton("🔙 Voltar", callback_data="menu_principal"))
            
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text="""
💎 *COMPRAR CRÉDITOS*

🎬 *1 CRÉDITO = 1 FILME/SÉRIE*

⚡ *OPÇÕES DISPONÍVEIS:*
• 💎 *1 Crédito* - 20 MZN
• 💎 *3 Créditos* - 50 MZN (economize 10 MZN)
• 💎 *5 Créditos* - 80 MZN (economize 20 MZN)

👑 *VIP RECOMENDADO:*
• Mais créditos + benefícios exclusivos
• Economia significativa
• Suporte prioritário

💫 *PAGAMENTOS VIA:*
• M-Pesa • e-Mola • PayPal
• Transferência • Dinheiro

📞 *Contato:* @{}
                """.format(ADMIN_USERNAME),
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
            markup.row(telebot.types.InlineKeyboardButton("🔙 Voltar", callback_data="menu_principal"))
            
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text="""
👑 *PLANOS VIP PREMIUM*

💎 *VANTAGENS EXCLUSIVAS:*
• ✅ Créditos mensais
• ✅ Acesso prioritário
• ✅ Suporte VIP 24/7
• ✅ Lançamentos antecipados
• ✅ Catálogo exclusivo

⚡ *ESCOLHA SEU PLANO:*

🎯 *Recomendado:* VIP 3 MESES
💫 *Melhor Custo-Benefício:* VIP 6 MESES

📞 *Contato:* @{}
                """.format(ADMIN_USERNAME),
                parse_mode='Markdown',
                reply_markup=markup
            )
        
        # 👑 ADMIN
        elif call.data == 'menu_admin':
            admin_panel(call.message)
        
        # 📊 CATEGORIAS
        elif call.data.startswith('categoria_'):
            categoria = call.data.replace('categoria_', '')
            conteudos = CATALOGO_PREMIUM.get(categoria, [])
            
            if not conteudos:
                bot.answer_callback_query(call.id, "📂 Catálogo em desenvolvimento!")
                return
            
            texto = f"🎬 *{categoria.upper()} - CATÁLOGO PREMIUM*\n\n"
            for item in conteudos:
                texto += f"• {item['titulo']}\n"
                texto += f"  🎯 {item['qualidade']}\n"
                texto += f"  ⏰ {item['duracao']} • {item['ano']}\n\n"
            
            markup = telebot.types.InlineKeyboardMarkup()
            markup.row(
                telebot.types.InlineKeyboardButton("🎬 Ver Trailers", callback_data="menu_trailers"),
                telebot.types.InlineKeyboardButton("📦 Fazer Pedido", callback_data="comprar_creditos")
            )
            markup.row(telebot.types.InlineKeyboardButton("🔙 Voltar", callback_data="menu_catalogo"))
            
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=texto + "\n💎 *Use /pedir NomeDoFilme para solicitar*",
                parse_mode='Markdown',
                reply_markup=markup
            )
        
        # 💰 CRÉDITOS INDIVIDUAIS
        elif call.data.startswith('credito_'):
            qtd = call.data.replace('credito_', '')
            precos = {'1': '20', '3': '50', '5': '80'}
            preco = precos.get(qtd, '20')
            
            markup = telebot.types.InlineKeyboardMarkup()
            markup.row(
                telebot.types.InlineKeyboardButton("📞 Comprar Agora", url=f"https://t.me/{ADMIN_USERNAME}"),
                telebot.types.InlineKeyboardButton("👑 Ver VIP", callback_data="planos_vip")
            )
            markup.row(telebot.types.InlineKeyboardButton("🔙 Voltar", callback_data="comprar_creditos"))
            
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=f"""
💎 *COMPRAR {qtd} CRÉDITO(S)*

💰 *Valor:* {preco} MZN
🎬 *Equivale a:* {qtd} filme(s)/série(s)

⚡ *PAGAMENTO VIA:*
• M-Pesa: `{CONTATOS['mpesa']}`
• e-Mola: `{CONTATOS['emola']}`
• PayPal: `{CONTATOS['paypal']}`
• Transferência

📞 *PROCEDIMENTO:*
1. Faça o pagamento
2. Envie comprovante para @{ADMIN_USERNAME}
3. Receba créditos em 2-5 minutos

🎯 *GARANTIA:* Processo 100% seguro!
                """,
                parse_mode='Markdown',
                reply_markup=markup
            )
        
        # 👑 PLANOS VIP INDIVIDUAIS
        elif call.data.startswith('vip_'):
            plano_key = call.data.replace('vip_', '')
            plano = PLANOS_VIP.get(plano_key)
            
            if plano:
                beneficios_text = '\n'.join(plano['beneficios'])
                
                markup = telebot.types.InlineKeyboardMarkup()
                markup.row(
                    telebot.types.InlineKeyboardButton("📞 Assinar Agora", url=f"https://t.me/{ADMIN_USERNAME}"),
                    telebot.types.InlineKeyboardButton("💎 Créditos Avulsos", callback_data="comprar_creditos")
                )
                markup.row(telebot.types.InlineKeyboardButton("🔙 Voltar", callback_data="planos_vip"))
                
                bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=message_id,
                    text=f"""
{plano['nome']} - {plano['preco']}

{beneficios_text}

⚡ *PAGAMENTO VIA:*
• M-Pesa: `{CONTATOS['mpesa']}`
• e-Mola: `{CONTATOS['emola']}`
• PayPal: `{CONTATOS['paypal']}`

📞 *PROCEDIMENTO:*
1. Escolha o plano {plano['nome']}
2. Faça o pagamento de {plano['preco']}
3. Envie comprovante para @{ADMIN_USERNAME}
4. Ativação em 5-10 minutos

🎯 *GARANTIA DE SATISFAÇÃO!*
                    """,
                    parse_mode='Markdown',
                    reply_markup=markup
                )
        
        # 📊 ADMIN CALLBACKS
        elif call.data.startswith('admin_'):
            bot.answer_callback_query(call.id, "👑 Painel Admin em desenvolvimento!")
        
        else:
            bot.answer_callback_query(call.id, "⚡ Funcionalidade em desenvolvimento!")
            
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
    print("🎬 Sistema 100% Funcional!")
    print("⚡ Todos os recursos ativos!")
    
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

