from Adafruit_IO import MQTTClient


class MyMQTT:
    USERNAME = None
    KEY = None
    FEED_ID_LIST = []
    CLIENT = None
    isConnected = False
    connectCallback = None
    subscribeCallback = None
    messageCallback = None
    disconnectCallback = None

    def getClient(self):
        return self.CLIENT

    def connect(self):
        if self.isConnected:
            print("[WARNING] Already connected!")
            return
        if not self.USERNAME or not self.KEY:
            print("[ERROR] None value. Use setParams() to set username and key before connect!")
        try:
            self.CLIENT.connect()
            self.isConnected = True
            self.CLIENT.loop_background()
        except Exception as e:
            print(e)
            print("[ERROR] Connection failed. Try again!")

    def setCallback(self, connect=None, subscribe=None, message=None, disconnect=None):
        if connect:
            self.connectCallback = connect
        if subscribe:
            self.subscribeCallback = subscribe
        if message:
            self.messageCallback = message
        if disconnect:
            self.disconnectCallback = disconnect

    def connected(self, client):
        if self.connectCallback:
            self.connectCallback()
        else:
            print("Connected to broker!")

    def subscribed(self, client, userdata, mid, granted_qos):
        if self.subscribeCallback:
            self.subscribeCallback()
        else:
            print("Subscribed successful!")

    def recv_message(self, client, feed_id, payload):
        if self.messageCallback:
            self.messageCallback(feed_id, payload)
        else:
            print("From", feed_id, "received: ", payload)

    def disconnected(self, client):
        self.isConnected = False
        if self.disconnectCallback:
            self.disconnectCallback()
        else:
            print("Disconnected to Broker!")

    def subscribe(self, sub_fid_list):
        if not self.isConnected:
            print("[WARNING] No connection!")
            return
        if not isinstance(sub_fid_list, list):
            print("[ERROR] The parameter in subscribe() should be a list!")

        for sub_fid in sub_fid_list:
            if isinstance(sub_fid, str):
                self.CLIENT.subscribe(sub_fid)

    def unsubscribe(self, unsub_fid_list):
        if not self.isConnected:
            print("[WARNING] No connection!")
            return
        if not isinstance(unsub_fid_list, list):
            print("[ERROR] The parameter in unsubscribe() should be a list!")

        for unsub_fid in unsub_fid_list:
            if isinstance(unsub_fid, str):
                self.CLIENT.unsubscribe(unsub_fid)

    def disconnect(self):
        if not self.isConnected:
            print("[WARNING] No connection!")
            return
        if self.CLIENT:
            self.CLIENT.disconnect()

    def publish(self, feed_id, payload):
        if not self.isConnected:
            print("[WARNING] No connection!")
            return
        if self.CLIENT:
            self.CLIENT.publish(str(feed_id), str(payload))

    def __init__(self, username, key):
        self.USERNAME = username
        self.KEY = key
        self.CLIENT = MQTTClient(self.USERNAME, self.KEY)
        self.CLIENT.on_connect = self.connected
        self.CLIENT.on_subscribe = self.subscribed
        self.CLIENT.on_message = self.recv_message
        self.CLIENT.on_disconnect = self.disconnected

