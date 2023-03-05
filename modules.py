import json
import requests
import telebot
from telebot import types
from get_material import conversion_name, log
from main import bot, red
from datetime import datetime

MATERIALS = {'Профиль': 'profile', 'Светодиодные модули': 'module', 'Драйвера': 'driver', 'Крышки': 'cover',
             'Система крепления': 'mounting_system'}

ADD_MATERIALS = {'Добавить профиль': 'profile', 'Добавить светодиодные модули': 'module',
                 'Добавить драйвера': 'driver',
                 'Добавить крышки': 'cover', 'Добавить систему крепления': 'mounting_system'}

DEL_MATERIALS = {'Списать профиль': 'profile', 'Списать светодиодные модули': 'module',
                 'Списать драйвера': 'driver',
                 'Списать крышки': 'cover', 'Списать систему крепления': 'mounting_system'}

CREATE_MATERIALS = {'Категория профиль': 'profile', 'Категория светодиодные модули': 'module',
                    'Категория драйвера': 'driver',
                    'Категория крышки': 'cover', 'Категория система крепления': 'mounting_system'}


"""CRUD func for materials"""

def add_material_get_name_material(message, chapter, bot):
    """Takes in a message, a chapter, and a bot object as input.
    It then uses the conversion_name() function to convert the message text to a desired format.
    Next, it calls the get_number_of_materials() function to get the number of materials in the
    specified chapter. Using this information, it creates a URL to query a local API.
    If the API returns a 404 status code, the function calls the retry_get_value() function.
    Otherwise, it prompts the user for the amount of material and registers
    the add_material_get_value_material() function to handle the input."""
    data = conversion_name(message.text)
    number_materials = get_number_of_materials(chapter)
    url = f'http://web:9000/api/{chapter}/{number_materials.get(data)}/'
    if requests.get(url).status_code == 404:
        retry_get_value(message, chapter, bot)
    else:
        inp = bot.send_message(message.chat.id, 'Теперь количество')
        bot.register_next_step_handler(inp, add_material_get_value_material, data, chapter, url)


def add_material_get_value_material(message, data, chapter, url):
    """Takes in a message, data, chapter, and url as input.
    It sends a GET request to the specified URL to retrieve the previous value of the material.
    Then, it prompts the user for the amount of material to add and updates the value accordingly.
    The function then sends a PUT request to update the material value in the local API.
    It logs the user action, material name, and value added to the system log.
    Finally, the function sends a message to the user confirming that the material has been added."""
    previous_value_request = requests.get(url)
    last_value_json = previous_value_request.json()
    last_value = last_value_json['value']
    end_data = {chapter: data,
                'value': int(message.text)}
    end_data['value'] = last_value + end_data['value']
    response = requests.put(url, data=end_data)
    log_data = {'user': int(message.from_user.id),
                'action': 'Добавлено',
                'category': chapter,
                'material': data,
                'value': end_data['value']}
    log(log_data)
    bot.send_message(message.chat.id, f"Материал добавлен")


def del_material_get_name_material(message, chapter, bot):
    """Takes in a message, a chapter, and a bot object as input.
    It then uses the conversion_name() function to convert the message text to a desired format.
    Next, it calls the get_number_of_materials() function to get the number
    of materials in the specified chapter. Using this information, it creates a URL to query a local API.
    If the API returns a 404 status code, the function calls the retry_get_value() function.
    Otherwise, it prompts the user for the amount of material to delete and registers
    the del_material_get_value_material() function to handle the input."""
    data = conversion_name(message.text)
    number_materials = get_number_of_materials(chapter)
    url = f'http://web:9000/api/{chapter}/{number_materials.get(data)}/'
    if requests.get(url).status_code == 404:
        retry_get_value_del(message, chapter, bot)
    else:
        inp = bot.send_message(message.chat.id, 'Теперь количество')
        bot.register_next_step_handler(inp, del_material_get_value_material, data, chapter, url)


def del_material_get_value_material(message, data, chapter, url):
    """Takes in a message, data, chapter, and url as input. It sends a GET request to the specified URL
    to retrieve the previous value of the material. Then, it prompts the user for the amount of material to delete
    and updates the value accordingly. The function checks if the updated value is less than or equal to the previous
    value. If so, it sends a PUT request to update the material value in the local API. It logs the user action,
    material name, and value removed to the system log. Finally, the function sends a message to the user confirming
    that the material has been removed. If the updated value is greater than the previous value, the function sends a
    message to the user indicating that there is not enough material to be removed. """
    previous_value_request = requests.get(url)
    last_value_json = previous_value_request.json()
    last_value = last_value_json['value']
    end_data = {chapter: data,
                'value': int(message.text)}
    value = end_data['value']
    if (last_value - end_data['value']) >= 0:
        end_data['value'] = last_value - end_data['value']
        response = requests.put(url, data=end_data)
        log_data = {'user': int(message.from_user.id),
                    'action': 'Списано',
                    'category': chapter,
                    'material': data,
                    'value': value}
        log(log_data)
        bot.send_message(message.chat.id, f"Материал списан")
    else:
        bot.send_message(message.chat.id, 'Не хватает матерала')


