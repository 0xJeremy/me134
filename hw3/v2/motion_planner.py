import numpy as np
import math
import sympy as sym

# https://stackoverflow.com/questions/1969240/mapping-a-range-of-values-to-another
def mapValue(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)


class Linkage:
    length = 0
    angle = 0
    origin = [0, 0]

    def __init__(self, length, angle, origin):
        self.length = length
        self.angle = angle
        self.origin = np.array(origin)

    def tip(self):
        return (
            self.length
            * np.array(
                [math.cos(math.radians(self.angle)), math.sin(math.radians(self.angle))]
            )
            + self.origin
        )


class MotionPlanner:
    def __init__(self, arm="short"):
        if arm is "short":
            self.links = [
                Linkage(46, 180, [0, 0]),  # Driver A
                Linkage(60, 64, [0, 0]),  # Driver B
                Linkage(60, 64, [-46, 0]),  # Link A to lever arm
                Linkage(46, 0, [-46, 60]),  # First section of lever arm
                Linkage(64, 0, [0, 60]),  # End effector of lever arm
            ]
        else:
            self.links = [
                Linkage(65, 180, [0, 0]),  # Driver A
                Linkage(85, 90, [0, 0]),  # Driver B
                Linkage(85, 90, [-65, 0]),  # Link A to lever arm
                Linkage(65, 0, [-65, 85]),  # First section of lever arm
                Linkage(90, 0, [0, 85]),  # End effector of lever arm
            ]

        self.theta0 = sym.Symbol("theta0", real=True)
        self.theta1 = sym.Symbol("theta1", real=True)
        self.theta2 = sym.Symbol("theta2", real=True)
        self.theta3 = sym.Symbol("theta3", real=True)

        self.x2 = sym.Symbol("x2", real=True)
        self.y2 = sym.Symbol("y2", real=True)
        self.x3 = sym.Symbol("x3", real=True)
        self.y3 = sym.Symbol("y3", real=True)

        self.e1 = sym.Eq(self.x3, self.x2 + self.links[2].length * sym.cos(self.theta2))
        self.e2 = sym.Eq(self.y3, self.y2 + self.links[2].length * sym.sin(self.theta2))
        self.e3 = sym.Eq(
            self.x3,
            self.links[1].length * sym.cos(self.theta1)
            - self.links[3].length * sym.cos(self.theta3),
        )
        self.e4 = sym.Eq(
            self.y3,
            self.links[1].length * sym.sin(self.theta1)
            - self.links[3].length * sym.sin(self.theta3),
        )
        self.e5 = sym.Eq(self.x2, self.links[0].length * sym.cos(self.theta0))
        self.e6 = sym.Eq(self.y2, self.links[0].length * sym.sin(self.theta0))

    def getAngles(self, x4, y4):
        e7 = sym.Eq(
            x4,
            self.links[1].length * sym.cos(self.theta1)
            + self.links[4].length * sym.cos(self.theta3),
        )
        e8 = sym.Eq(
            y4,
            self.links[1].length * sym.sin(self.theta1)
            + self.links[4].length * sym.sin(self.theta3),
        )

        solution = sym.nsolve(
            [self.e1, self.e2, self.e3, self.e4, self.e5, self.e6, e7, e8],
            [
                self.theta0,
                self.theta1,
                self.theta2,
                self.theta3,
                self.x2,
                self.y2,
                self.x3,
                self.y3,
            ],
            [
                math.radians(self.links[0].angle),
                math.radians(self.links[1].angle),
                math.radians(self.links[2].angle),
                math.radians(self.links[3].angle),
                self.links[2].origin[0],
                self.links[2].origin[1],
                self.links[3].origin[0],
                self.links[3].origin[1],
            ],
        )

        self.links[0].angle = math.degrees(solution[0])
        self.links[1].angle = math.degrees(solution[1])
        self.links[2].angle = math.degrees(solution[2])
        self.links[3].angle = math.degrees(solution[3])
        self.links[2].origin = [solution[4], solution[5]]
        self.links[3].origin = [solution[6], solution[7]]
        self.links[4].angle = self.links[3].angle
        self.links[4].origin = self.links[3].tip()

        return [math.degrees(solution[0]), math.degrees(solution[1])]


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    def plot_system(links):
        plt.figure()
        for link in links:
            plt.plot([link.origin[0], link.tip()[0]], [link.origin[1], link.tip()[1]])

    planner = MotionPlanner()

    plot_system(planner.links)
    print(planner.getAngles(120, 90))
    plot_system(planner.links)
    print(planner.getAngles(90, 95))
    plot_system(planner.links)
    print(planner.getAngles(95, 92.5))
    plot_system(planner.links)
    print(planner.getAngles(100, 95))
    plot_system(planner.links)
    print(planner.getAngles(100, 90))
    plot_system(planner.links)

    plt.show()
