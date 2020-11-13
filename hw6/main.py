# 172.20.10.2 on iPhone

import time
from receiver import Receiver
from pong import Pong, WIDTH, HEIGHT

try:
    from display import Display
    display = Display()

    def show(pixels):
        display.set(pixels)
except:
    import cv2
    def show(pixels):
        image = cv2.resize(pixels.astype('float32'), (400, 300))
        cv2.imshow('Pong!', image)
        cv2.waitKey(5)
# from display import Display

UPDATE = 0.5

receiver = Receiver().start()
pong = Pong()
# display = Display()

timer = time.time()

try:
    while True:
        data = receiver.data
        print("Data is", data)
        if data[0] is not None:
            print("Setting location to ", int(HEIGHT*data[0][1]))
            pong.setPaddle(0, int(HEIGHT*data[0][1]))
        if data[1] is not None:
            pong.setPaddle(1, int(HEIGHT*data[1][1]))

        pixels = pong.getBoard()
        # display.set(pixels)

        show(pixels)

        # if time.time() - timer > UPDATE:
        #     pong.step()
        #     timer = time.time()

        # pong.plot()
        # time.sleep(0.05)

except KeyboardInterrupt:
    receiver.stop()
