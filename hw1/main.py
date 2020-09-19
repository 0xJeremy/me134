import time
from xbox_controller import XboxController
from motor_driver import DFRobot_DC_Motor_IIC

# Robot IP Address on home network
# 192.168.0.233

BUS = 1
ADDRESS = 0x10

# Robot Class with high-level interface
class Robot:
    def __init__(self):
        self.driver = DFRobot_DC_Motor_IIC(BUS, ADDRESS)
        self.driver.set_encoder_enable(self.driver.ALL)
        self.driver.set_moter_pwm_frequency(1000)

    # Internal move function
    def _move(self, motor, speed):
        direction = self.driver.CW
        if speed < 0:
            direction = self.driver.CCW
            speed *= -1
        self.driver.motor_movement([motor], direction, speed)
        return direction, speed

    # Move interface
    def move(self, motor_left_speed=None, motor_right_speed=None):
        if motor_left_speed is not None:
            direction, speed = self._move(self.driver.M1, motor_left_speed)
            print("Setting left motor to {} with power {}".format(direction, speed))
        if motor_right_speed is not None:
            direction, speed = self._move(self.driver.M2, motor_right_speed * -1)
            print("Setting right motor to {} with power {}".format(direction, speed))
        time.sleep(0.01)

    # Stop interface
    def stop(self):
        self.driver.motor_stop(self.driver.ALL)


def main():
    robot = Robot()
    controller = XboxController()

    # Callback handlers for xbox-controller
    def leftWheel(value):
        robot.move(motor_left_speed=value * 100)

    def rightWheel(value):
        robot.move(motor_right_speed=value * 100)

    def stopRobot(value):
        robot.stop()

    # Setup callbacks
    controller.setupControlCallback(controller.XboxControls.LTHUMBY, leftWheel)
    controller.setupControlCallback(controller.XboxControls.RTHUMBY, rightWheel)
    controller.setupControlCallback(controller.XboxControls.X, stopRobot)

    # Main run loop
    controller.start()
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
