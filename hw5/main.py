# 172.20.10.2 on iPhone

from robot import Robot
from xbox_controller import XboxController
import time

DEBOUNCE = 0.3


timer = time.time()
inAutonomous = False


def resetTimer():
    global timer
    timer = time.time()


SLEEP = 1
# 8 forward
# turn +1 1
# 5 forward
# turn -1 2
# reverse 6
# turn +1 2
# forward 1
# turn -1 1
# forward 11 # back at beginning, facing backward
# turn -1 1
# 7 forward
# turn +1 2
# reverse 4
# 15 forward
def autonomous(robot):
    # angle 15
    global inAutonomous
    for i in range(8):
        robot.move(1)
        time.sleep(SLEEP)
    robot.turn(1)
    time.sleep(SLEEP)
    for i in range(5):
        robot.move(1)
        time.sleep(SLEEP * 2)
    robot.turn(-1)
    time.sleep(SLEEP)
    robot.turn(-1)
    time.sleep(SLEEP)
    for i in range(6):
        robot.move(-1)
        time.sleep(SLEEP * 2)
    robot.turn(1)
    time.sleep(SLEEP)
    robot.turn(1)
    time.sleep(SLEEP)
    robot.move(1)
    time.sleep(SLEEP * 2)
    robot.turn(-1)
    time.sleep(SLEEP)

    for i in range(11):
        robot.move(1)
        time.sleep(SLEEP)
    robot.turn(-1)
    time.sleep(SLEEP)
    for i in range(7):
        robot.move(1)
        time.sleep(SLEEP * 2)
    robot.turn(1)
    time.sleep(SLEEP)
    robot.turn(1)
    time.sleep(SLEEP)
    for i in range(4):
        robot.move(-1)
        time.sleep(SLEEP * 2)
    robot.turn(-1)
    time.sleep(SLEEP)
    for i in range(15):
        robot.move(1)
        time.sleep(SLEEP)
    # inAutonomous = False


def main():
    robot = Robot()
    xbox = XboxController()

    # Callback handlers for xbox-controller
    def forward(value):
        if time.time() - timer < DEBOUNCE or inAutonomous:
            return
        resetTimer()
        print("Forward!")
        robot.move(1)

    def reverse(value):
        if time.time() - timer < DEBOUNCE or inAutonomous:
            return
        resetTimer()
        print("Reverse!")
        robot.move(-1)

    def turnRight(value):
        if time.time() - timer < DEBOUNCE or inAutonomous:
            return
        resetTimer()
        print("Turning Right!")
        robot.turn(1)

    def turnLeft(value):
        if time.time() - timer < DEBOUNCE or inAutonomous:
            return
        resetTimer()
        print("Turning Left!")
        robot.turn(-1)

    def reset(value):
        if time.time() - timer < DEBOUNCE or inAutonomous:
            return
        resetTimer()
        print("Reset!")
        robot.reset()

    def auto(value):
        global inAutonomous
        if time.time() - timer < DEBOUNCE or inAutonomous:
            return
        inAutonomous = True
        print("Autonomous!")
        autonomous(robot)

    # Setup callbacks
    xbox.setupControlCallback(
        xbox.XboxControls.START, forward
    )  # actually right trigger
    xbox.setupControlCallback(xbox.XboxControls.A, reverse)
    xbox.setupControlCallback(xbox.XboxControls.Y, turnLeft)  # actually x
    xbox.setupControlCallback(xbox.XboxControls.B, turnRight)
    xbox.setupControlCallback(xbox.XboxControls.BACK, auto)
    # xbox.setupControlCallback(xbox.XboxControls.START, reset)

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
