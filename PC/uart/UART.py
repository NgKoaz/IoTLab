import socket
import threading


class UART:
    CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sendingLock = threading.Lock()

    def connect(self):
        self.CLIENT.connect(("192.168.1.11", 8888))
        print("Connected to UART!")

    def readSerial(self):
        self.sendingLock.acquire()
        self.CLIENT.send("!".encode("UTF-8"))

        numByte = self.CLIENT.recv(8).decode("UTF-8").strip()
        numByte = int(numByte)
        newMessage = self.CLIENT.recv(numByte).decode("UTF-8")
        self.sendingLock.release()

        return numByte, newMessage

    def writeSerial(self, payload):
        payload = payload.encode('UTF-8')
        size = str(len(payload)).encode('UTF-8')
        header = size + (8 - len(size)) * b" "
        with self.sendingLock:
            self.CLIENT.send("#".encode('UTF-8'))
            self.CLIENT.send(header)
            self.CLIENT.send(payload)


