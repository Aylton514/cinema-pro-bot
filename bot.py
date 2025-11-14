import os
import telebot
import sqlite3
import time
from flask import Flask, request

# 🔐 SUAS CONFIGURAÇÕES
TOKEN = "8306714275:AAGzNXE3TZKbe5-49YGTgNOMrJiLVxBjmLA"
ADMIN_USERNAME = "ayltonanna7"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# 💎 SEUS CONTATOS
CONTATOS = {
    'whatsapp': '848568229',
    'telegram': '@ayltonanna7',
    'email': 'ayltonanna7@gmail.com',
    'mpesa': '848568229', 
    'emola': '870612404',
    'paypal': 'ayltonanna7@gmail.com'
}

# 🎯 COMANDO START SIMPLES E FUNCIONAL
@bot.message_handler(commands=['start'])
def start_cmd(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row(
        telebot.types.InlineKeyboardButton("🎬 Ver Catálogo", callback_data="catalogo"),
        telebot.types.InlineKeyboardButton("💰 Comprar Créditos", callback_data="comprar")
    )
    markup.row(
        telebot.types.InlineKeyboardButton("📞 Atendimento", url=f"https://t.me/{ADMIN_USERNAME}"),
        telebot.types.InlineKeyboardButton("🌎 PayPal", callback_data="paypal")
    )
    
    bot.reply_to(message, f"""
🎬 *CINEMA PRO PREMIUM* 🎬

*Sistema Exclusivo de Filmes e Séries*

💎 *Catálogo Completo:*
• Filmes em 4K Ultra HD
• Séries completas
• Animes legendados
• Lançamentos 2025

⚡ *Entrega em 15-30 minutos!*

💰 *Preços:*
• 1 crédito = 40 MT
• 3 créditos = 100 MT (economia)
• VIP Mensal = 600 MT

📞 *Atendimento:*
WhatsApp: {CONTATOS['whatsapp']}
Telegram: @{ADMIN_USERNAME}

💎 *Escolha uma opção abaixo:*
    """, parse_mode='Markdown', reply_markup=markup)

# 📺 CATÁLOGO
@bot.message_handler(commands=['catalogo'])
def catalogo_cmd(message):
    bot.reply_to(message, """
🎬 *CATÁLOGO PREMIUM 2025* 🎬

🎥 *FILMES EM 4K:*
• VENOM 3: A Última Batalha
• AVATAR 4: O Legado 
• SPIDER-MAN: BEYOND
• JOHN WICK 5
• DEMON SLAYER: FINAL ARC

📺 *SÉRIES COMPLETAS:*
• STRANGER THINGS 5
• THE LAST OF US 3
• THE WITCHER 5
• HOUSE OF THE DRAGON 2
• ROUND 6: SEASON 2

🎌 *ANIMES:*
• ATTACK ON TITAN: FINAL
• ONE PIECE: EGGHEAD
• JUJUTSU KAISEN 3
• MY HERO ACADEMIA 7

💎 *Para pedir:*
`/pedir Nome do Filme`

🎯 *Exemplo:*
`/pedir VENOM 3`
    """, parse_mode='Markdown')

# 💰 PLANOS
@bot.message_handler(commands=['planos'])
def planos_cmd(message):
    bot.reply_to(message, f"""
💰 *PLANOS CINEMA PRO* 💰

💎 *CRÉDITOS:*
• 1 Crédito = 40 MT
• 3 Créditos = 100 MT (economize 20 MT)
• 10 Créditos = 350 MT (economize 50 MT)

👑 *VIP:*
• VIP Semanal = 200 MT
• VIP Mensal = 600 MT
• VIP Trimestral = 1500 MT

💳 *PAGAMENTO:*
📱 M-PESA: `{CONTATOS['mpesa']}`
📱 e-MOLA: `{CONTATOS['emola']}`
🌎 PAYPAL: `{CONTATOS['paypal']}`

📞 *Como comprar:*
1. Envie o valor para um dos números
2. Envie comprovante para atendimento
3. Ativação em 5-10 minutos!

💬 Atendimento: @{ADMIN_USERNAME}
    """, parse_mode='Markdown')

# 🌎 PAYPAL
@bot.message_handler(commands=['paypal'])
def paypal_cmd(message):
    bot.reply_to(message, f"""
💳 *PAYPAL - PAGAMENTO INTERNACIONAL* 💳

💰 *PREÇOS EM DÓLAR:*
• 1 Crédito = $2.50
• 3 Créditos = $6.00
• 10 Créditos = $20.00
• VIP Mensal = $35.00

🔒 *COMO PAGAR:*

1️⃣ *ENVIE PARA:*
PayPal: `{CONTATOS['paypal']}`
Nome: AILTON ARMINDO NHAMONEQUE

2️⃣ *ENVIE COMPROVANTE PARA:*
WhatsApp: {CONTATOS['whatsapp']}
Telegram: @{ADMIN_USERNAME}

3️⃣ *RECEBA SEUS CRÉDITOS* em 5-10 minutos!

⚡ *Sistema 100% Automático!*
    """, parse_mode='Markdown')

# 🎯 PEDIDOS
@bot.message_handler(commands=['pedir'])
def pedir_cmd(message):
    filme = message.text.replace('/pedir', '').strip()
    
    if not filme:
        bot.reply_to(message, """
🎬 *FAZER PEDIDO*

📝 *Use o formato:*
`/pedir Nome do Filme`

🎯 *Exemplos:*
`/pedir VENOM 3`
`/pedir STRANGER THINGS 5`
`/pedir DEMON SLAYER`

💎 *Custo: 1 crédito (40 MT)*

💰 *Sem créditos? Use /planos*
        """, parse_mode='Markdown')
        return
    
    # Simular pedido (em produção você teria database)
    bot.reply_to(message, f"""
✅ *PEDIDO REGISTRADO!*

🎬 *Filme:* {filme}
💎 *Status:* Processando
📨 *Entrega:* 15-30 minutos

📞 *Acompanhe seu pedido:*
💬 WhatsApp: {CONTATOS['whatsapp']}
👤 Telegram: @{ADMIN_USERNAME}

⚡ *Obrigado pela preferência!*
    """, parse_mode='Markdown')

# 🎪 BOTÕES INTERATIVOS
@bot.callback_query_handler(func=lambda call: True)
def handle_buttons(call):
    chat_id = call.message.chat.id
    
    if call.data == 'catalogo':
        catalogo_cmd(call.message)
    elif call.data == 'comprar':
        planos_cmd(call.message)
    elif call.data == 'paypal':
        paypal_cmd(call.message)
    
    bot.answer_callback_query(call.id)

# 🌐 CONFIGURAÇÃO WEB
@app.route('/')
def home():
    return "🤖 CINEMA PRO BOT - ONLINE! 🎬"

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
    print("🚀 BOT INICIADO!")
    print(f"💎 Admin: @{ADMIN_USERNAME}")
    
    # Configurar webhook para Railway
    bot.remove_webhook()
    time.sleep(1)
    
    # No Railway a URL é automática, então usamos polling como fallback
    try:
        # Tenta webhook primeiro
        bot.set_webhook(url="https://your-app-name.railway.app/webhook")
        print("✅ Webhook configurado")
    except:
        print("⚠️ Usando polling como fallback")
        bot.polling(none_stop=True)
    
    # Inicia servidor web
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)