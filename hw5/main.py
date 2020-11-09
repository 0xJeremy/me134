# 172.20.10.2 on iPhone

from robot import Robot
from xbox_controller import XboxController
import time

DEBOUNCE = 0.2


timer = time.time()


def resetTimer():
    timer = time.time()


def main():
    robot = Robot()
    xbox = XboxController()

    # Callback handlers for xbox-controller
    def forward(value):
        if time.time() - timer < DEBOUNCE:
            return
        print("Forward!")
        robot.move(1)
        resetTimer()

    def reverse(value):
        if time.time() - timer < DEBOUNCE:
            return
        print("Reverse!")
        robot.move(-1)
        resetTimer()

    def turnRight(value):
        if time.time() - timer < DEBOUNCE:
            return
        print("Turning Right!")
        robot.turn(1)
        resetTimer()

    def turnLeft(value):
        if time.time() - timer < DEBOUNCE:
            return
        print("Turning Left!")
        robot.turn(-1)
        resetTimer()

    def reset(value):
        if time.time() - timer < DEBOUNCE:
            return
        print("Reset!")
        robot.reset()
        resetTimer()

    # Setup callbacks
    xbox.setupControlCallback(xbox.XboxControls.Y, forward)
    xbox.setupControlCallback(xbox.XboxControls.A, reverse)
    xbox.setupControlCallback(xbox.XboxControls.X, turnLeft)
    xbox.setupControlCallback(xbox.XboxControls.B, turnRight)
    xbox.setupControlCallback(xbox.XboxControls.START, reset)

    # Main run loop
    xbox.start()
    print("Ready!")
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        print("Closing program...")
    finally:
        xbox.stop()


if __name__ == "__main__":
    main()
