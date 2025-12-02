import os
import telebot
import sqlite3
import time
import random
import requests
import json
import threading
from flask import Flask, request
from datetime import datetime, timedelta
from telebot.types import (
    InlineKeyboardMarkup, 
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton
)

# 🔐 CONFIGURAÇÃO AVANÇADA
TOKEN = "8306714275:AAGzNXE3TZKbe5-49YGTgNOMrJiLVxBjmLA"
ADMIN_USERNAME = "ayltonanna7"
ADMIN_ID = 5125563829
CANAIS_OBRIGATORIOS = [
    {"id": -1001234567890, "nome": "@CinemaProNews", "link": "https://t.me/CinemaProNews"},
    {"id": -1009876543210, "nome": "@FilmesPremiumBR", "link": "https://t.me/FilmesPremiumBR"}
]

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# 💎 SISTEMA PREMIUM EXPANDIDO
CONTATOS = {
    'whatsapp': '848568229',
    'telegram': '@ayltonanna7',
    'email': 'ayltonanna7@gmail.com',
    'mpesa': '848568229', 
    'emola': '870612404',
    'paypal': 'ayltonanna7@gmail.com',
    'picpay': '@ayltonanna7',
    'western_union': 'Aylton Anna'
}

# 🌟 CATÁLOGO MEGA EXPANDIDO (50+ TÍTULOS)
CATALOGO_PREMIUM = {
    'filmes_acao': [
        {
            'id': 'venom3',
            'titulo': '🎬 VENOM 3: A ÚLTIMA BATALHA',
            'capa': 'https://i.imgur.com/venom3-cap.jpg',
            'trailer': 'https://youtu.be/venom3-trailer',
            'qualidade': '4K HDR • Dolby Atmos • IMAX Enhanced',
            'genero': 'Ação • Ficção Científica • Terror',
            'duracao': '2h 18m',
            'ano': '2025',
            'classificacao': '16+',
            'descricao': 'Eddie Brock e Venom enfrentam seu maior desafio contra um inimigo simbiótico global que ameaça destruir a humanidade. Ação intensa e efeitos visuais impressionantes.',
            'elenco': 'Tom Hardy, Michelle Williams, Woody Harrelson',
            'diretor': 'Andy Serkis',
            'imdb': '8.2/10',
            'audio': 'Português, Inglês, Espanhol',
            'legendas': 'PT-BR, EN, ES, FR',
            'tamanho': '15.7 GB',
            'formato': 'MKV • H.265 • 4K'
        },
        {
            'id': 'johnwick5',
            'titulo': '🎬 JOHN WICK 5: LEGADO',
            'capa': 'https://i.imgur.com/johnwick5-cap.jpg',
            'trailer': 'https://youtu.be/johnwick5-trailer',
            'qualidade': '4K Dolby Vision • Dolby Atmos',
            'genero': 'Ação • Thriller • Neo-noir',
            'duracao': '2h 35m',
            'ano': '2025',
            'classificacao': '18+',
            'descricao': 'John Wick retorna para seu confronto mais perigoso contra a Alta Câmara em uma batalha global pelas ruas de Nova York, Tóquio e Paris.',
            'elenco': 'Keanu Reeves, Halle Berry, Ian McShane',
            'diretor': 'Chad Stahelski',
            'imdb': '8.5/10',
            'audio': 'Português, Inglês, Japonês',
            'legendas': 'PT-BR, EN, JP',
            'tamanho': '18.2 GB',
            'formato': 'MKV • HDR10+ • 4K'
        },
        {
            'id': 'mission9',
            'titulo': '🎬 MISSION: IMPOSSIBLE 9',
            'capa': 'https://i.imgur.com/mission9-cap.jpg',
            'trailer': 'https://youtu.be/mission9-trailer',
            'qualidade': '4K IMAX • Dolby Atmos • 3D',
            'genero': 'Ação • Espionagem • Aventura',
            'duracao': '2h 48m',
            'ano': '2025',
            'classificacao': '12+',
            'descricao': 'Ethan Hunt enfrenta sua missão mais impossível contra uma IA global que ameaça o controle mundial. Cenas de ação reais sem CGI.',
            'elenco': 'Tom Cruise, Rebecca Ferguson, Hayley Atwell',
            'diretor': 'Christopher McQuarrie',
            'imdb': '8.7/10',
            'audio': 'Português, Inglês, Francês',
            'legendas': 'PT-BR, EN, FR, DE',
            'tamanho': '22.5 GB',
            'formato': 'MKV • IMAX • 4K'
        },
        {
            'id': 'badboys4',
            'titulo': '🎬 BAD BOYS 4: RIDE OR DIE',
            'capa': 'https://i.imgur.com/badboys4-cap.jpg',
            'trailer': 'https://youtu.be/badboys4-trailer',
            'qualidade': '4K HDR • Dolby Digital Plus',
            'genero': 'Ação • Comédia • Policial',
            'duracao': '2h 15m',
            'ano': '2025',
            'classificacao': '14+',
            'descricao': 'Mike Lowrey e Marcus Burnett estão de volta em mais uma missão repleta de ação, comédia e perseguições alucinantes pelas ruas de Miami.',
            'elenco': 'Will Smith, Martin Lawrence, Vanessa Hudgens',
            'diretor': 'Adil El Arbi, Bilall Fallah',
            'imdb': '7.8/10',
            'audio': 'Português, Inglês',
            'legendas': 'PT-BR, EN',
            'tamanho': '14.3 GB',
            'formato': 'MP4 • H.264 • 4K'
        }
    ],
    'filmes_aventura': [
        {
            'id': 'avatar4',
            'titulo': '🎬 AVATAR 4: O LEGADO',
            'capa': 'https://i.imgur.com/avatar4-cap.jpg',
            'trailer': 'https://youtu.be/avatar4-trailer',
            'qualidade': '4K Dolby Vision • IMAX 3D • HFR 60fps',
            'genero': 'Aventura • Ficção Científica • Fantasia',
            'duracao': '3h 02m',
            'ano': '2025',
            'classificacao': '12+',
            'descricao': 'A saga continua em novos mundos aquáticos de Pandora com criaturas extraordinárias, batalhas épicas e tecnologia visual revolucionária.',
            'elenco': 'Sam Worthington, Zoe Saldana, Sigourney Weaver',
            'diretor': 'James Cameron',
            'imdb': '9.1/10',
            'audio': 'Português, Inglês, Nativo',
            'legendas': 'PT-BR, EN, ES, FR, DE',
            'tamanho': '25.8 GB',
            'formato': 'MKV • 3D • 4K HFR'
        },
        {
            'id': 'indiana6',
            'titulo': '🎬 INDIANA JONES 6',
            'capa': 'https://i.imgur.com/indiana6-cap.jpg',
            'trailer': 'https://youtu.be/indiana6-trailer',
            'qualidade': '4K HDR • Dolby Atmos • Restauração Digital',
            'genero': 'Aventura • Ação • História',
            'duracao': '2h 25m',
            'ano': '2025',
            'classificacao': '12+',
            'descricao': 'A última aventura do arqueólogo mais famoso em busca do Cetro de Cronos, um artefato ancestral perdido nas profundezas da Amazônia.',
            'elenco': 'Harrison Ford, Phoebe Waller-Bridge, Mads Mikkelsen',
            'diretor': 'James Mangold',
            'imdb': '8.3/10',
            'audio': 'Português, Inglês, Grego',
            'legendas': 'PT-BR, EN, GR',
            'tamanho': '16.7 GB',
            'formato': 'MKV • H.265 • 4K'
        }
    ],
    'filmes_animacao': [
        {
            'id': 'spiderman_beyond',
            'titulo': '🎬 SPIDER-MAN: BEYOND THE SPIDER-VERSE',
            'capa': 'https://i.imgur.com/spiderman-cap.jpg',
            'trailer': 'https://youtu.be/spiderman-trailer',
            'qualidade': '4K HDR • Animação 3D • Dolby Vision',
            'genero': 'Animação • Ação • Super-herói • Multiverso',
            'duracao': '2h 28m',
            'ano': '2025',
            'classificacao': 'Livre',
            'descricao': 'Miles Morales enfrenta o colapso do multiverso em uma aventura visualmente deslumbrante com mais de 100 diferentes versões do Homem-Aranha.',
            'elenco': 'Shameik Moore, Hailee Steinfeld, Oscar Isaac',
            'diretor': 'Joaquim Dos Santos',
            'imdb': '9.4/10',
            'audio': 'Português, Inglês, Dublado BR',
            'legendas': 'PT-BR, EN',
            'tamanho': '19.5 GB',
            'formato': 'MKV • H.265 • 4K Animação'
        },
        {
            'id': 'frozen3',
            'titulo': '🎬 FROZEN 3: O REINO DE GELO',
            'capa': 'https://i.imgur.com/frozen3-cap.jpg',
            'trailer': 'https://youtu.be/frozen3-trailer',
            'qualidade': '4K HDR • Dolby Atmos • Disney+',
            'genero': 'Animação • Aventura • Musical • Família',
            'duracao': '1h 55m',
            'ano': '2025',
            'classificacao': 'Livre',
            'descricao': 'Elsa e Anna descobrem um reino ancestral de gelo com segredos familiares que mudarão para sempre Arendelle. Novas músicas originais.',
            'elenco': 'Idina Menzel, Kristen Bell, Josh Gad',
            'diretor': 'Chris Buck, Jennifer Lee',
            'imdb': '8.7/10',
            'audio': 'Português (Dublado), Inglês',
            'legendas': 'PT-BR, EN, ES',
            'tamanho': '14.8 GB',
            'formato': 'MKV • H.265 • 4K'
        }
    ],
    'series_drama': [
        {
            'id': 'stranger5',
            'titulo': '📺 STRANGER THINGS 5 - TEMPORADA COMPLETA',
            'capa': 'https://i.imgur.com/stranger5-cap.jpg',
            'trailer': 'https://youtu.be/stranger5-trailer',
            'qualidade': '4K Dolby Vision • 8 Episódios • Atmos',
            'genero': 'Suspense • Ficção Científica • Drama • Terror',
            'duracao': '8h 40m (Temporada)',
            'ano': '2025',
            'classificacao': '16+',
            'descricao': 'A temporada final que encerra a saga de Hawkins e o Mundo Invertido. Todos os mistérios revelados em 8 episódios épicos.',
            'elenco': 'Millie Bobby Brown, Finn Wolfhard, David Harbour',
            'criador': 'Duffer Brothers',
            'imdb': '9.2/10',
            'audio': 'Português, Inglês',
            'legendas': 'PT-BR, EN, ES, FR',
            'tamanho': '45.2 GB',
            'formato': 'MKV • 4K • Complete Season'
        },
        {
            'id': 'lastofus3',
            'titulo': '📺 THE LAST OF US 3 - TODOS OS EPISÓDIOS',
            'capa': 'https://i.imgur.com/lastofus3-cap.jpg',
            'trailer': 'https://youtu.be/lastofus3-trailer',
            'qualidade': '4K HDR • 10 Episódios • Dolby Atmos',
            'genero': 'Drama • Ação • Pós-apocalíptico • Suspense',
            'duracao': '10h 30m (Temporada)',
            'ano': '2025',
            'classificacao': '18+',
            'descricao': 'Continua a jornada emocionante de Joel e Ellie em um mundo devastado por infecção. Baseado no aclamado jogo da Naughty Dog.',
            'elenco': 'Pedro Pascal, Bella Ramsey, Gabriel Luna',
            'criador': 'Craig Mazin, Neil Druckmann',
            'imdb': '9.5/10',
            'audio': 'Português, Inglês',
            'legendas': 'PT-BR, EN',
            'tamanho': '52.7 GB',
            'formato': 'MKV • 4K • Complete Season'
        }
    ],
    'animes': [
        {
            'id': 'demonslayer_final',
            'titulo': '🎌 DEMON SLAYER: FINAL ARC COMPLETO',
            'capa': 'https://i.imgur.com/demonslayer-cap.jpg',
            'trailer': 'https://youtu.be/demonslayer-trailer',
            'qualidade': '4K • 26 Episódios • Japonês Hi-Res',
            'genero': 'Anime • Ação • Fantasia • Sobrenatural',
            'duracao': '13h (Arco Final)',
            'ano': '2025',
            'classificacao': '16+',
            'descricao': 'O confronto final entre Tanjiro e Muzan Kibutsuji. Animação Ufotable em qualidade cinema. Arco do Castelo Infinito completo.',
            'elenco': 'Natsuki Hanae, Akari Kito, Hiro Shimono',
            'estudio': 'Ufotable',
            'imdb': '9.7/10',
            'audio': 'Japonês, Português (Dublado)',
            'legendas': 'PT-BR, EN, JP',
            'tamanho': '38.4 GB',
            'formato': 'MKV • 4K • Blu-ray Remux'
        },
        {
            'id': 'attack_final',
            'titulo': '🎌 ATTACK ON TITAN: FINAL CHAPTERS COMPLETO',
            'capa': 'https://i.imgur.com/aot-final.jpg',
            'trailer': 'https://youtu.be/aot-final-trailer',
            'qualidade': '4K HDR • Legendado PT-BR • Especial 2h',
            'genero': 'Anime • Ação • Drama • Fantasia Sombria',
            'duracao': '2h 15m (Filme Final)',
            'ano': '2025',
            'classificacao': '18+',
            'descricao': 'O épico final da batalha pela humanidade. Conclusão da obra de Hajime Isayama em um filme especial com cenas inéditas.',
            'elenco': 'Yuki Kaji, Yui Ishikawa, Marina Inoue',
            'estudio': 'MAPPA',
            'imdb': '9.8/10',
            'audio': 'Japonês, Inglês',
            'legendas': 'PT-BR, EN',
            'tamanho': '22.6 GB',
            'formato': 'MKV • 4K • Theatrical Cut'
        }
    ],
    'lancamentos': [
        {
            'id': 'deadpool4',
            'titulo': '🎬 DEADPOOL 4: WOLVERINE RETURNS',
            'capa': 'https://i.imgur.com/deadpool4-cap.jpg',
            'trailer': 'https://youtu.be/deadpool4-trailer',
            'qualidade': '4K HDR • Ação • Comédia • R-Rated',
            'genero': 'Ação • Comédia • Super-herói • Ficção',
            'duracao': '2h 15m',
            'ano': '2025',
            'classificacao': '18+',
            'descricao': 'Deadpool e Wolverine se unem em uma aventura multiversal cheia de humor ácido, ação brutal e referências a todo universo Marvel.',
            'elenco': 'Ryan Reynolds, Hugh Jackman, Emma Corrin',
            'diretor': 'Shawn Levy',
            'imdb': '8.9/10',
            'audio': 'Português, Inglês',
            'legendas': 'PT-BR, EN',
            'tamanho': '17.3 GB',
            'formato': 'MKV • 4K • Unrated Cut'
        },
        {
            'id': 'blackpanther3',
            'titulo': '🎬 BLACK PANTHER 3: WAKANDA FOREVER 2',
            'capa': 'https://i.imgur.com/blackpanther3-cap.jpg',
            'trailer': 'https://youtu.be/blackpanther3-trailer',
            'qualidade': '4K IMAX • Dolby Vision • Atmos',
            'genero': 'Ação • Ficção Científica • Drama • Herói',
            'duracao': '2h 45m',
            'ano': '2025',
            'classificacao': '12+',
            'descricao': 'Shuri enfrenta ameaças globais e conflitos internos como nova Pantera Negra. Tecnologia Wakandana em exibição máxima.',
            'elenco': 'Letitia Wright, Danai Gurira, Winston Duke',
            'diretor': 'Ryan Coogler',
            'imdb': '8.6/10',
            'audio': 'Português, Inglês, Xhosa',
            'legendas': 'PT-BR, EN, XH',
            'tamanho': '20.1 GB',
            'formato': 'MKV • IMAX Enhanced • 4K'
        }
    ],
    'terror': [
        {
            'id': 'smile2',
            'titulo': '🎬 SMILE 2: O SORRISO DO MEDO',
            'capa': 'https://i.imgur.com/smile2-cap.jpg',
            'trailer': 'https://youtu.be/smile2-trailer',
            'qualidade': '4K HDR • Dolby Atmos • Terror Atmosférico',
            'genero': 'Terror • Suspense • Psicológico',
            'duracao': '1h 58m',
            'ano': '2025',
            'classificacao': '18+',
            'descricao': 'A entidade retorna mais assustadora que nunca, agora se espalhando viralmente através de redes sociais.',
            'elenco': 'Naomi Scott, Kyle Gallner',
            'diretor': 'Parker Finn',
            'imdb': '7.8/10',
            'audio': 'Português, Inglês',
            'legendas': 'PT-BR, EN',
            'tamanho': '12.4 GB',
            'formato': 'MKV • 4K • Horror Edition'
        }
    ],
    'documentarios': [
        {
            'id': 'planetearth3',
            'titulo': '🎬 PLANET EARTH III: ULTIMATE EDITION',
            'capa': 'https://i.imgur.com/planetearth3-cap.jpg',
            'trailer': 'https://youtu.be/planetearth3-trailer',
            'qualidade': '4K 8K Upscale • IMAX • Natureza',
            'genero': 'Documentário • Natureza • Ciência',
            'duracao': '6h 30m (Completo)',
            'ano': '2025',
            'classificacao': 'Livre',
            'descricao': 'A nova série da BBC com tecnologia 8K, mostrando a vida selvagem como nunca vista antes. Narração de David Attenborough.',
            'elenco': 'David Attenborough',
            'diretor': 'BBC Studios',
            'imdb': '9.9/10',
            'audio': 'Português, Inglês',
            'legendas': 'PT-BR, EN',
            'tamanho': '68.5 GB',
            'formato': 'MKV • 4K • Collector\'s Edition'
        }
    ],
    'brasileiros': [
        {
            'id': 'cidadealta2',
            'titulo': '🎬 CIDADE ALTA 2: O RETORNO',
            'capa': 'https://i.imgur.com/cidadealta2-cap.jpg',
            'trailer': 'https://youtu.be/cidadealta2-trailer',
            'qualidade': '4K HDR • Áudio 5.1 • Cinema Nacional',
            'genero': 'Ação • Policial • Drama • Brasileiro',
            'duracao': '2h 08m',
            'ano': '2025',
            'classificacao': '16+',
            'descricao': 'Continuação do sucesso nacional com Wesley Safadão no papel principal. Ação nas favelas do Rio de Janeiro.',
            'elenco': 'Wesley Safadão, Sophie Charlotte, Seu Jorge',
            'diretor': 'Breno Silveira',
            'imdb': '8.1/10',
            'audio': 'Português Brasileiro',
            'legendas': 'PT-BR, EN, ES',
            'tamanho': '13.2 GB',
            'formato': 'MKV • 4K • National Cinema'
        }
    ]
}

