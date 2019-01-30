from pyzbar import pyzbar
import numpy as np
import cv2
import time
import requests
import json


class VideoCamera(object):
    start_time = time.time()
    counter = 0
    barcodeText = ''

    def __init__(self):
        self.video = cv2.VideoCapture("http://192.168.55.12:8081/")

    def __del__(self):
        self.video.release()

    def get_frame(self):

        success, image = self.video.read()
        for x in range(10):
            success, image = self.video.read()

        barcodes = pyzbar.decode(image)

        for barcode in barcodes:
            (x, y, w, h) = barcode.rect
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
            barcodeData = barcode.data.decode("utf-8")
            if (barcodeData != self.barcodeText):
                print(barcodeData)
                self.barcodeText = barcodeData
                j = json.loads(barcodeData)
                print(j)
                try:
                    r = requests.post(
                        'http://192.168.55.11:5001/api/barcodes/',
                        json=j)
                    print(r)
                except:
                    print('error connecting to websocket server. ')

            text = "{} ".format(barcodeData)
            cv2.putText(image, text, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        ret, jpeg = cv2.imencode('.jpg', image)

        return jpeg.tobytes()
