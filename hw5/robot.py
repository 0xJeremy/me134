from solver import Solver
from adafruit_servokit import ServoKit

# link -> kit number, channel number
LINKS = {
    0: (1, 0),
    1: (1, 1),
    2: (1, 2),
    3: (1, 3),
    4: (1, 4),
    5: (1, 5),
    6: (1, 6),
    7: (1, 7),
    8: (2, 0),
    9: (2, 1),
    10: (2, 2),
    11: (2, 3),
    12: (2, 4),
    13: (2, 5),
    14: (2, 6),
    15: (2, 7),
}


class Robot:
    def __init__(self):
        self.solver = Solver()
        self.kits = [
            ServoKit(channels=16, address=0x40),
            ServoKit(channels=16, address=0x41),
        ]

    def updateModel(self, value):
        print("Updating model... {}".format(value))

    def updatePosition(self):
        points = self.solver.getPoints()
        for i, point in enumerate(points):
            link1 = LINKS[i]
            link2 = LINKS[i + 1]
            self.kits[link1[0]].servo[link1[1]] = point.theta1
            self.kits[link2[0]].servo[link2[1]] = point.theta2

    def stop(self):
        pass
