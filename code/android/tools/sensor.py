from socketclass import *
import time
import json

class Sensor:  # Sensor class to save sensor data
    def __init__(self,f_parent,f_id='default',f_ip='127.0.0.1', f_unit='default', f_buf_size=1024):
        self.id = f_id
        self.name = f_id
        self.unit = f_unit

        self.sock = SocketClass(f_ip, 1111, f_buf_size)
        self.opened = True

        self.data = ''
        self.receiving = False
        self.updated = 0

        self.parent = f_parent

    def toString(self):
        return self.name+": "+str(self.data)+ " ["+self.unit+"]"

    def getData(self):
        return str(self.data) + " [" + self.unit + "]"

    def getModulData(self):
        responseInJson = self.receive()
        data = json.loads(responseInJson)[0]
        self.id = data["deviceid"]
        self.unit = data["unit"]


    def toArray(self):
        array = {}
        array["id"]=self.id
        data = {}
        data["name"] = self.name
        data["ip"] = self.sock.getip()
        data["unit"] = self.unit
        data["receiving"] = self.receiving
        array["data"] = data
        return array

    def fromArray(self, array):
        self.id = array["id"]
        data = array["data"]
        self.name = data["name"]
        self.sock= SocketClass(data["ip"], 1111,1024)
        self.unit = data["unit"]
        self.receiving = data["receiving"]

    def connect(self):
        if self.sock.isConnected():
            return True

        timeout = time.time() + 1
        while time.time() < timeout:
            try:
                self.sock.connect_socket(self.sock.getip(), 1111)
                self.receiving = True
                self.getModulData()
                return True
            except Exception as e:
                self.parent.notify("Error","Can't connect to sensor")
        return False

    def close(self):
        self.sock.close_socket()

    def receive(self):
        return self.sock.receive()

    def setip(self, ip):
        self.stop_receiving()
        self.sock.setip(ip)

    def setport(self, port):
        self.stop_receiving()
        self.sock.setport(port)

    def setbuf_size(self, buf_size):
        self.stop_receiving()
        self.sock.setbuf_size(buf_size)

    def start_receiving(self):
        self.receiving = 1

    def stop_receiving(self):
        self.receiving = 0

