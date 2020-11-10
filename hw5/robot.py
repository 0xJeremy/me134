from solver3 import Solver
from adafruit_servokit import ServoKit

# link -> kit number, channel number, min pulse width, max pulse width
LINKS = {
    0: (0, 0, 400, 2500),
    1: (0, 1, 400, 2500),
    2: (0, 2, 400, 2500),
    3: (0, 3, 500, 2600),
    4: (0, 4, 400, 2500),
    5: (0, 5, 400, 2500),
    6: (0, 6, 400, 2500),
    7: (0, 7, 300, 2400),
    8: (1, 0, 300, 2500),
    9: (1, 1, 500, 2600),
    10: (1, 2, 400, 2500),
    11: (1, 3, 400, 2500),
    12: (1, 4, 400, 2500),
    13: (1, 5, 500, 2600),
    14: (1, 6, 400, 2500),
    15: (1, 7, 500, 2600),
}


class Robot:
    def __init__(self):
        self.solver = Solver()
        self.kits = [
            ServoKit(channels=16, address=0x40),
            ServoKit(channels=16, address=0x41),
        ]
        self.tick = 0
        for link in LINKS.values():
            self.kits[link[0]].servo[link[1]].set_pulse_width_range(link[2], link[3])
        self.updatePosition()

    def move(self, direction):
        self.solver.step(direction)
        self.updatePosition()

    def turn(self, direction):
        self.solver.turn(direction)
        self.updatePosition()

    def updatePosition(self):
        points = self.solver.getPoints()

        for i in range(0, 15, 2):
            link1 = LINKS[i]
            link2 = LINKS[i + 1]
            self.kits[link1[0]].servo[link1[1]].angle = points[int(i / 2)].theta1
            self.kits[link2[0]].servo[link2[1]].angle = points[int(i / 2)].theta2

    def reset(self, angle=90):
        for i in range(16):
            for kit in self.kits:
                kit.servo[i].angle = angle
