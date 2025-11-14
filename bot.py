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

# 🎬 CATÁLOGO COMPLETO EXPANDIDO
CATALOGO_PREMIUM = {
    'filmes_acao': [
        {
            'titulo': '🎬 VENOM 3: A ÚLTIMA BATALHA',
            'capa': 'https://i.imgur.com/venom3-cap.jpg',
            'trailer': 'https://youtu.be/venom3-trailer',
            'qualidade': '4K HDR • Dolby Atmos',
            'genero': 'Ação • Ficção Científica',
            'duracao': '2h 18m',
            'ano': '2025',
            'descricao': 'Eddie Brock e Venom enfrentam seu maior desafio contra um inimigo simbiótico global que ameaça destruir a humanidade.',
            'elenco': 'Tom Hardy, Michelle Williams',
            'diretor': 'Andy Serkis'
        },
        {
            'titulo': '🎬 JOHN WICK 5: LEGADO',
            'capa': 'https://i.imgur.com/johnwick5-cap.jpg',
            'trailer': 'https://youtu.be/johnwick5-trailer',
            'qualidade': '4K HDR • Dolby Vision',
            'genero': 'Ação • Thriller',
            'duracao': '2h 35m',
            'ano': '2025',
            'descricao': 'John Wick retorna para seu confronto mais perigoso contra a Alta Câmara em uma batalha global.',
            'elenco': 'Keanu Reeves, Halle Berry',
            'diretor': 'Chad Stahelski'
        },
        {
            'titulo': '🎬 MISSION: IMPOSSIBLE 9',
            'capa': 'https://i.imgur.com/mission9-cap.jpg',
            'trailer': 'https://youtu.be/mission9-trailer',
            'qualidade': '4K IMAX • Dolby Atmos',
            'genero': 'Ação • Espionagem',
            'duracao': '2h 48m',
            'ano': '2025',
            'descricao': 'Ethan Hunt enfrenta sua missão mais impossível contra uma IA global que ameaça o mundo.',
            'elenco': 'Tom Cruise, Rebecca Ferguson',
            'diretor': 'Christopher McQuarrie'
        }
    ],
    'filmes_aventura': [
        {
            'titulo': '🎬 AVATAR 4: O LEGADO',
            'capa': 'https://i.imgur.com/avatar4-cap.jpg', 
            'trailer': 'https://youtu.be/avatar4-trailer',
            'qualidade': '4K Dolby Vision • IMAX',
            'genero': 'Aventura • Ficção Científica',
            'duracao': '3h 02m',
            'ano': '2025',
            'descricao': 'A saga continua em novos mundos com criaturas extraordinárias e batalhas épicas por Pandora.',
            'elenco': 'Sam Worthington, Zoe Saldana',
            'diretor': 'James Cameron'
        },
        {
            'titulo': '🎬 INDIANA JONES 6',
            'capa': 'https://i.imgur.com/indiana6-cap.jpg',
            'trailer': 'https://youtu.be/indiana6-trailer',
            'qualidade': '4K HDR • Atmos',
            'genero': 'Aventura • Ação',
            'duracao': '2h 25m',
            'ano': '2025',
            'descricao': 'A última aventura do arqueólogo mais famoso em busca de um artefato ancestral perdido.',
            'elenco': 'Harrison Ford, Phoebe Waller-Bridge',
            'diretor': 'James Mangold'
        }
    ],
    'filmes_animacao': [
        {
            'titulo': '🎬 SPIDER-MAN: BEYOND THE SPIDER-VERSE',
            'capa': 'https://i.imgur.com/spiderman-cap.jpg',
            'trailer': 'https://youtu.be/spiderman-trailer',
            'qualidade': '4K HDR • Animação',
            'genero': 'Ação • Animação • Super-herói',
            'duracao': '2h 28m',
            'ano': '2025',
            'descricao': 'Miles Morales enfrenta o multiverso em uma aventura visualmente deslumbrante.',
            'elenco': 'Shameik Moore, Hailee Steinfeld',
            'diretor': 'Joaquim Dos Santos'
        },
        {
            'titulo': '🎬 FROZEN 3: O REINO DE GELO',
            'capa': 'https://i.imgur.com/frozen3-cap.jpg',
            'trailer': 'https://youtu.be/frozen3-trailer',
            'qualidade': '4K HDR • Animação',
            'genero': 'Animação • Aventura • Musical',
            'duracao': '1h 55m',
            'ano': '2025',
            'descricao': 'Elsa e Anna descobrem um reino ancestral de gelo com segredos familiares.',
            'elenco': 'Idina Menzel, Kristen Bell',
            'diretor': 'Chris Buck'
        }
    ],
    'series_drama': [
        {
            'titulo': '📺 STRANGER THINGS 5 - TEMPORADA COMPLETA',
            'capa': 'https://i.imgur.com/stranger5-cap.jpg',
            'trailer': 'https://youtu.be/stranger5-trailer',
            'qualidade': '4K Dolby Vision • 8 Episódios',
            'genero': 'Suspense • Ficção Científica • Drama',
            'duracao': 'Temporada Completa',
            'ano': '2025',
            'descricao': 'A temporada final que encerra a saga de Hawkins e o Mundo Invertido.',
            'elenco': 'Millie Bobby Brown, Finn Wolfhard',
            'diretor': 'Duffer Brothers'
        },
        {
            'titulo': '📺 THE LAST OF US 3 - TODOS OS EPISÓDIOS',
            'capa': 'https://i.imgur.com/lastofus3-cap.jpg',
            'trailer': 'https://youtu.be/lastofus3-trailer',
            'qualidade': '4K HDR • 10 Episódios',
            'genero': 'Drama • Ação • Pós-apocalíptico',
            'duracao': 'Temporada Completa',
            'ano': '2025',
            'descricao': 'Continua a jornada emocionante em um mundo devastado por infecção.',
            'elenco': 'Pedro Pascal, Bella Ramsey',
            'diretor': 'Craig Mazin'
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
            'descricao': 'O confronto final entre Tanjiro e Muzan Kibutsuji.',
            'elenco': 'Natsuki Hanae, Akari Kito',
            'diretor': 'Haruo Sotozaki'
        },
        {
            'titulo': '🎌 ATTACK ON TITAN: FINAL CHAPTERS',
            'capa': 'https://i.imgur.com/aot-final.jpg',
            'trailer': 'https://youtu.be/aot-final-trailer',
            'qualidade': '4K HDR • Legendado PT-BR',
            'genero': 'Anime • Ação • Drama',
            'duracao': 'Capítulos Finais',
            'ano': '2025',
            'descricao': 'O épico final da batalha pela humanidade.',
            'elenco': 'Yuki Kaji, Yui Ishikawa',
            'diretor': 'Yuichiro Hayashi'
        }
    ],
    'lancamentos': [
        {
            'titulo': '🎬 DEADPOOL 4: WOLVERINE RETURNS',
            'capa': 'https://i.imgur.com/deadpool4-cap.jpg',
            'trailer': 'https://youtu.be/deadpool4-trailer',
            'qualidade': '4K HDR • Ação',
            'genero': 'Ação • Comédia • Super-herói',
            'duracao': '2h 15m',
            'ano': '2025',
            'descricao': 'Deadpool e Wolverine se unem em uma aventura multiversal cheia de humor.',
            'elenco': 'Ryan Reynolds, Hugh Jackman',
            'diretor': 'Shawn Levy'
        },
        {
            'titulo': '🎬 BLACK PANTHER 3: WAKANDA FOREVER 2',
            'capa': 'https://i.imgur.com/blackpanther3-cap.jpg',
            'trailer': 'https://youtu.be/blackpanther3-trailer',
            'qualidade': '4K IMAX • Dolby Vision',
            'genero': 'Ação • Ficção Científica',
            'duracao': '2h 45m',
            'ano': '2025',
            'descricao': 'O novo protetor de Wakanda enfrenta ameaças globais e conflitos internos.',
            'elenco': 'Letitia Wright, Danai Gurira',
            'diretor': 'Ryan Coogler'
        }
    ]
}

