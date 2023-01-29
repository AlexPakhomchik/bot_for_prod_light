def get_all_materials(json_data, name_material):
    data_str = ''
    for i in range(len(json_data)):
        data = json_data[i]
        print(data)
        data_str += str(data[name_material]) + '  --  ' + str(data['value']) + ' шт(м). \n'
    return data_str

