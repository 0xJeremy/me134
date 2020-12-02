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

    def forward(value):
        debounce(robot.forward, moveTimeout)

    def backward(value):
        debounce(robot.backward, moveTimeout)

    def turnLeft(value):
        debounce(robot.turnLeft, moveTimeout)

    def turnRight(value):
        debounce(robot.turnRight, moveTimeout)

    def up(value):
        debounce(robot.up, raiseLowerTimeout)

    def down(value):
        debounce(robot.down, raiseLowerTimeout)

    controller.setupControlCallback(controller.XboxControls.Y, forward)
    controller.setupControlCallback(controller.XboxControls.A, backward)
    controller.setupControlCallback(controller.XboxControls.X, turnLeft)
    controller.setupControlCallback(controller.XboxControls.B, turnRight)
    controller.setupControlCallback(controller.XboxControls.RTRIGGER, up)
    controller.setupControlCallback(controller.XboxControls.LTRIGGER, down)

    controller.start()
    robot.stand(knee=155, foot=65, runtime=0.060)
    print("Ready!")
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        print("Closing program...")
    finally:
        controller.stop()


if __name__ == "__main__":
    main()
