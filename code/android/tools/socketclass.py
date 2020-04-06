import socket

class SocketClass:
    def __init__(self, ip, port, buf_size):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.sock = None
        self.ip = ip
        self.port = port
        self.buf_size = buf_size
        self.connected = False
        self.opened = True

    def setip(self, ip):
        self.close_socket()
        self.ip = ip
        self.open_socket()

    def getip(self):
        return self.ip

    def setport(self, port):
        self.close_socket()
        self.port = port
        self.open_socket()

    def setbuf_size(self, buf_size):
        self.close_socket()
        self.buf_size = buf_size
        self.open_socket()

    def getbuf_size(self):
        return self.buf_size

    def getindex(self):
        for i, item in enumerate([o.sock for o in server.parent.sensors]):
            if item == self:
                return i
            else:
                pass

    def connect_socket(self, ip, port):
        if self.connected:
            return True
        if not self.opened:
            self.open_socket()
            self.opened = True

        self.sock.connect((ip, port))
        self.connected = True
        return True

    def open_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def close_socket(self):
        self.sock.close()
        self.connected = False
        self.opened = False

    def receive(self):
        return self.sock.recv(self.buf_size)

    def send(self,f_data):
        self.sock.send(f_data)

    def isConnected(self):
        return self.connected