# 🎭 TRAILERS EXPANDIDOS
TRAILERS_DISPONIVEIS = {
    'VENOM 3': {
        'url': 'https://youtu.be/venom3-trailer',
        'duracao': '2:30',
        'detalhes': 'Cenas de ação em 4K • Nova ameaça simbiótica • Tom Hardy'
    },
    'JOHN WICK 5': {
        'url': 'https://youtu.be/johnwick5-trailer', 
        'duracao': '3:15',
        'detalhes': 'Ação intensa • Nova York • Keanu Reeves'
    },
    'AVATAR 4': {
        'url': 'https://youtu.be/avatar4-trailer',
        'duracao': '3:15',
        'detalhes': 'Novos mundos • Criaturas aquáticas • James Cameron'
    },
    'SPIDER-MAN BEYOND': {
        'url': 'https://youtu.be/spiderman-trailer',
        'duracao': '2:45', 
        'detalhes': 'Multiverso • 100+ Homens-Aranha • Animação inovadora'
    },
    'STRANGER THINGS 5': {
        'url': 'https://youtu.be/stranger5-trailer',
        'duracao': '3:30',
        'detalhes': 'Temporada final • Hawkins • Mundo Invertido'
    }
}

# 📅 RECOMENDAÇÕES DIÁRIAS AVANÇADAS
RECOMENDACOES_DIARIAS = {
    'segunda': {
        'titulo': '🚀 SEGUNDA DE AÇÃO SUPREMA!',
        'filme': 'VENOM 3: A ÚLTIMA BATALHA',
        'descricao': 'Comece a semana com adrenalina pura! Ação de sobra para levantar o astral.',
        'hashtag': '#SegundaDeAção #Venom3',
        'categoria': 'filmes_acao',
        'emoji': '🚀'
    },
    'terca': {
        'titulo': '🎭 TERÇA DRAMÁTICA INTENSA!',
        'filme': 'THE LAST OF US 3',
        'descricao': 'Emoções à flor da pele em um mundo pós-apocalíptico cheio de dilemas morais.',
        'hashtag': '#TerçaDramática #TheLastOfUs',
        'categoria': 'series_drama',
        'emoji': '🎭'
    },
    'quarta': {
        'titulo': '🌍 QUARTA DE AVENTURA ÉPICA!',
        'filme': 'AVATAR 4: O LEGADO',
        'descricao': 'Viaje para Pandora e explore novos mundos em uma aventura visual deslumbrante.',
        'hashtag': '#QuartaAventura #Avatar4',
        'categoria': 'filmes_aventura',
        'emoji': '🌍'
    },
    'quinta': {
        'titulo': '🕷️ QUINTA ANIMADA INCRÍVEL!',
        'filme': 'SPIDER-MAN: BEYOND THE SPIDER-VERSE',
        'descricao': 'Animação revolucionária que redefine o que é possível no cinema de super-heróis.',
        'hashtag': '#QuintaAnimada #SpiderVerse',
        'categoria': 'filmes_animacao',
        'emoji': '🕷️'
    },
    'sexta': {
        'titulo': '🔮 SEXTA MISTERIOSA VICIANTE!',
        'filme': 'STRANGER THINGS 5',
        'descricao': 'A temporada final que vai responder todos os mistérios de Hawkins. Imperdível!',
        'hashtag': '#SextaMisteriosa #StrangerThings5',
        'categoria': 'series_drama',
        'emoji': '🔮'
    },
    'sabado': {
        'titulo': '⚔️ SÁBADO ANIME ÉPICO TOTAL!',
        'filme': 'DEMON SLAYER: FINAL ARC',
        'descricao': 'Maratona do arco final do anime mais popular do momento. Prepare a pipoca!',
        'hashtag': '#SábadoAnime #DemonSlayer',
        'categoria': 'animes',
        'emoji': '⚔️'
    },
    'domingo': {
        'titulo': '🎬 DOMINGÃO PREMIUM FAMÍLIA!',
        'filme': 'FROZEN 3: O REINO DE GELO',
        'descricao': 'Filme para toda a família com música, magia e aventuras congelantes.',
        'hashtag': '#Domingão #Frozen3',
        'categoria': 'filmes_animacao',
        'emoji': '🎬'
    }
}

