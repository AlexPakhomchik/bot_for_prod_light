import json

import requests
import telebot
from telebot import types

from get_material import conversion_name
from main import bot

MATERIALS = {'Профиль': 'profile', 'Светодиодные модули': 'module', 'Драйвера': 'driver', 'Крышки': 'cover',
             'Система крепления': 'mounting_system'}

ADD_MATERIALS = {'Добавить профиль': 'profile', 'Добавить светодиодные модули': 'module', 'Добавить драйвера': 'driver',
                 'Добавить крышки': 'cover', 'Добавить систему крепления': 'mounting_system'}

DEL_MATERIALS = {'Списать профиль': 'profile', 'Списать светодиодные модули': 'module', 'Списать драйвера': 'driver',
                 'Списать крышки': 'cover', 'Списать систему крепления': 'mounting_system'}

CREATE_MATERIALS = {'Категория профиль': 'profile', 'Категория светодиодные модули': 'module', 'Категория драйвера': 'driver',
                 'Категория крышки': 'cover', 'Категория система крепления': 'mounting_system'}

LAST_CHOICES_LAMP = {}



def get_number_of_materials(material):
    """
    This function takes one parameter as input:
    - material (str): The name of the material for which to retrieve the count.

    The function makes a GET request to an API endpoint to retrieve data for the specified material. The function returns a
    dictionary mapping the names of the materials to their corresponding count.
    """
    response = requests.get(f'http://127.0.0.1:9000/api/{material}/')
    data = response.json()
    dict_of_material = {item['profile']: item['id'] for item in data}
    return dict_of_material


def add_material_get_name_material(message, chapter, bot):
    """
    This function takes two parameters as input:
    - message (object): The message object received from the chat API.
    - chapter (object): The chapter object associated with the material being added.

    The function prompts the user for the name of the material to be added. Once the name is received, the function calls
    the add_material_get_value_material function to prompt the user for the quantity of the material.
    """
    data = conversion_name(message.text)
    number_materials = get_number_of_materials(chapter)
    url = f'http://127.0.0.1:9000/api/{chapter}/{number_materials.get(data)}/'
    if requests.get(url).status_code == 404:
        retry_get_value(message, chapter, bot)
    else:
        inp = bot.send_message(message.chat.id, 'Теперь количество')
        bot.register_next_step_handler(inp, add_material_get_value_material, data, chapter, url)


def add_material_get_value_material(message, data, chapter, url):
    """
    This function takes three parameters as input:
    - message (object): The message object received from the chat API.
    - data (str): The name of the material to be added.
    - chapter (object): The chapter object associated with the material being added.

    The function retrieves the current number of materials for the specified chapter. It then makes a GET request to an API
    endpoint to retrieve the current value of the material. The function adds the newly provided quantity to the current value
    and updates the material count by making a PUT request to the API endpoint. Finally, the function sends a confirmation
    message to the user indicating that the material has been added.
    """
    previous_value_request = requests.get(url)
    last_value_json = previous_value_request.json()
    last_value = last_value_json['value']
    end_data = {chapter: data, 'value': int(message.text)}
    end_data['value'] = last_value + end_data['value']
    response = requests.put(url, data=end_data)
    bot.send_message(message.chat.id, f"Материал добавлен")


def del_material_get_name_material(message, chapter, bot):
    data = conversion_name(message.text)
    inp = bot.send_message(message.chat.id, 'Теперь количество')
    bot.register_next_step_handler(inp, del_material_get_value_material, data, chapter)


def del_material_get_value_material(message, data, chapter):
    number_materials = get_number_of_materials(chapter)
    url = f'http://127.0.0.1:9000/api/{chapter}/{number_materials.get(data)}/'
    previous_value_request = requests.get(url)
    last_value_json = previous_value_request.json()
    last_value = last_value_json['value']
    end_data = {chapter: data, 'value': int(message.text)}
    end_data['value'] = last_value - end_data['value']
    response = requests.put(url, data=end_data)
    bot.send_message(message.chat.id, f"Материал списан")