def create_material_get_name_material(message, chapter, bot):
    """Takes in a message, chapter, and bot as input. It prompts the user for the name of the material
    and sends the user's input to the conversion_name() function to format the material name. Then, it prompts the
    user for the amount of material to create and waits for the user's input. The function passes the formatted
    material name, chapter, and user input to the create_material_get_value_material() function. """
    data = conversion_name(message.text)
    inp = bot.send_message(message.chat.id, 'Теперь количество')
    bot.register_next_step_handler(inp, create_material_get_value_material, data, chapter)


def create_material_get_value_material(message, data, chapter):
    """Takes in a message, data, and chapter as input. It constructs a URL to make a POST request to
    the API endpoint with the formatted chapter and data input to create a new material with the given name and
    amount. Then, it sends a message to the user indicating that the material has been created """
    url = f'http://web:9000/api/{chapter}/'
    end_data = {chapter: data, 'value': int(message.text)}
    response = requests.post(url, data=end_data)
    bot.send_message(message.chat.id, f"Материал создан")


def retry_get_value(message, chapter, bot):
    """Takes in a message, chapter, and bot as input. It sends a message to the user indicating that
    the value input was incorrect and to try again. Then, it registers the next step handler to the
    add_material_get_name_material function with the chapter and bot input. """
    bot.send_message(message.chat.id, f"Неправильное значение, попробуйте еще раз")
    bot.register_next_step_handler(message, add_material_get_name_material, chapter, bot)


def retry_get_value_del(message, chapter, bot):
    """Takes in a message, chapter, and bot as input. It sends a message to the user indicating that
    the value input was incorrect and to try again. Then, it registers the next step handler to the
    add_material_get_name_material function with the chapter and bot input. """
    bot.send_message(message.chat.id, f"Неправильное значение, попробуйте еще раз")
    bot.register_next_step_handler(message, del_material_get_name_material, chapter, bot)


def get_number_of_materials(material):
    """Takes in a material name as input and sends a GET request to the API endpoint to retrieve a list
    of materials with the given name. It then extracts the ID and name of each material and stores it in a dictionary
    where the material name is the key and the ID is the value. The function returns the dictionary. """
    response = requests.get(f'http://web:9000/api/{material}/')
    data = response.json()
    dict_of_material = {item[material]: item['id'] for item in data['results']}
    return dict_of_material


"""Authorization"""


def get_name(message):
    """Receives a message with a username and telegram_id, and sends a request to a server to check if the
    telegram_id matches the username. If the response is successful and the telegram_id matches the username,
    the user is granted access to the bot, and the start_message function is called. Otherwise, the user is informed
    that they do not have access to the bot."""
    username = message.text
    telegram_id = message.from_user.id
    response = requests.get('http://web:9000/check_telegram_id/',
                            params={'username': username, 'telegram_id': telegram_id})
    if response.status_code == 200:
        data = response.json()
        print(data)
        if data['result']:
            bot.send_message(message.chat.id, 'Проверка прошла успешна')
            start_message(message.chat.id)
        else:
            bot.send_message(message.chat.id, 'У вас нет доступа к этому боту')
    else:
        bot.send_message(message.chat.id, 'Неправильные данные')


def check_id_for_functionality(message):
    """Checks if the user has access to the bot based on telegram_id"""
    telegram_id = message.from_user.id
    response = requests.get('http://web:9000/check_functionality/',
                            params={'telegram_id': telegram_id})
    if response.status_code != 200:
        bot.send_message(message.chat.id, 'Вы не можете пользоваться данным ботом')
        return False
    else:
        return True


"""Bot menu buttons"""


def start_message(message_chat_id):
    """Used to send the initial message with a keyboard menu to the user when they first start
    interacting with the bot. It takes the message_chat_id parameter, which is the unique identifier for the chat the
    user is interacting with.

    The function creates a markup object of type telebot.types.ReplyKeyboardMarkup(), which is used to create the
    keyboard menu. The menu consists of several buttons, each with a specific functionality.

    Finally, the function sends the initial message to the user with the keyboard menu using the bot.send_message()
    method, passing the message_chat_id and markup parameters. """
    markup = telebot.types.ReplyKeyboardMarkup()
    markup.row(telebot.types.KeyboardButton('Добавить материал'))
    markup.row(telebot.types.KeyboardButton('Списать материал'))
    markup.row(telebot.types.KeyboardButton('Просмотр количества материала'))
    markup.row(telebot.types.KeyboardButton('Создать новый матерал'))
    markup.row(telebot.types.KeyboardButton('Проекты светильников'))
    markup.row(telebot.types.KeyboardButton('История действий'))
    bot.send_message(message_chat_id, "Добро пожаловать в начальное меню", reply_markup=markup)


"""Actions with lamp projects"""


