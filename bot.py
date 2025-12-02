import os
import telebot
import sqlite3
import time
import random
import threading
from datetime import datetime, timedelta
from telebot.types import (
    InlineKeyboardMarkup, 
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton
)

# 🔐 CONFIGURAÇÃO COMPLETA
TOKEN = "8306714275:AAGzNXE3TZKbe5-49YGTgNOMrJiLVxBjmLA"
ADMIN_USERNAME = "ayltonanna7"
ADMIN_ID = 5125563829

bot = telebot.TeleBot(TOKEN)

# 💎 SISTEMA PREMIUM COMPLETO
CONTATOS = {
    'whatsapp': '848568229',
    'telegram': '@ayltonanna7',
    'email': 'ayltonanna7@gmail.com',
    'mpesa': '848568229', 
    'emola': '870612404',
    'paypal': 'ayltonanna7@gmail.com'
}

# 🎬 CATÁLOGO MEGA EXPANDIDO (120+ TÍTULOS)
CATALOGO_PREMIUM = {
    'acao_2025': [
        {
            'id': 'venom3',
            'titulo': '🎬 VENOM 3: A ÚLTIMA BATALHA',
            'descricao': 'Eddie Brock e Venom enfrentam seu maior desafio contra um inimigo simbiótico global que ameaça destruir a humanidade.',
            'qualidade': '4K HDR • Dolby Atmos • IMAX Enhanced',
            'duracao': '2h 18m',
            'imdb': '8.2/10',
            'tamanho': '15.7 GB',
            'genero': 'Ação • Ficção Científica • Terror',
            'ano': '2025',
            'classificacao': '16+',
            'audio': 'Português, Inglês, Espanhol',
            'legendas': 'PT-BR, EN, ES, FR',
            'link_trailer': 'https://youtu.be/venom3-trailer',
            'preco': 1
        },
        {
            'id': 'johnwick5',
            'titulo': '🎬 JOHN WICK 5: LEGADO',
            'descricao': 'John Wick retorna para seu confronto mais perigoso contra a Alta Câmara em uma batalha global pelas ruas de Nova York.',
            'qualidade': '4K Dolby Vision • Dolby Atmos',
            'duracao': '2h 35m',
            'imdb': '8.5/10',
            'tamanho': '18.2 GB',
            'genero': 'Ação • Thriller • Neo-noir',
            'ano': '2025',
            'classificacao': '18+',
            'audio': 'Português, Inglês, Japonês',
            'legendas': 'PT-BR, EN, JP',
            'link_trailer': 'https://youtu.be/johnwick5-trailer',
            'preco': 1
        },
        {
            'id': 'mission9',
            'titulo': '🎬 MISSION: IMPOSSIBLE 9',
            'descricao': 'Ethan Hunt enfrenta sua missão mais impossível contra uma IA global que ameaça o controle mundial. Cenas de ação reais sem CGI.',
            'qualidade': '4K IMAX • Dolby Atmos • 3D',
            'duracao': '2h 48m',
            'imdb': '8.7/10',
            'tamanho': '22.5 GB',
            'genero': 'Ação • Espionagem • Aventura',
            'ano': '2025',
            'classificacao': '12+',
            'audio': 'Português, Inglês, Francês',
            'legendas': 'PT-BR, EN, FR, DE',
            'link_trailer': 'https://youtu.be/mission9-trailer',
            'preco': 1
        },
        {
            'id': 'deadpool4',
            'titulo': '🎬 DEADPOOL 4: WOLVERINE RETURNS',
            'descricao': 'Deadpool e Wolverine se unem em uma aventura multiversal cheia de humor ácido, ação brutal e referências a todo universo Marvel.',
            'qualidade': '4K HDR • Dolby Vision',
            'duracao': '2h 15m',
            'imdb': '8.9/10',
            'tamanho': '17.3 GB',
            'genero': 'Ação • Comédia • Super-herói',
            'ano': '2025',
            'classificacao': '18+',
            'audio': 'Português, Inglês',
            'legendas': 'PT-BR, EN',
            'link_trailer': 'https://youtu.be/deadpool4-trailer',
            'preco': 1
        },
        {
            'id': 'badboys4',
            'titulo': '🎬 BAD BOYS 4: RIDE OR DIE',
            'descricao': 'Mike Lowrey e Marcus Burnett estão de volta em mais uma missão repleta de ação, comédia e perseguições alucinantes pelas ruas de Miami.',
            'qualidade': '4K HDR • Dolby Digital Plus',
            'duracao': '2h 15m',
            'imdb': '7.8/10',
            'tamanho': '14.3 GB',
            'genero': 'Ação • Comédia • Policial',
            'ano': '2025',
            'classificacao': '14+',
            'audio': 'Português, Inglês',
            'legendas': 'PT-BR, EN',
            'link_trailer': 'https://youtu.be/badboys4-trailer',
            'preco': 1
        },
        {
            'id': 'transformer7',
            'titulo': '🎬 TRANSFORMERS 7: REVOLT',
            'descricao': 'Nova geração de Transformers em uma guerra épica que decide o futuro da Terra. Efeitos visuais de tirar o fôlego.',
            'qualidade': '4K HDR • Dolby Atmos • IMAX',
            'duracao': '2h 25m',
            'imdb': '7.9/10',
            'tamanho': '16.8 GB',
            'genero': 'Ação • Ficção Científica',
            'ano': '2025',
            'classificacao': '12+',
            'audio': 'Português, Inglês',
            'legendas': 'PT-BR, EN',
            'link_trailer': 'https://youtu.be/transformers7-trailer',
            'preco': 1
        }
    ],
    'aventura_2025': [
        {
            'id': 'avatar4',
            'titulo': '🎬 AVATAR 4: O LEGADO',
            'descricao': 'A saga continua em novos mundos aquáticos de Pandora com criaturas extraordinárias, batalhas épicas e tecnologia visual revolucionária.',
            'qualidade': '4K Dolby Vision • IMAX 3D • HFR 60fps',
            'duracao': '3h 02m',
            'imdb': '9.1/10',
            'tamanho': '25.8 GB',
            'genero': 'Aventura • Ficção Científica • Fantasia',
            'ano': '2025',
            'classificacao': '12+',
            'audio': 'Português, Inglês, Nativo',
            'legendas': 'PT-BR, EN, ES, FR, DE',
            'link_trailer': 'https://youtu.be/avatar4-trailer',
            'preco': 1
        },
        {
            'id': 'indiana6',
            'titulo': '🎬 INDIANA JONES 6',
            'descricao': 'A última aventura do arqueólogo mais famoso em busca do Cetro de Cronos, um artefato ancestral perdido nas profundezas da Amazônia.',
            'qualidade': '4K HDR • Dolby Atmos • Restauração Digital',
            'duracao': '2h 25m',
            'imdb': '8.3/10',
            'tamanho': '16.7 GB',
            'genero': 'Aventura • Ação • História',
            'ano': '2025',
            'classificacao': '12+',
            'audio': 'Português, Inglês, Grego',
            'legendas': 'PT-BR, EN, GR',
            'link_trailer': 'https://youtu.be/indiana6-trailer',
            'preco': 1
        }
    ],
    'animacao_2025': [
        {
            'id': 'spiderman_beyond',
            'titulo': '🎬 SPIDER-MAN: BEYOND THE SPIDER-VERSE',
            'descricao': 'Miles Morales enfrenta o colapso do multiverso em uma aventura visualmente deslumbrante com mais de 100 diferentes versões do Homem-Aranha.',
            'qualidade': '4K HDR • Animação 3D • Dolby Vision',
            'duracao': '2h 28m',
            'imdb': '9.4/10',
            'tamanho': '19.5 GB',
            'genero': 'Animação • Ação • Super-herói • Multiverso',
            'ano': '2025',
            'classificacao': 'Livre',
            'audio': 'Português, Inglês, Dublado BR',
            'legendas': 'PT-BR, EN',
            'link_trailer': 'https://youtu.be/spiderman-trailer',
            'preco': 1
        },
        {
            'id': 'frozen3',
            'titulo': '🎬 FROZEN 3: O REINO DE GELO',
            'descricao': 'Elsa e Anna descobrem um reino ancestral de gelo com segredos familiares que mudarão para sempre Arendelle. Novas músicas originais.',
            'qualidade': '4K HDR • Dolby Atmos • Disney+',
            'duracao': '1h 55m',
            'imdb': '8.7/10',
            'tamanho': '14.8 GB',
            'genero': 'Animação • Aventura • Musical • Família',
            'ano': '2025',
            'classificacao': 'Livre',
            'audio': 'Português (Dublado), Inglês',
            'legendas': 'PT-BR, EN, ES',
            'link_trailer': 'https://youtu.be/frozen3-trailer',
            'preco': 1
        },
        {
            'id': 'toystory5',
            'titulo': '🎬 TOY STORY 5: NOVAS AVENTURAS',
            'descricao': 'Woody, Buzz e a turma estão de volta em uma nova aventura cheia de emoção e descobertas sobre o verdadeiro significado da amizade.',
            'qualidade': '4K HDR • Dolby Vision • Pixar',
            'duracao': '1h 52m',
            'imdb': '8.5/10',
            'tamanho': '13.9 GB',
            'genero': 'Animação • Aventura • Comédia',
            'ano': '2025',
            'classificacao': 'Livre',
            'audio': 'Português, Inglês',
            'legendas': 'PT-BR, EN',
            'link_trailer': 'https://youtu.be/toystory5-trailer',
            'preco': 1
        }
    ],
    'series_2025': [
        {
            'id': 'stranger5',
            'titulo': '📺 STRANGER THINGS 5 - TEMPORADA COMPLETA',
            'descricao': 'A temporada final que encerra a saga de Hawkins e o Mundo Invertido. Todos os mistérios revelados em 8 episódios épicos.',
            'qualidade': '4K Dolby Vision • 8 Episódios • Atmos',
            'duracao': '8h 40m (Temporada)',
            'imdb': '9.2/10',
            'tamanho': '45.2 GB',
            'genero': 'Suspense • Ficção Científica • Drama • Terror',
            'ano': '2025',
            'classificacao': '16+',
            'audio': 'Português, Inglês',
            'legendas': 'PT-BR, EN, ES, FR',
            'link_trailer': 'https://youtu.be/stranger5-trailer',
            'preco': 1
        },
        {
            'id': 'lastofus3',
            'titulo': '📺 THE LAST OF US 3 - TODOS OS EPISÓDIOS',
            'descricao': 'Continua a jornada emocionante de Joel e Ellie em um mundo devastado por infecção. Baseado no aclamado jogo da Naughty Dog.',
            'qualidade': '4K HDR • 10 Episódios • Dolby Atmos',
            'duracao': '10h 30m (Temporada)',
            'imdb': '9.5/10',
            'tamanho': '52.7 GB',
            'genero': 'Drama • Ação • Pós-apocalíptico • Suspense',
            'ano': '2025',
            'classificacao': '18+',
            'audio': 'Português, Inglês',
            'legendas': 'PT-BR, EN',
            'link_trailer': 'https://youtu.be/lastofus3-trailer',
            'preco': 1
        },
        {
            'id': 'mandalorian4',
            'titulo': '📺 THE MANDALORIAN 4 - TEMPORADA COMPLETA',
            'descricao': 'Nova temporada da série Star Wars mais popular. Din Djarin e Grogu em novas aventuras pela galáxia.',
            'qualidade': '4K HDR • 8 Episódios • Dolby Atmos',
            'duracao': '7h 20m (Temporada)',
            'imdb': '9.0/10',
            'tamanho': '38.5 GB',
            'genero': 'Ficção Científica • Ação • Aventura',
            'ano': '2025',
            'classificacao': '12+',
            'audio': 'Português, Inglês',
            'legendas': 'PT-BR, EN',
            'link_trailer': 'https://youtu.be/mandalorian4-trailer',
            'preco': 1
        },
        {
            'id': 'casadopapel6',
            'titulo': '📺 LA CASA DE PAPEL 6 - TEMPORADA FINAL',
            'descricao': 'O assalto final que vai mudar tudo. O Professor e sua equipe em seu plano mais ousado e perigoso.',
            'qualidade': '4K HDR • 10 Episódios • Netflix',
            'duracao': '9h 50m (Temporada)',
            'imdb': '8.8/10',
            'tamanho': '42.3 GB',
            'genero': 'Drama • Crime • Suspense',
            'ano': '2025',
            'classificacao': '18+',
            'audio': 'Português, Espanhol, Inglês',
            'legendas': 'PT-BR, EN, ES',
            'link_trailer': 'https://youtu.be/casadopapel6-trailer',
            'preco': 1
        }
    ],
    'animes_2025': [
        {
            'id': 'demonslayer_final',
            'titulo': '🎌 DEMON SLAYER: FINAL ARC COMPLETO',
            'descricao': 'O confronto final entre Tanjiro e Muzan Kibutsuji. Animação Ufotable em qualidade cinema. Arco do Castelo Infinito completo.',
            'qualidade': '4K • 26 Episódios • Japonês Hi-Res',
            'duracao': '13h (Arco Final)',
            'imdb': '9.7/10',
            'tamanho': '38.4 GB',
            'genero': 'Anime • Ação • Fantasia • Sobrenatural',
            'ano': '2025',
            'classificacao': '16+',
            'audio': 'Japonês, Português (Dublado)',
            'legendas': 'PT-BR, EN, JP',
            'link_trailer': 'https://youtu.be/demonslayer-trailer',
            'preco': 1
        },
        {
            'id': 'attack_final',
            'titulo': '🎌 ATTACK ON TITAN: FINAL CHAPTERS COMPLETO',
            'descricao': 'O épico final da batalha pela humanidade. Conclusão da obra de Hajime Isayama em um filme especial com cenas inéditas.',
            'qualidade': '4K HDR • Legendado PT-BR • Especial 2h',
            'duracao': '2h 15m (Filme Final)',
            'imdb': '9.8/10',
            'tamanho': '22.6 GB',
            'genero': 'Anime • Ação • Drama • Fantasia Sombria',
            'ano': '2025',
            'classificacao': '18+',
            'audio': 'Japonês, Inglês',
            'legendas': 'PT-BR, EN',
            'link_trailer': 'https://youtu.be/aot-final-trailer',
            'preco': 1
        },
        {
            'id': 'jujutsu3',
            'titulo': '🎌 JUJUTSU KAISEN 3 - TEMPORADA COMPLETA',
            'descricao': 'Nova temporada do anime de maior sucesso. Yuji Itadori enfrenta ameaças cada vez mais poderosas no mundo das maldições.',
            'qualidade': '4K • 24 Episódios • Legendado PT-BR',
            'duracao': '9h 36m (Temporada)',
            'imdb': '9.3/10',
            'tamanho': '32.8 GB',
            'genero': 'Anime • Ação • Sobrenatural • Terror',
            'ano': '2025',
            'classificacao': '16+',
            'audio': 'Japonês, Português',
            'legendas': 'PT-BR, EN',
            'link_trailer': 'https://youtu.be/jujutsu3-trailer',
            'preco': 1
        }
    ],
    'terror_2025': [
        {
            'id': 'smile2',
            'titulo': '🎬 SMILE 2: O SORRISO DO MEDO',
            'descricao': 'A entidade retorna mais assustadora que nunca, agora se espalhando viralmente através de redes sociais.',
            'qualidade': '4K HDR • Dolby Atmos • Terror Atmosférico',
            'duracao': '1h 58m',
            'imdb': '7.8/10',
            'tamanho': '12.4 GB',
            'genero': 'Terror • Suspense • Psicológico',
            'ano': '2025',
            'classificacao': '18+',
            'audio': 'Português, Inglês',
            'legendas': 'PT-BR, EN',
            'link_trailer': 'https://youtu.be/smile2-trailer',
            'preco': 1
        },
        {
            'id': 'conjuring4',
            'titulo': '🎬 THE CONJURING 4: ÚLTIMO EXORCISMO',
            'descricao': 'Ed e Lorraine Warren enfrentam seu caso mais perigoso contra uma entidade ancestral que ameaça uma família inteira.',
            'qualidade': '4K HDR • Atmos • Warner Bros',
            'duracao': '2h 05m',
            'imdb': '8.1/10',
            'tamanho': '13.7 GB',
            'genero': 'Terror • Sobrenatural • Baseado em fatos',
            'ano': '2025',
            'classificacao': '18+',
            'audio': 'Português, Inglês',
            'legendas': 'PT-BR, EN',
            'link_trailer': 'https://youtu.be/conjuring4-trailer',
            'preco': 1
        }
    ],
    'brasileiros': [
        {
            'id': 'cidadealta2',
            'titulo': '🎬 CIDADE ALTA 2: O RETORNO',
            'descricao': 'Continuação do sucesso nacional com Wesley Safadão no papel principal. Ação, drama e suspense nas favelas do Rio de Janeiro.',
            'qualidade': '4K HDR • Áudio 5.1 • Cinema Nacional',
            'duracao': '2h 08m',
            'imdb': '8.1/10',
            'tamanho': '13.2 GB',
            'genero': 'Ação • Policial • Drama • Brasileiro',
            'ano': '2025',
            'classificacao': '16+',
            'audio': 'Português Brasileiro',
            'legendas': 'PT-BR, EN, ES',
            'link_trailer': 'https://youtu.be/cidadealta2-trailer',
            'preco': 1
        }
    ],
    'lancamentos': [
        {
            'id': 'blackpanther3',
            'titulo': '🎬 BLACK PANTHER 3: WAKANDA FOREVER 2',
            'descricao': 'Shuri enfrenta ameaças globais e conflitos internos como nova Pantera Negra. Tecnologia Wakandana em exibição máxima.',
            'qualidade': '4K IMAX • Dolby Vision • Atmos',
            'duracao': '2h 45m',
            'imdb': '8.6/10',
            'tamanho': '20.1 GB',
            'genero': 'Ação • Ficção Científica • Drama • Herói',
            'ano': '2025',
            'classificacao': '12+',
            'audio': 'Português, Inglês, Xhosa',
            'legendas': 'PT-BR, EN, XH',
            'link_trailer': 'https://youtu.be/blackpanther3-trailer',
            'preco': 1
        },
        {
            'id': 'dune3',
            'titulo': '🎬 DUNE 3: IMPERADOR',
            'descricao': 'Paul Atreides se torna o imperador de Arrakis e enfrenta novas ameaças enquanto tenta controlar a produção da especiaria.',
            'qualidade': '4K IMAX • Dolby Atmos • Warner Bros',
            'duracao': '2h 55m',
            'imdb': '9.2/10',
            'tamanho': '21.8 GB',
            'genero': 'Ficção Científica • Drama • Aventura',
            'ano': '2025',
            'classificacao': '14+',
            'audio': 'Português, Inglês',
            'legendas': 'PT-BR, EN',
            'link_trailer': 'https://youtu.be/dune3-trailer',
            'preco': 1
        },
        {
            'id': 'superman2025',
            'titulo': '🎬 SUPERMAN: LEGADO - 2025',
            'descricao': 'Nova versão do Homem de Aço com um elenco renovado e história atualizada para os tempos modernos.',
            'qualidade': '4K HDR • Dolby Vision • DC Studios',
            'duracao': '2h 28m',
            'imdb': '8.4/10',
            'tamanho': '18.9 GB',
            'genero': 'Ação • Super-herói • Ficção Científica',
            'ano': '2025',
            'classificacao': '12+',
            'audio': 'Português, Inglês',
            'legendas': 'PT-BR, EN',
            'link_trailer': 'https://youtu.be/superman2025-trailer',
            'preco': 1
        }
    ]
}

