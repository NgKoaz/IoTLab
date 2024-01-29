from mylib.my_mqtt import MyMQTT
import time
import threading
import random
import sys


USERNAME = "nguyenkhoa2207"
KEY = "aio_RDeE09lGMAxiNO3pWIUzz6cK8lOO"

BUTTON_FEED_IDs = ["button1", "button2"]
SENSOR_FEED_IDs = ["sensor1", "sensor2", "sensor3"]
AI_FEED_IDs = ["ai"]

my_mqtt = MyMQTT(username=USERNAME, key=KEY)


def simulate_sensors():
    sensor_type = 0
    while True:
        if sensor_type == 0:
            sensor_type = 1
            temp = random.randint(20, 30)
            print("Temperature: ", temp)
            my_mqtt.publish("sensor1", temp)
        elif sensor_type == 1:
            sensor_type = 2
            light_intensive = random.randint(100, 500)
            print("Light Intensive: ", light_intensive)
            my_mqtt.publish("sensor2", light_intensive)
        elif sensor_type == 2:
            sensor_type = 0
            humi = random.randint(60, 80)
            print("Humidity: ", humi)
            my_mqtt.publish("sensor3", humi)

        time.sleep(1)


def connectedCallback():
    print("Connect successful! Hohohoho")
    my_mqtt.subscribe(BUTTON_FEED_IDs)

    thread = threading.Thread(target=simulate_sensors)
    thread.daemon = True
    thread.start()


def command_line():
    while True:
        cmd = input()
        if cmd == "exit":
            my_mqtt.disconnect()
            sys.exit(1)
            break


if __name__ == "__main__":
    my_mqtt.setCallback(connect=connectedCallback)
    my_mqtt.connect()
    command_line()

