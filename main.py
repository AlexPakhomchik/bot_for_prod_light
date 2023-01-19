import json

import requests
import telebot
from dotenv import load_dotenv
import os

from get_material import *

load_dotenv()


bot = telebot.TeleBot(os.getenv('TOKEN_API'))


@bot.message_handler(commands=['start'])
def start_message(message):
    markup = telebot.types.ReplyKeyboardMarkup()
    markup.row(telebot.types.KeyboardButton('Добавить материал'))
    markup.row(telebot.types.KeyboardButton('Списать материал'))
    markup.row(telebot.types.KeyboardButton('Просмотр количества материала'))
    bot.send_message(message.chat.id, "Welcome! Press the 'Menu' button to see options.", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == 'Добавить материал':
        markup = telebot.types.ReplyKeyboardMarkup(row_width=1)
        button_1 = telebot.types.KeyboardButton('Профиль')
        button_2 = telebot.types.KeyboardButton('Светодиодные модули')
        button_3 = telebot.types.KeyboardButton('Драйвера')
        button_4 = telebot.types.KeyboardButton('Крышки')
        button_5 = telebot.types.KeyboardButton('Система крепления')
        markup.add(button_1, button_2, button_3, button_4, button_5)
        bot.send_message(message.chat.id,
                         "Menu: \n1. Option 1 \n2. Option 2 \n3. Option 3 \n4. Option 4 \n5. Option 5",
                         reply_markup=markup)

    if message.text == 'Списать материал':
        markup = telebot.types.ReplyKeyboardMarkup(row_width=1)
        button_1 = telebot.types.KeyboardButton('Профиль')
        button_2 = telebot.types.KeyboardButton('Светодиодные модули')
        button_3 = telebot.types.KeyboardButton('Драйвера')
        button_4 = telebot.types.KeyboardButton('Крышки')
        button_5 = telebot.types.KeyboardButton('Система крепления')
        markup.add(button_1, button_2, button_3, button_4, button_5)
        bot.send_message(message.chat.id,
                         "Menu: \n1. Option 1 \n2. Option 2 \n3. Option 3 \n4. Option 4 \n5. Option 5",
                         reply_markup=markup)

    if message.text == 'Просмотр количества материала':
        markup = telebot.types.ReplyKeyboardMarkup(row_width=1)
        button_1 = telebot.types.KeyboardButton('Профиль')
        button_2 = telebot.types.KeyboardButton('Светодиодные модули')
        button_3 = telebot.types.KeyboardButton('Драйвера')
        button_4 = telebot.types.KeyboardButton('Крышки')
        button_5 = telebot.types.KeyboardButton('Система крепления')
        markup.add(button_1, button_2, button_3, button_4, button_5)
        bot.send_message(message.chat.id,
                'Menu: \n1. Профиль \n2. Светодиодные модули 2 \n3. Драйвера \n4. Крышки \n5. Система крепления',
                reply_markup=markup)
    elif message.text == 'Профиль':
        response = requests.get('http://127.0.0.1:9000/profile/')
        data = response.json()
        bot.send_message(message.chat.id, get_all_profile(data))
    elif message.text == 'Светодиодные модули':
        response = requests.get('http://127.0.0.1:9000/module/')
        data = response.json()
        bot.send_message(message.chat.id, get_all_module(data))
    elif message.text == 'Драйвера':
        response = requests.get('http://127.0.0.1:9000/driver/')
        data = response.json()
        bot.send_message(message.chat.id, get_all_drivers(data))
    elif message.text == 'Крышки':
        response = requests.get('http://127.0.0.1:9000/cover/')
        data = response.json()
        bot.send_message(message.chat.id, get_all_covers(data))
    elif message.text == 'Система крепления':
        response = requests.get('http://127.0.0.1:9000/mounting_system/')
        data = response.json()
        bot.send_message(message.chat.id, get_all_mounting_system(data))


bot.polling()
