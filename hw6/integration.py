from camera import Camera, mpHands, mpDrawing
from sender import Sender
from pong import Pong
import numpy as np
import time
import cv2

WIDTH = 20
HEIGHT = 15

camera = Camera(camera=2).start()
sender = Sender()
pong = Pong()
started = False

while camera.safeFrame is None:
    time.sleep(0.1)

while True:

    toShow = np.copy(camera.safeFrame)
    toShow = cv2.cvtColor(toShow, cv2.COLOR_RGB2BGR)

    if camera.results.multi_hand_landmarks:
        for hand in camera.results.multi_hand_landmarks:
            mpDrawing.draw_landmarks(toShow, hand, mpHands.HAND_CONNECTIONS)

    cv2.imshow("Hands!", toShow)

    pixels = pong.getBoard()
    image = cv2.resize(pixels.astype('float32'), (40, 30))
    cv2.imshow('Pong!', image)

    if cv2.waitKey(5) & 0xFF == ord("q"):
        break

    if camera.hands[0] is not None:
        # sender.send(camera.hands)
        if camera.hands[0] is not None:
            pong.setPaddle(0, int(HEIGHT*camera.hands[0][1]))
        if camera.hands[1] is not None:
            pong.setPaddle(1, int(HEIGHT*camera.hands[1][1]))
            started = True

    if started:
        pong.step()

    time.sleep(0.05)

camera.stop()
