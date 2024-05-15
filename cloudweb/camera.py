import cv2
from detectors.detectionyolo8 import Detect
from verification.adaverefication import Verificathion
# import telebot
import struct
import threading
import socket
import pickle
from checkoutput.checkexitenter import *


class Camera(threading.Thread):
    def __init__(self):
        super().__init__()
        self.recognizer = Detect()
        self.verificathion = Verificathion()
        self.cam = cv2.VideoCapture(0)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.last = {}

    def run(self, *args, **kwargs):
        try:
            while True:
                try:
                    ret, im = self.cam.read()
                    faces = self.recognizer.mypredict(im)
                    weapon = self.recognizer.mypredictknife(im)
                    now = {}
                    if len(faces) != 0:
                        for i in faces:
                            coor = list(map(int, list(i)[:-2]))
                            coor[0] = max(coor[0], 0)
                            coor[1] = max(coor[1], 0)
                            coor[2] = coor[2]
                            coor[3] = coor[3]
                            cv2.rectangle(im, (coor[0], coor[1]), (coor[2], coor[3]), (0, 255, 255), 2)
                            a = self.verificathion.mypredict(im[coor[1]:coor[3], coor[0]:coor[2]])
                            if a[0] > 0.15:
                                cv2.putText(
                                    im, str(float(a[0]))[:3] + str(a[1]), (coor[0] + 5, coor[1] + 10),
                                    cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)
                                now[str(a[1])] = coor
                            else:
                                cv2.putText(
                                    im, "undefined", (coor[0] + 5, coor[1] + 10),
                                    cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)
                    print(check_enter(self.last, now, im.shape))
                    print(check_exit(self.last, now, im.shape))
                    self.last = now
                    if len(weapon) != 0:
                        for i in weapon:
                            coor = list(map(int, list(i)[:-2]))
                            coor[0] = max(coor[0], 0)
                            coor[1] = max(coor[1], 0)
                            coor[2] = coor[2]
                            coor[3] = coor[3]
                            cv2.rectangle(im, (coor[0], coor[1]), (coor[2], coor[3]), (0, 255, 0), 2)
                    data = pickle.dumps(im)
                    message = struct.pack("Q", len(data)) + data
                    self.server_socket.sendall(message)
                except Exception as e:
                    print(e, 1)
        except Exception as e:
            print(e, 2)

    def setServer(self, ip, port):
        print(ip, port)
        self.server_socket.connect((ip, port))