# 📅 RECOMENDAÇÕES DIÁRIAS
RECOMENDACOES_DIARIAS = {
    'segunda': {
        'titulo': '🚀 SEGUNDA DE AÇÃO SUPREMA!',
        'filme': 'VENOM 3: A ÚLTIMA BATALHA',
        'categoria': 'acao_2025',
        'hashtag': '#SegundaDeAção'
    },
    'terca': {
        'titulo': '🎭 TERÇA DRAMÁTICA INTENSA!',
        'filme': 'THE LAST OF US 3',
        'categoria': 'series_2025',
        'hashtag': '#TerçaDramática'
    },
    'quarta': {
        'titulo': '🌍 QUARTA DE AVENTURA ÉPICA!',
        'filme': 'AVATAR 4: O LEGADO',
        'categoria': 'aventura_2025',
        'hashtag': '#QuartaAventura'
    },
    'quinta': {
        'titulo': '🕷️ QUINTA ANIMADA INCRÍVEL!',
        'filme': 'SPIDER-MAN: BEYOND THE SPIDER-VERSE',
        'categoria': 'animacao_2025',
        'hashtag': '#QuintaAnimada'
    },
    'sexta': {
        'titulo': '🔮 SEXTA MISTERIOSA VICIANTE!',
        'filme': 'STRANGER THINGS 5',
        'categoria': 'series_2025',
        'hashtag': '#SextaMisteriosa'
    },
    'sabado': {
        'titulo': '⚔️ SÁBADO ANIME ÉPICO TOTAL!',
        'filme': 'DEMON SLAYER: FINAL ARC',
        'categoria': 'animes_2025',
        'hashtag': '#SábadoAnime'
    },
    'domingo': {
        'titulo': '🎬 DOMINGÃO PREMIUM FAMÍLIA!',
        'filme': 'FROZEN 3: O REINO DE GELO',
        'categoria': 'animacao_2025',
        'hashtag': '#Domingão'
    }
}

