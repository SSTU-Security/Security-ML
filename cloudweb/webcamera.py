import cv2
import socket
import pickle
import struct
import requests



print(requests.post("http://localhost:8000/setCamera", json={"ip": "localhost", "port": 8081}))
camera_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
camera_socket.connect(('localhost', 8081))
cam = cv2.VideoCapture(0)
print(requests.post("http://localhost:8000/update"))

while True:
    ret, im = cam.read()
    data = pickle.dumps(im)
    message = struct.pack("Q", len(data)) + data
    camera_socket.sendall(message)
