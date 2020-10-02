from adafruit_servokit import ServoKit

RANGES = {0: (0, 270), 1: (30, 270), 2: (20, 270), 3: (0, 180)}


def setupServos(kit):
    # Set the actuation range
    kit.servo[0].actuation_range = 270
    kit.servo[1].actuation_range = 270
    kit.servo[2].actuation_range = 270
    # Set the PWM range
    kit.servo[0].set_pulse_width_range(500, 2500)
    kit.servo[1].set_pulse_width_range(500, 2500)
    kit.servo[2].set_pulse_width_range(500, 2500)
    # Set the initial Angle
    kit.servo[0].angle = RANGES[0][0]
    kit.servo[1].angle = RANGES[1][0]
    kit.servo[2].angle = RANGES[2][0]


class Robot:
    def __init__(self):
        self.kit = ServoKit(channels=16)
        setupServos(self.kit)

    def goto(self, angle1, angle2, angle3, angle4=0):
        self.kit.servo[0].angle = angle1 + RANGES[0][0]
        self.kit.servo[1].angle = angle2 + RANGES[1][0]
        self.kit.servo[2].angle = angle3 + RANGES[2][0]
        self.kit.servo[3].angle = angle4 + RANGES[3][0]
