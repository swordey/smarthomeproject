from socketclass import *
import time
import json
import collections


class Actuator:  # Actuator class to save actuator data
    def __init__(self, f_parent,f_id='default',f_ip='127.0.0.1'):
        self.id = f_id
        self.name = f_id
        self.sock = SocketClass(f_ip, 2222, 1024)
        self.opened = True
        self.state = "off"
        self.commands = []
        self.parent = f_parent
        self.commandData = []

    def getCommandFromModul(self):
        if self.connect():
            command = "{\"deviceid\":\"actuator1\",\"get\":\"commands\"}"
            self.sock.send(command)
            responseInJson = self.sock.receive()
            self.commandData = json.loads(responseInJson)[0]
            self.commands = self.commandData["set"].split("|")

    def close(self):
        self.sock.close_socket()

    def connect(self):
        if self.sock.isConnected():
            return True

        timeout = time.time() + 1
        while time.time() < timeout:
            try:
                self.sock.connect_socket(self.sock.getip(), 2222)
                while not self.getStatus():
                    pass
                return True
            except:
                self.parent.notify("Error", "Can't connect actuator")
        return False

    def toArray(self):
        array = {}
        array["id"]=self.id
        data = {}
        data["name"] = self.name
        data["ip"] = self.sock.getip()
        data["state"] = self.state
        data["commands"] = self.commands
        data["commandData"] = self.commandData
        array["data"] = data
        return array

    def fromArray(self, array):
        self.id = array["id"]
        data = array["data"]
        self.name = data["name"]
        self.sock = SocketClass(data["ip"], 2222,1024)
        self.state = data["state"]
        self.commands = data["commands"]
        self.commandData = data["commandData"]

    def changeState(self, f_state):
        if f_state not in self.commands:
            return
        if self.state is f_state:
            return
        self.commandData["set"] = f_state

        jsonData = json.dumps(self.commandData)
        print '['+str(jsonData)+']'
        self.sock.send(str(jsonData))
        responseInJson = self.sock.receive()
        responseArray = json.loads(responseInJson)[0]
        if 'error' in responseArray["status"]:
            return False
        if responseArray['status'] == f_state:
            self.state = f_state
        return True

    def getStatus(self):
        command = "{\"deviceid\":\"actuator1\",\"get\":\"status\"}"
        self.sock.send(command)
        responseInJson = self.sock.receive()
        responseArray = json.loads(responseInJson)[0]
        if 'error' in responseArray["status"]:
            return False
        self.state = responseArray["status"]
        return True


    def setip(self, ip):
        self.sock.setip(ip)