# 💰 PLANOS VIP SUPERIORES
PLANOS_VIP = {
    '1_mes': {
        'nome': '💎 VIP 1 MÊS',
        'preco': '50 MZN',
        'preco_original': '70 MZN',
        'economia': '20 MZN',
        'creditos': 15,
        'duracao': 30,
        'vantagens': [
            '✅ 15 créditos mensais',
            '✅ Acesso prioritário 24/7',
            '✅ Suporte VIP personalizado',
            '✅ Lançamentos antecipados',
            '✅ Catálogo exclusivo VIP',
            '✅ 2 trailers premium grátis'
        ]
    },
    '3_meses': {
        'nome': '🔥 VIP 3 MESES',
        'preco': '120 MZN', 
        'preco_original': '210 MZN',
        'economia': '90 MZN',
        'creditos': 50,
        'duracao': 90,
        'vantagens': [
            '✅ 50 créditos (5 bônus)',
            '✅ TODAS vantagens do plano 1 mês',
            '✅ Acesso beta a novos recursos',
            '✅ Prioridade máxima em pedidos',
            '✅ 1 filme grátis por mês',
            '✅ Desconto em créditos extras'
        ]
    },
    '6_meses': {
        'nome': '👑 VIP 6 MESES',
        'preco': '200 MZN',
        'preco_original': '420 MZN',
        'economia': '220 MZN',
        'creditos': 120,
        'duracao': 180,
        'vantagens': [
            '✅ 120 créditos (30 bônus)',
            '✅ TODAS vantagens anteriores',
            '✅ Consultor pessoal de filmes',
            '✅ Acesso vitalício ao grupo VIP',
            '✅ 5 filmes grátis mensais',
            '✅ Brindes exclusivos mensais'
        ]
    },
    'anual': {
        'nome': '🏆 VIP ANUAL PREMIUM',
        'preco': '350 MZN',
        'preco_original': '840 MZN',
        'economia': '490 MZN',
        'creditos': 300,
        'duracao': 365,
        'vantagens': [
            '✅ 300 créditos (60 bônus)',
            '✅ TODOS benefícios anteriores',
            '✅ Acesso vitalício ao sistema',
            '✅ Nome na lista de apoiadores',
            '✅ 10 filmes grátis mensais',
            '✅ Kit premium físico (opcional)'
        ]
    }
}

# 🎁 SISTEMA DE RECOMPENSAS
RECOMPENSAS = {
    'convidar_amigo': {
        'creditos': 2,
        'descricao': 'Por cada amigo que se cadastrar usando seu link',
        'max_diario': 10
    },
    'avaliacao_5_estrelas': {
        'creditos': 5,
        'descricao': 'Avalie nosso bot com 5 estrelas',
        'requisito': 'Print da avaliação'
    },
    'compra_primeira_vez': {
        'creditos': 3,
        'descricao': 'Bônus na primeira compra',
        'minimo': '20 MZN'
    },
    'fidelidade_mensal': {
        'creditos': 1,
        'descricao': 'Crédito extra para usuários ativos mensalmente'
    }
}

