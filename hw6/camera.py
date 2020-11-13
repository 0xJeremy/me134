import cv2
import mediapipe as mp
from threading import Thread

mpHands = mp.solutions.hands
mpDrawing = mp.solutions.drawing_utils

CAMERA = 0

MIDDLE_JOINT = 9


class Camera:
    def __init__(self, camera=CAMERA):
        self.cam = cv2.VideoCapture(camera)
        self.tracker = mpHands.Hands(
            max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.5
        )
        self.stopped = False
        self.results = None
        self.frame = None
        self.safeFrame = None
        self.hands = [None, None]

    def start(self):
        Thread(target=self.run, args=()).start()
        return self

    def run(self):
        while not self.stopped:
            ret, self.frame = self.cam.read()
            self.frame = cv2.cvtColor(cv2.flip(self.frame, 1), cv2.COLOR_BGR2RGB)
            self.frame.flags.writeable = False
            self.results = self.tracker.process(self.frame)
            if self.results.multi_hand_landmarks:
                self.processLocations()
            else:
                self.hands = [None, None]
            self.safeFrame = self.frame

        self.tracker.close()
        self.cam.release()

    def processLocations(self):
        numHands = len(self.results.multi_hand_landmarks)
        if numHands == 0:
            return

        height, width, _ = self.frame.shape

        hand1 = self.results.multi_hand_landmarks[0].landmark[MIDDLE_JOINT]
        # location1 = (int(hand1.x * width), int(hand1.y * height))
        location1 = (hand1.x, hand1.y)
        if numHands == 1:
            self.hands = [location1, None]
        elif numHands == 2:
            hand2 = self.results.multi_hand_landmarks[1].landmark[MIDDLE_JOINT]
            # location2 = (int(hand2.x * width), int(hand2.y * height))
            location2 = (hand2.x, hand2.y)
            if location1[0] < location2[0]:
                self.hands = [location1, location2]
            else:
                self.hands = [location2, location1]

        # print("Hands are", self.hands)


    def stop(self):
        self.stopped = True


if __name__ == "__main__":
    import time

    CAMERA = 2
    camera = Camera().start()
    time.sleep(1)

    while True:

        if camera.hands[0]:
            position = camera.hands[0]
            cv2.line(camera.frame, position, (position[0] + 10, position[1] + 10), (0,0,255), 15)

        if camera.hands[1]:
            position = camera.hands[1]
            cv2.line(camera.frame, position, (position[0] + 10, position[1] + 10), (255,0,0), 15)

        # if camera.results.multi_hand_landmarks:
            # print(dir(camera.results.multi_hand_landmarks[0]))
            # print(camera.results.multi_hand_landmarks[0].landmark[0].x)
            # landmark = camera.results.multi_hand_landmarks[0].landmark[9]
            # print(camera.frame.shape)
            # width, height, _ = camera.frame.shape
            # position = (int(landmark.x * height), int(landmark.y * width))
            # cv2.line(camera.frame, position, (position[0] + 10, position[1] + 10), (255,255,255), 15)
            # print()
            # for hand_landmarks in camera.results.multi_hand_landmarks:
            #     mpDrawing.draw_landmarks(
            #         camera.frame, hand_landmarks, mpHands.HAND_CONNECTIONS
            #     )
        cv2.imshow("Hands!", camera.safeFrame)
        if cv2.waitKey(5) & 0xFF == ord("q"):
            break
        time.sleep(0.05)
    camera.stop()