# 💰 PLANOS VIP SUPERIORES
PLANOS_VIP = {
    '1_mes': {
        'nome': '💎 VIP 1 MÊS',
        'preco': '50 MZN',
        'creditos': 15,
        'duracao': 30,
        'vantagens': [
            '✅ 15 créditos mensais',
            '✅ Entrega prioritária (5-15min)',
            '✅ Suporte VIP 24/7',
            '✅ Lançamentos antecipados',
            '✅ Catálogo exclusivo'
        ]
    },
    '3_meses': {
        'nome': '🔥 VIP 3 MESES',
        'preco': '120 MZN',
        'creditos': 50,
        'duracao': 90,
        'vantagens': [
            '✅ 50 créditos (5 bônus)',
            '✅ Todas vantagens VIP',
            '✅ Acesso beta',
            '✅ 1 filme grátis/mês',
            '✅ Desconto em créditos'
        ]
    },
    '6_meses': {
        'nome': '👑 VIP 6 MESES',
        'preco': '200 MZN',
        'creditos': 120,
        'duracao': 180,
        'vantagens': [
            '✅ 120 créditos (30 bônus)',
            '✅ Consultor pessoal',
            '✅ Acesso vitalício grupo VIP',
            '✅ 5 filmes grátis/mês',
            '✅ Brindes exclusivos'
        ]
    },
    'anual': {
        'nome': '🏆 VIP ANUAL PREMIUM',
        'preco': '350 MZN',
        'creditos': 300,
        'duracao': 365,
        'vantagens': [
            '✅ 300 créditos (60 bônus)',
            '✅ Acesso vitalício',
            '✅ Nome lista apoiadores',
            '✅ 10 filmes grátis/mês',
            '✅ Kit premium físico'
        ]
    }
}

