import requests
import telebot
from dotenv import load_dotenv
import os
from telebot import types
from get_material import *
from materials import get_number_of_materials, MATERIALS

load_dotenv()


bot = telebot.TeleBot(os.getenv('TOKEN_API'))


@bot.message_handler(commands=['start'])
def start_message(message):
    markup = telebot.types.ReplyKeyboardMarkup()
    markup.row(telebot.types.KeyboardButton('Добавить материал'))
    markup.row(telebot.types.KeyboardButton('Списать материал'))
    markup.row(telebot.types.KeyboardButton('Просмотр количества материала'))
    bot.send_message(message.chat.id, "Добро пожаловать в начальное меню", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Назад в меню')
def handle_menu_button(message):
    start_message(message)


def add_materials(message, chapter):
    number_profile = get_number_of_materials(chapter)
    data = message.text.split()
    new_dict = {chapter: data[0], 'value': data[1]}
    url = f'http://127.0.0.1:9000/api/{chapter}/{number_profile.get(data[0])}/'
    previous_value_request = requests.get(url)
    last_value_json = previous_value_request.json()
    last_value = last_value_json['value']
    new_dict['value'] = last_value + int(data[1])
    response = requests.put(url, data=new_dict)
    bot.send_message(message.chat.id, f"Материал добавлен")

@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == 'Добавить материал':
        markup = telebot.types.ReplyKeyboardMarkup(row_width=1)
        button_1 = telebot.types.KeyboardButton('Добавить профиль')
        button_2 = telebot.types.KeyboardButton('Добавить светодиодные модули')
        button_3 = telebot.types.KeyboardButton('Добавить драйвера')
        button_4 = telebot.types.KeyboardButton('Добавить крышки')
        button_5 = telebot.types.KeyboardButton('Добавить систему крепления')
        button_6 = types.KeyboardButton('Назад в меню')
        markup.add(button_1, button_2, button_3, button_4, button_5, button_6)
        bot.send_message(message.chat.id,
                         "Menu: \n1. Профиль 1 \n2. Светодиодные модули \n3. Драйвера \n4. Крышки \n5. Крепления",
                         reply_markup=markup)
    elif message.text == 'Добавить профиль':
        chapter = 'profile'
        bot.send_message(message.chat.id, "Пожалуйста, введите наименование профиля и количество, которое хотите"
                                          " добавить")
        bot.register_next_step_handler(message, add_materials, chapter)
    elif message.text == 'Добавить светодиодные модули':
        chapter = 'module'
        bot.send_message(message.chat.id, "Пожалуйста, введите наименование светодиодных модулей и количество, "
                                          "которое хотите добавить")
        bot.register_next_step_handler(message, add_materials, chapter)
    elif message.text == 'Добавить драйвера':
        chapter = 'driver'
        bot.send_message(message.chat.id, "Пожалуйста, введите наименование драйвера и количество, которое хотите"
                                          " добавить")
        bot.register_next_step_handler(message, add_materials, chapter)
    elif message.text == 'Добавить крышки':
        chapter = 'cover'
        bot.send_message(message.chat.id, "Пожалуйста, введите наименование крышек и количество, которое хотите"
                                          " добавить")
        bot.register_next_step_handler(message, add_materials, chapter)
    elif message.text == 'Добавить систему крепления':
        chapter = 'mounting_system'
        bot.send_message(message.chat.id, "Пожалуйста, введите наименование системы крепления и количество, "
                                          "которое хотите добавить")
        bot.register_next_step_handler(message, add_materials, chapter)

    if message.text == 'Списать материал':
        markup = telebot.types.ReplyKeyboardMarkup(row_width=1)
        button_1 = telebot.types.KeyboardButton('Профиль')
        button_2 = telebot.types.KeyboardButton('Светодиодные модули')
        button_3 = telebot.types.KeyboardButton('Драйвера')
        button_4 = telebot.types.KeyboardButton('Крышки')
        button_5 = telebot.types.KeyboardButton('Система крепления')
        button_6 = types.KeyboardButton('Назад в меню')
        markup.add(button_1, button_2, button_3, button_4, button_5, button_6)
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
        button_6 = types.KeyboardButton('Назад в меню')
        markup.add(button_1, button_2, button_3, button_4, button_5, button_6)
        bot.send_message(message.chat.id,
                'Menu: \n1. Профиль \n2. Светодиодные модули 2 \n3. Драйвера \n4. Крышки \n5. Система крепления',
                reply_markup=markup)
    elif message.text in list(MATERIALS.keys()):
        response = requests.get(f'http://127.0.0.1:9000/api/{MATERIALS[message.text]}/')
        data = response.json()
        bot.send_message(message.chat.id, get_all_materials(data, MATERIALS[message.text]))


bot.polling()
