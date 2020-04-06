import json


def read():
    data = []
    with open('./config/sensordata.txt', 'r') as file:
        jsonInput = json.load(file)
        for sensor in jsonInput:
            data.append(sensor["id"])
    return data


def read1():
    data = []
    with open('./config/actuatordata.txt', 'r') as file:
        jsonInput = json.load(file)
        for actuator in jsonInput:
            data.append(actuator["id"])
    return data