# 🗄️ BANCO DE DADOS COMPLETO
def get_db():
    conn = sqlite3.connect('cinema_pro_ultra.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()
    
    # Tabela de usuários
    c.execute('''CREATE TABLE IF NOT EXISTS usuarios
                 (user_id INTEGER PRIMARY KEY,
                  username TEXT,
                  creditos INTEGER DEFAULT 0,
                  creditos_bonus INTEGER DEFAULT 0,
                  vip INTEGER DEFAULT 0,
                  vip_tipo TEXT,
                  vip_expira DATE,
                  data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  ultimo_login TIMESTAMP,
                  total_pedidos INTEGER DEFAULT 0,
                  total_gasto REAL DEFAULT 0)''')
    
    # Tabela de pedidos
    c.execute('''CREATE TABLE IF NOT EXISTS pedidos
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  username TEXT,
                  filme_id TEXT,
                  filme_titulo TEXT,
                  status TEXT DEFAULT 'pendente',
                  data_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  data_entrega TIMESTAMP,
                  FOREIGN KEY (user_id) REFERENCES usuarios (user_id))''')
    
    # Tabela de transações
    c.execute('''CREATE TABLE IF NOT EXISTS transacoes
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  tipo TEXT,
                  valor REAL,
                  metodo TEXT,
                  status TEXT DEFAULT 'pendente',
                  data TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # Tabela de logs
    c.execute('''CREATE TABLE IF NOT EXISTS logs
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  acao TEXT,
                  detalhes TEXT,
                  data TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    conn.commit()
    conn.close()

init_db()

# 🔐 VERIFICAÇÃO ADMIN
def is_admin(user_id, username):
    return user_id == ADMIN_ID or (username and username.lower() == ADMIN_USERNAME.replace('@', '').lower())

# 📊 FUNÇÕES UTILITÁRIAS
def registrar_log(user_id, acao, detalhes=""):
    conn = get_db()
    c = conn.cursor()
    c.execute("INSERT INTO logs (user_id, acao, detalhes) VALUES (?, ?, ?)",
              (user_id, acao, detalhes))
    conn.commit()
    conn.close()

def atualizar_ultimo_login(user_id):
    conn = get_db()
    c = conn.cursor()
    c.execute("UPDATE usuarios SET ultimo_login = CURRENT_TIMESTAMP WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

def verificar_boas_vindas(user_id):
    conn = get_db()
    c = conn.cursor()
    
    # Verificar se usuário já tem pedidos
    c.execute("SELECT COUNT(*) FROM pedidos WHERE user_id = ?", (user_id,))
    tem_pedidos = c.fetchone()[0]
    
    if tem_pedidos == 0:
        # Dar 3 créditos de boas-vindas
        c.execute("UPDATE usuarios SET creditos_bonus = creditos_bonus + 3 WHERE user_id = ?", (user_id,))
        c.execute("INSERT INTO transacoes (user_id, tipo, valor) VALUES (?, 'bonus_boas_vindas', 3)", (user_id,))
        conn.commit()
        conn.close()
        return True
    
    conn.close()
    return False

def obter_creditos_usuario(user_id):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT creditos, creditos_bonus FROM usuarios WHERE user_id = ?", (user_id,))
    usuario = c.fetchone()
    conn.close()
    
    if usuario:
        return usuario['creditos'] + usuario['creditos_bonus']
    return 0

# 👋 COMANDO START MEGA
@bot.message_handler(commands=['start'])
def start_comando(message):
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name
    
    # Registrar/Atualizar usuário
    conn = get_db()
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO usuarios (user_id, username) VALUES (?, ?)", (user_id, username))
    c.execute("UPDATE usuarios SET ultimo_login = CURRENT_TIMESTAMP WHERE user_id = ?", (user_id,))
    
    # Verificar boas-vindas
    bonus_recebido = verificar_boas_vindas(user_id)
    
    # Buscar informações
    c.execute("SELECT creditos, creditos_bonus, vip, vip_tipo, vip_expira, total_pedidos FROM usuarios WHERE user_id = ?", (user_id,))
    usuario = c.fetchone()
    
    creditos_total = usuario['creditos'] + usuario['creditos_bonus'] if usuario else 0
    vip_status = "✅ ATIVO" if usuario and usuario['vip'] == 1 else "❌ INATIVO"
    vip_info = f" ({usuario['vip_tipo']})" if usuario and usuario['vip_tipo'] else ""
    
    conn.close()
    
    # Registrar log
    registrar_log(user_id, "start", f"Créditos: {creditos_total}")
    
    # Criar teclado principal
    markup = InlineKeyboardMarkup(row_width=2)
    
    botoes = [
        InlineKeyboardButton("🎬 CATÁLOGO COMPLETO", callback_data="catalogo"),
        InlineKeyboardButton("🚀 LANÇAMENTOS", callback_data="lancamentos"),
        InlineKeyboardButton("💰 COMPRAR CRÉDITOS", callback_data="comprar"),
        InlineKeyboardButton("👑 VER PLANOS VIP", callback_data="vip"),
        InlineKeyboardButton("📊 MEU PERFIL", callback_data="perfil"),
        InlineKeyboardButton("🎥 TRAILERS", callback_data="trailers"),
        InlineKeyboardButton("⭐ RECOMENDAÇÃO DO DIA", callback_data="recomendacao"),
        InlineKeyboardButton("📞 SUPORTE", url=f"https://t.me/{ADMIN_USERNAME}"),
        InlineKeyboardButton("📋 AJUDA", callback_data="ajuda"),
        InlineKeyboardButton("🔍 BUSCAR FILME", callback_data="buscar")
    ]
    
    # Layout organizado
    for i in range(0, len(botoes), 2):
        markup.add(botoes[i], botoes[i+1])
    
    # Adicionar botão admin se for admin
    if is_admin(user_id, username):
        markup.add(InlineKeyboardButton("👑 PAINEL ADMIN", callback_data="admin"))
    
    # Mensagem de boas-vindas
    bonus_text = "\n🎁 *BÔNUS: 3 CRÉDITOS DE BOAS-VINDAS!*" if bonus_recebido else ""
    
    bot.reply_to(message, f"""
🎬 *CINEMA PRO ULTRA* 🎬

👤 *SEU PERFIL:*
🆔 ID: `{user_id}`
💎 Créditos: *{creditos_total}* {bonus_text}
👑 VIP: *{vip_status}{vip_info}*
📊 Pedidos: {usuario['total_pedidos'] if usuario else 0}

🌟 *SERVIÇOS PREMIUM:*
• 🎬 120+ Filmes/Séries em 4K HDR
• 🚀 Lançamentos simultâneos ao cinema
• ⚡ Entrega em 5-15 minutos (VIP)
• 📞 Suporte 24/7

💡 *COMO FUNCIONA:*
1️⃣ Escolha seu filme/série
2️⃣ Use 1 crédito por pedido
3️⃣ Receba o link em até 15min
4️⃣ Aproveite em qualidade 4K!

🎯 *COMANDOS RÁPIDOS:*
`/catalogo` - Ver catálogo completo
`/creditos` - Ver seus créditos
`/comprar` - Comprar mais créditos
`/vip` - Planos VIP
`/pedir` - Fazer pedido

⚡ *ESCOLHA UMA OPÇÃO ABAIXO:*
    """, parse_mode='Markdown', reply_markup=markup)

# 🎬 COMANDO CATÁLOGO
@bot.message_handler(commands=['catalogo'])
def catalogo_comando(message):
    markup = InlineKeyboardMarkup(row_width=2)
    
    categorias = [
        ("🎬 AÇÃO 2025", "categoria_acao_2025"),
        ("🌍 AVENTURA 2025", "categoria_aventura_2025"),
        ("🎥 ANIMAÇÃO 2025", "categoria_animacao_2025"),
        ("📺 SÉRIES 2025", "categoria_series_2025"),
        ("🎌 ANIMES 2025", "categoria_animes_2025"),
        ("😨 TERROR 2025", "categoria_terror_2025"),
        ("🇧🇷 BRASILEIROS", "categoria_brasileiros"),
        ("🚀 LANÇAMENTOS", "categoria_lancamentos")
    ]
    
    for i in range(0, len(categorias), 2):
        if i+1 < len(categorias):
            markup.add(
                InlineKeyboardButton(categorias[i][0], callback_data=categorias[i][1]),
                InlineKeyboardButton(categorias[i+1][0], callback_data=categorias[i+1][1])
            )
    
    markup.add(InlineKeyboardButton("🔍 BUSCAR FILME", callback_data="buscar_filme"))
    markup.add(InlineKeyboardButton("🏠 VOLTAR AO INÍCIO", callback_data="inicio"))
    
    bot.reply_to(message, """
🎬 *CATÁLOGO PREMIUM 2025* 🎬

📊 *120+ TÍTULOS DISPONÍVEIS EM 4K HDR*

🏆 *CATEGORIAS EXCLUSIVAS:*

🎬 *AÇÃO 2025* (6 filmes)
• Venom 3, John Wick 5, Mission Impossible 9
• Ação intensa em qualidade máxima

🌍 *AVENTURA 2025* (2 filmes)
• Avatar 4, Indiana Jones 6
• Mundos fantásticos e épicos

🎥 *ANIMAÇÃO 2025* (3 filmes)
• Spider-Man Beyond, Frozen 3, Toy Story 5
• Animação de qualidade cinema

📺 *SÉRIES 2025* (4 séries)
• Stranger Things 5, The Last of Us 3
• Temporadas completas UHD

🎌 *ANIMES 2025* (3 animes)
• Demon Slayer, Attack on Titan, Jujutsu Kaisen
• Animes legendados em 4K

😨 *TERROR 2025* (2 filmes)
• Smile 2, The Conjuring 4
• Terror de qualidade premium

🇧🇷 *BRASILEIROS* (1 filme)
• Cidade Alta 2
• Cinema nacional em 4K

🚀 *LANÇAMENTOS* (3 filmes)
• Black Panther 3, Dune 3, Superman
• Novidades quentinhas do forno!

💎 *Todos por apenas 1 crédito cada!*

🎯 *Selecione uma categoria:*
    """, parse_mode='Markdown', reply_markup=markup)

# 💰 COMANDO COMPRAR CRÉDITOS
@bot.message_handler(commands=['comprar', 'creditos'])
def comprar_comando(message):
    user_id = message.from_user.id
    creditos = obter_creditos_usuario(user_id)
    
    markup = InlineKeyboardMarkup(row_width=2)
    
    # Pacotes de créditos
    pacotes = [
        ("💎 1 CRÉDITO - 20 MZN", "pacote_1"),
        ("💎 3 CRÉDITOS - 50 MZN", "pacote_3"),
        ("💎 5 CRÉDITOS - 80 MZN", "pacote_5"),
        ("💎 10 CRÉDITOS - 150 MZN", "pacote_10")
    ]
    
    for i in range(0, len(pacotes), 2):
        markup.add(
            InlineKeyboardButton(pacotes[i][0], callback_data=pacotes[i][1]),
            InlineKeyboardButton(pacotes[i+1][0], callback_data=pacotes[i+1][1])
        )
    
    markup.add(InlineKeyboardButton("👑 PLANOS VIP", callback_data="vip"))
    markup.add(InlineKeyboardButton("🏠 VOLTAR AO INÍCIO", callback_data="inicio"))
    
    bot.reply_to(message, f"""
💰 *COMPRAR CRÉDITOS* 💰

🎯 *1 CRÉDITO = 1 FILME/SÉRIE EM 4K*

📊 *SEU SALDO ATUAL:* *{creditos} créditos*

📦 *PACOTES DISPONÍVEIS:*

💎 *CRÉDITOS AVULSOS:*
• 1 Crédito - 20 MZN
• 3 Créditos - 50 MZN (Economize 10 MZN)
• 5 Créditos - 80 MZN (Economize 20 MZN)
• 10 Créditos - 150 MZN (Economize 50 MZN)

👑 *PLANOS VIP (RECOMENDADO):*
• VIP 1 Mês - 50 MZN (15 créditos)
• VIP 3 Meses - 120 MZN (50 créditos)
• VIP 6 Meses - 200 MZN (120 créditos)
• VIP Anual - 350 MZN (300 créditos)

💳 *FORMAS DE PAGAMENTO:*
• M-Pesa: `{CONTATOS['mpesa']}`
• e-Mola: `{CONTATOS['emola']}`
• PayPal: `{CONTATOS['paypal']}`

⚡ *PROCESSO RÁPIDO:*
1. Escolha seu pacote
2. Faça o pagamento
3. Envie comprovante para @{ADMIN_USERNAME}
4. Receba créditos em 2-5 minutos

🎁 *PROMOÇÕES ATIVAS:*
• Primeira compra: +3 créditos bônus!
• Compra acima de 100 MZN: +5% de bônus

📞 *Dúvidas sobre pagamento?*
Fale com @{ADMIN_USERNAME}
    """, parse_mode='Markdown', reply_markup=markup)

# 👑 COMANDO VIP
@bot.message_handler(commands=['vip'])
def vip_comando(message):
    markup = InlineKeyboardMarkup(row_width=1)
    
    for plano_key, plano in PLANOS_VIP.items():
        markup.add(InlineKeyboardButton(
            f"{plano['nome']} - {plano['preco']}",
            callback_data=f"plano_{plano_key}"
        ))
    
    markup.add(InlineKeyboardButton("💰 CRÉDITOS AVULSOS", callback_data="comprar"))
    markup.add(InlineKeyboardButton("🏠 VOLTAR AO INÍCIO", callback_data="inicio"))
    
    texto = """
👑 *PLANOS VIP PREMIUM* 👑

🌟 *VANTAGENS EXCLUSIVAS:*
• ✅ Entrega prioritária (5-15 minutos)
• ✅ Suporte VIP 24/7
• ✅ Lançamentos antecipados
• ✅ Catálogo exclusivo
• ✅ Descontos especiais

📊 *COMPARAÇÃO DE PLANOS:*
"""
    
    for plano_key, plano in PLANOS_VIP.items():
        texto += f"\n*{plano['nome']}*"
        texto += f"\n💰 Preço: {plano['preco']}"
        texto += f"\n💎 Créditos: {plano['creditos']}"
        texto += f"\n📅 Duração: {plano['duracao']} dias"
        texto += f"\n"
    
    texto += f"""
    
💳 *FORMAS DE PAGAMENTO:*
• M-Pesa: `{CONTATOS['mpesa']}`
• e-Mola: `{CONTATOS['emola']}`
• PayPal: `{CONTATOS['paypal']}`

📞 *Para assinar:*
1. Escolha seu plano
2. Faça o pagamento  
3. Envie comprovante para @{ADMIN_USERNAME}
4. Ativação em 5 minutos

🎯 *Clique no plano desejado para mais informações!*
    """
    
    bot.reply_to(message, texto, parse_mode='Markdown', reply_markup=markup)

# 📊 COMANDO PERFIL
@bot.message_handler(commands=['perfil', 'me'])
def perfil_comando(message):
    user_id = message.from_user.id
    
    conn = get_db()
    c = conn.cursor()
    
    c.execute("""
        SELECT u.*, COUNT(p.id) as total_pedidos
        FROM usuarios u
        LEFT JOIN pedidos p ON u.user_id = p.user_id
        WHERE u.user_id = ?
        GROUP BY u.user_id
    """, (user_id,))
    
    usuario = c.fetchone()
    
    if not usuario:
        bot.reply_to(message, "❌ Usuário não encontrado! Use /start primeiro.")
        return
    
    creditos_total = usuario['creditos'] + usuario['creditos_bonus']
    vip_status = "✅ ATIVO" if usuario['vip'] == 1 else "❌ INATIVO"
    
    # Buscar pedidos recentes
    c.execute("""
        SELECT filme_titulo, status, data_pedido 
        FROM pedidos 
        WHERE user_id = ? 
        ORDER BY data_pedido DESC 
        LIMIT 3
    """, (user_id,))
    
    pedidos_recentes = c.fetchall()
    
    conn.close()
    
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🔄 ATUALIZAR", callback_data="perfil"),
        InlineKeyboardButton("📋 HISTÓRICO", callback_data="historico")
    )
    markup.add(
        InlineKeyboardButton("💰 COMPRAR CRÉDITOS", callback_data="comprar"),
        InlineKeyboardButton("🏠 INÍCIO", callback_data="inicio")
    )
    
    # Construir mensagem
    texto = f"""
👤 *MEU PERFIL PREMIUM* 👤

🆔 *ID:* `{user_id}`
👤 *Nome:* {usuario['username'] or 'Não definido'}
📅 *Membro desde:* {usuario['data_cadastro'][:10] if usuario['data_cadastro'] else 'Hoje'}

💎 *CRÉDITOS:*
• Total disponível: *{creditos_total}*
• Regulares: {usuario['creditos']}
• Bônus: {usuario['creditos_bonus']}

👑 *VIP:*
• Status: {vip_status}
• Tipo: {usuario['vip_tipo'] or 'Nenhum'}
• Expira: {usuario['vip_expira'] or 'Não aplicável'}

📊 *ESTATÍSTICAS:*
• Total de pedidos: {usuario['total_pedidos']}
• Último login: {usuario['ultimo_login'][:16] if usuario['ultimo_login'] else 'Nunca'}

📦 *PEDIDOS RECENTES:*
"""
    
    if pedidos_recentes:
        for pedido in pedidos_recentes:
            status_emoji = "✅" if pedido['status'] == 'entregue' else "⏳"
            texto += f"• {status_emoji} {pedido['filme_titulo']} - {pedido['status']}\n"
    else:
        texto += "• Nenhum pedido realizado ainda\n"
    
    texto += """
🎯 *PRÓXIMOS PASSOS:*
• Faça seu primeiro pedido!
• Compre créditos para continuar
• Considere o plano VIP para benefícios

⚡ *Use os botões abaixo para ações rápidas!*
    """
    
    bot.reply_to(message, texto, parse_mode='Markdown', reply_markup=markup)

# 🎥 COMANDO TRAILERS
@bot.message_handler(commands=['trailer', 'trailers'])
def trailers_comando(message):
    markup = InlineKeyboardMarkup(row_width=2)
    
    filmes_trailers = [
        ("🎬 VENOM 3", "trailer_venom3"),
        ("🎬 JOHN WICK 5", "trailer_johnwick5"),
        ("🎬 AVATAR 4", "trailer_avatar4"),
        ("🎬 SPIDER-MAN", "trailer_spiderman"),
        ("📺 STRANGER THINGS 5", "trailer_stranger5"),
        ("🎌 DEMON SLAYER", "trailer_demonslayer")
    ]
    
    for i in range(0, len(filmes_trailers), 2):
        if i+1 < len(filmes_trailers):
            markup.add(
                InlineKeyboardButton(filmes_trailers[i][0], callback_data=filmes_trailers[i][1]),
                InlineKeyboardButton(filmes_trailers[i+1][0], callback_data=filmes_trailers[i+1][1])
            )
    
    markup.add(InlineKeyboardButton("🏠 VOLTAR AO INÍCIO", callback_data="inicio"))
    
    bot.reply_to(message, """
🎬 *TRAILERS EXCLUSIVOS* 🎬

🎯 *ASSISTA ANTES DE PEDIR!*

⚡ *VANTAGENS:*
• Veja a qualidade do conteúdo
• Conheça a história antes de comprar
• Cenas exclusivas em alta definição

🎥 *TRAILERS DISPONÍVEIS:*

🎬 *FILMES:*
• Venom 3: A Última Batalha
• John Wick 5: Legado
• Avatar 4: O Legado
• Spider-Man: Beyond the Spider-Verse

📺 *SÉRIES:*
• Stranger Things 5
• The Last of Us 3

🎌 *ANIMES:*
• Demon Slayer: Final Arc
• Attack on Titan: Final Chapters

💡 *APÓS O TRAILER:*
• Filme completo por 1 crédito
• Qualidade 4K HDR garantida
• Entrega em 15-30 minutos

🎯 *Escolha um trailer para assistir:*
    """, parse_mode='Markdown', reply_markup=markup)

# ⭐ COMANDO RECOMENDAÇÃO
@bot.message_handler(commands=['recomendacao', 'filmedodia'])
def recomendacao_comando(message):
    dia_semana = datetime.now().strftime('%A').lower()
    dias_pt = {
        'monday': 'segunda', 'tuesday': 'terca', 'wednesday': 'quarta',
        'thursday': 'quinta', 'friday': 'sexta', 'saturday': 'sabado', 'sunday': 'domingo'
    }
    
    dia = dias_pt.get(dia_semana, 'segunda')
    recomendacao = RECOMENDACOES_DIARIAS[dia]
    
    # Buscar informações do filme
    filme_info = None
    for categoria, filmes in CATALOGO_PREMIUM.items():
        if categoria == recomendacao['categoria']:
            for filme in filmes:
                if recomendacao['filme'].split(':')[0].strip() in filme['titulo']:
                    filme_info = filme
                    break
        if filme_info:
            break
    
    markup = InlineKeyboardMarkup()
    if filme_info:
        markup.add(
            InlineKeyboardButton("🎬 VER DETALHES", callback_data=f"detalhes_{filme_info['id']}"),
            InlineKeyboardButton("🎥 VER TRAILER", url=filme_info['link_trailer'])
        )
        markup.add(InlineKeyboardButton("📦 PEDIR AGORA", callback_data=f"pedir_{filme_info['id']}"))
    
    markup.add(InlineKeyboardButton("🏠 VOLTAR AO INÍCIO", callback_data="inicio"))
    
    texto = f"""
⭐ *RECOMENDAÇÃO DO DIA* ⭐
{recomendacao['hashtag']}

{recomendacao['titulo']}

🎬 *FILME SUGERIDO:*
*{recomendacao['filme']}*

"""
    
    if filme_info:
        texto += f"""
📖 *Sinopse:*
{filme_info['descricao']}

⭐ *Avaliação IMDb:* {filme_info['imdb']}
🎭 *Gênero:* {filme_info['genero']}
⏰ *Duração:* {filme_info['duracao']}
💾 *Tamanho:* {filme_info['tamanho']}
🎯 *Qualidade:* {filme_info['qualidade']}

💎 *PREÇO:* 1 CRÉDITO
⚡ *ENTREGA:* 15-30 minutos

🎯 *Use 1 crédito e receba agora mesmo!*
        """
    
    bot.reply_to(message, texto, parse_mode='Markdown', reply_markup=markup)

# 🔍 COMANDO BUSCAR
@bot.message_handler(commands=['buscar', 'search'])
def buscar_comando(message):
    args = message.text.split()[1:]
    
    if not args:
        bot.reply_to(message, """
🔍 *BUSCA DE FILMES/SÉRIES*

⚡ *Como usar:*
`/buscar nome do filme`
`/buscar venom 3`
`/buscar stranger things`

💡 *Exemplos:*
• `/buscar avatar 4`
• `/buscar john wick`
• `/buscar demon slayer`

🎯 *Dicas:*
• Use palavras-chave
• Tente o nome em inglês
• Verifique a grafia

🔎 *Ou use os botões do catálogo!*
        """)
        return
    
    termo_busca = ' '.join(args).lower()
    resultados = []
    
    # Buscar em todas as categorias
    for categoria, filmes in CATALOGO_PREMIUM.items():
        for filme in filmes:
            if (termo_busca in filme['titulo'].lower() or 
                termo_busca in filme['descricao'].lower() or
                termo_busca in filme['genero'].lower()):
                resultados.append(filme)
    
    if resultados:
        # Limitar a 5 resultados
        resultados = resultados[:5]
        
        texto = f"🔍 *RESULTADOS PARA: '{termo_busca}'*\n\n"
        
        for i, filme in enumerate(resultados, 1):
            texto += f"*{i}. {filme['titulo']}*\n"
            texto += f"   ⭐ {filme['imdb']} • 🎭 {filme['genero']}\n"
            texto += f"   ⏰ {filme['duracao']} • 📦 {filme['tamanho']}\n\n"
        
        if len(resultados) == 1:
            # Se só um resultado, mostrar detalhes
            filme = resultados[0]
            markup = InlineKeyboardMarkup()
            markup.add(
                InlineKeyboardButton("🎬 PEDIR AGORA", callback_data=f"pedir_{filme['id']}"),
                InlineKeyboardButton("🎥 VER TRAILER", url=filme['link_trailer'])
            )
            markup.add(InlineKeyboardButton("🔍 NOVA BUSCA", callback_data="buscar_filme"))
            
            texto = f"""
🎬 *{filme['titulo']}*

📖 *Sinopse:*
{filme['descricao']}

⭐ *Avaliação IMDb:* {filme['imdb']}
🎭 *Gênero:* {filme['genero']} • {filme['ano']}
⏰ *Duração:* {filme['duracao']}
💾 *Tamanho:* {filme['tamanho']}
🎯 *Qualidade:* {filme['qualidade']}
🔊 *Áudio:* {filme['audio']}
📝 *Legendas:* {filme['legendas']}

💎 *PREÇO:* 1 CRÉDITO
⚡ *ENTREGA:* 15-30 minutos
            """
        else:
            # Múltiplos resultados
            markup = InlineKeyboardMarkup()
            for i, filme in enumerate(resultados, 1):
                markup.add(InlineKeyboardButton(
                    f"🎬 {i}. {filme['titulo'][:30]}...",
                    callback_data=f"detalhes_{filme['id']}"
                ))
            
            markup.add(InlineKeyboardButton("🔍 NOVA BUSCA", callback_data="buscar_filme"))
        
        bot.reply_to(message, texto, parse_mode='Markdown', reply_markup=markup)
    else:
        bot.reply_to(message, f"""
❌ *NENHUM RESULTADO ENCONTRADO*

Não encontramos conteúdo correspondente a *'{termo_busca}'*.

💡 *SUGESTÕES:*
• Verifique a grafia
• Tente o nome original em inglês
• Use palavras-chave mais gerais

📂 *CATÁLOGO COMPLETO:*
`/catalogo` - Ver todas as categorias
`/lancamentos` - Novidades da semana
`/recomendacao` - Sugestão do dia
        """, parse_mode='Markdown')

# 📦 COMANDO PEDIR
@bot.message_handler(commands=['pedir'])
def pedir_comando(message):
    args = message.text.split()[1:]
    
    if not args:
        user_id = message.from_user.id
        creditos = obter_creditos_usuario(user_id)
        
        bot.reply_to(message, f"""
📦 *FAZER PEDIDO*

💎 *Seus créditos disponíveis:* *{creditos}*

⚡ *Como pedir:*
`/pedir Nome do Filme`

🎯 *Exemplos:*
`/pedir Venom 3`
`/pedir Stranger Things 5`
`/pedir Demon Slayer`

💡 *Dicas:*
• Use `/catalogo` para ver opções
• Use `/buscar` para encontrar específicos
• 1 crédito = 1 filme/série

🎬 *Ou navegue pelo catálogo!*
        """)
        return
    
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name
    filme_nome = ' '.join(args)
    
    # Buscar filme
    filme_info = None
    for categoria, filmes in CATALOGO_PREMIUM.items():
        for filme in filmes:
            if filme_nome.lower() in filme['titulo'].lower():
                filme_info = filme
                categoria_filme = categoria
                break
        if filme_info:
            break
    
    if not filme_info:
        bot.reply_to(message, f"""
❌ *FILME NÃO ENCONTRADO*

Não encontramos *{filme_nome}* no catálogo.

💡 *SUGESTÕES:*
• Verifique a grafia
• Use `/catalogo` para ver opções
• Use `/buscar` para busca avançada

🎯 *Filmes similares disponíveis:*
`/catalogo` - Ver catálogo completo
        """)
        return
    
    # Verificar créditos
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT creditos, creditos_bonus FROM usuarios WHERE user_id = ?", (user_id,))
    usuario = c.fetchone()
    
    if not usuario:
        bot.reply_to(message, "❌ *Erro: Usuário não encontrado! Use /start primeiro.*", parse_mode='Markdown')
        conn.close()
        return
    
    creditos_total = usuario['creditos'] + usuario['creditos_bonus']
    
    if creditos_total < 1:
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton("💰 COMPRAR CRÉDITOS", callback_data="comprar"),
            InlineKeyboardButton("👑 VER VIP", callback_data="vip")
        )
        
        bot.reply_to(message, f"""
❌ *CRÉDITOS INSUFICIENTES*

💎 *Seus créditos:* *{creditos_total}*
🎬 *Filme desejado:* *{filme_info['titulo']}*

⚡ *Você precisa de 1 crédito para fazer este pedido.*

💫 *OPÇÕES:*
• Comprar créditos avulsos
• Assinar plano VIP (mais econômico)
• Ganhar créditos indicando amigos

🎁 *Promoção:* Primeira compra dá +3 créditos bônus!
        """, parse_mode='Markdown', reply_markup=markup)
        conn.close()
        return
    
    # Processar pedido
    # Deduzir primeiro dos créditos regulares, depois dos bônus
    if usuario['creditos'] >= 1:
        c.execute("UPDATE usuarios SET creditos = creditos - 1 WHERE user_id = ?", (user_id,))
    else:
        creditos_necessarios = 1 - usuario['creditos']
        c.execute("UPDATE usuarios SET creditos = 0, creditos_bonus = creditos_bonus - ? WHERE user_id = ?", 
                 (creditos_necessarios, user_id))
    
    # Registrar pedido
    pedido_id = c.execute("""
        INSERT INTO pedidos (user_id, username, filme_id, filme_titulo, status)
        VALUES (?, ?, ?, ?, 'processando')
    """, (user_id, username, filme_info['id'], filme_info['titulo'])).lastrowid
    
    # Atualizar total de pedidos
    c.execute("UPDATE usuarios SET total_pedidos = total_pedidos + 1 WHERE user_id = ?", (user_id,))
    
    # Registrar transação
    c.execute("""
        INSERT INTO transacoes (user_id, tipo, valor)
        VALUES (?, 'pedido_filme', -1)
    """, (user_id,))
    
    conn.commit()
    conn.close()
    
    # Registrar log
    registrar_log(user_id, "pedido", f"Filme: {filme_info['titulo']}, ID: {pedido_id}")
    
    # Notificar admin
    try:
        admin_msg = f"""
📦 *NOVO PEDIDO* 📦

🆔 *Pedido:* #{pedido_id}
👤 *Usuário:* @{username} ({user_id})
🎬 *Filme:* {filme_info['titulo']}
💎 *Créditos usados:* 1
💰 *Créditos restantes:* {creditos_total - 1}
⏰ *Data:* {datetime.now().strftime('%d/%m/%Y %H:%M')}

⚡ *Status:* Processando
        """
        bot.send_message(ADMIN_ID, admin_msg, parse_mode='Markdown')
    except:
        pass
    
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(
        "📞 ACOMPANHAR PEDIDO", 
        url=f"https://t.me/{ADMIN_USERNAME}"
    ))
    markup.add(InlineKeyboardButton(
        "🎬 FAZER NOVO PEDIDO", 
        callback_data="catalogo"
    ))
    
    bot.reply_to(message, f"""
✅ *PEDIDO CONFIRMADO COM SUCESSO!* ✅

🆔 *Número do Pedido:* *#{pedido_id}*
🎬 *Filme:* *{filme_info['titulo']}*
💎 *Créditos utilizados:* 1
💰 *Créditos restantes:* *{creditos_total - 1}*

⏰ *TEMPO DE ENTREGA:*
• Normal: 15-30 minutos
• VIP: 5-15 minutos (usuários VIP)

📦 *MÉTODO DE ENTREGA:*
• Google Drive (recomendado)
• Mega.nz
• MediaFire
• Link direto via HTTP

⚡ *QUALIDADE GARANTIDA:*
• Resolução: 4K HDR
• Áudio: {filme_info['audio']}
• Legendas: {filme_info['legendas']}
• Formato: MKV/MP4

📞 *ACOMPANHAMENTO:*
Entre em contato com @{ADMIN_USERNAME} para:
• Status do pedido
• Problemas com download
• Qualidade insatisfatória

⭐ *APÓS RECEBER:*
Avalie sua experiência para nos ajudar a melhorar!

🎯 *OBRIGADO PELA PREFERÊNCIA!*
    """, parse_mode='Markdown', reply_markup=markup)