# 🎭 TRAILERS DISPONÍVEIS EXPANDIDOS
TRAILERS_DISPONIVEIS = {
    'VENOM 3': '🎬 *Trailer Venom 3*\nhttps://youtu.be/venom3-trailer\n⚡ 2:30 min • Cenas de ação em 4K',
    'JOHN WICK 5': '🎬 *Trailer John Wick 5*\nhttps://youtu.be/johnwick5-trailer\n🔫 3:15 min • Ação intensa',
    'MISSION IMPOSSIBLE 9': '🎬 *Trailer Mission Impossible 9*\nhttps://youtu.be/mission9-trailer\n🏃‍♂️ 2:45 min • Cenas de risco real',
    'AVATAR 4': '🎬 *Trailer Avatar 4*\nhttps://youtu.be/avatar4-trailer\n🌍 3:15 min • Novos mundos revelados', 
    'SPIDER-MAN BEYOND': '🎬 *Trailer Spider-Man Beyond*\nhttps://youtu.be/spiderman-trailer\n🕷️ 2:45 min • Multiverso expandido',
    'FROZEN 3': '🎬 *Trailer Frozen 3*\nhttps://youtu.be/frozen3-trailer\n❄️ 2:20 min • Nova aventura gelada',
    'STRANGER THINGS 5': '📺 *Trailer Stranger Things 5*\nhttps://youtu.be/stranger5-trailer\n🔮 3:30 min • Temporada final épica',
    'THE LAST OF US 3': '📺 *Trailer The Last of Us 3*\nhttps://youtu.be/lastofus3-trailer\n🧟 3:10 min • Drama intenso',
    'DEMON SLAYER FINAL': '🎌 *Trailer Demon Slayer Final*\nhttps://youtu.be/demonslayer-trailer\n⚔️ 2:15 min • Batalhas emocionantes',
    'ATTACK ON TITAN FINAL': '🎌 *Trailer Attack on Titan Final*\nhttps://youtu.be/aot-final-trailer\n👹 3:05 min • Conclusão épica',
    'DEADPOOL 4': '🎬 *Trailer Deadpool 4*\nhttps://youtu.be/deadpool4-trailer\n💀 2:50 min • Humor e ação',
    'BLACK PANTHER 3': '🎬 *Trailer Black Panther 3*\nhttps://youtu.be/blackpanther3-trailer\n🐾 3:20 min • Aventura em Wakanda'
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

📋 *COMANDOS DISPONÍVEIS:*
`/start` - Menu principal
`/comandos` - Lista completa de comandos  
`/catalogo` - Ver catálogo completo
`/trailer` - Ver trailers
`/pedir` - Fazer pedido de filme/série
`/recomendacao` - Recomendação do dia

📞 *Dúvidas?* @{ADMIN_USERNAME}
            """, parse_mode='Markdown')
        except:
            pass
        return True
    
    conn.close()
    return False

# 📋 COMANDO LISTA DE COMANDOS
@bot.message_handler(commands=['comandos', 'ajuda', 'help'])
def comandos_lista(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row(
        telebot.types.InlineKeyboardButton("🎬 Catálogo", callback_data="menu_catalogo"),
        telebot.types.InlineKeyboardButton("🎥 Trailers", callback_data="menu_trailers")
    )
    markup.row(
        telebot.types.InlineKeyboardButton("💰 Créditos", callback_data="comprar_creditos"),
        telebot.types.InlineKeyboardButton("👑 VIP", callback_data="planos_vip")
    )
    
    bot.reply_to(message, f"""
📋 *LISTA DE COMANDOS - CINEMA PRO* 📋

🎬 *COMANDOS PRINCIPAIS:*
`/start` - Menu inicial e status
`/comandos` - Esta lista de comandos
`/catalogo` - Catálogo completo de filmes/séries
`/trailer` - Ver trailers disponíveis
`/pedir [nome]` - Fazer pedido de filme/série
`/recomendacao` - Recomendação do dia

💰 *SISTEMA DE CRÉDITOS:*
`/creditos` - Ver seus créditos
`/comprar` - Comprar mais créditos
`/vip` - Ver planos VIP

📞 *SUPORTE:*
`/suporte` - Falar com atendimento
`/info` - Informações do sistema

🎯 *EXEMPLOS DE USO:*
• `/pedir Venom 3` - Pedir filme específico
• `/trailer Avatar 4` - Ver trailer
• `/catalogo` - Navegar catálogo

💡 *DICAS:*
• 1 crédito = 1 filme/série
• Qualidade 4K garantida
• Entrega em 15-30 minutos

📞 *ATENDIMENTO:* @{ADMIN_USERNAME}
    """, parse_mode='Markdown', reply_markup=markup)

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

📋 *COMANDOS NO GRUPO:*
`/recomendacao` - Filme do dia
`/lancamentos` - Novidades da semana  
`/catalogo` - Catálogo completo
`/trailer` - Ver trailers

💡 *Use /start no privado para acessar todo o catálogo!*

📞 *ATENDIMENTO:* @{ADMIN_USERNAME}
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

# 🎥 SISTEMA DE TRAILERS EXPANDIDO
@bot.message_handler(commands=['trailer'])
def trailer_cmd(message):
    args = message.text.split()[1:]
    
    if not args:
        markup = telebot.types.InlineKeyboardMarkup()
        
        # Agrupar trailers em categorias
        filmes_trailers = ['VENOM 3', 'JOHN WICK 5', 'AVATAR 4', 'SPIDER-MAN BEYOND']
        series_trailers = ['STRANGER THINGS 5', 'THE LAST OF US 3']
        animes_trailers = ['DEMON SLAYER FINAL', 'ATTACK ON TITAN FINAL']
        
        # Filmes
        for i in range(0, len(filmes_trailers), 2):
            row = []
            for j in range(2):
                if i + j < len(filmes_trailers):
                    filme = filmes_trailers[i + j]
                    callback_data = f"trailer_{filme.split()[0].upper()}"
                    row.append(telebot.types.InlineKeyboardButton(
                        f"🎬 {filme.split()[0]}", 
                        callback_data=callback_data
                    ))
            if row:
                markup.add(*row)
        
        # Séries
        for i in range(0, len(series_trailers), 2):
            row = []
            for j in range(2):
                if i + j < len(series_trailers):
                    serie = series_trailers[i + j]
                    callback_data = f"trailer_{serie.split()[0].upper()}"
                    row.append(telebot.types.InlineKeyboardButton(
                        f"📺 {serie.split()[0]}", 
                        callback_data=callback_data
                    ))
            if row:
                markup.add(*row)
        
        # Animes
        for i in range(0, len(animes_trailers), 2):
            row = []
            for j in range(2):
                if i + j < len(animes_trailers):
                    anime = animes_trailers[i + j]
                    callback_data = f"trailer_{anime.split()[0].upper()}"
                    row.append(telebot.types.InlineKeyboardButton(
                        f"🎌 {anime.split()[0]}", 
                        callback_data=callback_data
                    ))
            if row:
                markup.add(*row)
        
        markup.row(telebot.types.InlineKeyboardButton("🔙 Menu Principal", callback_data="menu_principal"))
        
        bot.reply_to(message, """
🎬 *TRAILERS EXCLUSIVOS* 🎬

⚠️ *ASSISTA ANTES DE PEDIR!*

Escolha uma categoria e veja os trailers disponíveis:

🎯 *VANTAGENS:*
• Veja a qualidade do conteúdo
• Conheça a história antes de comprar
• Cenas exclusivas em alta definição

💡 *APÓS O TRAILER:*
• Pedido completo por 1 crédito
• Filme/série completo em 4K
• Entrega rápida

*🚀 EXPERIÊNCIA COMPLETA!*
        """, parse_mode='Markdown', reply_markup=markup)
        return
    
    # Se tem argumentos, busca trailer específico
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

# 🎨 CATÁLOGO PROFISSIONAL EXPANDIDO
@bot.message_handler(commands=['catalogo', 'lancamentos'])
def catalogo_premium(message):
    markup = telebot.types.InlineKeyboardMarkup()
    
    markup.row(
        telebot.types.InlineKeyboardButton("🎬 AÇÃO", callback_data="categoria_filmes_acao"),
        telebot.types.InlineKeyboardButton("🌍 AVENTURA", callback_data="categoria_filmes_aventura")
    )
    markup.row(
        telebot.types.InlineKeyboardButton("📺 SÉRIES", callback_data="categoria_series_drama"),
        telebot.types.InlineKeyboardButton("🎌 ANIMES", callback_data="categoria_animes")
    )
    markup.row(
        telebot.types.InlineKeyboardButton("🚀 LANÇAMENTOS", callback_data="categoria_lancamentos"),
        telebot.types.InlineKeyboardButton("🎥 ANIMAÇÃO", callback_data="categoria_filmes_animacao")
    )
    markup.row(
        telebot.types.InlineKeyboardButton("🎥 TRAILERS", callback_data="menu_trailers"),
        telebot.types.InlineKeyboardButton("📞 ATENDIMENTO", url=f"https://t.me/{ADMIN_USERNAME}")
    )
    markup.row(telebot.types.InlineKeyboardButton("📋 COMANDOS", callback_data="menu_comandos"))
    
    bot.reply_to(message, f"""
🎬 *CATÁLOGO PREMIUM 2025* 🎬

💫 *EXPERIÊNCIA CINEMATOGRÁFICA COMPLETA*

⚡ *CATEGORIAS EXCLUSIVAS:*

🎬 *FILMES DE AÇÃO*
• Venom 3, John Wick 5, Mission Impossible 9
• Qualidade 4K HDR • Áudio Dolby Atmos

🌍 *FILMES DE AVENTURA*  
• Avatar 4, Indiana Jones 6
• Mundos fantásticos • Aventuras épicas

📺 *SÉRIES DRAMA*
• Stranger Things 5, The Last of Us 3
• Temporadas completas • Qualidade streaming

🎌 *ANIMES LEGENDADOS*
• Demon Slayer, Attack on Titan
• Japonês original • Legendas profissionais

🚀 *LANÇAMENTOS 2025*
• Deadpool 4, Black Panther 3
• Primeira exibição • Conteúdo inédito

🎥 *ANIMAÇÕES*
• Spider-Man Beyond, Frozen 3
• Animação de qualidade • Para toda família

💎 *SISTEMA PROFISSIONAL:*
• Entrega automática em 15-30 minutos
• Suporte 24/7 via @{ADMIN_USERNAME}
• Qualidade 4K verificada

📞 *ATENDIMENTO PERSONALIZADO!*
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
`/pedir Demon Slayer`

💡 *Dica:* Use `/catalogo` para ver o catálogo completo!
`/comandos` para ver todos os comandos
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

# 👑 PAINEL ADMIN COMPLETO (mantenha igual ao anterior)
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
    pedidos_24h = c.execute("SELECT COUNT(*) FROM pedidos WHERE datetime(data) > datetime('now', '-1 day')").fetchone()[0]
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

# 🎯 COMANDO START PREMIUM ATUALIZADO
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
        telebot.types.InlineKeyboardButton("📋 Lista de Comandos", callback_data="menu_comandos"),
        telebot.types.InlineKeyboardButton("📞 Atendimento", url=f"https://t.me/{ADMIN_USERNAME}")
    ]
    
    if is_admin(user_id, username):
        botoes.append(telebot.types.InlineKeyboardButton("👑 Painel Admin", callback_data="menu_admin"))
    
    markup.row(botoes[0], botoes[1])
    markup.row(botoes[2], botoes[3])
    markup.row(botoes[4], botoes[5])
    if len(botoes) > 6:
        markup.row(botoes[6])
    
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

