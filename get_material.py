import requests


def get_all_materials(json_data, name_material):
    """
    Takes two parameters as input:
    - json_data (list): A list of dictionaries representing the material data retrieved from an API.
    - name_material (str): The name of the material to be retrieved.

    The function iterates over the list of material data and retrieves the specified material. The function returns a string
    containing the name and quantity of the material.
    """
    data_str = ''
    for i in range(len(json_data['results'])):
        data = json_data['results'][i]
        data_str += str(data[name_material]) + '  --  ' + str(data['value']) + ' шт(м). \n'
    return data_str


def conversion_name(name):
    """Takes a name string as input and returns a formatted string with underscores separating each
    word and all letters converted to uppercase. """
    step_1 = name.split(' ')
    step_2 = list(filter(lambda x: x.strip(), step_1))
    return '_'.join(step_2).upper()


def log(add_data_list_history):
    """This function sends a POST request to the server's history_log API endpoint with add_data_list_history data."""
    response = requests.post('http://127.0.0.1:9000/api/history_log/', data=add_data_list_history)

