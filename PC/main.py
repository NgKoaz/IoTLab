from mylib.my_mqtt import MyMQTT
from ai.simple_ai import SimpleAI
from uart.UART import UART
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
uart = UART()
lastAIResult = ""

counter_ai = 11

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


def aiThread():
    while True:
        global counter_ai, lastAIResult
        counter_ai = counter_ai - 1
        if counter_ai <= 0:
            counter_ai = 10
            ai_result = simpleAI.processImage()
            if ai_result != "" and lastAIResult != ai_result:
                lastAIResult = ai_result
                print("AI OUTPUT: ", lastAIResult)
                my_mqtt.publish(AI_FEED_IDs, lastAIResult)
        time.sleep(1)


def processData(rawData):
    # !TEMP:23#
    payload = rawData.replace("!", "").replace("#", "")
    try:
        key, value = payload.split(":")
        print(key + " = " + value)
        if key == "TEMP":
            my_mqtt.publish("sensor1", value)
        elif key == "LIGHT":
            my_mqtt.publish("sensor2", value)
        elif key == "HUMI":
            my_mqtt.publish("sensor3", value)
    except:
        print("WRONG FORMAT: " + payload)


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


def readSerial():
    global messageUART
    while True:
        numByte, newMessage = uart.readSerial()
        messageUART = messageUART + newMessage
        if numByte > 0:
            print(messageUART)
            checkUARTMessage()
        time.sleep(1)


def processMessage(feed_id, payload):
    if feed_id == "button1":
        uart.writeSerial("B1:" + payload)
    elif feed_id == "button2":
        uart.writeSerial("B2:" + payload)


if __name__ == "__main__":
    my_mqtt.setCallback(connect=connectedCallback, message=processMessage)
    my_mqtt.connect()
    uart.connect()

    thread = threading.Thread(target=readSerial)
    thread.daemon = True
    thread.start()

    thread = threading.Thread(target=aiThread)
    thread.daemon = True
    thread.start()

    command_line()

