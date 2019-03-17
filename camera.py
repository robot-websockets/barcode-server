import argparse
from pyzbar import pyzbar
import numpy as np
import cv2
import time
import requests
import json

# local_server_address = '127.0.0.0:5001'
# video_server_address = '192.168.0.30:8081'
# video_server_address = '192.168.55.12:8081'


parser = argparse.ArgumentParser()
parser.add_argument('-W', '--websocket_server')
parser.add_argument('-V', '--video_server')

args = parser.parse_args()

web_socket_server = "192.168.0.10:5001"
if (args.websocket_server):
    web_socket_server = args.websocket_server

video_server = "192.168.0.30:8081"
if (args.video_server):
    video_server = args.video_server

print('\n video feed url: {} \n websocket server url:{}'.format(
    video_server, web_socket_server))


class VideoCamera():
    start_time = time.time()
    counter = 0
    barcodeText = ''

    def __init__(self):
        self.video = cv2.VideoCapture(
            "http://{}/".format(video_server))

    def __del__(self):
        self.video.release()

    def get_frame(self):

        success, image = self.video.read()
        for x in range(10):
            success, image = self.video.read()

        barcodes = pyzbar.decode(image)

        for barcode in barcodes:
            # draw the bounding rectangle
            (x, y, w, h) = barcode.rect
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
            barcodeData = barcode.data.decode("utf-8")
            if (barcodeData != self.barcodeText):
                print(barcodeData)
                data = float(barcodeData)
                speed = int(data)
                dir = int(float(data) - speed) * 10
                direction = 'forwards'
                if int(dir) == 2:
                    direction = 'backwards'
                # self.barcodeText = barcodeData
                # j = json.loads(barcodeData)
                js = '{' + \
                    ' "direction":"{}", "speed":{}'.format(
                        direction, speed) + '}'
                j = json.loads(js)

                print(j)
                try:
                    r = requests.post(
                        'http://{}/api/barcodes/'.format(web_socket_server),
                        json=j)
                    print(r)
                except:
                    print('error connecting to websocket server. ')

            text = "{} ".format(barcodeData)
            cv2.putText(image, text, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        ret, jpeg = cv2.imencode('.jpg', image)

        return jpeg.tobytes()
