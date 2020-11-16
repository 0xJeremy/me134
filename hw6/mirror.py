import cv2
import time


class Mirror:
    def __init__(self):
        self.cam = cv2.VideoCapture(0)

    def play(self, display):
        while True:
            ret, frame = self.cam.read()

            frame = cv2.resize(frame, (20, 15))
            # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.flip(frame, 1)

            display.set(frame)

            time.sleep(0.05)
