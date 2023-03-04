import json

import telebot
from dotenv import load_dotenv
import os
import redis

from get_material import *
from modules import *

load_dotenv()

red = redis.StrictRedis(
    host='localhost',
    port=6379,
    password=''
)

bot = telebot.TeleBot(os.getenv('TOKEN_API'))


@bot.message_handler(commands=['start'])
def start_handler(message):
    inp = bot.send_message(message.chat.id, 'Введите логин')
    bot.register_next_step_handler(message, get_name)


@bot.message_handler(func=lambda message: message.text == 'Назад в меню')
def handle_menu_button(message):
    start_message(message.chat.id)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    if check_id_for_functionality(message):
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
                             "Выберите одну из опций",
                             reply_markup=markup)
        elif message.text in list(ADD_MATERIALS.keys()):
            chapter = ADD_MATERIALS[message.text]
            response = requests.get(f'http://127.0.0.1:9000/api/{ADD_MATERIALS[message.text]}/')
            data = response.json()
            bot.send_message(message.chat.id, "Количество материала на складе. Пожалуйста, введите "
                                            "наименование, которое хотите добавить")
            bot.send_message(message.chat.id, get_all_materials(data, ADD_MATERIALS[message.text]))
            bot.register_next_step_handler(message, add_material_get_name_material, chapter, bot)


        if message.text == 'Списать материал':
            markup = telebot.types.ReplyKeyboardMarkup(row_width=1)
            button_1 = telebot.types.KeyboardButton('Списать профиль')
            button_2 = telebot.types.KeyboardButton('Списать светодиодные модули')
            button_3 = telebot.types.KeyboardButton('Списать драйвера')
            button_4 = telebot.types.KeyboardButton('Списать крышки')
            button_5 = telebot.types.KeyboardButton('Списать систему крепления')
            button_6 = types.KeyboardButton('Назад в меню')
            markup.add(button_1, button_2, button_3, button_4, button_5, button_6)
            bot.send_message(message.chat.id,
                             "Выберите категорию",
                             reply_markup=markup)
        elif message.text in list(DEL_MATERIALS.keys()):
            chapter = DEL_MATERIALS[message.text]
            response = requests.get(f'http://127.0.0.1:9000/api/{DEL_MATERIALS[message.text]}/')
            data = response.json()
            bot.send_message(message.chat.id, "Пожалуйста, введите наименование и количество, которое хотите"
                                              " списать")
            bot.send_message(message.chat.id, get_all_materials(data, DEL_MATERIALS[message.text]))
            bot.register_next_step_handler(message, del_material_get_name_material, chapter, bot)




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
                    'Выбирайте категорию',
                    reply_markup=markup)
        elif message.text in list(MATERIALS.keys()):
            response = requests.get(f'http://127.0.0.1:9000/api/{MATERIALS[message.text]}/')
            data = response.json()
            bot.send_message(message.chat.id, get_all_materials(data, MATERIALS[message.text]))




        if message.text == 'Создать новый матерал':
            markup = telebot.types.ReplyKeyboardMarkup(row_width=1)
            button_1 = telebot.types.KeyboardButton('Категория профиль')
            button_2 = telebot.types.KeyboardButton('Категория светодиодные модули')
            button_3 = telebot.types.KeyboardButton('Категория драйвера')
            button_4 = telebot.types.KeyboardButton('Категория крышки')
            button_5 = telebot.types.KeyboardButton('Категория система крепления')
            button_6 = types.KeyboardButton('Назад в меню')
            markup.add(button_1, button_2, button_3, button_4, button_5, button_6)
            bot.send_message(message.chat.id,
                             "Выбирайте категорию",
                             reply_markup=markup)
        elif message.text in list(CREATE_MATERIALS.keys()):
            chapter = CREATE_MATERIALS[message.text]
            bot.send_message(message.chat.id, "Пожалуйста, введите "
                                            "наименование материала, которое хотите создать")
            bot.register_next_step_handler(message, create_material_get_name_material, chapter, bot)

        if message.text == 'Проекты светильников':
            send_lamp_page(message, 'http://127.0.0.1:9000/api/lamp/')
            @bot.callback_query_handler(func=lambda call: call.data.startswith('next_page_'))
            def handle_next_page(call):
                page_url = call.data.replace('next_page_', '')
                send_lamp_page(call.message, page_url)

        if message.text == 'Списать материалы светильника':
            choice = red.get('last_choices_lamp')
            choice_decode = json.loads(choice.decode('utf-8'))
            delete_materials_lamp(message, choice_decode)

        if message.text == 'История действий':
            response = requests.get(f'http://127.0.0.1:9000/api/history_log/')
            data = response.json()
            get_history_log(message, data)



        elif message.text == 'Следующая страница истории действий':
            history_log_next_page = red.get('history_log_page')
            history_log_data = json.loads(history_log_next_page.decode('utf-8'))
            history_log_next_page_use(message, next_page=history_log_data)


    else:
        bot.send_message(message.chat.id, 'Доступ закрыт')
        return



@bot.callback_query_handler(func=lambda call: call.data.startswith('lamp_'))
def show_lamp_info(call):
    lamp_id = call.data.split('_')[1]
    response = requests.get(f'http://127.0.0.1:9000/api/lamp/{lamp_id}')
    lamp = response.json()
    last_choices_lamp = json.dumps(lamp).encode('utf8')
    red.set('last_choices_lamp', last_choices_lamp)
    mess = f'Светильник: {lamp["name_lamp"]}\n'
    mess += f'Профиль: {lamp["use_profile"]} ({lamp["value_profile"]})\n'
    mess += f'Светодиодный модуль: {lamp["use_module"]} ({lamp["value_module"]})\n'
    mess += f'Драйвер: {lamp["use_driver"]} ({lamp["value_driver"]})\n'
    mess += f'Крышки: {lamp["use_cover"]} ({lamp["value_cover"]})\n'
    mess += f'Крепление: {lamp["use_mounting_system"]} ({lamp["value_mounting_system"]})\n\n'
    bot.send_message(call.message.chat.id, mess)
    markup = telebot.types.ReplyKeyboardMarkup(row_width=1)
    button_1 = telebot.types.KeyboardButton('Списать материалы светильника')
    buttom_2 = telebot.types.KeyboardButton('Назад в меню')
    markup.add(button_1, buttom_2)
    bot.send_message(call.message.chat.id, "_______________________", reply_markup=markup)


if __name__ == "__main__":
    bot.polling()
