import threading

class UART:
    sendingLock = threading.Lock()