📋 *Use /comandos para ver todos os comandos*

🎯 *ESCOLHA UMA OPÇÃO:*
    """, parse_mode='Markdown', reply_markup=markup)

# 📨 SISTEMA DE CALLBACKS COMPLETO ATUALIZADO
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
                markup.row(telebot.types.InlineKeyboardButton("🔙 Voltar Trailers", callback_data="menu_trailers"))
                
                bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=message_id,
                    text=f"{trailer_info}\n\n💫 *VERSÃO COMPLETA INCLUI:*\n• Conteúdo integral em 4K HDR\n• Download direto\n• Áudio original + legendas\n• Entrega em 15-30 minutos\n\n💎 *PREÇO: 1 CRÉDITO*",
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
        
        # 📋 COMANDOS
        elif call.data == 'menu_comandos':
            comandos_lista(call.message)
        
        # 👑 ADMIN
        elif call.data == 'menu_admin':
            admin_panel(call.message)
        
        # 📊 CATEGORIAS DETALHADAS
        elif call.data.startswith('categoria_'):
            categoria = call.data.replace('categoria_', '')
            conteudos = CATALOGO_PREMIUM.get(categoria, [])
            
            if not conteudos:
                bot.answer_callback_query(call.id, "📂 Catálogo em desenvolvimento!")
                return
            
            texto = f"🎬 *{categoria.upper().replace('_', ' ')} - CATÁLOGO PREMIUM*\n\n"
            for i, item in enumerate(conteudos, 1):
                texto += f"*{i}. {item['titulo']}*\n"
                texto += f"   🎯 {item['qualidade']}\n"
                texto += f"   ⏰ {item['duracao']} • {item['ano']}\n"
                texto += f"   🎭 {item['genero']}\n"
                texto += f"   📖 {item['descricao'][:100]}...\n\n"
            
            markup = telebot.types.InlineKeyboardMarkup()
            markup.row(
                telebot.types.InlineKeyboardButton("🎬 Ver Trailers", callback_data="menu_trailers"),
                telebot.types.InlineKeyboardButton("💎 Comprar Créditos", callback_data="comprar_creditos")
            )
            markup.row(telebot.types.InlineKeyboardButton("🔙 Voltar Catálogo", callback_data="menu_catalogo"))
            
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=texto + "💎 *Use /pedir NomeDoFilme para solicitar*",
                parse_mode='Markdown',
                reply_markup=markup
            )
        
        # 💰 COMPRAR CRÉDITOS - CORRIGIDO
        elif call.data == 'comprar_creditos':
            markup = telebot.types.InlineKeyboardMarkup()
            markup.row(
                telebot.types.InlineKeyboardButton("💎 1 Crédito - 20 MZN", url=f"https://t.me/{ADMIN_USERNAME}?text=Quero+comprar+1+crédito"),
                telebot.types.InlineKeyboardButton("💎 3 Créditos - 50 MZN", url=f"https://t.me/{ADMIN_USERNAME}?text=Quero+comprar+3+créditos")
            )
            markup.row(
                telebot.types.InlineKeyboardButton("💎 5 Créditos - 80 MZN", url=f"https://t.me/{ADMIN_USERNAME}?text=Quero+comprar+5+créditos"),
                telebot.types.InlineKeyboardButton("👑 Ver Planos VIP", callback_data="planos_vip")
            )
            markup.row(telebot.types.InlineKeyboardButton("🔙 Voltar", callback_data="menu_principal"))
            
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=f"""
💎 *COMPRAR CRÉDITOS* 💎