def create_material_get_name_material(message, chapter, bot):
    data = conversion_name(message.text)
    inp = bot.send_message(message.chat.id, 'Теперь количество')
    bot.register_next_step_handler(inp, create_material_get_value_material, data, chapter)


def create_material_get_value_material(message, data, chapter):
    url = f'http://127.0.0.1:9000/api/{chapter}/'
    end_data = {chapter: data, 'value': int(message.text)}
    response = requests.post(url, data=end_data)
    bot.send_message(message.chat.id, f"Материал создан")


def retry_get_value(message, chapter, bot):
    bot.send_message(message.chat.id, f"Неправильное значение, попробуйте еще раз")
    bot.register_next_step_handler(message, add_material_get_name_material, chapter, bot)



def get_name(message):
    username = message.text
    telegram_id = message.from_user.id
    response = requests.get('http://127.0.0.1:9000/check_telegram_id/',
                            params={'username': username, 'telegram_id': telegram_id})
    if response.status_code == 200:
        data = response.json()
        print(data)
        if data['result']:
            bot.send_message(message.chat.id, 'Проверка прошла успешна')
            start_message(message.chat.id)
        else:
            print('User does not exist or telegram_id does not match')
    else:
        print('Failed to check telegram_id')

def check_id_for_functionality(message):
    telegram_id = message.from_user.id
    response = requests.get('http://127.0.0.1:9000/check_functionality/',
                            params={'telegram_id': telegram_id})
    if response.status_code != 200:
        bot.send_message(message.chat.id, 'Вы не можете пользоваться данным ботом')
        return False
    else:
        return True



def start_message(message_chat_id):
    markup = telebot.types.ReplyKeyboardMarkup()
    markup.row(telebot.types.KeyboardButton('Добавить материал'))
    markup.row(telebot.types.KeyboardButton('Списать материал'))
    markup.row(telebot.types.KeyboardButton('Просмотр количества материала'))
    markup.row(telebot.types.KeyboardButton('Создать новый матерал'))
    markup.row(telebot.types.KeyboardButton('Проекты светильников'))
    bot.send_message(message_chat_id, "Добро пожаловать в начальное меню", reply_markup=markup)


def send_lamp_page(message, page_url):
    response = requests.get(page_url)
    lamps = response.json()

    for lamp in lamps['results']:
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton(lamp["name_lamp"], callback_data=f'lamp_{lamp["id"]}')
        markup.add(button1)
        bot.send_message(message.chat.id, 'Светильник: ', reply_markup=markup)

    if lamps['next']:
        markup = types.InlineKeyboardMarkup()
        button_next = types.InlineKeyboardButton("Следующая страница",
                                                 callback_data=f'next_page_{lamps["next"]}')
        markup.add(button_next)
        bot.send_message(message.chat.id, 'Выберите светильник:', reply_markup=markup)


def delete_materials_lamp(message, data):
    materials_lamp = {'type_profile': {'profile': data['use_profile'], 'value': data['value_profile']},
                      'type_module': {'module': data['use_module'], 'value': data['value_module']},
                      'type_driver': {'driver': data['use_driver'], 'value': data['value_driver']},
                      'type_cover': {'cover': data['use_cover'], 'value': data['value_cover']},
                      'type_mounting_system': {'mounting_system': data['use_mounting_system'],
                                              'value': data['value_mounting_system']}}
    url = f'http://127.0.0.1:9000/delete_materials_lamp/'
    headers = {'Content-type': 'application/json'}
    response = requests.post(url, data=json.dumps(materials_lamp), headers=headers)
    if response.status_code == 400:
        bot.send_message(message.chat.id, 'Не хватает матерала')
    else:
        bot.send_message(message.chat.id, 'Материалы светильника списаны')