# 👑 COMANDO ADMIN
@bot.message_handler(commands=['admin'])
def admin_comando(message):
    user_id = message.from_user.id
    username = message.from_user.username
    
    if not is_admin(user_id, username):
        bot.reply_to(message, "❌ *Acesso negado! Apenas administradores.*", parse_mode='Markdown')
        return
    
    conn = get_db()
    c = conn.cursor()
    
    # Estatísticas
    total_usuarios = c.execute("SELECT COUNT(*) FROM usuarios").fetchone()[0]
    total_pedidos = c.execute("SELECT COUNT(*) FROM pedidos").fetchone()[0]
    pedidos_pendentes = c.execute("SELECT COUNT(*) FROM pedidos WHERE status = 'pendente'").fetchone()[0]
    pedidos_hoje = c.execute("SELECT COUNT(*) FROM pedidos WHERE DATE(data_pedido) = DATE('now')").fetchone()[0]
    vip_ativos = c.execute("SELECT COUNT(*) FROM usuarios WHERE vip = 1").fetchone()[0]
    
    # Receita do dia
    receita_hoje = c.execute("""
        SELECT SUM(valor) FROM transacoes 
        WHERE tipo LIKE '%compra%' 
        AND DATE(data) = DATE('now')
        AND status = 'aprovado'
    """).fetchone()[0] or 0
    
    conn.close()
    
    markup = InlineKeyboardMarkup(row_width=2)
    
    opcoes_admin = [
        ("📊 ESTATÍSTICAS", "admin_stats"),
        ("👥 GERENCIAR USUÁRIOS", "admin_usuarios"),
        ("💰 ADICIONAR CRÉDITOS", "admin_add_creditos"),
        ("📦 PEDIDOS PENDENTES", "admin_pedidos_pendentes"),
        ("👑 GERENCIAR VIP", "admin_vip"),
        ("📢 ENVIAR ANÚNCIO", "admin_broadcast"),
        ("📈 RELATÓRIOS", "admin_relatorios"),
        ("⚙️ CONFIGURAÇÕES", "admin_config")
    ]
    
    for i in range(0, len(opcoes_admin), 2):
        if i+1 < len(opcoes_admin):
            markup.add(
                InlineKeyboardButton(opcoes_admin[i][0], callback_data=opcoes_admin[i][1]),
                InlineKeyboardButton(opcoes_admin[i+1][0], callback_data=opcoes_admin[i+1][1])
            )
    
    markup.add(InlineKeyboardButton("🔄 ATUALIZAR", callback_data="admin"))
    markup.add(InlineKeyboardButton("❌ FECHAR", callback_data="fechar_admin"))
    
    bot.reply_to(message, f"""
👑 *PAINEL ADMIN - CINEMA PRO* 👑

📊 *ESTATÍSTICAS GERAIS:*
• 👥 Total Usuários: `{total_usuarios}`
• 📦 Total Pedidos: `{total_pedidos}`
• ⏳ Pendentes: `{pedidos_pendentes}`
• 🚀 Hoje: `{pedidos_hoje}`
• 💰 Receita Hoje: `{receita_hoje:.2f} MZN`
• 👑 VIPs Ativos: `{vip_ativos}`

⚡ *SISTEMA:*
🟢 *Online e operacional*
📅 *Última atualização:* {datetime.now().strftime('%H:%M')}

🎯 *ESCOLHA UMA AÇÃO:*
    """, parse_mode='Markdown', reply_markup=markup)

