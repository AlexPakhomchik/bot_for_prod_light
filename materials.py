import requests


def get_number_of_materials(material):
    response = requests.get(f'http://127.0.0.1:9000/api/{material}/')
    data = response.json()
    count = 1
    dict_of_material = {}
    for i in data:
        dict_of_material[i[material]] = count
        count += 1
    return dict_of_material
