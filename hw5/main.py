# 172.20.10.2 on iPhone

from robot import Robot
from xbox_controller import XboxController


def main():
    robot = Robot()
    xbox = XboxController()

    # Callback handlers for xbox-controller
    def leftWheel(value):
        robot.updateModel(value * 100)

    def rightWheel(value):
        robot.updateModel(value * 100)

    def stopRobot(value):
        robot.stop()

    # Setup callbacks
    xbox.setupControlCallback(xbox.XboxControls.LTHUMBY, leftWheel)
    xbox.setupControlCallback(xbox.XboxControls.RTHUMBY, rightWheel)
    xbox.setupControlCallback(xbox.XboxControls.X, stopRobot)


if __name__ == "__main__":
    main()
