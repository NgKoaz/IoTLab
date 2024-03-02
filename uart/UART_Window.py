import serial.tools.list_ports
import time
import socket
import threading


class UART:
    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    IP = socket.gethostbyname(socket.gethostname())
    PORT = 8888
    SERVER.bind((IP, PORT))
    ser = None
    message = ""
    lock = threading.Lock()

    def __init__(self):
        self.connectCOM()

        self.SERVER.listen()
        print("Listening on " + self.IP + ":" + str(self.PORT))

        thread = threading.Thread(target=self.listen)
        thread.daemon = True
        thread.start()

        while True:
            self.readSerial()
            time.sleep(1)

    def listen(self):
        while True:
            conn, addr = self.SERVER.accept()
            print(str(addr) + " is connected!")
            thread = threading.Thread(target=self.handleRequest, args=(conn, addr))
            thread.daemon = True
            thread.start()

    def handleRequest(self, conn, addr):
        while True:
            try:
                mes = conn.recv(1).decode("UTF-8")
            except:
                print(str(addr) + " is disconnected!")
                return

            self.lock.acquire()
            try:
                if mes == "!":

                    # Eight bytes for length of message
                    payload = self.message.encode("UTF-8")
                    payloadSize = str(len(payload)).encode("UTF-8")

                    # Send length first
                    header = payloadSize + (8 - len(payloadSize)) * b" "
                    conn.send(header)
                    # Send payload
                    conn.send(payload)
                    self.message = ""

                else:
                    conn.send("#".encode("UTF-8"))
            except:
                print(str(addr) + " is disconnected!")
                self.lock.release()
                return
            self.lock.release()

    def readSerial(self):
        numByteInWaiting = self.ser.inWaiting()
        if numByteInWaiting <= 0:
            return
        self.lock.acquire()
        self.message = self.message + self.ser.read(numByteInWaiting).decode("UTF-8")
        self.lock.release()

    def connectCOM(self):
        for port in serial.tools.list_ports.comports():
            for _str in str(port).split(" "):
                if _str.startswith("COM"):
                    try:
                        self.ser = serial.Serial(port=_str, baudrate=115200)
                        print("Connected to " + _str)
                        return
                    except:
                        print(_str + " is not available!")
                        break
        print("Can't find any COM!")


UART()
