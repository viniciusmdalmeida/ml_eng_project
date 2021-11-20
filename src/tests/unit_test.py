#Importando bibliotecas nescessárias


def conver_json(data):
    if type(data) != dict and type(data) != list:
        return str(data)
    else:
        if type(data) == dict:
            for key in data:
                data[key] = conver_json(data[key])
        elif type(data) == list:
            for cont in range(len(data)):
                data[cont] = conver_json(data[cont])
    return data
                

def unit_test(config_data,config_test):
    pass