🎬 *1 CRÉDITO = 1 FILME/SÉRIE*

⚡ *OPÇÕES DISPONÍVEIS:*
• 💎 *1 Crédito* - 20 MZN
• 💎 *3 Créditos* - 50 MZN (economize 10 MZN)
• 💎 *5 Créditos* - 80 MZN (economize 20 MZN)

💰 *FORMAS DE PAGAMENTO:*
• M-Pesa: `{CONTATOS['mpesa']}`
• e-Mola: `{CONTATOS['emola']}`
• PayPal: `{CONTATOS['paypal']}`

📞 *PROCEDIMENTO:*
1. Escolha quantos créditos quer
2. Clique no botão para falar comigo
3. Faça o pagamento
4. Envie comprovante
5. Receba créditos em 2-5 minutos

🎯 *GARANTIA DE ENTREGA RÁPIDA!*
                """,
                parse_mode='Markdown',
                reply_markup=markup
            )
            bot.answer_callback_query(call.id, "💎 Escolha quantos créditos deseja!")
        
        # 👑 PLANOS VIP - CORRIGIDO
        elif call.data == 'planos_vip':
            markup = telebot.types.InlineKeyboardMarkup()
            
            for plano_key, plano in PLANOS_VIP.items():
                markup.row(telebot.types.InlineKeyboardButton(
                    f"{plano['nome']} - {plano['preco']}", 
                    url=f"https://t.me/{ADMIN_USERNAME}?text=Quero+assinar+{plano['nome'].replace(' ', '+')}"
                ))
            
            markup.row(telebot.types.InlineKeyboardButton("💎 Créditos Avulsos", callback_data="comprar_creditos"))
            markup.row(telebot.types.InlineKeyboardButton("🔙 Voltar", callback_data="menu_principal"))
            
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=f"""
👑 *PLANOS VIP PREMIUM* 👑

