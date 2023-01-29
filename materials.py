import requests

MATERIALS = {'Профиль': 'profile', 'Светодиодные модули': 'module', 'Драйвера': 'driver', 'Крышки': 'cover',
             'Система крепления': 'mounting_system'}

ADD_MATERIALS = {'Добавить профиль': 'profile', 'Добавить светодиодные модули': 'module', 'Добавить драйвера': 'driver',
                 'Добавить крышки': 'cover', 'Добавить систему крепления': 'mounting_system'}

DEL_MATERIALS = {'Списать профиль': 'profile', 'Списать светодиодные модули': 'module', 'Списать драйвера': 'driver',
                 'Списать крышки': 'cover', 'Списать систему крепления': 'mounting_system'}

def get_number_of_materials(material):
    response = requests.get(f'http://127.0.0.1:9000/api/{material}/')
    data = response.json()
    count = 1
    dict_of_material = {}
    for i in data:
        dict_of_material[i[material]] = count
        count += 1
    return dict_of_material
