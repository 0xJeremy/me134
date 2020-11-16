from motor_driver import DFRobot_DC_Motor_IIC
from time import sleep
from threading import Thread
from pid import PID

BUS = 1
ADDR_1 = 0x10
ADDR_2 = 0x11

MOTOR_RATIO = 20.4


def boundSpeed(value):
    if value > 100:
        return 100
    if value < -100:
        return -100
    return value


P = 1.0
I = 0.0
D = 0.0


# class Wheel:
#     def __init__(self, driver, id):
#         self.driver = driver
#         self.id = id
#         self.setpoint = 0
#         self.stopped = False
#         self.pid = PID(P=P, I=I, D=D)
#         Thread(target=self.run, args=()).start()

#     def run(self):
#         while not self.stopped:
#             self._goto()
#             sleep(0.01)

#     def _goto(self):
#         actualSpeed = self.driver.get_encoder_speed([self.id])[0]
#         speed = boundSpeed(self.pid.update(actualSpeed))

#         direction = self.driver.CW
#         if speed < 0:
#             speed = -speed
#             direction = self.driver.CCW
#         self.driver.motor_movement([self.id], direction, speed)

#     def speed(self, speed):
#         self.pid.SetPoint = speed
#         self._goto()

#     def stop(self):
#         self.stopped = True


class Wheel:
    def __init__(self, driver, id):
        self.driver = driver
        self.id = id

    def speed(self, speed):
        direction = self.driver.CW
        if speed < 0:
            speed = -speed
            direction = self.driver.CCW
        self.driver.motor_movement([self.id], direction, speed)


class Robot:
    def __init__(self):
        self.drivers = [
            DFRobot_DC_Motor_IIC(BUS, ADDR_1),
            DFRobot_DC_Motor_IIC(BUS, ADDR_2),
        ]

        self.wheels = [
            Wheel(self.drivers[1], self.drivers[1].M1),
            Wheel(self.drivers[1], self.drivers[1].M2),
            Wheel(self.drivers[0], self.drivers[0].M1),
        ]

        self.initialize()

    def initialize(self):
        for driver in self.drivers:
            while driver.begin() != driver.STA_OK:
                print("Waiting for driver to load...")
                sleep(1)
            driver.set_encoder_enable(driver.ALL)
            driver.set_encoder_reduction_ratio(driver.ALL, MOTOR_RATIO)
            driver.set_moter_pwm_frequency(1000)

    def speed(self, motor, speed):
        self.wheels[motor].speed(speed)

    def speedAll(self, speed):
        for wheel in self.wheels:
            wheel.speed(speed)

    def stop(self):
        # for wheel in self.wheels:
        #     wheel.stop()
        for driver in self.drivers:
            driver.motor_stop(driver.ALL)
