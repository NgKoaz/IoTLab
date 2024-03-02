import serial.tools.list_ports
import time
import socket
import threading


class UART:
    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    IP = socket.gethostbyname(socket.gethostname())
    PORT = 8888
    SERVER.bind((IP, PORT))
    message = ""
    lock = threading.Lock()

    def __init__(self):
        self.port = self.getPort()
        if not self.port:
            print("Can't find COM port.")
            return
        self.ser = serial.Serial(port=self.port, baudrate=115200)
        print("Connected to " + self.port)

        self.SERVER.listen()
        print("Connected to " + self.IP + ":" + str(self.PORT))

        thread = threading.Thread(target=self.handleRequest)
        thread.daemon = True
        thread.start()

        while True:
            self.readSerial()
            time.sleep(1)

    def handleRequest(self):
        conn, addr = self.SERVER.accept()
        while True:
            mes = conn.recv(1).decode("UTF-8")
            if mes == "!":
                self.lock.acquire()
                # Eight bytes for length of message
                payload = self.message.encode("UTF-8")
                payloadSize = str(len(payload)).encode("UTF-8")

                # Send length first
                header = payloadSize + (8 - len(payloadSize)) * b" "
                conn.send(header)
                # Send payload
                conn.send(payload)
                self.message = ""
                self.lock.release()
            else:
                conn.send("#".encode("UTF-8"))

    def readSerial(self):
        numByteInWaiting = self.ser.inWaiting()
        if numByteInWaiting <= 0:
            return
        self.lock.acquire()
        self.message = self.message + self.ser.read(numByteInWaiting).decode("UTF-8")
        self.lock.release()

    @staticmethod
    def getPort():
        for port in serial.tools.list_ports.comports():
            for _str in str(port).split(" "):
                if _str.startswith("COM"):
                    return _str
        return None


UART()
