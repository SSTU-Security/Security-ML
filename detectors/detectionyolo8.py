from ultralytics import YOLO
import torch


class Detect:
    def __init__(self):
        self.conf_yolo = 0.3
        self.model = YOLO('weigts/yolov8n-face.pt')
        self.kmodel = YOLO('weigts/yolov8n.pt')
    def mypredict(self, img):
        predict_yolo = self.model.predict(
            source=img, conf=self.conf_yolo, verbose=False
        )

        return predict_yolo[0].boxes.data

    def mypredictknife(self, img):
        kpredict_yolo = self.kmodel.predict(
            source=img, conf=0.1, verbose=False
        )
        return list(filter(lambda x: x[5] == 44, kpredict_yolo[0].boxes.data))
