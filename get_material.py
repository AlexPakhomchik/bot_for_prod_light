def get_all_profile(json_data):
    data_str = ''
    for i in range(len(json_data)):
        data = json_data[i]
        data_str += str(data['profile']) + '  --  ' + str(data['value']) + ' кг. \n'
    return data_str


def get_all_module(json_data):
    data_str = ''
    for i in range(len(json_data)):
        data = json_data[i]
        data_str += str(data['module']) + '  --  ' + str(data['value']) + ' шт. \n'
    return data_str


def get_all_drivers(json_data):
    data_str = ''
    for i in range(len(json_data)):
        data = json_data[i]
        data_str += str(data['drivers']) + '  --  ' + str(data['value']) + ' шт. \n'
    return data_str


def get_all_covers(json_data):
    data_str = ''
    for i in range(len(json_data)):
        data = json_data[i]
        data_str += str(data['cover']) + '  --  ' + str(data['value']) + ' шт. \n'
    return data_str


def get_all_mounting_system(json_data):
    data_str = ''
    for i in range(len(json_data)):
        data = json_data[i]
        data_str += str(data['mounting_system']) + '  --  ' + str(data['value']) + ' шт. \n'
    return data_str
