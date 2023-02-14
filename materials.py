import requests

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
