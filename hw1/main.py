import time
from xbox_one import xbox_one
from motor_driver import DFRobot_DC_Motor_IIC

BUS = 1
ADDRESS = 0x10

# def board_detect():
#   l = DFRobot_DC_Motor_IIC.detecte()
#   print("Board list conform:")
#   print(l)


class Robot:
    def __init__(self):
        self.driver = DFRobot_DC_Motor_IIC(BUS, ADDRESS)

    def move(self, motor_left_speed=None, motor_right_speed=None):
        if motor_left_speed is not None:
            direction_left = self.driver.CW if motor_left_speed > 0 else self.driver.CCW
            self.driver.motor_movement(
                [self.driver.M1], direction_left, motor_left_speed
            )
            print(
                "Setting left motor to {} with power {}".format(
                    direction_left, motor_left_speed
                )
            )
        if motor_right_speed is not None:
            direction_right = (
                self.driver.CW if motor_right_speed > 0 else self.driver.CCW
            )
            self.driver.motor_movement(
                [self.driver.M2], direction_right, motor_right_speed
            )
            print(
                "Setting right motor to {} with power {}".format(
                    direction_right, motor_right_speed
                )
            )

    def stop(self):
        self.move(0, 0)


def main():
    robot = Robot()
    controller = xbox_one()

    def leftWheel(value):
        robot.move(motor_left_speed=value)

    def rightWheel(value):
        robot.move(motor_right_speed=value)

    def stopRobot():
        robot.stop()

    controller.setupControlCallback(controller.ctrls.LTHUMBX, leftWheel)
    controller.setupControlCallback(controller.ctrls.LTHUMBY, rightWheel)
    controller.setupControlCallback(controller.ctrls.X, stopRobot)

    while True:
        try:
            time.sleep(5)
        except KeyboardInterrupt:
            robot.stop()


if __name__ == "__main__":
    main()
