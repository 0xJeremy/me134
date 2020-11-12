import cv2
import mediapipe as mp
from threading import Thread

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

CAMERA = 0

class Camera:
    def __init__(self):
        self.cam = cv2.VideoCapture(CAMERA)
        self.hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
        self.stopped = False
        self.results = None
        self.frame = None

    def start(self):
        Thread(target=self.run, args=()).start()
        return self

    def run(self):
        while not self.stopped:
            ret, self.frame = self.cam.read()
            self.frame = cv2.cvtColor(cv2.flip(self.frame, 1), cv2.COLOR_BGR2RGB)
            self.frame.flags.writeable = False
            self.results = self.hands.process(self.frame)

        self.hands.close()
        self.cam.release()

    def stop(self):
        self.stopped = True

if __name__ == '__main__':
    import time
    CAMERA = 2
    camera = Camera().start()
    time.sleep(1)

    while True:
        if camera.results.multi_hand_landmarks:
            for hand_landmarks in camera.results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(camera.frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        cv2.imshow('Hands!', camera.frame)
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break
        time.sleep(0.05)
    camera.stop()
