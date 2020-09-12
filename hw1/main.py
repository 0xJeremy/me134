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
            direction_left = self.driver.CW
            if motor_left_speed < 0:
                direction_left = self.driver.CCW
                motor_left_speed *= -1
            self.driver.motor_movement(
                [self.driver.M1], direction_left, motor_left_speed
            )
            print(
                "Setting left motor to {} with power {}".format(
                    direction_left, motor_left_speed
                )
            )
        if motor_right_speed is not None:
            direction_right = self.driver.CW
            if motor_right_speed < 0:
                direction_right = self.driver.CCW
                motor_right_speed *= -1
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
        time.sleep(0.01)

    def stop(self):
        self.driver.motor_stop(self.driver.ALL)


def main():
    robot = Robot()
    controller = xbox_one()

    def leftWheel(value):
        robot.move(motor_left_speed=value*100)

    def rightWheel(value):
        robot.move(motor_right_speed=value*100)

    def stopRobot(value):
        robot.stop()

    controller.setupControlCallback(controller.ctrls.LTHUMBY, leftWheel)
    controller.setupControlCallback(controller.ctrls.RTHUMBY, rightWheel)
    controller.setupControlCallback(controller.ctrls.X, stopRobot)

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        print("Closing program...")
    finally:
        robot.stop()
        controller.stop()


if __name__ == "__main__":
    main()
