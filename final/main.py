# 172.20.10.2 on iPhone

from xbox_controller import XboxController
from debounce import debounce
from routines import wall
from robot import Robot
from camera import Camera
from publisher import Publisher
import time

moveTimeout = 1
raiseLowerTimeout = 0.5


def main():
    robot = Robot()

    def forward(value):
        if value:
            print("Forward!")
            robot.forward()

    def backward(value):
        if value:
            print("Backward!")
            robot.backward()

    def turnLeft(value):
        if value:
            print("Turn Left!")
            robot.turnLeft()

    def turnRight(value):
        if value:
            print("Turn Right!")
            robot.turnRight()

    def controlCallBack(xboxControlId, value):
        if value == 0:
            return
        if xboxControlId == 13:  # right bumper
            print("Go tall")
            robot.goTall()
        elif xboxControlId == 12:  # left bumper
            print("Go short")
            robot.goShort()

        elif xboxControlId == 4 and value == 1:  # right trigger, full decompress
            print("Run Autonomous Wall!")
            wall(robot)
        elif xboxControlId == 5 and value == 1:  # left trigger, full decompress
            print("Run Autonomous Debris")
        # print("Control Id = {}, Value = {}".format(xboxControlId, value))

    controller = XboxController(controlCallBack)
    controller.setupControlCallback(
        controller.XboxControls.Y, turnLeft
    )  # actually button X
    controller.setupControlCallback(controller.XboxControls.A, backward)
    controller.setupControlCallback(controller.XboxControls.B, turnRight)
    controller.setupControlCallback(
        controller.XboxControls.LB, forward
    )  # actually Y button

    publisher = Publisher()
    camera = Camera(callback=publisher.sendImage).start()

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
        camera.stop()


if __name__ == "__main__":
    main()