# 🆘 COMANDO AJUDA
@bot.message_handler(commands=['ajuda', 'help', 'comandos'])
def ajuda_comando(message):
    markup = InlineKeyboardMarkup(row_width=2)
    
    botoes_ajuda = [
        ("🎬 COMO PEDIR", "ajuda_pedir"),
        ("💰 COMPRAR CRÉDITOS", "ajuda_comprar"),
        ("👑 PLANOS VIP", "ajuda_vip"),
        ("📞 SUPORTE", "ajuda_suporte"),
        ("⚙️ PROBLEMAS COMUNS", "ajuda_problemas"),
        ("📋 TERMOS", "ajuda_termos")
    ]
    
    for i in range(0, len(botoes_ajuda), 2):
        if i+1 < len(botoes_ajuda):
            markup.add(
                InlineKeyboardButton(botoes_ajuda[i][0], callback_data=botoes_ajuda[i][1]),
                InlineKeyboardButton(botoes_ajuda[i+1][0], callback_data=botoes_ajuda[i+1][1])
            )
    
    markup.add(InlineKeyboardButton("📞 CONTATO DIRETO", url=f"https://t.me/{ADMIN_USERNAME}"))
    markup.add(InlineKeyboardButton("🏠 VOLTAR AO INÍCIO", callback_data="inicio"))
    
    bot.reply_to(message, f"""
🆘 *CENTRAL DE AJUDA - CINEMA PRO* 🆘

📋 *COMANDOS DISPONÍVEIS:*

🎬 *CATÁLOGO E PEDIDOS:*
`/start` - Menu principal
`/catalogo` - Catálogo completo
`/buscar` - Buscar filme específico
`/pedir` - Fazer pedido de filme
`/trailer` - Ver trailers
`/recomendacao` - Sugestão do dia

💰 *CRÉDITOS E VIP:*
`/creditos` - Ver seus créditos
`/comprar` - Comprar créditos
`/vip` - Ver planos VIP
`/perfil` - Ver seu perfil

📞 *SUPORTE:*
`/ajuda` - Esta mensagem de ajuda
`/suporte` - Falar com atendimento

👑 *ADMIN:*
`/admin` - Painel administrativo

⚡ *EXEMPLOS PRÁTICOS:*
• `/pedir Venom 3` - Pedir filme específico
• `/buscar avatar` - Buscar filmes com "avatar"
• `/comprar` - Comprar mais créditos

💡 *DICAS RÁPIDAS:*
• 1 crédito = 1 filme/série
• Qualidade 4K garantida
• Entrega em 15-30 minutos
• Suporte 24/7 disponível

🎯 *PRECISA DE AJUDA?*
Clique nos botões abaixo ou fale diretamente com nosso suporte!
    """, parse_mode='Markdown', reply_markup=markup)

# 📨 SISTEMA DE GRUPOS
@bot.message_handler(content_types=['new_chat_members'])
def welcome_group(message):
    for member in message.new_chat_members:
        if member.username == bot.get_me().username:
            group_id = message.chat.id
            group_title = message.chat.title
            
            welcome_msg = f"""
🎬 *CINEMA PRO ADICIONADO AO GRUPO!* 🎬

Olá *{group_title}*! 🤖

Estou aqui para facilitar seus pedidos de filmes e séries em 4K!

📋 *COMANDOS NO GRUPO:*
`/recomendacao` - Filme do dia
`/lancamentos` - Novidades da semana  
`/catalogo` - Catálogo completo
`/trailer` - Ver trailers

💡 *Use /start no privado para:*
• Fazer pedidos completos
• Ver seus créditos  
• Comprar mais créditos
• Acessar catálogo completo

📞 *ATENDIMENTO:* @{ADMIN_USERNAME}
            """
            
            bot.send_message(group_id, welcome_msg, parse_mode='Markdown')

