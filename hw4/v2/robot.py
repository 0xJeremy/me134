from motor_driver import DFRobot_DC_Motor_IIC
from wheel import Wheel

BUS = 1
ADDR_1 = 0x10
ADDR_2 = 0x11


class Robot:
    def __init__(self):
        self.drivers = [
            DFRobot_DC_Motor_IIC(BUS, ADDR_1),
            DFRobot_DC_Motor_IIC(BUS, ADDR_2),
        ]
        self.wheels = [
            Wheel(self.drivers[0], 1),
            Wheel(self.drivers[0], 2),
            Wheel(self.drivers[1], 1),
        ]
