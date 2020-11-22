# 172.20.10.2 on iPhone

from xbox_controller import XboxController
from debounce import debounce
from robot import Robot
import time

moveTimeout = 1
raiseLowerTimeout = 0.5


def main():
    robot = Robot()
    controller = XboxController()

    def forward():
        debounce(robot.forward, moveTimeout)

    def backward():
        debounce(robot.backward, moveTimeout)

    def turnLeft():
        debounce(robot.turnLeft, moveTimeout)

    def turnRight():
        debounce(robot.turnRight, moveTimeout)

    def up():
        debounce(robot.up, raiseLowerTimeout)

    def down():
        debounce(robot.down, raiseLowerTimeout)

    controller.setupControlCallback(controller.XboxControls.Y, forward)
    controller.setupControlCallback(controller.XboxControls.A, backward)
    controller.setupControlCallback(controller.XboxControls.X, turnLeft)
    controller.setupControlCallback(controller.XboxControls.B, turnRight)
    controller.setupControlCallback(controller.XboxControls.RTRIGGER, up)
    controller.setupControlCallback(controller.XboxControls.LTRIGGER, down)

    controller.start()
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
