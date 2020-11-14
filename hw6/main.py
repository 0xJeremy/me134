# 172.20.10.2 on iPhone

import argparse
import time
from receiver import Receiver
from pong import Pong, WIDTH, HEIGHT
from display import Display
from textscroller import TextScroller

UPDATE = 0.5

BRIGHTNESS = 0.5


def pong():
    receiver = Receiver().start()
    pong = Pong()
    display = Display(brightness=BRIGHTNESS)
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

            display.set(pong.getBoard())
            if started:
                pong.step()

            time.sleep(0.05)

    except KeyboardInterrupt:
        receiver.stop()

def rainbow():
    display = Display(brightness=BRIGHTNESS)
    while True:
        display.rainbow()

def pong_head():
    print("Not implemented")

def segment():
    print("Not implemented")

def text(text):
    scroller = TextScroller()
    disp = Display()
    time.sleep(1)
    scroller.displayTextScroll(disp, text)


if __name__ == '__main__':
    parser = argparse.ArgumentParser('A small robotics project :)')
    parser.add_argument('--pong', help='Plays a game of pong (requires streaming from a laptop)', action='store_true')
    parser.add_argument('--rainbow', help='Displays a nice rainbow :)', action='store_true')
    parser.add_argument('--brightness', type=float, help='Sets the brightness of the display, default={}'.format(BRIGHTNESS))
    parser.add_argument('--pong_head', help='Plays a game of pong using head tracking', action='store_true')
    parser.add_argument('--segment', help='Displays a segmented display of an image', action='store_true')
    parser.add_argument('--text', type=str, help='Displays a string of text')

    args = parser.parse_args()

    if args.brightness:
        BRIGHTNESS = args.brightness

    if args.pong:
        pong()
    elif args.rainbow:
        rainbow()
    elif args.pong_head:
        pong_head()
    elif args.segment:
        segment()
    elif args.text:
        text(args.text)