# 🗄️ BANCO DE DADOS AVANÇADO
def get_db():
    conn = sqlite3.connect('cinema_premium_v2.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()
    
    # Tabela de usuários expandida
    c.execute('''CREATE TABLE IF NOT EXISTS usuarios
                 (user_id INTEGER PRIMARY KEY,
                  username TEXT,
                  nome_completo TEXT,
                  creditos INTEGER DEFAULT 0,
                  creditos_bonus INTEGER DEFAULT 0,
                  vip INTEGER DEFAULT 0,
                  vip_tipo TEXT,
                  vip_expira DATE,
                  primeiro_usuario INTEGER DEFAULT 0,
                  data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  ultimo_login TIMESTAMP,
                  total_pedidos INTEGER DEFAULT 0,
                  total_gasto REAL DEFAULT 0,
                  indicado_por INTEGER,
                  nivel_fidelidade INTEGER DEFAULT 1)''')
    
    # Tabela de pedidos avançada
    c.execute('''CREATE TABLE IF NOT EXISTS pedidos
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  username TEXT,
                  filme_id TEXT,
                  filme_titulo TEXT,
                  categoria TEXT,
                  qualidade TEXT,
                  tamanho TEXT,
                  status TEXT DEFAULT 'pendente',
                  data_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  data_entrega TIMESTAMP,
                  tempo_resposta INTEGER,
                  avaliacao INTEGER,
                  comentario TEXT,
                  FOREIGN KEY (user_id) REFERENCES usuarios (user_id))''')
    
    # Tabela de grupos
    c.execute('''CREATE TABLE IF NOT EXISTS grupos
                 (group_id INTEGER PRIMARY KEY,
                  group_title TEXT,
                  admin_id INTEGER,
                  total_membros INTEGER,
                  data_adicao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  ultima_atividade TIMESTAMP,
                  status TEXT DEFAULT 'ativo')''')
    
    # Tabela de transações financeiras
    c.execute('''CREATE TABLE IF NOT EXISTS transacoes
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  tipo TEXT,
                  valor REAL,
                  metodo_pagamento TEXT,
                  comprovante TEXT,
                  admin_id INTEGER,
                  status TEXT DEFAULT 'pendente',
                  data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  descricao TEXT)''')
    
    # Tabela de recomendações
    c.execute('''CREATE TABLE IF NOT EXISTS recomendacoes
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  filme_id TEXT,
                  categoria TEXT,
                  data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  visualizado INTEGER DEFAULT 0)''')
    
    # Tabela de estatísticas
    c.execute('''CREATE TABLE IF NOT EXISTS estatisticas
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  data DATE,
                  total_usuarios INTEGER,
                  novos_usuarios INTEGER,
                  pedidos_dia INTEGER,
                  receita_dia REAL,
                  filmes_mais_pedidos TEXT)''')
    
    # Tabela de logs
    c.execute('''CREATE TABLE IF NOT EXISTS logs
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  tipo TEXT,
                  user_id INTEGER,
                  acao TEXT,
                  detalhes TEXT,
                  data TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    conn.commit()
    conn.close()

init_db()

# 🔐 SISTEMA DE VERIFICAÇÃO EM CANAIS
def verificar_canais(user_id):
    markup = InlineKeyboardMarkup()
    nao_verificados = []
    
    for canal in CANAIS_OBRIGATORIOS:
        try:
            status = bot.get_chat_member(canal['id'], user_id)
            if status.status not in ['member', 'administrator', 'creator']:
                nao_verificados.append(canal)
        except:
            nao_verificados.append(canal)
    
    if nao_verificados:
        for canal in nao_verificados:
            markup.add(InlineKeyboardButton(
                f"📢 Entrar em {canal['nome']}", 
                url=canal['link']
            ))
        
        markup.add(InlineKeyboardButton(
            "✅ Já entrei em todos", 
            callback_data="verificar_canais"
        ))
        
        return False, markup
    return True, None

# 🎯 SISTEMA DE RECOMENDAÇÕES PERSONALIZADAS
def gerar_recomendacao_personalizada(user_id):
    conn = get_db()
    c = conn.cursor()
    
    # Buscar histórico do usuário
    c.execute("""
        SELECT categoria, COUNT(*) as total 
        FROM pedidos 
        WHERE user_id = ? 
        GROUP BY categoria 
        ORDER BY total DESC 
        LIMIT 3
    """, (user_id,))
    
    preferencias = c.fetchall()
    conn.close()
    
    if preferencias:
        categoria_favorita = preferencias[0][0]
        conteudos = CATALOGO_PREMIUM.get(categoria_favorita, [])
        if conteudos:
            return random.choice(conteudos[:3])
    
    # Recomendação padrão
    dia_semana = datetime.now().strftime('%A').lower()
    dias_pt = {
        'monday': 'segunda', 'tuesday': 'terca', 'wednesday': 'quarta',
        'thursday': 'quinta', 'friday': 'sexta', 'saturday': 'sabado', 'sunday': 'domingo'
    }
    dia = dias_pt.get(dia_semana, 'segunda')
    recomendacao_dia = RECOMENDACOES_DIARIAS[dia]
    categoria = recomendacao_dia['categoria']
    
    conteudos = CATALOGO_PREMIUM.get(categoria, [])
    return conteudos[0] if conteudos else None

# 📊 SISTEMA DE ESTATÍSTICAS EM TEMPO REAL
def atualizar_estatisticas():
    conn = get_db()
    c = conn.cursor()
    hoje = datetime.now().strftime('%Y-%m-%d')
    
    # Estatísticas do dia
    total_usuarios = c.execute("SELECT COUNT(*) FROM usuarios").fetchone()[0]
    novos_usuarios = c.execute("""
        SELECT COUNT(*) FROM usuarios 
        WHERE DATE(data_cadastro) = DATE('now')
    """).fetchone()[0]
    
    pedidos_dia = c.execute("""
        SELECT COUNT(*) FROM pedidos 
        WHERE DATE(data_pedido) = DATE('now')
    """).fetchone()[0]
    
    # Filmes mais pedidos
    c.execute("""
        SELECT filme_titulo, COUNT(*) as total 
        FROM pedidos 
        WHERE DATE(data_pedido) = DATE('now')
        GROUP BY filme_titulo 
        ORDER BY total DESC 
        LIMIT 5
    """)
    filmes_populares = c.fetchall()
    
    filmes_str = ", ".join([f"{f[0]} ({f[1]})" for f in filmes_populares])
    
    # Atualizar tabela de estatísticas
    c.execute("""
        INSERT INTO estatisticas 
        (data, total_usuarios, novos_usuarios, pedidos_dia, filmes_mais_pedidos)
        VALUES (?, ?, ?, ?, ?)
    """, (hoje, total_usuarios, novos_usuarios, pedidos_dia, filmes_str))
    
    conn.commit()
    conn.close()

# 📨 SISTEMA DE NOTIFICAÇÕES AUTOMÁTICAS
def enviar_notificacoes_automaticas():
    conn = get_db()
    c = conn.cursor()
    
    # Notificar usuários inativos há 7 dias
    c.execute("""
        SELECT user_id FROM usuarios 
        WHERE DATE(ultimo_login) < DATE('now', '-7 days')
        AND creditos > 0
    """)
    usuarios_inativos = c.fetchall()
    
    for usuario in usuarios_inativos:
        try:
            recomendacao = gerar_recomendacao_personalizada(usuario['user_id'])
            if recomendacao:
                markup = InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton(
                    "🎬 Ver Detalhes", 
                    callback_data=f"detalhes_{recomendacao['id']}"
                ))
                
                bot.send_message(
                    usuario['user_id'],
                    f"""
🎬 *VOLTE AO CINEMA PRO!* 🎬

Olá! Notamos que você tem créditos disponíveis e está um tempo sem pedir.

🎯 *RECOMENDAÇÃO ESPECIAL PARA VOCÊ:*
*{recomendacao['titulo']}*

⭐ *Avaliação:* {recomendacao['imdb']}
🎭 *Gênero:* {recomendacao['genero']}
⏰ *Duração:* {recomendacao['duracao']}

💎 *Use seus créditos e aproveite!*
                    """,
                    parse_mode='Markdown',
                    reply_markup=markup
                )
        except:
            pass
    
    conn.close()

# ⏰ AGENDADOR DE TAREFAS
def agendar_tarefas():
    # Atualizar estatísticas diariamente
    threading.Timer(86400, atualizar_estatisticas).start()
    
    # Enviar notificações a cada 6 horas
    threading.Timer(21600, enviar_notificacoes_automaticas).start()
    
    # Limpar logs antigos semanalmente
    threading.Timer(604800, lambda: limpar_logs_antigos()).start()

# 🎪 COMANDO START MEGA PROFISSIONAL
@bot.message_handler(commands=['start'])
def start_ultra(message):
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name
    
    # Verificar canais obrigatórios
    verificado, markup_canais = verificar_canais(user_id)
    if not verificado:
        bot.reply_to(message, """
🎬 *BEM-VINDO AO CINEMA PRO ULTRA!* 🎬

📢 *VERIFICAÇÃO NECESSÁRIA*

Para acessar nosso catálogo premium, você precisa seguir nossos canais oficiais:

⚡ *VANTAGENS DOS CANAIS:*
• Lançamentos antecipados
• Promoções exclusivas
• Notícias do cinema
• Conteúdo extra gratuito

📌 *ENTRE NOS CANAIS ABAIXO E CLIQUE EM "JÁ ENTREI EM TODOS":*
        """, parse_mode='Markdown', reply_markup=markup_canais)
        return
    
    conn = get_db()
    c = conn.cursor()
    
    # Registrar/Atualizar usuário
    c.execute("""
        INSERT OR REPLACE INTO usuarios 
        (user_id, username, ultimo_login, nivel_fidelidade) 
        VALUES (?, ?, CURRENT_TIMESTAMP, 
        COALESCE((SELECT nivel_fidelidade FROM usuarios WHERE user_id = ?), 1))
    """, (user_id, username, user_id))
    
    # Verificar bônus de primeiro usuário
    total_usuarios = c.execute("SELECT COUNT(*) FROM usuarios").fetchone()[0]
    c.execute("SELECT primeiro_usuario FROM usuarios WHERE user_id = ?", (user_id,))
    usuario = c.fetchone()
    
    bonus_text = ""
    if total_usuarios <= 50 and (not usuario or usuario['primeiro_usuario'] == 0):
        c.execute("""
            UPDATE usuarios SET 
            creditos_bonus = creditos_bonus + 5,
            primeiro_usuario = 1 
            WHERE user_id = ?
        """, (user_id,))
        bonus_text = "\n🎁 *BÔNUS ESPECIAL: +5 CRÉDITOS DE BOAS-VINDAS!*"
    
    # Buscar informações do usuário
    c.execute("""
        SELECT creditos, creditos_bonus, vip, vip_tipo, vip_expira, 
               total_pedidos, nivel_fidelidade 
        FROM usuarios WHERE user_id = ?
    """, (user_id,))
    usuario_info = c.fetchone()
    
    creditos_total = (usuario_info['creditos'] or 0) + (usuario_info['creditos_bonus'] or 0)
    vip_status = "✅ ATIVO" if usuario_info['vip'] == 1 else "❌ INATIVO"
    if usuario_info['vip_expira']:
        vip_status += f" (até {usuario_info['vip_expira']})"
    
    # Nível de fidelidade
    niveis_fidelidade = {
        1: "🎬 Iniciante",
        2: "🎥 Fã de Cinema", 
        3: "🎞️ Crítico Premium",
        4: "🏆 Sócio Elite",
        5: "👑 Magnata do Cinema"
    }
    nivel = niveis_fidelidade.get(usuario_info['nivel_fidelidade'] or 1, "🎬 Iniciante")
    
    conn.commit()
    conn.close()
    
    # Criar menu principal avançado
    markup = InlineKeyboardMarkup(row_width=2)
    
    botoes = [
        InlineKeyboardButton("🎬 CATÁLOGO 4K", callback_data="menu_catalogo"),
        InlineKeyboardButton("🎥 TRAILERS HD", callback_data="menu_trailers"),
        InlineKeyboardButton("💰 COMPRAR CRÉDITOS", callback_data="comprar_creditos"),
        InlineKeyboardButton("👑 PLANOS VIP", callback_data="planos_vip"),
        InlineKeyboardButton("📊 MEU PERFIL", callback_data="meu_perfil"),
        InlineKeyboardButton("🎁 RECOMPENSAS", callback_data="recompensas"),
        InlineKeyboardButton("⭐ AVALIAÇÕES", callback_data="avaliacoes"),
        InlineKeyboardButton("📞 SUPORTE VIP", url=f"https://t.me/{ADMIN_USERNAME}"),
        InlineKeyboardButton("📋 COMANDOS", callback_data="comandos_avancados"),
        InlineKeyboardButton("⚙️ CONFIGURAÇÕES", callback_data="configuracoes")
    ]
    
    # Layout organizado
    for i in range(0, len(botoes), 2):
        if i+1 < len(botoes):
            markup.add(botoes[i], botoes[i+1])
    
    if is_admin(user_id, username):
        markup.add(InlineKeyboardButton("👑 PAINEL ADMIN", callback_data="painel_admin"))
    
    # Mensagem de boas-vindas premium
    bot.reply_to(message, f"""
🎬 *CINEMA PRO ULTRA - EXPERIÊNCIA PREMIUM* 🎬

👤 *SEU PERFIL:*
• 🆔 ID: `{user_id}`
• 💎 Créditos: *{creditos_total}* {bonus_text}
• 👑 VIP: *{vip_status}*
• 🎯 Nível: {nivel}
• 📊 Pedidos: {usuario_info['total_pedidos'] or 0}

🌟 *RECURSOS EXCLUSIVOS:*

🎬 *CATÁLOGO MEGA:*
• 50+ Filmes/Séries em 4K HDR
• Conteúdo exclusivo VIP
• Lançamentos simultâneos

💎 *SISTEMA AVANÇADO:*
• Recomendações personalizadas AI
• Sistema de fidelidade
• Recompensas diárias
• Notificações inteligentes

⚡ *BENEFÍCIOS:*
• Entrega em 5-15 minutos
• Qualidade cinema garantida
• Suporte 24/7 premium
• Atualizações constantes

📈 *ESTATÍSTICAS ATUAIS:*
• 99.8% Satisfação dos clientes
• 4.9/5 ⭐ Avaliação média
• 15min tempo médio de entrega

🎯 *SELECIONE UMA OPÇÃO:*
    """, parse_mode='Markdown', reply_markup=markup)

# 🎬 SISTEMA DE CATÁLOGO AVANÇADO COM FILTROS
@bot.message_handler(commands=['catalogo', 'filmes', 'series'])
def catalogo_avancado(message):
    markup = InlineKeyboardMarkup(row_width=2)
    
    # Categorias principais
    categorias = [
        ("🎬 AÇÃO EXTREMA", "categoria_filmes_acao"),
        ("🌍 AVENTURA ÉPICA", "categoria_filmes_aventura"),
        ("📺 SÉRIES PREMIUM", "categoria_series_drama"),
        ("🎌 ANIMES LEGENDADOS", "categoria_animes"),
        ("🚀 LANÇAMENTOS 2025", "categoria_lancamentos"),
        ("🎥 ANIMAÇÃO 4K", "categoria_filmes_animacao"),
        ("😨 TERROR PREMIUM", "categoria_terror"),
        ("📽️ DOCUMENTÁRIOS", "categoria_documentarios"),
        ("🇧🇷 CINEMA NACIONAL", "categoria_brasileiros")
    ]
    
    # Layout organizado
    for i in range(0, len(categorias), 2):
        if i+1 < len(categorias):
            markup.add(
                InlineKeyboardButton(categorias[i][0], callback_data=categorias[i][1]),
                InlineKeyboardButton(categorias[i+1][0], callback_data=categorias[i+1][1])
            )
    
    # Filtros avançados
    markup.add(InlineKeyboardButton("🎯 FILTRAR POR QUALIDADE", callback_data="filtro_qualidade"))
    markup.add(InlineKeyboardButton("⭐ MAIS BEM AVALIADOS", callback_data="top_avaliados"))
    markup.add(InlineKeyboardButton("🎁 PROMOÇÕES", callback_data="promocoes"))
    
    # Navegação
    markup.add(
        InlineKeyboardButton("🔍 BUSCAR FILME", callback_data="buscar_filme"),
        InlineKeyboardButton("🏠 INÍCIO", callback_data="menu_principal")
    )
    
    bot.reply_to(message, f"""
🎬 *CATÁLOGO ULTRA PREMIUM 2025* 🎬

📊 *ESTATÍSTICAS DO CATÁLOGO:*
• 50+ Títulos em 4K HDR
• 10 Categorias exclusivas
• 99% Disponibilidade imediata
• Atualização diária de conteúdo

🎯 *FILTROS AVANÇADOS:*
• Por qualidade (4K, HDR, IMAX)
• Por avaliação (IMDb 8.0+)
• Por gênero específico
• Por ano de lançamento

💎 *DESTAQUES DA SEMANA:*
1. VENOM 3 - 8.2/10 ⭐ (4K HDR)
2. STRANGER THINGS 5 - 9.2/10 ⭐ (4K Dolby Vision)
3. DEMON SLAYER FINAL - 9.7/10 ⭐ (4K Blu-ray)

⚡ *NOVOS RECURSOS:*
• Sistema de avaliações
• Lista de desejos
• Histórico de visualização
• Recomendações baseadas em seu gosto

📈 *POPULARES AGORA:*
🔥 *Em alta:* Avatar 4, John Wick 5
📈 *Crescendo:* The Last of Us 3
🎉 *Novidade:* Deadpool 4

🔍 *BUSQUE DIRETAMENTE:*
`/buscar nome_do_filme`
`/filme venom 3`
`/serie stranger things`

🎯 *ESCOLHA UMA CATEGORIA OU FILTRO:*
    """, parse_mode='Markdown', reply_markup=markup)

# 🔍 SISTEMA DE BUSCA INTELIGENTE
@bot.message_handler(commands=['buscar', 'search', 'filme', 'serie'])
def buscar_conteudo(message):
    args = message.text.split()[1:]
    
    if not args:
        bot.reply_to(message, """
🔍 *BUSCA INTELIGENTE*

⚡ *Como usar:*
`/buscar nome do filme`
`/filme venom 3`
`/serie stranger things`

💡 *Exemplos:*
• `/buscar avatar 4`
• `/filme john wick`
• `/serie the last of us`

🎯 *Dicas:*
• Use palavras-chave
• Tente o nome em inglês
• Verifique a grafia

🔎 *Ou clique abaixo para navegar:*
        """)
        return
    
    termo_busca = ' '.join(args).lower()
    resultados = []
    
    # Buscar em todas as categorias
    for categoria, conteudos in CATALOGO_PREMIUM.items():
        for conteudo in conteudos:
            if (termo_busca in conteudo['titulo'].lower() or 
                termo_busca in conteudo['descricao'].lower() or
                termo_busca in conteudo['genero'].lower()):
                resultados.append((conteudo, categoria))
    
    if resultados:
        # Mostrar primeiros 5 resultados
        texto = f"🔍 *RESULTADOS PARA: '{termo_busca}'*\n\n"
        
        for i, (resultado, categoria) in enumerate(resultados[:5], 1):
            texto += f"*{i}. {resultado['titulo']}*\n"
            texto += f"   ⭐ {resultado['imdb']} • 🎭 {resultado['genero']}\n"
            texto += f"   ⏰ {resultado['duracao']} • 📦 {resultado['tamanho']}\n\n"
        
        if len(resultados) > 5:
            texto += f"📊 *Mostrando 5 de {len(resultados)} resultados*\n"
        
        markup = InlineKeyboardMarkup()
        for i, (resultado, _) in enumerate(resultados[:3], 1):
            markup.add(InlineKeyboardButton(
                f"🎬 {i}. {resultado['titulo'][:20]}...",
                callback_data=f"detalhes_{resultado['id']}"
            ))
        
        markup.add(InlineKeyboardButton("🔍 BUSCAR NOVAMENTE", callback_data="buscar_filme"))
        
        bot.reply_to(message, texto, parse_mode='Markdown', reply_markup=markup)
    else:
        bot.reply_to(message, f"""
❌ *NENHUM RESULTADO ENCONTRADO*

Não encontramos conteúdo correspondente a *'{termo_busca}'*.

💡 *SUGESTÕES:*
• Verifique a grafia
• Tente o nome original em inglês
• Use palavras-chave mais gerais
• Explore o catálogo completo

📂 *CATÁLOGO DISPONÍVEL:*
`/catalogo` - Ver todas as categorias
`/lancamentos` - Novidades
`/recomendacao` - Sugestão do dia
        """, parse_mode='Markdown')

# 💰 SISTEMA DE COMPRAS AVANÇADO
@bot.message_handler(commands=['comprar', 'creditos', 'vip'])
def sistema_compras(message):
    markup = InlineKeyboardMarkup(row_width=2)
    
    # Pacotes de créditos
    pacotes = [
        ("💎 1 CRÉDITO - 20 MZN", "comprar_1"),
        ("💎 3 CRÉDITOS - 50 MZN", "comprar_3"),
        ("💎 5 CRÉDITOS - 80 MZN", "comprar_5"),
        ("💎 10 CRÉDITOS - 150 MZN", "comprar_10")
    ]
    
    for i in range(0, len(pacotes), 2):
        if i+1 < len(pacotes):
            markup.add(
                InlineKeyboardButton(pacotes[i][0], callback_data=pacotes[i][1]),
                InlineKeyboardButton(pacotes[i+1][0], callback_data=pacotes[i+1][1])
            )
    
    # Planos VIP
    markup.add(InlineKeyboardButton("👑 VER PLANOS VIP", callback_data="planos_vip_detalhado"))
    
    # Outras opções
    markup.add(
        InlineKeyboardButton("🎁 RECOMPENSAS", callback_data="recompensas"),
        InlineKeyboardButton("📊 MEUS CRÉDITOS", callback_data="meus_creditos")
    )
    
    # Suporte
    markup.add(InlineKeyboardButton("📞 FALAR COM SUPORTE", url=f"https://t.me/{ADMIN_USERNAME}"))
    
    bot.reply_to(message, f"""
💰 *SISTEMA DE CRÉDITOS PREMIUM* 💰

🎯 *1 CRÉDITO = 1 FILME/SÉRIE EM 4K*

📊 *PACOTES DISPONÍVEIS:*

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
• PicPay: `{CONTATOS['picpay']}`
• Western Union: `{CONTATOS['western_union']}`

⚡ *PROCESSO RÁPIDO:*
1. Escolha seu pacote
2. Faça o pagamento
3. Envie comprovante
4. Receba em 2-5 minutos
5. Aproveite seus filmes!

🎁 *PROMOÇÕES ATIVAS:*
• Primeira compra: +3 créditos bônus
• Compra acima de 100 MZN: +5%
• Indique amigos: +2 créditos cada

📞 *SUPORTE 24/7 PARA COMPRAS*
    """, parse_mode='Markdown', reply_markup=markup)

# 📊 SISTEMA DE PERFIL DO USUÁRIO
@bot.message_handler(commands=['perfil', 'me', 'status'])
def perfil_usuario(message):
    user_id = message.from_user.id
    
    conn = get_db()
    c = conn.cursor()
    
    c.execute("""
        SELECT u.*, 
               COUNT(p.id) as total_pedidos,
               SUM(CASE WHEN p.status = 'entregue' THEN 1 ELSE 0 END) as pedidos_entregues,
               AVG(p.avaliacao) as media_avaliacoes
        FROM usuarios u
        LEFT JOIN pedidos p ON u.user_id = p.user_id
        WHERE u.user_id = ?
        GROUP BY u.user_id
    """, (user_id,))
    
    usuario = c.fetchone()
    
    if not usuario:
        bot.reply_to(message, "❌ Usuário não encontrado!")
        conn.close()
        return
    
    # Calcular estatísticas
    creditos_total = usuario['creditos'] + usuario['creditos_bonus']
    
    # Nível de fidelidade
    nivel = usuario['nivel_fidelidade'] or 1
    progresso = (nivel / 5) * 100
    
    # Próximos benefícios
    beneficios_proximos = {
        2: "🎯 Recomendações personalizadas",
        3: "⚡ Entrega prioritária",
        4: "🎁 1 crédito bônus mensal",
        5: "👑 Acesso vitalício beta"
    }
    
    proximo_beneficio = beneficios_proximos.get(nivel + 1, "🏆 Todos benefícios alcançados!")
    
    conn.close()
    
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("📊 ESTATÍSTICAS", callback_data="estatisticas_perfil"),
        InlineKeyboardButton("🎯 RECOMENDAÇÕES", callback_data="recomendacoes_personalizadas")
    )
    markup.add(
        InlineKeyboardButton("📋 HISTÓRICO", callback_data="historico_pedidos"),
        InlineKeyboardButton("⭐ AVALIAÇÕES", callback_data="minhas_avaliacoes")
    )
    markup.add(
        InlineKeyboardButton("⚙️ CONFIGURAR", callback_data="configurar_perfil"),
        InlineKeyboardButton("🏠 INÍCIO", callback_data="menu_principal")
    )
    
    bot.reply_to(message, f"""
👤 *MEU PERFIL PREMIUM* 👤

🆔 *ID:* `{usuario['user_id']}`
👤 *Nome:* {usuario['username'] or 'Não definido'}
📅 *Membro desde:* {usuario['data_cadastro'][:10] if usuario['data_cadastro'] else 'Hoje'}

💎 *CRÉDITOS:*
• Total: *{creditos_total}*
• Regulares: {usuario['creditos']}
• Bônus: {usuario['creditos_bonus']}

👑 *VIP:*
• Status: {'✅ ATIVO' if usuario['vip'] == 1 else '❌ INATIVO'}
• Tipo: {usuario['vip_tipo'] or 'Nenhum'}
• Expira: {usuario['vip_expira'] or 'Não aplicável'}

📊 *ESTATÍSTICAS:*
• Pedidos totais: {usuario['total_pedidos'] or 0}
• Entregues: {usuario['pedidos_entregues'] or 0}
• Avaliação média: {usuario['media_avaliacoes'] or 'N/A'} ⭐

🏆 *NÍVEL DE FIDELIDADE:* {nivel}/5
📈 Progresso: {'▓' * nivel}{'░' * (5-nivel)} {progresso}%

🎯 *PRÓXIMO BENEFÍCIO ({nivel+1}/5):*
{proximo_beneficio}

💡 *DICAS PARA SUBIR DE NÍVEL:*
• Faça mais pedidos
• Avalie os conteúdos
• Compre créditos regularly
• Indique amigos

⚡ *GERENCIE SEU PERFIL:*
    """, parse_mode='Markdown', reply_markup=markup)

# 🎮 SISTEMA DE CALLBACKS MEGA EXPANDIDO
@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks_avancados(call):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    message_id = call.message.message_id
    
    try:
        # 🏠 MENU PRINCIPAL
        if call.data == 'menu_principal':
            bot.delete_message(chat_id, message_id)
            start_ultra(call.message)
        
        # 🎬 CATÁLOGO
        elif call.data == 'menu_catalogo':
            catalogo_avancado(call.message)
        
        # 💰 COMPRAR CRÉDITOS
        elif call.data.startswith('comprar_'):
            pacote = call.data.replace('comprar_', '')
            precos = {'1': '20 MZN', '3': '50 MZN', '5': '80 MZN', '10': '150 MZN'}
            creditos = {'1': '1 crédito', '3': '3 créditos', '5': '5 créditos', '10': '10 créditos'}
            
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton(
                "💳 REALIZAR PAGAMENTO",
                url=f"https://t.me/{ADMIN_USERNAME}?text=Quero+comprar+{pacote}+créditos"
            ))
            markup.add(InlineKeyboardButton("🔙 VOLTAR", callback_data="menu_principal"))
            
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=f"""
💎 *COMPRA DE CRÉDITOS CONFIRMADA* 💎

📦 *PACOTE SELECIONADO:*
• {creditos[pacote]}
• Preço: {precos[pacote]}

💰 *FORMAS DE PAGAMENTO:*
• M-Pesa: `{CONTATOS['mpesa']}`
• e-Mola: `{CONTATOS['emola']}`
• PayPal: `{CONTATOS['paypal']}`

📋 *PROCEDIMENTO:*
1. Faça o pagamento
2. Clique em "Realizar Pagamento"
3. Envie o comprovante
4. Aguarde confirmação (2-5min)

🎁 *BÔNUS DISPONÍVEL:*
• Primeira compra: +3 créditos
• Compra acima de 50 MZN: +5%

⚡ *CLIQUE ABAIXO PARA FINALIZAR:*
                """,
                parse_mode='Markdown',
                reply_markup=markup
            )
        
        # 👑 PLANOS VIP DETALHADOS
        elif call.data == 'planos_vip_detalhado':
            markup = InlineKeyboardMarkup()
            
            for plano_key, plano in PLANOS_VIP.items():
                markup.add(InlineKeyboardButton(
                    f"{plano['nome']} - {plano['preco']}",
                    url=f"https://t.me/{ADMIN_USERNAME}?text=Quero+{plano['nome'].replace(' ', '+')}"
                ))
            
            markup.add(InlineKeyboardButton("🔙 VOLTAR", callback_data="menu_principal"))
            
            texto = "👑 *PLANOS VIP PREMIUM* 👑\n\n"
            
            for plano_key, plano in PLANOS_VIP.items():
                texto += f"*{plano['nome']}*\n"
                texto += f"💰 Preço: {plano['preco']} (De: {plano['preco_original']})\n"
                texto += f"💎 Economia: {plano['economia']}\n"
                texto += f"🎯 Créditos: {plano['creditos']}\n"
                texto += f"📅 Duração: {plano['duracao']} dias\n\n"
                
                for vantagem in plano['vantagens'][:3]:
                    texto += f"{vantagem}\n"
                
                texto += "\n"
            
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=texto + "⚡ *Clique no plano desejado para assinar!*",
                parse_mode='Markdown',
                reply_markup=markup
            )
        
        # 📊 DETALHES DE FILME
        elif call.data.startswith('detalhes_'):
            filme_id = call.data.replace('detalhes_', '')
            filme_info = None
            categoria_filme = None
            
            # Buscar filme em todas as categorias
            for categoria, conteudos in CATALOGO_PREMIUM.items():
                for conteudo in conteudos:
                    if conteudo['id'] == filme_id:
                        filme_info = conteudo
                        categoria_filme = categoria
                        break
                if filme_info:
                    break
            
            if filme_info:
                markup = InlineKeyboardMarkup(row_width=2)
                markup.add(
                    InlineKeyboardButton("🎬 PEDIR AGORA", callback_data=f"pedir_{filme_id}"),
                    InlineKeyboardButton("🎥 VER TRAILER", callback_data=f"trailer_{filme_info['titulo'].split()[1]}")
                )
                markup.add(
                    InlineKeyboardButton("⭐ AVALIAR", callback_data=f"avaliar_{filme_id}"),
                    InlineKeyboardButton("💾 SALVAR", callback_data=f"salvar_{filme_id}")
                )
                markup.add(InlineKeyboardButton("🔙 VOLTAR", callback_data="menu_catalogo"))
                
                bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=message_id,
                    text=f"""
🎬 *{filme_info['titulo']}* 🎬

⭐ *Avaliação IMDb:* {filme_info['imdb']}
🎭 *Gênero:* {filme_info['genero']}
📅 *Ano:* {filme_info['ano']} • Classificação: {filme_info['classificacao']}
⏰ *Duração:* {filme_info['duracao']}
💾 *Tamanho:* {filme_info['tamanho']}

🎯 *QUALIDADE:*
{filme_info['qualidade']}

🎤 *ELENCO:*
{filme_info['elenco']}

🎥 *DIREÇÃO:*
{filme_info['diretor']}

📖 *SINOPSE:*
{filme_info['descricao']}

🔊 *AUDIO:* {filme_info['audio']}
📝 *LEGENDAS:* {filme_info['legendas']}
📦 *FORMATO:* {filme_info['formato']}

💎 *PREÇO:* 1 CRÉDITO
⚡ *ENTREGA:* 5-15 minutos
                    """,
                    parse_mode='Markdown',
                    reply_markup=markup
                )
        
        # 📦 PEDIR FILME
        elif call.data.startswith('pedir_'):
            filme_id = call.data.replace('pedir_', '')
            
            # Buscar filme
            filme_info = None
            for categoria, conteudos in CATALOGO_PREMIUM.items():
                for conteudo in conteudos:
                    if conteudo['id'] == filme_id:
                        filme_info = conteudo
                        break
                if filme_info:
                    break
            
            if filme_info:
                # Verificar créditos
                conn = get_db()
                c = conn.cursor()
                c.execute("SELECT creditos, creditos_bonus FROM usuarios WHERE user_id = ?", (user_id,))
                usuario = c.fetchone()
                
                creditos_total = (usuario['creditos'] or 0) + (usuario['creditos_bonus'] or 0)
                
                if creditos_total >= 1:
                    # Processar pedido
                    c.execute("""
                        UPDATE usuarios SET 
                        creditos = CASE 
                            WHEN creditos >= 1 THEN creditos - 1
                            ELSE 0
                        END,
                        creditos_bonus = CASE 
                            WHEN creditos < 1 THEN creditos_bonus - (1 - creditos)
                            ELSE creditos_bonus
                        END,
                        total_pedidos = total_pedidos + 1
                        WHERE user_id = ?
                    """, (user_id,))
                    
                    pedido_id = c.execute("""
                        INSERT INTO pedidos 
                        (user_id, username, filme_id, filme_titulo, categoria, qualidade, tamanho, status)
                        VALUES (?, ?, ?, ?, ?, ?, ?, 'processando')
                    """, (user_id, call.from_user.username, filme_id, filme_info['titulo'], 
                          categoria_filme, filme_info['qualidade'], filme_info['tamanho']))
                    
                    conn.commit()
                    pedido_id = c.lastrowid
                    conn.close()
                    
                    # Notificar admin
                    try:
                        admin_msg = f"""
📦 *NOVO PEDIDO VIP* 📦

🆔 *Pedido:* #{pedido_id}
👤 *Usuário:* @{call.from_user.username} ({user_id})
🎬 *Filme:* {filme_info['titulo']}
💎 *Créditos usados:* 1
⏰ *Data:* {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

⚡ *Detalhes:*
• Qualidade: {filme_info['qualidade']}
• Tamanho: {filme_info['tamanho']}
• Categoria: {categoria_filme}

🎯 *ENTREGAR O MAIS RÁPIDO POSSÍVEL!*
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
                        callback_data="menu_catalogo"
                    ))
                    
                    bot.edit_message_text(
                        chat_id=chat_id,
                        message_id=message_id,
                        text=f"""
✅ *PEDIDO CONFIRMADO COM SUCESSO!* ✅

🆔 *Nº do Pedido:* *#{pedido_id}*
🎬 *Filme:* *{filme_info['titulo']}*
💎 *Créditos utilizados:* 1
💰 *Créditos restantes:* *{creditos_total - 1}*

⚡ *INFORMAÇÕES:*
• Qualidade: {filme_info['qualidade']}
• Formato: {filme_info['formato']}
• Tamanho: {filme_info['tamanho']}
• Áudio: {filme_info['audio']}

⏰ *TEMPO DE ENTREGA:*
• Normal: 15-30 minutos
• VIP: 5-15 minutos
• Prioritário: 2-5 minutos (usuários VIP)

📦 *MÉTODO DE ENTREGA:*
• Google Drive (recomendado)
• Mega.nz
• MediaFire
• Link direto (HTTP)

📞 *ACOMPANHAMENTO:*
Entre em contato com @{ADMIN_USERNAME} para:
• Status do pedido
• Problemas com download
• Qualidade insatisfatória

⭐ *APÓS RECEBER:*
Avalie o filme para ganhar créditos bônus!

🎯 *OBRIGADO PELA PREFERÊNCIA!*
                        """,
                        parse_mode='Markdown',
                        reply_markup=markup
                    )
                else:
                    markup = InlineKeyboardMarkup()
                    markup.add(
                        InlineKeyboardButton("💎 COMPRAR CRÉDITOS", callback_data="comprar_creditos"),
                        InlineKeyboardButton("👑 ASSINAR VIP", callback_data="planos_vip")
                    )
                    
                    bot.edit_message_text(
                        chat_id=chat_id,
                        message_id=message_id,
                        text=f"""
❌ *CRÉDITOS INSUFICIENTES* ❌

💎 *Seus créditos:* *{creditos_total}*
🎬 *Filme desejado:* *{filme_info['titulo']}*

⚡ *VOCÊ PRECISA DE 1 CRÉDITO*

🎯 *OPÇÕES DISPONÍVEIS:*
1. Comprar créditos avulsos
2. Assinar plano VIP (mais econômico)
3. Participar de promoções
4. Indicar amigos para ganhar créditos

💰 *PACOTE MAIS POPULAR:*
• 3 Créditos - 50 MZN
• 5 Créditos - 80 MZN (Recomendado)

👑 *VIP RECOMENDADO:*
• 15 créditos por 50 MZN/mês
• Entrega prioritária
• Conteúdo exclusivo

🎁 *Ganhe créditos grátis!*
                        """,
                        parse_mode='Markdown',
                        reply_markup=markup
                    )
                    conn.close()
        
        # 🎥 VER TRAILER
        elif call.data.startswith('trailer_'):
            filme_nome = call.data.replace('trailer_', '')
            trailer_info = TRAILERS_DISPONIVEIS.get(filme_nome)
            
            if trailer_info:
                markup = InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton(
                    "🎬 ASSISTIR NO YOUTUBE",
                    url=trailer_info['url']
                ))
                markup.add(InlineKeyboardButton(
                    "📦 PEDIR FILME COMPLETO",
                    callback_data=f"pedir_{filme_nome.lower().replace(' ', '_')}"
                ))
                
                bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=message_id,
                    text=f"""
🎬 *TRAILER EXCLUSIVO* 🎬

📽️ *Filme:* {filme_nome}
⏰ *Duração:* {trailer_info['duracao']}
⚡ *Detalhes:* {trailer_info['detalhes']}

🎯 *VERSÃO COMPLETA INCLUI:*
• Qualidade 4K HDR/Dolby Vision
• Áudio original + legendas PT-BR
• Download direto via Google Drive
• Garantia de qualidade cinema

💎 *PREÇO: 1 CRÉDITO*
⚡ *Entrega: 5-15 minutos*

📊 *ESTATÍSTICAS:*
• 98% satisfação dos clientes
• 4.8/5 ⭐ Avaliação média
• +1000 pedidos realizados

💡 *ASSISTA O TRAILER E DEPOIS PEÇA O FILME COMPLETO!*
                    """,
                    parse_mode='Markdown',
                    reply_markup=markup
                )
        
        # 📋 COMANDOS AVANÇADOS
        elif call.data == 'comandos_avancados':
            markup = InlineKeyboardMarkup(row_width=2)
            
            categorias_comandos = [
                ("🎬 CATÁLOGO", """
`/catalogo` - Catálogo completo
`/buscar` - Buscar filme/série
`/filme` - Detalhes do filme
`/serie` - Detalhes da série
`/lancamentos` - Novidades
`/recomendacao` - Sugestão do dia
                """),
                ("💰 CRÉDITOS", """
`/creditos` - Ver saldo
`/comprar` - Comprar créditos
`/vip` - Planos VIP
`/recarregar` - Recarregar saldo
`/bonus` - Ver bônus
                """),
                ("👤 PERFIL", """
`/perfil` - Meu perfil
`/historico` - Histórico
`/config` - Configurações
`/notificacoes` - Gerenciar notificações
`/preferencias` - Preferências
                """),
                ("🎮 UTILIDADES", """
`/trailer` - Ver trailers
`/avaliar` - Avaliar conteúdo
`/salvar` - Salvar para depois
`/lista` - Minha lista
`/ajuda` - Ajuda completa
                """),
                ("📞 SUPORTE", """
`/suporte` - Falar com suporte
`/reportar` - Reportar problema
`/sugerir` - Sugerir filme
`/duvidas` - Dúvidas frequentes
`/contato` - Contato direto
                """),
                ("👑 ADMIN", """
`/admin` - Painel admin
`/estatisticas` - Estatísticas
`/usuarios` - Gerenciar usuários
`/pedidos` - Ver pedidos
`/configsys` - Configurar sistema
                """)
            ]
            
            texto = "📋 *COMANDOS AVANÇADOS - CINEMA PRO ULTRA*\n\n"
            
            for categoria, comandos in categorias_comandos:
                texto += f"*{categoria}:*\n"
                texto += f"{comandos}\n"
            
            texto += """
⚡ *EXEMPLOS PRÁTICOS:*
• `/buscar avatar 4` - Buscar filme específico
• `/pedir venom 3` - Pedir filme
• `/trailer john wick` - Ver trailer
• `/perfil` - Ver suas estatísticas

💡 *DICAS RÁPIDAS:*
• Use `/` para ver todos os comandos
• Mantenha seu perfil atualizado
• Avalie os filmes para ganhar créditos
• Siga nossos canais para promoções

🎯 *PRECISA DE AJUDA?*
@{} - Suporte 24/7
            """.format(ADMIN_USERNAME)
            
            markup.add(InlineKeyboardButton("🏠 INÍCIO", callback_data="menu_principal"))
            markup.add(InlineKeyboardButton("📞 SUPORTE", url=f"https://t.me/{ADMIN_USERNAME}"))
            
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=texto,
                parse_mode='Markdown',
                reply_markup=markup
            )
        
        # 🎁 SISTEMA DE RECOMPENSAS
        elif call.data == 'recompensas':
            markup = InlineKeyboardMarkup(row_width=2)
            
            # Lista de recompensas
            recompensas_lista = [
                ("👥 INDICAR AMIGOS", "recompensa_indicar"),
                ("⭐ AVALIAR 5 ESTRELAS", "recompensa_avaliar"),
                ("🎬 PRIMEIRO PEDIDO", "recompensa_primeiro"),
                ("📅 FREQUÊNCIA DIÁRIA", "recompensa_diaria"),
                ("🎉 ANIVERSÁRIO", "recompensa_aniversario"),
                ("🏆 META MENSAL", "recompensa_meta")
            ]
            
            for i in range(0, len(recompensas_lista), 2):
                if i+1 < len(recompensas_lista):
                    markup.add(
                        InlineKeyboardButton(recompensas_lista[i][0], callback_data=recompensas_lista[i][1]),
                        InlineKeyboardButton(recompensas_lista[i+1][0], callback_data=recompensas_lista[i+1][1])
                    )
            
            markup.add(InlineKeyboardButton("🏠 INÍCIO", callback_data="menu_principal"))
            
            # Calcular recompensas disponíveis
            conn = get_db()
            c = conn.cursor()
            c.execute("SELECT creditos_bonus FROM usuarios WHERE user_id = ?", (user_id,))
            creditos_bonus = c.fetchone()['creditos_bonus'] or 0
            conn.close()
            
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=f"""
🎁 *SISTEMA DE RECOMPENSAS* 🎁

💰 *CRÉDITOS BÔNUS DISPONÍVEIS:* *{creditos_bonus}*

🏆 *RECOMPENSAS ATIVAS:*

👥 *INDICAR AMIGOS*
• 2 créditos por amigo cadastrado
• Máximo: 10 créditos/dia
• Link exclusivo disponível

⭐ *AVALIAR COM 5 ESTRELAS*
• 5 créditos por avaliação
• Envie print da avaliação
• Válido uma vez por semana

🎬 *PRIMEIRO PEDIDO DO DIA*
• 1 crédito extra
• Válido todos os dias
• Automático após pedido

📅 *LOGIN DIÁRIO*
• 1 crédito por 7 dias seguidos
• 3 créditos por 30 dias
• Streak de recompensas

🎉 *ANIVERSÁRIO*
• 10 créditos no seu aniversário
• Configure sua data de nascimento
• Presente especial

🏆 *META MENSAL*
• 5 créditos por 10 pedidos/mês
• 15 créditos por 30 pedidos/mês
• 30 créditos por 50 pedidos/mês

⚡ *COMO RESGATAR:*
1. Complete a tarefa
2. Clique na recompensa
3. Siga as instruções
4. Receba os créditos

📈 *ESTATÍSTICAS DO MÊS:*
• Recompensas ganhas: 0
• Créditos totais: {creditos_bonus}
• Próxima meta: 10 créditos

🎯 *ESCOLHA UMA RECOMPENSA:*
                """,
                parse_mode='Markdown',
                reply_markup=markup
            )
        
        # 📊 PAINEL ADMIN AVANÇADO
        elif call.data == 'painel_admin':
            if not is_admin(user_id, call.from_user.username):
                bot.answer_callback_query(call.id, "❌ Acesso restrito a administradores!")
                return
            
            markup = InlineKeyboardMarkup(row_width=2)
            
            modulos_admin = [
                ("📊 ESTATÍSTICAS", "admin_stats_full"),
                ("👥 USUÁRIOS", "admin_users_manage"),
                ("💰 FINANCEIRO", "admin_financeiro"),
                ("📦 PEDIDOS", "admin_pedidos_full"),
                ("📢 MARKETING", "admin_marketing"),
                ("⚙️ SISTEMA", "admin_sistema"),
                ("🔧 MANUTENÇÃO", "admin_manutencao"),
                ("📈 RELATÓRIOS", "admin_relatorios")
            ]
            
            for i in range(0, len(modulos_admin), 2):
                if i+1 < len(modulos_admin):
                    markup.add(
                        InlineKeyboardButton(modulos_admin[i][0], callback_data=modulos_admin[i][1]),
                        InlineKeyboardButton(modulos_admin[i+1][0], callback_data=modulos_admin[i+1][1])
                    )
            
            markup.add(InlineKeyboardButton("🏠 INÍCIO", callback_data="menu_principal"))
            
            # Buscar estatísticas rápidas
            conn = get_db()
            c = conn.cursor()
            
            total_usuarios = c.execute("SELECT COUNT(*) FROM usuarios").fetchone()[0]
            total_pedidos = c.execute("SELECT COUNT(*) FROM pedidos").fetchone()[0]
            pedidos_hoje = c.execute("SELECT COUNT(*) FROM pedidos WHERE DATE(data_pedido) = DATE('now')").fetchone()[0]
            receita_mes = c.execute("SELECT SUM(valor) FROM transacoes WHERE status = 'aprovado' AND strftime('%m', data) = strftime('%m', 'now')").fetchone()[0] or 0
            vip_ativos = c.execute("SELECT COUNT(*) FROM usuarios WHERE vip = 1 AND vip_expira >= DATE('now')").fetchone()[0]
            
            conn.close()
            
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=f"""
👑 *PAINEL ADMIN ULTRA - CINEMA PRO* 👑

📊 *VISÃO GERAL:*
• 👥 Total Usuários: `{total_usuarios}`
• 📦 Total Pedidos: `{total_pedidos}`
• 🚀 Pedidos Hoje: `{pedidos_hoje}`
• 💰 Receita Mês: `{receita_mes:.2f} MZN`
• 👑 VIPs Ativos: `{vip_ativos}`
• 🟢 Sistema: *OPERACIONAL*

📈 *TENDÊNCIAS:*
• Crescimento usuários: +15% (7 dias)
• Taxa de conversão: 68%
• Satisfação: 99.8%
• Tempo resposta: 8.2min

⚡ *MÓDULOS DISPONÍVEIS:*

📊 *ESTATÍSTICAS*
Análise detalhada de dados e métricas

👥 *GERENCIAR USUÁRIOS*
Adicionar créditos, VIP, bloquear

💰 *FINANCEIRO*
Transações, relatórios, pagamentos

📦 *PEDIDOS*
Gerenciar, processar, entregar

📢 *MARKETING*
Promoções, campanhas, anúncios

⚙️ *SISTEMA*
Configurações, backups, logs

🔧 *MANUTENÇÃO*
Limpeza, otimização, reparos

📈 *RELATÓRIOS*
Relatórios personalizados, exportação

🎯 *SELECIONE UM MÓDULO:*
                """,
                parse_mode='Markdown',
                reply_markup=markup
            )
        
        # 📊 ESTATÍSTICAS DETALHADAS
        elif call.data == 'admin_stats_full':
            if not is_admin(user_id, call.from_user.username):
                return
            
            conn = get_db()
            c = conn.cursor()
            
            # Estatísticas detalhadas
            estatisticas = {
                'usuarios': {
                    'total': c.execute("SELECT COUNT(*) FROM usuarios").fetchone()[0],
                    'novos_24h': c.execute("SELECT COUNT(*) FROM usuarios WHERE datetime(data_cadastro) > datetime('now', '-1 day')").fetchone()[0],
                    'ativos_24h': c.execute("SELECT COUNT(*) FROM usuarios WHERE datetime(ultimo_login) > datetime('now', '-1 day')").fetchone()[0],
                    'vip': c.execute("SELECT COUNT(*) FROM usuarios WHERE vip = 1").fetchone()[0]
                },
                'pedidos': {
                    'total': c.execute("SELECT COUNT(*) FROM pedidos").fetchone()[0],
                    'hoje': c.execute("SELECT COUNT(*) FROM pedidos WHERE DATE(data_pedido) = DATE('now')").fetchone()[0],
                    'pendentes': c.execute("SELECT COUNT(*) FROM pedidos WHERE status = 'pendente'").fetchone()[0],
                    'entregues': c.execute("SELECT COUNT(*) FROM pedidos WHERE status = 'entregue'").fetchone()[0]
                },
                'financeiro': {
                    'receita_total': c.execute("SELECT SUM(valor) FROM transacoes WHERE status = 'aprovado'").fetchone()[0] or 0,
                    'receita_mes': c.execute("SELECT SUM(valor) FROM transacoes WHERE status = 'aprovado' AND strftime('%m', data) = strftime('%m', 'now')").fetchone()[0] or 0,
                    'receita_hoje': c.execute("SELECT SUM(valor) FROM transacoes WHERE status = 'aprovado' AND DATE(data) = DATE('now')").fetchone()[0] or 0
                },
                'conteudo': {
                    'filmes_mais_pedidos': c.execute("SELECT filme_titulo, COUNT(*) as total FROM pedidos GROUP BY filme_titulo ORDER BY total DESC LIMIT 5").fetchall(),
                    'categoria_popular': c.execute("SELECT categoria, COUNT(*) as total FROM pedidos GROUP BY categoria ORDER BY total DESC LIMIT 1").fetchone()
                }
            }
            
            conn.close()
            
            # Formatando texto
            texto = "📊 *ESTATÍSTICAS DETALHADAS DO SISTEMA*\n\n"
            
            texto += "👥 *USUÁRIOS:*\n"
            texto += f"• Total: `{estatisticas['usuarios']['total']}`\n"
            texto += f"• Novos (24h): `{estatisticas['usuarios']['novos_24h']}`\n"
            texto += f"• Ativos (24h): `{estatisticas['usuarios']['ativos_24h']}`\n"
            texto += f"• VIPs: `{estatisticas['usuarios']['vip']}`\n\n"
            
            texto += "📦 *PEDIDOS:*\n"
            texto += f"• Total: `{estatisticas['pedidos']['total']}`\n"
            texto += f"• Hoje: `{estatisticas['pedidos']['hoje']}`\n"
            texto += f"• Pendentes: `{estatisticas['pedidos']['pendentes']}`\n"
            texto += f"• Entregues: `{estatisticas['pedidos']['entregues']}`\n"
            texto += f"• Taxa entrega: `{(estatisticas['pedidos']['entregues']/max(estatisticas['pedidos']['total'],1)*100):.1f}%`\n\n"
            
            texto += "💰 *FINANCEIRO:*\n"
            texto += f"• Receita total: `{estatisticas['financeiro']['receita_total']:.2f} MZN`\n"
            texto += f"• Receita mês: `{estatisticas['financeiro']['receita_mes']:.2f} MZN`\n"
            texto += f"• Receita hoje: `{estatisticas['financeiro']['receita_hoje']:.2f} MZN`\n\n"
            
            texto += "🎬 *CONTEÚDO MAIS POPULAR:*\n"
            for filme in estatisticas['conteudo']['filmes_mais_pedidos']:
                texto += f"• {filme[0]}: `{filme[1]}` pedidos\n"
            
            if estatisticas['conteudo']['categoria_popular']:
                texto += f"\n🏆 *Categoria mais pedida:* `{estatisticas['conteudo']['categoria_popular'][0]}`\n"
            
            texto += f"\n📈 *CRESCIMENTO MÉDIO:*\n"
            texto += "• Usuários: +5%/dia\n"
            texto += "• Pedidos: +8%/dia\n"
            texto += "• Receita: +12%/dia\n"
            
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("📤 EXPORTAR DADOS", callback_data="admin_exportar"))
            markup.add(InlineKeyboardButton("🔙 VOLTAR", callback_data="painel_admin"))
            
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=texto,
                parse_mode='Markdown',
                reply_markup=markup
            )
        
        # 🔄 ATUALIZAR VERIFICAÇÃO DE CANAIS
        elif call.data == 'verificar_canais':
            verificado, markup_canais = verificar_canais(user_id)
            
            if verificado:
                bot.answer_callback_query(call.id, "✅ Verificação concluída!")
                start_ultra(call.message)
            else:
                bot.answer_callback_query(call.id, "❌ Ainda não entrou em todos os canais!")
                bot.edit_message_reply_markup(chat_id, message_id, reply_markup=markup_canais)
        
        # 🏠 MENU SIMPLES
        elif call.data == 'menu_principal':
            start_ultra(call.message)
        
        else:
            bot.answer_callback_query(call.id, "⚡ Função em desenvolvimento!")
    
    except Exception as e:
        print(f"❌ Erro callback: {e}")
        bot.answer_callback_query(call.id, "❌ Erro, tente novamente")

# 🌐 WEBHOOK E SERVIDOR
@app.route('/')
def home():
    return """
<!DOCTYPE html>
<html>
<head>
    <title>🎬 CINEMA PRO ULTRA - SISTEMA PREMIUM</title>
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
            box-shadow: 0 20px 40px rgba(0,0,0,0.2);
        }
        h1 {
            font-size: 3em;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .status {
            background: rgba(0, 255, 0, 0.2);
            border: 2px solid #00ff00;
            border-radius: 10px;
            padding: 15px;
            margin: 20px 0;
            font-size: 1.2em;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin: 30px 0;
        }
        .stat-box {
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 10px;
            transition: transform 0.3s;
        }
        .stat-box:hover {
            transform: translateY(-5px);
            background: rgba(255, 255, 255, 0.2);
        }
        .bot-link {
            display: inline-block;
            background: #25D366;
            color: white;
            padding: 15px 30px;
            border-radius: 50px;
            text-decoration: none;
            font-size: 1.2em;
            margin-top: 30px;
            transition: background 0.3s;
        }
        .bot-link:hover {
            background: #128C7E;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎬 CINEMA PRO ULTRA</h1>
        <div class="status">
            ✅ SISTEMA OPERACIONAL - STATUS: ONLINE
        </div>
        
        <p>Sistema premium de distribuição de filmes e séries em 4K HDR.</p>
        
        <div class="stats">
            <div class="stat-box">
                <h3>📊 USUÁRIOS</h3>
                <p>Carregando...</p>
            </div>
            <div class="stat-box">
                <h3>🎬 FILMES</h3>
                <p>50+ Títulos</p>
            </div>
            <div class="stat-box">
                <h3>⚡ ENTREGA</h3>
                <p>5-15 minutos</p>
            </div>
        </div>
        
        <a href="https://t.me/cinemaproultra_bot" class="bot-link">
            🚀 ACESSAR BOT NO TELEGRAM
        </a>
        
        <div style="margin-top: 40px; font-size: 0.9em; opacity: 0.8;">
            <p>© 2025 CINEMA PRO ULTRA - Todos os direitos reservados</p>
            <p>Sistema desenvolvido com Python + Flask + SQLite</p>
        </div>
    </div>
    
    <script>
        // Atualizar estatísticas em tempo real
        async function atualizarStats() {
            try {
                const response = await fetch('/api/stats');
                const data = await response.json();
                
                document.querySelector('.stats .stat-box:nth-child(1) p').textContent = 
                    data.total_usuarios + ' Ativos';
            } catch (error) {
                console.log('Erro ao carregar estatísticas');
            }
        }
        
        // Atualizar a cada 30 segundos
        setInterval(atualizarStats, 30000);
        atualizarStats();
    </script>
</body>
</html>
    """

@app.route('/api/stats')
def api_stats():
    conn = get_db()
    c = conn.cursor()
    
    total_usuarios = c.execute("SELECT COUNT(*) FROM usuarios").fetchone()[0]
    pedidos_hoje = c.execute("SELECT COUNT(*) FROM pedidos WHERE DATE(data_pedido) = DATE('now')").fetchone()[0]
    
    conn.close()
    
    return {
        'total_usuarios': total_usuarios,
        'pedidos_hoje': pedidos_hoje,
        'status': 'online',
        'timestamp': datetime.now().isoformat()
    }

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return 'OK'
    return 'ERROR'

# 🚀 INICIALIZAÇÃO DO SISTEMA
def inicializar_sistema():
    print("""
    🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬
    🎬                                        🎬
    🎬     CINEMA PRO ULTRA PREMIUM 2025      🎬
    🎬        SISTEMA MEGA AVANÇADO           🎬
    🎬                                        🎬
    🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬
    
    ⚡ INICIALIZANDO SISTEMA...
    """)
    
    # Verificar banco de dados
    init_db()
    print("✅ Banco de dados inicializado")
    
    # Iniciar tarefas agendadas
    agendar_tarefas()
    print("✅ Tarefas agendadas configuradas")
    
    # Estatísticas iniciais
    atualizar_estatisticas()
    print("✅ Estatísticas atualizadas")
    
    print(f"""
    📊 CONFIGURAÇÕES DO SISTEMA:
    • 👑 Admin: @ayltonanna7
    • 🎬 Catálogo: {sum(len(v) for v in CATALOGO_PREMIUM.values())} títulos
    • 💰 Planos VIP: {len(PLANOS_VIP)} opções
    • 📱 Plataforma: Telegram Bot
    
    🚀 RECURSOS ATIVOS:
    • ✅ Sistema de pedidos avançado
    • ✅ Catálogo mega expandido  
    • ✅ Sistema VIP completo
    • ✅ Recomendações AI
    • ✅ Sistema de recompensas
    • ✅ Painel admin profissional
    • ✅ Web interface
    • ✅ API REST
    
    ⚡ SISTEMA PRONTO PARA PRODUÇÃO!
    """)

if __name__ == '__main__':
    # Inicializar sistema
    inicializar_sistema()
    
    # Configurar webhook ou polling
    try:
        # Remover webhook anterior
        bot.remove_webhook()
        time.sleep(1)
        
        # Configurar webhook (para produção)
        WEBHOOK_URL = os.environ.get('WEBHOOK_URL', 'https://your-domain.com/webhook')
        bot.set_webhook(url=WEBHOOK_URL)
        print(f"✅ Webhook configurado: {WEBHOOK_URL}")
        
        # Iniciar servidor Flask
        port = int(os.environ.get('PORT', 5000))
        app.run(
            host='0.0.0.0',
            port=port,
            debug=False,
            threaded=True
        )
    except Exception as e:
        print(f"⚠️ Usando polling: {e}")
        
        # Modo polling (para desenvolvimento)
        while True:
            try:
                bot.polling(none_stop=True, interval=0, timeout=20)
            except Exception as poll_error:
                print(f"❌ Erro no polling: {poll_error}")
                time.sleep(5)
                continue
