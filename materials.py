import requests

from main import bot

MATERIALS = {'Профиль': 'profile', 'Светодиодные модули': 'module', 'Драйвера': 'driver', 'Крышки': 'cover',
             'Система крепления': 'mounting_system'}

ADD_MATERIALS = {'Добавить профиль': 'profile', 'Добавить светодиодные модули': 'module', 'Добавить драйвера': 'driver',
                 'Добавить крышки': 'cover', 'Добавить систему крепления': 'mounting_system'}

DEL_MATERIALS = {'Списать профиль': 'profile', 'Списать светодиодные модули': 'module', 'Списать драйвера': 'driver',
                 'Списать крышки': 'cover', 'Списать систему крепления': 'mounting_system'}

CREATE_MATERIALS = {'Категория профиль': 'profile', 'Категория светодиодные модули': 'module', 'Категория драйвера': 'driver',
                 'Категория крышки': 'cover', 'Категория система крепления': 'mounting_system'}

def get_number_of_materials(material):
    """
    This function takes one parameter as input:
    - material (str): The name of the material for which to retrieve the count.

    The function makes a GET request to an API endpoint to retrieve data for the specified material. The function returns a
    dictionary mapping the names of the materials to their corresponding count.
    """
    response = requests.get(f'http://127.0.0.1:9000/api/{material}/')
    data = response.json()
    count = 1
    dict_of_material = {}
    for i in data:
        dict_of_material[i[material]] = count
        count += 1
    return dict_of_material


def add_material_get_name_material(message, chapter, bot):
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
    print("Adding")
    number_materials = get_number_of_materials(chapter)
    url = f'http://127.0.0.1:9000/api/{chapter}/{number_materials.get(data)}/'
    previous_value_request = requests.get(url)
    last_value_json = previous_value_request.json()
    last_value = last_value_json['value']
    end_data = {chapter: data, 'value': int(message.text)}
    end_data['value'] = last_value + end_data['value']
    response = requests.put(url, data=end_data)
    bot.send_message(message.chat.id, f"Материал добавлен")


def del_material_get_name_material(message, chapter, bot):
    data = message.text.upper()
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
    data = message.text.upper()
    inp = bot.send_message(message.chat.id, 'Теперь количество')
    bot.register_next_step_handler(inp, create_material_get_value_material, data, chapter)


def create_material_get_value_material(message, data, chapter):
    url = f'http://127.0.0.1:9000/api/{chapter}/'
    end_data = {chapter: data, 'value': int(message.text)}
    response = requests.post(url, data=end_data)
    bot.send_message(message.chat.id, f"Материал создан")