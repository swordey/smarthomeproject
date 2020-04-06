import select
import threading


class Server(threading.Thread):
    def __init__(self, parent):
        threading.Thread.__init__(self)
        self.running = False
        self.daemon = True
        self.parent = parent
        self.lock = threading.RLock()

    def startThread(self):
        self.running = True
        self.start()

    def stopThread(self):
        self.running = False

    def run(self):
        while self.running:
            if len([o for o in self.parent.sensors if o.receiving]) > 0:
                read, write, error = select.select([o.sock.sock for o in self.parent.sensors if o.receiving], [], [])
                for r in read:
                    for i, item in enumerate([o.sock.sock for o in self.parent.sensors]):
                        if r == item:
                            try:
                                data = item.recv(1024)
                                if len(data) > 0:
                                    self.readData(data)
                                else:
                                    pass
                            except:
                                pass

    def readData(self, data):
        self.lock.acquire()
        try:
            self.parent.incomingData.append(data)
        finally:
            self.lock.release()
