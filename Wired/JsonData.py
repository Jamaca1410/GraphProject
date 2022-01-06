import json


def Json():
    #Guardamos los datos del Json en una variable llamada data
    File = open('json_data.json', 'r')
    data = json.load(File)
    File.close()

    return data

