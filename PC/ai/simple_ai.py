from keras.models import load_model  # TensorFlow is required for Keras to work
import cv2  # Install opencv-python
import numpy as np
import threading
import time
import socket


class SimpleAI:
    latestImage = None
    isStart = False
    isReading = False
    hImage = None
    wImage = None
    padX = None
    padY = None
    rawImage = None

    isProcessingImage = False

    def __init__(self):
        # Disable scientific notation for clarity
        np.set_printoptions(suppress=True)

        # Load the model
        self.model = load_model("./ai/keras_model.h5", compile=False)

        # Load the labels
        self.class_names = open("./ai/labels.txt", "r").readlines()

        # CAMERA can be 0 or 1 based on default camera of your computer
        self.camera = cv2.VideoCapture("http://192.168.1.2:8000/camera/mjpeg")

        thread = threading.Thread(target=self.update)
        thread.daemon = True
        thread.start()

    def update(self):
        while True:
            if self.isProcessingImage:
                time.sleep(0.01)
                continue
            self.isReading = True
            ret, self.rawImage = self.camera.read()
            self.isReading = False
            if ret:
                if not self.isStart:
                    height, width, channels = self.rawImage.shape
                    self.hImage = int(height)
                    self.wImage = int(width)
                    if self.hImage > self.wImage:
                        self.padX = 0
                        self.padY = int((self.hImage - self.wImage) / 2)
                    else:
                        self.padX = int((self.wImage - self.hImage) / 2)
                        self.padY = 0
                self.isStart = True

    def processImage(self):
        if not self.isStart:
            time.sleep(0.1)
            return ""

        # Resize the raw image into (224-height,224-width) pixels
        self.isProcessingImage = True
        while self.isReading:
            pass
        image = cv2.resize(self.rawImage[self.padY:self.hImage - self.padY, self.padX:self.wImage - self.padX],
                           (224, 224),
                           interpolation=cv2.INTER_AREA)
        self.isProcessingImage = False

        # Show the image in a window
        # cv2.imshow("Webcam Image", image)

        # Make the image a numpy array and reshape it to the models input shape.
        image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)

        # Normalize the image array
        image = (image / 127.5) - 1

        # Predicts the model
        prediction = self.model.predict(image)
        index = np.argmax(prediction)
        class_name = self.class_names[index]
        confidence_score = prediction[0][index]

        # Print prediction and confidence score
        # print("Class:", class_name[2:], end="")
        # print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")
        if np.round(confidence_score * 100) > 75:
            return class_name[2:]
        return ""

    def __del__(self):
        self.camera.release()