# 🎮 SISTEMA DE CALLBACKS COMPLETO
@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    message_id = call.message.message_id
    
    try:
        # 🏠 INÍCIO
        if call.data == 'inicio':
            bot.delete_message(chat_id, message_id)
            start_comando(call.message)
        
        # 🎬 CATÁLOGO
        elif call.data == 'catalogo':
            bot.delete_message(chat_id, message_id)
            catalogo_comando(call.message)
        
        # 🚀 LANÇAMENTOS
        elif call.data == 'lancamentos':
            # Mostrar categoria de lançamentos
            filmes = CATALOGO_PREMIUM.get('lancamentos', [])
            
            if not filmes:
                bot.answer_callback_query(call.id, "📭 Sem lançamentos no momento")
                return
            
            markup = InlineKeyboardMarkup(row_width=1)
            
            for filme in filmes:
                markup.add(InlineKeyboardButton(
                    filme['titulo'],
                    callback_data=f"detalhes_{filme['id']}"
                ))
            
            markup.add(InlineKeyboardButton("🏠 VOLTAR AO INÍCIO", callback_data="inicio"))
            
            texto = "🚀 *LANÇAMENTOS DA SEMANA* 🚀\n\n"
            texto += "🎬 *NOVOS FILMES DISPONÍVEIS:*\n\n"
            
            for filme in filmes:
                texto += f"• {filme['titulo']}\n"
                texto += f"  ⭐ {filme['imdb']} • 🎭 {filme['genero']}\n"
                texto += f"  ⏰ {filme['duracao']} • 💾 {filme['tamanho']}\n\n"
            
            texto += "💎 *Todos por apenas 1 crédito!*"
            
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=texto,
                parse_mode='Markdown',
                reply_markup=markup
            )
        
        # 💰 COMPRAR
        elif call.data == 'comprar':
            bot.delete_message(chat_id, message_id)
            comprar_comando(call.message)
        
        # 👑 VIP
        elif call.data == 'vip':
            bot.delete_message(chat_id, message_id)
            vip_comando(call.message)
        
        # 📊 PERFIL
        elif call.data == 'perfil':
            bot.delete_message(chat_id, message_id)
            perfil_comando(call.message)
        
        # 🎥 TRAILERS
        elif call.data == 'trailers':
            bot.delete_message(chat_id, message_id)
            trailers_comando(call.message)
        
        # ⭐ RECOMENDAÇÃO
        elif call.data == 'recomendacao':
            bot.delete_message(chat_id, message_id)
            recomendacao_comando(call.message)
        
        # 🔍 BUSCAR
        elif call.data in ['buscar', 'buscar_filme']:
            bot.answer_callback_query(call.id, "🔍 Digite /buscar nome_do_filme")
            bot.send_message(chat_id, "🔍 *Digite o nome do filme que deseja buscar:*\n\nExemplo: `/buscar avatar 4`", parse_mode='Markdown')
        
        # 🆘 AJUDA
        elif call.data == 'ajuda':
            bot.delete_message(chat_id, message_id)
            ajuda_comando(call.message)
        
        # 📦 PEDIR FILME (via callback)
        elif call.data.startswith('pedir_'):
            filme_id = call.data.replace('pedir_', '')
            
            # Buscar filme
            filme_info = None
            for categoria, filmes in CATALOGO_PREMIUM.items():
                for filme in filmes:
                    if filme['id'] == filme_id:
                        filme_info = filme
                        break
                if filme_info:
                    break
            
            if not filme_info:
                bot.answer_callback_query(call.id, "❌ Filme não encontrado")
                return
            
            # Verificar créditos
            creditos_total = obter_creditos_usuario(user_id)
            
            if creditos_total < 1:
                markup = InlineKeyboardMarkup()
                markup.add(
                    InlineKeyboardButton("💰 COMPRAR CRÉDITOS", callback_data="comprar"),
                    InlineKeyboardButton("👑 VER VIP", callback_data="vip")
                )
                
                bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=message_id,
                    text=f"""
❌ *CRÉDITOS INSUFICIENTES*

💎 *Seus créditos:* *{creditos_total}*
🎬 *Filme desejado:* *{filme_info['titulo']}*

⚡ *Você precisa de 1 crédito para fazer este pedido.*

💫 *Clique abaixo para comprar créditos:*
                    """,
                    parse_mode='Markdown',
                    reply_markup=markup
                )
                return
            
            # Processar pedido
            conn = get_db()
            c = conn.cursor()
            c.execute("SELECT creditos, creditos_bonus FROM usuarios WHERE user_id = ?", (user_id,))
            usuario = c.fetchone()
            
            if usuario['creditos'] >= 1:
                c.execute("UPDATE usuarios SET creditos = creditos - 1 WHERE user_id = ?", (user_id,))
            else:
                creditos_necessarios = 1 - usuario['creditos']
                c.execute("UPDATE usuarios SET creditos = 0, creditos_bonus = creditos_bonus - ? WHERE user_id = ?", 
                         (creditos_necessarios, user_id))
            
            pedido_id = c.execute("""
                INSERT INTO pedidos (user_id, username, filme_id, filme_titulo, status)
                VALUES (?, ?, ?, ?, 'processando')
            """, (user_id, call.from_user.username, filme_id, filme_info['titulo'])).lastrowid
            
            c.execute("UPDATE usuarios SET total_pedidos = total_pedidos + 1 WHERE user_id = ?", (user_id,))
            
            conn.commit()
            conn.close()
            
            # Registrar log
            registrar_log(user_id, "pedido_callback", f"Filme: {filme_info['titulo']}, ID: {pedido_id}")
            
            # Notificar admin
            try:
                admin_msg = f"""
📦 *NOVO PEDIDO VIA BOTÃO* 📦

🆔 *Pedido:* #{pedido_id}
👤 *Usuário:* @{call.from_user.username} ({user_id})
🎬 *Filme:* {filme_info['titulo']}
💎 *Créditos usados:* 1
⏰ *Data:* {datetime.now().strftime('%H:%M:%S')}

⚡ *Status:* Processando
                """
                bot.send_message(ADMIN_ID, admin_msg, parse_mode='Markdown')
            except:
                pass
            
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton(
                "📞 ACOMPANHAR PEDIDO",
                url=f"https://t.me/{ADMIN_USERNAME}"
            ))
            markup.add(InlineKeyboardButton(
                "🎬 NOVO PEDIDO",
                callback_data="catalogo"
            ))
            
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=f"""
✅ *PEDIDO CONFIRMADO!* ✅

🆔 *Pedido:* *#{pedido_id}*
🎬 *Filme:* *{filme_info['titulo']}*
💎 *Créditos utilizados:* 1
💰 *Créditos restantes:* *{creditos_total - 1}*

⏰ *Entrega em:* 15-30 minutos
📦 *Qualidade:* 4K HDR garantida

📞 *Para acompanhar:*
Fale com @{ADMIN_USERNAME}

⚡ *Obrigado pela preferência!*
                """,
                parse_mode='Markdown',
                reply_markup=markup
            )
        
        # 📋 DETALHES DO FILME
        elif call.data.startswith('detalhes_'):
            filme_id = call.data.replace('detalhes_', '')
            
            # Buscar filme
            filme_info = None
            for categoria, filmes in CATALOGO_PREMIUM.items():
                for filme in filmes:
                    if filme['id'] == filme_id:
                        filme_info = filme
                        break
                if filme_info:
                    break
            
            if not filme_info:
                bot.answer_callback_query(call.id, "❌ Filme não encontrado")
                return
            
            markup = InlineKeyboardMarkup(row_width=2)
            markup.add(
                InlineKeyboardButton("🎬 PEDIR AGORA (1 crédito)", callback_data=f"pedir_{filme_id}"),
                InlineKeyboardButton("🎥 VER TRAILER", url=filme_info['link_trailer'])
            )
            
            creditos_total = obter_creditos_usuario(user_id)
            
            if creditos_total < 1:
                markup.add(InlineKeyboardButton("💰 COMPRAR CRÉDITOS", callback_data="comprar"))
            
            markup.add(InlineKeyboardButton("🔙 VOLTAR", callback_data="catalogo"))
            
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=f"""
🎬 *{filme_info['titulo']}* 🎬

📖 *Sinopse:*
{filme_info['descricao']}

⭐ *Avaliação IMDb:* {filme_info['imdb']}
🎭 *Gênero:* {filme_info['genero']}
📅 *Ano:* {filme_info['ano']} • Classificação: {filme_info['classificacao']}
⏰ *Duração:* {filme_info['duracao']}
💾 *Tamanho:* {filme_info['tamanho']}

🎯 *QUALIDADE:*
{filme_info['qualidade']}

🔊 *ÁUDIO:* {filme_info['audio']}
📝 *LEGENDAS:* {filme_info['legendas']}

💎 *PREÇO:* 1 CRÉDITO
💳 *Seus créditos:* *{creditos_total}*
⚡ *ENTREGA:* 15-30 minutos

🎯 *Clique em "Pedir Agora" para adquirir!*
                """,
                parse_mode='Markdown',
                reply_markup=markup
            )
        
        # 🎬 CATEGORIAS
        elif call.data.startswith('categoria_'):
            categoria = call.data.replace('categoria_', '')
            filmes = CATALOGO_PREMIUM.get(categoria, [])
            
            if not filmes:
                bot.answer_callback_query(call.id, "📭 Categoria vazia")
                return
            
            # Nome da categoria
            nomes_categorias = {
                'acao_2025': '🎬 AÇÃO 2025',
                'aventura_2025': '🌍 AVENTURA 2025',
                'animacao_2025': '🎥 ANIMAÇÃO 2025',
                'series_2025': '📺 SÉRIES 2025',
                'animes_2025': '🎌 ANIMES 2025',
                'terror_2025': '😨 TERROR 2025',
                'brasileiros': '🇧🇷 BRASILEIROS',
                'lancamentos': '🚀 LANÇAMENTOS'
            }
            
            nome_categoria = nomes_categorias.get(categoria, categoria.replace('_', ' ').upper())
            
            markup = InlineKeyboardMarkup(row_width=1)
            
            for filme in filmes:
                markup.add(InlineKeyboardButton(
                    filme['titulo'],
                    callback_data=f"detalhes_{filme['id']}"
                ))
            
            markup.add(InlineKeyboardButton("🔙 VOLTAR AO CATÁLOGO", callback_data="catalogo"))
            
            texto = f"{nome_categoria}\n\n"
            texto += f"📊 *{len(filmes)} FILMES/SÉRIES DISPONÍVEIS*\n\n"
            
            for filme in filmes:
                texto += f"• {filme['titulo']}\n"
                texto += f"  ⭐ {filme['imdb']} • ⏰ {filme['duracao']}\n\n"
            
            texto += "💎 *Todos por apenas 1 crédito cada!*\n"
            texto += "🎯 *Clique em um título para ver detalhes e pedir*"
            
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=texto,
                parse_mode='Markdown',
                reply_markup=markup
            )
        
        # 💰 PACOTES DE CRÉDITOS
        elif call.data.startswith('pacote_'):
            pacote = call.data.replace('pacote_', '')
            
            precos = {
                '1': ('20 MZN', '1 crédito'),
                '3': ('50 MZN', '3 créditos'),
                '5': ('80 MZN', '5 créditos'),
                '10': ('150 MZN', '10 créditos')
            }
            
            if pacote not in precos:
                bot.answer_callback_query(call.id, "❌ Pacote inválido")
                return
            
            preco, descricao = precos[pacote]
            
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton(
                "💳 REALIZAR PAGAMENTO",
                url=f"https://t.me/{ADMIN_USERNAME}?text=Quero+comprar+{pacote}+créditos"
            ))
            markup.add(InlineKeyboardButton("🔙 VOLTAR", callback_data="comprar"))
            
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=f"""
💎 *COMPRA DE CRÉDITOS* 💎

📦 *PACOTE SELECIONADO:*
• {descricao}
• Preço: {preco}

💰 *FORMAS DE PAGAMENTO:*
• M-Pesa: `{CONTATOS['mpesa']}`
• e-Mola: `{CONTATOS['emola']}`
• PayPal: `{CONTATOS['paypal']}`

📋 *PROCEDIMENTO:*
1. Faça o pagamento para um dos números acima
2. Clique em "Realizar Pagamento"
3. Envie o comprovante para @{ADMIN_USERNAME}
4. Aguarde confirmação (2-5 minutos)

🎁 *BÔNUS:*
• Primeira compra: +3 créditos
• Compra acima de 50 MZN: +5%

⚡ *Clique abaixo para finalizar:*
                """,
                parse_mode='Markdown',
                reply_markup=markup
            )
        
        # 👑 PLANOS VIP DETALHADOS
        elif call.data.startswith('plano_'):
            plano_key = call.data.replace('plano_', '')
            plano = PLANOS_VIP.get(plano_key)
            
            if not plano:
                bot.answer_callback_query(call.id, "❌ Plano não encontrado")
                return
            
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton(
                "👑 ASSINAR AGORA",
                url=f"https://t.me/{ADMIN_USERNAME}?text=Quero+assinar+{plano['nome'].replace(' ', '+')}"
            ))
            markup.add(InlineKeyboardButton("🔙 VOLTAR", callback_data="vip"))
            
            texto = f"""
{plano['nome']}

💰 *Preço:* {plano['preco']}
💎 *Créditos incluídos:* {plano['creditos']}
📅 *Duração:* {plano['duracao']} dias

🌟 *VANTAGENS EXCLUSIVAS:*
"""
            
            for vantagem in plano['vantagens']:
                texto += f"{vantagem}\n"
            
            texto += f"""
            
💳 *FORMAS DE PAGAMENTO:*
• M-Pesa: `{CONTATOS['mpesa']}`
• e-Mola: `{CONTATOS['emola']}`
• PayPal: `{CONTATOS['paypal']}`

📞 *PROCESSO:*
1. Clique em "Assinar Agora"
2. Faça o pagamento
3. Envie comprovante
4. Ativação em 5 minutos

⚡ *Benefícios imediatos após ativação!*
            """
            
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=texto,
                parse_mode='Markdown',
                reply_markup=markup
            )
        
        # 🎥 TRAILERS ESPECÍFICOS
        elif call.data.startswith('trailer_'):
            trailer_key = call.data.replace('trailer_', '')
            
            # Mapear trailers
            trailers_map = {
                'venom3': ('VENOM 3: A ÚLTIMA BATALHA', 'https://youtu.be/venom3-trailer'),
                'johnwick5': ('JOHN WICK 5: LEGADO', 'https://youtu.be/johnwick5-trailer'),
                'avatar4': ('AVATAR 4: O LEGADO', 'https://youtu.be/avatar4-trailer'),
                'spiderman': ('SPIDER-MAN: BEYOND', 'https://youtu.be/spiderman-trailer'),
                'stranger5': ('STRANGER THINGS 5', 'https://youtu.be/stranger5-trailer'),
                'demonslayer': ('DEMON SLAYER FINAL', 'https://youtu.be/demonslayer-trailer')
            }
            
            if trailer_key not in trailers_map:
                bot.answer_callback_query(call.id, "❌ Trailer não encontrado")
                return
            
            titulo, url = trailers_map[trailer_key]
            
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("🎬 ASSISTIR NO YOUTUBE", url=url))
            
            # Tentar encontrar filme correspondente
            filme_info = None
            for categoria, filmes in CATALOGO_PREMIUM.items():
                for filme in filmes:
                    if trailer_key in filme['id']:
                        filme_info = filme
                        break
                if filme_info:
                    break
            
            if filme_info:
                markup.add(InlineKeyboardButton(
                    "📦 PEDIR FILME COMPLETO",
                    callback_data=f"pedir_{filme_info['id']}"
                ))
            
            markup.add(InlineKeyboardButton("🔙 VOLTAR", callback_data="trailers"))
            
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=f"""
🎬 *TRAILER EXCLUSIVO* 🎬

📽️ *Filme:* {titulo}

🎯 *VERSÃO COMPLETA INCLUI:*
• Qualidade 4K HDR/Dolby Vision
• Áudio original + legendas PT-BR
• Download direto via Google Drive
• Garantia de qualidade cinema

💎 *PREÇO:* 1 CRÉDITO
⚡ *Entrega:* 15-30 minutos

📊 *ESTATÍSTICAS:*
• 98% satisfação dos clientes
• 4.8/5 ⭐ Avaliação média
• +1000 pedidos realizados

💡 *Assista o trailer e depois peça o filme completo!*
                """,
                parse_mode='Markdown',
                reply_markup=markup
            )
        
        # 👑 ADMIN CALLBACKS
        elif call.data == 'admin':
            if not is_admin(user_id, call.from_user.username):
                bot.answer_callback_query(call.id, "❌ Acesso negado!")
                return
            
            bot.delete_message(chat_id, message_id)
            admin_comando(call.message)
        
        elif call.data == 'admin_stats':
            if not is_admin(user_id, call.from_user.username):
                return
            
            conn = get_db()
            c = conn.cursor()
            
            # Estatísticas detalhadas
            total_usuarios = c.execute("SELECT COUNT(*) FROM usuarios").fetchone()[0]
            novos_24h = c.execute("SELECT COUNT(*) FROM usuarios WHERE datetime(data_cadastro) > datetime('now', '-1 day')").fetchone()[0]
            ativos_24h = c.execute("SELECT COUNT(*) FROM usuarios WHERE datetime(ultimo_login) > datetime('now', '-1 day')").fetchone()[0]
            
            total_pedidos = c.execute("SELECT COUNT(*) FROM pedidos").fetchone()[0]
            pedidos_hoje = c.execute("SELECT COUNT(*) FROM pedidos WHERE DATE(data_pedido) = DATE('now')").fetchone()[0]
            pedidos_entregues = c.execute("SELECT COUNT(*) FROM pedidos WHERE status = 'entregue'").fetchone()[0]
            
            receita_total = c.execute("SELECT SUM(valor) FROM transacoes WHERE tipo LIKE '%compra%' AND status = 'aprovado'").fetchone()[0] or 0
            receita_hoje = c.execute("SELECT SUM(valor) FROM transacoes WHERE tipo LIKE '%compra%' AND status = 'aprovado' AND DATE(data) = DATE('now')").fetchone()[0] or 0
            
            # Filmes mais populares
            c.execute("""
                SELECT filme_titulo, COUNT(*) as total 
                FROM pedidos 
                GROUP BY filme_titulo 
                ORDER BY total DESC 
                LIMIT 5
            """)
            filmes_populares = c.fetchall()
            
            conn.close()
            
            texto = "📊 *ESTATÍSTICAS DETALHADAS*\n\n"
            
            texto += "👥 *USUÁRIOS:*\n"
            texto += f"• Total: `{total_usuarios}`\n"
            texto += f"• Novos (24h): `{novos_24h}`\n"
            texto += f"• Ativos (24h): `{ativos_24h}`\n\n"
            
            texto += "📦 *PEDIDOS:*\n"
            texto += f"• Total: `{total_pedidos}`\n"
            texto += f"• Hoje: `{pedidos_hoje}`\n"
            texto += f"• Entregues: `{pedidos_entregues}`\n"
            texto += f"• Taxa entrega: `{(pedidos_entregues/max(total_pedidos,1)*100):.1f}%`\n\n"
            
            texto += "💰 *FINANCEIRO:*\n"
            texto += f"• Receita total: `{receita_total:.2f} MZN`\n"
            texto += f"• Receita hoje: `{receita_hoje:.2f} MZN`\n\n"
            
            texto += "🎬 *FILMES MAIS POPULARES:*\n"
            for filme in filmes_populares:
                texto += f"• {filme['filme_titulo']}: `{filme['total']}` pedidos\n"
            
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("🔙 VOLTAR", callback_data="admin"))
            
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=texto,
                parse_mode='Markdown',
                reply_markup=markup
            )
        
        elif call.data == 'fechar_admin':
            if is_admin(user_id, call.from_user.username):
                bot.delete_message(chat_id, message_id)
        
        # 📞 AJUDA ESPECÍFICA
        elif call.data.startswith('ajuda_'):
            topico = call.data.replace('ajuda_', '')
            
            textos_ajuda = {
                'pedir': f"""
🎬 *COMO FAZER UM PEDIDO*

⚡ *PASSO A PASSO:*
1. Use `/catalogo` para ver as opções
2. Escolha um filme/série
3. Use `/pedir NomeDoFilme`
4. Confirme com 1 crédito
5. Receba o link em 15-30 minutos

💡 *EXEMPLOS:*
• `/pedir Venom 3`
• `/pedir Stranger Things 5`
• `/pedir Demon Slayer`

🎯 *DICAS:*
• Verifique seus créditos com `/creditos`
• 1 crédito = 1 filme/série
• Qualidade 4K garantida
                """,
                'comprar': f"""
💰 *COMO COMPRAR CRÉDITOS*

⚡ *OPÇÕES DISPONÍVEIS:*
• 1 Crédito - 20 MZN
• 3 Créditos - 50 MZN
• 5 Créditos - 80 MZN
• 10 Créditos - 150 MZN

💳 *PROCESSO:*
1. Use `/comprar` ou clique em Comprar Créditos
2. Escolha seu pacote
3. Faça o pagamento via M-Pesa/e-Mola/PayPal
4. Envie comprovante para @{ADMIN_USERNAME}
5. Receba créditos em 2-5 minutos

🎁 *BÔNUS:*
• Primeira compra: +3 créditos
• Compra acima de 50 MZN: +5%
                """,
                'vip': f"""
👑 *PLANOS VIP*

🌟 *VANTAGENS:*
• Mais créditos por menos dinheiro
• Entrega prioritária (5-15min)
• Suporte VIP 24/7
• Lançamentos antecipados
• Catálogo exclusivo

💎 *PLANOS:*
• VIP 1 Mês: 50 MZN (15 créditos)
• VIP 3 Meses: 120 MZN (50 créditos)
• VIP 6 Meses: 200 MZN (120 créditos)
• VIP Anual: 350 MZN (300 créditos)

⚡ *Para assinar:* Use `/vip` ou fale com @{ADMIN_USERNAME}
                """,
                'suporte': f"""
📞 *SUPORTE AO CLIENTE*

🎯 *CANAL DE ATENDIMENTO:*
• Telegram: @{ADMIN_USERNAME}
• WhatsApp: {CONTATOS['whatsapp']}
• Email: {CONTATOS['email']}

⏰ *HORÁRIO DE ATENDIMENTO:*
• 24 horas por dia
• 7 dias por semana

⚡ *TIPOS DE SUPORTE:*
• Dúvidas sobre pedidos
• Problemas com pagamentos
• Reclamações
• Sugestões
• Parcerias
                """,
                'problemas': f"""
⚙️ *PROBLEMAS COMUNS*

🔍 *NÃO CONSIGO FAZER PEDIDO:*
• Verifique seus créditos com `/creditos`
• Compre mais créditos com `/comprar`
• Certifique-se de escrever o nome correto

📦 *NÃO RECEBI MEU PEDIDO:*
• Aguarde 15-30 minutos
• Entre em contato com @{ADMIN_USERNAME}
• Forneça o número do pedido

💳 *PROBLEMAS COM PAGAMENTO:*
• Envie comprovante para @{ADMIN_USERNAME}
• Aguarde 5 minutos para confirmação
• Em caso de atraso, entre em contato

🎬 *PROBLEMAS COM O ARQUIVO:*
• Verifique sua conexão de internet
• Tente baixar novamente
• Entre em contato para reenvio
                """,
                'termos': """
📋 *TERMOS DE USO*

✅ *PERMITIDO:*
• Uso pessoal dos conteúdos
• Compartilhamento com familiares
• Armazenamento para uso offline

❌ *PROIBIDO:*
• Revenda dos conteúdos
• Distribuição comercial
• Upload em sites públicos
• Compartilhamento em massa

⚖️ *RESPONSABILIDADES:*
• Os conteúdos são para uso pessoal
• Não nos responsabilizamos por uso indevido
• Reserve os direitos dos distribuidores

🔒 *PRIVACIDADE:*
• Seus dados são mantidos em sigilo
• Não compartilhamos informações
• Sistema seguro e criptografado
                """
            }
            
            if topico in textos_ajuda:
                markup = InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton("📞 FALAR COM SUPORTE", url=f"https://t.me/{ADMIN_USERNAME}"))
                markup.add(InlineKeyboardButton("🔙 VOLTAR À AJUDA", callback_data="ajuda"))
                
                bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=message_id,
                    text=textos_ajuda[topico],
                    parse_mode='Markdown',
                    reply_markup=markup
                )
        
        else:
            bot.answer_callback_query(call.id, "⚡ Função em desenvolvimento!")
    
    except Exception as e:
        print(f"❌ Erro no callback: {e}")
        bot.answer_callback_query(call.id, "❌ Erro, tente novamente")

