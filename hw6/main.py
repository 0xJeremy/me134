# 172.20.10.2 on iPhone

import time
from receiver import Receiver
from pong import Pong, WIDTH, HEIGHT
from display import Display

UPDATE = 0.5

receiver = Receiver().start()
pong = Pong()
display = Display()
started = False

try:
    while True:
        data = receiver.data
        print("Data:", data)
        if data[0] is not None:
            pong.setPaddle(0, int(HEIGHT * data[0][1]))
        if data[1] is not None:
            pong.setPaddle(1, int(HEIGHT * data[1][1]))
            started = True

        pixels = pong.getBoard()

        display.set(pixels)

        if started:
            pong.step()

        time.sleep(0.05)

except KeyboardInterrupt:
    receiver.stop()
