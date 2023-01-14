import telebot
from dotenv import load_dotenv
import os
load_dotenv()


bot = telebot.TeleBot(os.getenv('TOKEN_API'))


@bot.message_handler(commands=['start'])
def start_message(message):
    markup = telebot.types.ReplyKeyboardMarkup()
    markup.row(telebot.types.KeyboardButton('Menu'))
    bot.send_message(message.chat.id, "Welcome! Press the 'Menu' button to see options.", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == 'Menu':
        bot.send_message(message.chat.id, "Menu: \n1. Option 1 \n2. Option 2 \n3. Option 3")


bot.polling()