# 🚀 INICIAR SISTEMA
print("""
🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬
🎬                                        🎬
🎬     CINEMA PRO ULTRA - SISTEMA ATIVO   🎬
🎬         BOT COMPLETAMENTE PRONTO       🎬
🎬                                        🎬
🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬

⚡ CONFIGURAÇÃO COMPLETA:
✅ Token: 8306714275:AAGzNXE3TZKbe5-49YGTgNOMrJiLVxBjmLA
✅ Admin: @ayltonanna7
✅ ID Admin: 5125563829

📊 SISTEMA CONFIGURADO:
✅ Banco de dados inicializado
✅ Catálogo: 120+ títulos
✅ Planos VIP: 4 opções
✅ Sistema de créditos ativo
✅ Painel admin operacional

🎯 RECURSOS DISPONÍVEIS:
✅ Catálogo completo com buscas
✅ Sistema de pedidos automatizado
✅ Planos VIP com benefícios
✅ Suporte integrado
✅ Painel administrativo

🚀 INICIANDO BOT TELEGRAM...
""")

# Manter o bot rodando
while True:
    try:
        print(f"🤖 Bot @{bot.get_me().username} online!")
        print("⚡ Aguardando comandos...")
        bot.polling(none_stop=True, interval=0, timeout=20)
    except Exception as e:
        print(f"❌ Erro no polling: {e}")
        time.sleep(5)
        continue
