import cv2
from display import Display
import time


class Video:
    def __init__(self, path="videos/test.mp4"):
        self.cam = cv2.VideoCapture(path)

    def play(self, display):
        while self.cam.isOpened():
            ret, frame = self.cam.read()

            frame = cv2.resize(frame, (20, 15))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            display.set(frame)
            time.sleep(0.05)


if __name__ == "__main__":
    video = Video()
    display = Display()
    video.play(display)
