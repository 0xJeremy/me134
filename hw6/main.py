# 172.20.10.2 on iPhone

import argparse
import time
from receiver import Receiver
from pong import Pong, WIDTH, HEIGHT
from display import Display
from textscroller import TextScroller
from segment import Segmenter

BRIGHTNESS = 0.5
SHOW_INTRO = True


def pong():
    receiver = Receiver().start()
    pong = Pong()
    display = Display(brightness=BRIGHTNESS)

    if SHOW_INTRO:
        scroller = TextScroller()
        scroller.displayTextScroll(display, "Welcome to PONG!")
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

            display.set(pong.getBoard(display))
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
    import cv2

    display = Display(brightness=BRIGHTNESS)
    engine = Segmenter()
    cam = cv2.VideoCapture(0)

    try:
        while True:
            start = time.time()
            ret, frame = cam.read()
            frame = cv2.flip(frame, 1)
            start = time.time()
            engine.inference(frame)
            display.set(engine.getForDisplay())
            # cv2.imshow("frame", engine.getForDisplay())
            print("{:.2f} ms".format((time.time() - start) * 1000))
    except KeyboardInterrupt:
        cam.release()


def text(text):
    scroller = TextScroller()
    disp = Display(brightness=BRIGHTNESS)
    time.sleep(1)
    scroller.displayTextScroll(disp, text)


def snake():
    # import cv2
    from snake import Snake

    # from facedetector2 import FaceDetector
    from facedetector import FaceDetector

    detector = FaceDetector().start()
    display = Display(brightness=BRIGHTNESS)

    if SHOW_INTRO:
        scroller = TextScroller()
        scroller.displayTextScroll(display, "This is SNAKE!")
    snake = Snake()

    while detector.frame is None:
        time.sleep(0.1)

    while True:
        board = snake.generateBoard()
        display.set(board)

        move = detector.quadrant
        print(move)
        snake.setVelocity(x=move[0], y=move[1])

        # key = input()
        # if key == 'q':
        #     break
        # elif key == 'w':
        #     snake.setVelocity(x=-1, y=0)
        # elif key == 'a':
        #     snake.setVelocity(x=0, y=-1)
        # elif key == 's':
        #     snake.setVelocity(x=1, y=0)
        # elif key == 'd':
        #     snake.setVelocity(x=0, y=1)

        snake.step()
        time.sleep(0.5)
        if snake.lost:
            board = snake.generateBoard()
            display.set(board)
            time.sleep(3)
            snake.reset()
            # break


def video():
    from video import Video

    video = Video()
    display = Display(brightness=BRIGHTNESS)
    video.play(display)


def mirror():
    from mirror import Mirror

    mirror = Mirror()
    display = Display(brightness=BRIGHTNESS)
    mirror.play(display)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("A small robotics project :)")
    parser.add_argument(
        "--pong",
        help="Plays a game of pong! (requires streaming from a laptop)",
        action="store_true",
    )
    parser.add_argument(
        "--rainbow", help="Displays a nice rainbow :)", action="store_true"
    )
    parser.add_argument(
        "--brightness",
        type=float,
        help="Sets the brightness of the display, default={}".format(BRIGHTNESS),
    )
    parser.add_argument(
        "--pong_head",
        help="Plays a game of pong using head tracking!",
        action="store_true",
    )
    parser.add_argument(
        "--segment",
        help="Displays a segmented display of an image",
        action="store_true",
    )
    parser.add_argument("--text", type=str, help="Displays a string of text")
    parser.add_argument("--snake", help="Plays a game of snake!", action="store_true")
    parser.add_argument("--skip", help="Skips the intro screen of any game", action="store_true")
    parser.add_argument("--video", help="Plays a video!", action="store_true")
    parser.add_argument(
        "--mirror", help="Displays the camera input", action="store_true"
    )

    args = parser.parse_args()

    if args.brightness:
        BRIGHTNESS = args.brightness

    if args.skip:
        SHOW_INTRO = False

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
    elif args.snake:
        snake()
    elif args.video:
        video()
    elif args.mirror:
        mirror()
