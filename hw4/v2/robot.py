from motor_driver import DFRobot_DC_Motor_IIC
from time import sleep

BUS = 1
ADDR_1 = 0x10
ADDR_2 = 0x11

MOTOR_RATIO = 20.4


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
            Wheel(self.drivers[0], self.drivers[0].M1),
            Wheel(self.drivers[1], self.drivers[1].M1),
            Wheel(self.drivers[1], self.drivers[1].M2),
        ]

        self.initialize()

    def initialize(self):
        for driver in self.drivers:
            while driver.begin() != driver.STA_OK:
                print("Waiting for driver to load...")
                sleep(2)
            driver.set_encoder_enable(driver.ALL)
            driver.set_encoder_reduction_ratio(driver.ALL, MOTOR_RATIO)
            driver.set_moter_pwm_frequency(1000)

    def speed(self, motor, speed):
        self.wheels[motor].speed(speed)

    def speedAll(self, speed):
        for wheel in self.wheels:
            wheel.speed(speed)

    def stop(self):
        for driver in self.drivers:
            driver.motor_stop(driver.ALL)
