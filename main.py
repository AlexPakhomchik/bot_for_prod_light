import requests
import telebot
from dotenv import load_dotenv
import os
from telebot import types
from get_material import *
from materials import get_number_of_materials, MATERIALS, DEL_MATERIALS, ADD_MATERIALS

load_dotenv()


bot = telebot.TeleBot(os.getenv('TOKEN_API'))


@bot.message_handler(commands=['start'])
def start_message(message):
    """
    This function serves as the starting point for the bot's interaction with the user. It displays a set of options for the user to choose from.

    Parameters:
    message (telebot.types.Message): A Message object that represents the incoming message from the user.
    """
    id_user = message.from_user.id
    print(id_user)
    markup = telebot.types.ReplyKeyboardMarkup()
    markup.row(telebot.types.KeyboardButton('Добавить материал'))
    markup.row(telebot.types.KeyboardButton('Списать материал'))
    markup.row(telebot.types.KeyboardButton('Просмотр количества материала'))
    bot.send_message(message.chat.id, "Добро пожаловать в начальное меню", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Назад в меню')
def handle_menu_button(message):
    """
    This function is used to return back to the main menu when the "Назад в меню" button is pressed.
The main menu is displayed by calling the start_message function.
    """
    start_message(message)


def add_material_get_name_material(message, chapter):
    """
    This function takes two parameters as input:
    - message (object): The message object received from the chat API.
    - chapter (object): The chapter object associated with the material being added.

    The function prompts the user for the name of the material to be added. Once the name is received, the function calls
    the add_material_get_value_material function to prompt the user for the quantity of the material.
    """
    data = message.text.upper()
    inp = bot.send_message(message.chat.id, 'Теперь количество')
    bot.register_next_step_handler(inp, add_material_get_value_material, data, chapter)


def add_material_get_value_material(message, data, chapter):
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
    number_materials = get_number_of_materials(chapter)
    url = f'http://127.0.0.1:9000/api/{chapter}/{number_materials.get(data)}/'
    previous_value_request = requests.get(url)
    last_value_json = previous_value_request.json()
    last_value = last_value_json['value']
    end_data = {chapter: data, 'value': int(message.text)}
    end_data['value'] = last_value + end_data['value']
    response = requests.put(url, data=end_data)
    bot.send_message(message.chat.id, f"Материал добавлен")


def del_materials(message, chapter):
    number_materials = get_number_of_materials(chapter)
    data = message.text.split()
    new_dict = {chapter: data[0], 'value': data[1]}
    url = f'http://127.0.0.1:9000/api/{chapter}/{number_materials.get(data[0])}/'
    previous_value_request = requests.get(url)
    last_value_json = previous_value_request.json()
    last_value = last_value_json['value']
    new_dict['value'] = last_value - int(data[1])
    response = requests.put(url, data=new_dict)
    bot.send_message(message.chat.id, f"Материал списан")

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
                         "Menu: \n1. Профиль \n2. Светодиодные модули \n3. Драйвера \n4. Крышки \n5. Крепления",
                         reply_markup=markup)
    elif message.text in list(ADD_MATERIALS.keys()):
        chapter = ADD_MATERIALS[message.text]
        response = requests.get(f'http://127.0.0.1:9000/api/{ADD_MATERIALS[message.text]}/')
        data = response.json()
        bot.send_message(message.chat.id, "Пожалуйста, введите "
                                        "наименование и количество, которое хотите добавить")
        bot.send_message(message.chat.id, get_all_materials(data, ADD_MATERIALS[message.text]))
        bot.register_next_step_handler(message, add_material_get_name_material, chapter)


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
                         "Menu: \n1. Option 1 \n2. Option 2 \n3. Option 3 \n4. Option 4 \n5. Option 5",
                         reply_markup=markup)
    elif message.text in list(DEL_MATERIALS.keys()):
        chapter = DEL_MATERIALS[message.text]
        response = requests.get(f'http://127.0.0.1:9000/api/{DEL_MATERIALS[message.text]}/')
        data = response.json()
        bot.send_message(message.chat.id, "Пожалуйста, введите наименование и количество, которое хотите"
                                          " списать")
        bot.send_message(message.chat.id, get_all_materials(data, DEL_MATERIALS[message.text]))
        bot.register_next_step_handler(message, del_materials, chapter)




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

    if message.text == 'test':
        inp = bot.send_message(message.chat.id, 'Введите наименование профиля')
        bot.register_next_step_handler(inp, data_1)





bot.polling()
