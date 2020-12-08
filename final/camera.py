import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread, Lock


class Camera:
    def __init__(self, size=(480, 368), callback=None):
        # self.cam = cv2.VideoCapture(camera)
        self.cam = PiCamera()
        self.cam.resolution = size
        self.cam.framerate = 24
        self.rawCapture = PiRGBArray(self.cam, size=size)
        self.stopped = False
        self.safeFrame = None
        self.size = size
        self.lock = Lock()
        self.callback = callback

    def start(self):
        Thread(target=self.run, args=()).start()
        return self

    def run(self):
        for frame in self.cam.capture_continuous(self.rawCapture, format='bgr', use_video_port=True):
            if self.stopped:
                break
            image = frame.array
            with self.lock:
                self.safeFrame = image
            if self.callback is not None:
                self.callback(self.safeFrame)
            self.rawCapture.truncate(0)
        # while not self.stopped:
        #     ret, frame = self.cam.read()
        #     with self.lock:
        #         self.safeFrame = cv2.resize(frame, self.size)
        #     if self.callback is not None:
        #         self.callback(self.safeFrame)

    def stop(self):
        self.stopped = True


if __name__ == "__main__":
    import time

    camera = Camera(camera=2).start()

    while camera.safeFrame is None:
        time.sleep(0.1)

    while True:
        cv2.imshow("Frame", camera.safeFrame)
        key = cv2.waitKey(100) & 0xFF
        if key == ord("q"):
            break

    camera.stop()