💎 *VANTAGENS EXCLUSIVAS:*
• ✅ Créditos mensais
• ✅ Acesso prioritário  
• ✅ Suporte VIP 24/7
• ✅ Lançamentos antecipados
• ✅ Catálogo exclusivo

⚡ *ESCOLHA SEU PLANO:*

💎 *VIP 1 MÊS* - 50 MZN
• 10 créditos mensais
• Todos benefícios VIP

🔥 *VIP 3 MESES* - 120 MZN  
• 35 créditos (5 bônus)
• Economia de 30 MZN

👑 *VIP 6 MESES* - 200 MZN
• 80 créditos (20 bônus)
• Melhor custo-benefício

💰 *FORMAS DE PAGAMENTO:*
• M-Pesa: `{CONTATOS['mpesa']}`
• e-Mola: `{CONTATOS['emola']}`
• PayPal: `{CONTATOS['paypal']}`

📞 *Clique no plano desejado para falar comigo!*
                """,
                parse_mode='Markdown',
                reply_markup=markup
            )
            bot.answer_callback_query(call.id, "👑 Escolha seu plano VIP!")
        
        # ADMIN CALLBACKS (mantenha iguais)
        elif call.data == 'admin_stats':
            from_user = type('User', (), {'id': user_id, 'username': call.from_user.username})()
            msg = type('Msg', (), {
                'chat': type('Chat', (), {'id': chat_id}), 
                'from_user': from_user
            })()
            stats_cmd(msg)
        
        elif call.data in ['admin_add_creditos', 'admin_vip']:
            bot.answer_callback_query(call.id, "👑 Use os comandos no chat!")
        
        elif call.data == 'admin_refresh':
            admin_panel(call.message)
        
        elif call.data == 'admin_close':
            bot.delete_message(chat_id, message_id)
        
        else:
            bot.answer_callback_query(call.id, "⚡ Redirecionando...")
            
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
    print("🎬 Catálogo Expandido com 12+ Filmes/Séries!")
    print("📋 Sistema de Comandos Completo!")
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
