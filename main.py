from mylib.my_mqtt import MyMQTT
from ai.simple_ai import SimpleAI
import time
import threading
import socket
import random
import sys
from ai.simple_ai import *

USERNAME = "nguyenkhoa2207"
KEY = "aio_WJGG26JYscLn0DvE8VDfdi2DPpEP"

BUTTON_FEED_IDs = ["button1", "button2"]
SENSOR_FEED_IDs = ["sensor1", "sensor2", "sensor3"]
AI_FEED_IDs = ["ai"]

my_mqtt = MyMQTT(username=USERNAME, key=KEY)
simpleAI = SimpleAI()
lastAIResult = ""

counter_ai = 6

CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sendingLock = threading.Lock()


# For UART
messageUART = ""


def connectedCallback():
    my_mqtt.subscribe(BUTTON_FEED_IDs)


def command_line():
    while True:
        cmd = input()
        if cmd == "exit":
            my_mqtt.disconnect()
            break


def whileRun():
    while True:
        global counter_ai, lastAIResult
        counter_ai = counter_ai - 1
        if counter_ai <= 0:
            counter_ai = 5
            ai_result = simpleAI.processImage()
            if ai_result != "" and lastAIResult != ai_result:
                lastAIResult = ai_result
                print("AI OUTPUT: ", lastAIResult)
                my_mqtt.publish(AI_FEED_IDs, lastAIResult)
        time.sleep(1)


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
        my_mqtt.publish("sensor1", value)
    elif key == "LIGHT":
        my_mqtt.publish("sensor2", value)
    elif key == "HUMI":
        my_mqtt.publish("sensor3", value)


def checkUARTMessage():
    global messageUART
    while ("!" in messageUART) and ("#" in messageUART):
        start = messageUART.find("!")
        end = messageUART.find("#")
        while start != -1 and end != -1 and start > end:
            end = messageUART.find("#", end)
        if start == -1 or end == -1:
            return
        processData(messageUART[start:end + 1])
        if end == len(messageUART) - 1:
            messageUART = ""
        else:
            messageUART = messageUART[end + 1:]


def connectUART():
    CLIENT.connect(("192.168.1.11", 8888))
    print("Connected to UART!")

    # Handle data recv
    global messageUART
    while True:
        sendingLock.acquire()
        CLIENT.send("!".encode("UTF-8"))

        numByte = CLIENT.recv(8).decode("UTF-8").strip()
        numByte = int(numByte)
        newMessage = CLIENT.recv(numByte).decode("UTF-8")
        sendingLock.release()

        messageUART = messageUART + newMessage

        if numByte > 0:
            print(messageUART)
            checkUARTMessage()
        time.sleep(1)


def processMessage(feed_id, payload):
    print(feed_id, payload)
    if feed_id == "button1":
        serialWrite("B1:" + payload)
    elif feed_id == "button2":
        serialWrite("B2:" + payload)


def serialWrite(payload):
    payload = payload.encode('UTF-8')
    size = str(len(payload)).encode('UTF-8')
    header = size + (8 - len(size)) * b" "
    with sendingLock:
        CLIENT.send("#".encode('UTF-8'))
        CLIENT.send(header)
        CLIENT.send(payload)


if __name__ == "__main__":
    my_mqtt.setCallback(connect=connectedCallback, message=processMessage)
    my_mqtt.connect()

    thread = threading.Thread(target=connectUART)
    thread.daemon = True
    thread.start()

    thread = threading.Thread(target=whileRun)
    thread.daemon = True
    thread.start()

    command_line()

