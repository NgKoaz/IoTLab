import serial.tools.list_ports
import time



class UART:
    message = ""

    def __init__(self):
        self.port = self.getPort()
        if not self.port:
            print("Can't find COM port.")
            return
        self.ser = serial.Serial(port=self.port, baudrate=115200)
        print("Connected to " + self.port)
        while True:
            self.readSerial()
            time.sleep(1)

    def readSerial(self):
        numByteInWaiting = self.ser.inWaiting()
        if numByteInWaiting <= 0:
            return

        self.message = self.message + self.ser.read(numByteInWaiting).decode("UTF-8")
        while ("!" in self.message) and ("#" in self.message):
            start = self.message.find("!")
            end = self.message.find("#")
            while start != -1 and end != -1 and start > end:
                end = self.message.find("#", end)
            if start == -1 or end == -1:
                return
            self.processData(self.message[start:end + 1])
            if end == len(self.message) - 1:
                self.message = ""
            else:
                self.message = self.message[end + 1:]

    @staticmethod
    def processData(rawData):
        # !TEMP:23#
        payload = rawData.replace("!", "").replace("#", "")
        key, value = None, None
        try:
            key, value = payload.split(":")
        except:
            print("WRONG FORMAT!")

        print(key + " = " + value)
        if key == "TEMP":
            pass

    @staticmethod
    def getPort():
        for port in serial.tools.list_ports.comports():
            for _str in str(port).split(" "):
                if _str.startswith("COM"):
                    return _str
        return None



UART()