def send_lamp_page(message, page_url):
    """Sends a list of lamps to the user. It takes a message object and a URL for the page containing
    the lamps as input. It sends an HTTP GET request to the URL to retrieve the list of lamps, and then sends a
    message to the user with an inline keyboard containing buttons for each lamp. Each button is labeled with the
    name of the lamp and has a callback data that includes the ID of the lamp. If there are more pages of lamps,
    a button labeled "Следующая страница" is added to the keyboard with a callback data that includes the URL of the
    next page """
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
    """Sends a POST request to the API endpoint /delete_materials_lamp/ with the dictionary of materials
    used in the lamp. If there is enough material to delete, it sends a success message to the user. If there is not
    enough material to delete, it sends a message to the user that the material is insufficient. """
    materials_lamp = {'type_profile': {'profile': data['use_profile'], 'value': data['value_profile']},
                      'type_module': {'module': data['use_module'], 'value': data['value_module']},
                      'type_driver': {'driver': data['use_driver'], 'value': data['value_driver']},
                      'type_cover': {'cover': data['use_cover'], 'value': data['value_cover']},
                      'type_mounting_system': {'mounting_system': data['use_mounting_system'],
                                               'value': data['value_mounting_system']}}
    url = f'http://web:9000/delete_materials_lamp/'
    headers = {'Content-type': 'application/json'}
    response = requests.post(url, data=json.dumps(materials_lamp), headers=headers)
    if response.status_code == 400:
        bot.send_message(message.chat.id, 'Не хватает матерала')
    else:
        bot.send_message(message.chat.id, 'Материалы светильника списаны')


def get_history_log(message, data):
    """Responsible for retrieving the history log for the bot's actions, which includes the user who performed the
    action, the material that was affected, the quantity of material that was affected, and the date of the action.
    If there are more pages of history to display, the function will also display a "next page" button to allow the
    user to view more history. """
    for history in data['results']:
        response_name = requests.get(f'http://web:9000/get_username_by_telegram_id/{history["user"]}/')
        name_user = response_name.json()
        mess = f'Пользователь {name_user["username"]}: {history["action"]} {history["material"]} ' \
               f'в количестве {history["value"]} шт. Дата: {formate_date(history["date_update"])}'
        bot.send_message(message.chat.id, mess)
    if data['next']:
        next_page = json.dumps(data['next']).encode('utf8')
        red.set('history_log_page', next_page)
        markup = telebot.types.ReplyKeyboardMarkup(row_width=1)
        button_1 = telebot.types.KeyboardButton('Следующая страница истории действий')
        button_2 = telebot.types.KeyboardButton('Назад в меню')
        markup.add(button_1, button_2)
        bot.send_message(message.chat.id,
                         "_______________________",
                         reply_markup=markup)
    else:
        markup = telebot.types.ReplyKeyboardMarkup(row_width=1)
        button_1 = telebot.types.KeyboardButton('Назад в меню')
        markup.add(button_1)
        bot.send_message(message.chat.id,
                         "_______________________",
                         reply_markup=markup)


def history_log_next_page_use(message, next_page):
    """Appears to be a continuation of the get_history_log function and handles the logic for
    displaying the next page of history logs.

    The next_page argument contains a URL for the next page of history logs, which is used to make a GET request to the
    server. The response data is then processed similarly to the get_history_log function to extract the relevant
    information and display it to the user.

    If the server response contains a next page URL, the URL is stored in Redis for later use and a new keyboard markup is created to allow the user to navigate to the next page or back to the main menu. If there is no next page, a different keyboard markup is created with only an option to go back to the main menu."""
    page_num = next_page.split('/')[-1]
    response = requests.get(f'http://web:9000/api/history_log/{page_num}')
    response_json = response.json()
    for history in response_json['results']:
        response_name = requests.get(f'http://web:9000/get_username_by_telegram_id/{history["user"]}/')
        name_user = response_name.json()
        mess = f'Пользователь {name_user["username"]}: {history["action"]} {history["material"]} ' \
               f'в количестве {history["value"]} шт. Дата: {formate_date(history["date_update"])}'
        bot.send_message(message.chat.id, mess)
    if response_json['next']:
        next_page = json.dumps(response_json['next']).encode('utf8')
        red.set('history_log_page', next_page)
        markup = telebot.types.ReplyKeyboardMarkup(row_width=1)
        button_1 = telebot.types.KeyboardButton('Следующая страница истории действий')
        button_2 = telebot.types.KeyboardButton('Назад в меню')
        markup.add(button_1, button_2)
        bot.send_message(message.chat.id,
                         "_______________________",
                         reply_markup=markup)
    else:
        markup = telebot.types.ReplyKeyboardMarkup(row_width=1)
        button_1 = telebot.types.KeyboardButton('Назад в меню')
        markup.add(button_1)
        bot.send_message(message.chat.id,
                         "_______________________",
                         reply_markup=markup)


def formate_date(date):
    """Takes a date in string format and converts it to a formatted string with the day, month, year,
    hours, and minutes. """
    date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ')
    formatted_date = datetime.strftime(date, '%d.%m.%Y - %H.%M')
    return formatted_date
