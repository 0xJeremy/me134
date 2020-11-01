import matplotlib.pyplot as plt
import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from collections import deque

TURN_ANGLE = 30



def shift(seq, n=0):
    a = n % len(seq)
    return seq[-a:] + seq[:-a]


def translate(value, leftMin, leftMax, rightMin, rightMax):
    return rightMin + (
        (float(value - leftMin) / float(leftMax - leftMin)) * (rightMax - rightMin)
    )

TRANSLATION = [-1, 1, 0, 1, -1, 0, 0, 0]
TRANSLATION = shift(TRANSLATION, 1)


colors = ["red", "green", "blue", "orange", "darkcyan", "black", "purple", "deeppink"]


class Point:
    def __init__(self, theta1=0, theta2=0):
        self.startTheta1 = theta1
        self.theta1 = theta1
        self.setXDirection()
        self.color = colors.pop()

        self.startTheta2 = theta2
        self.theta2 = theta2
        self.translation = 0

    def setXDirection(self):
        if self.theta1 == 0:
            self.positive = True
        elif self.theta1 == 90:
            self.positive = False

    def assignTranslation(self, translation):
        self.translation = translation

    def updateX(self, tick):
        self.setXDirection()
        self.theta1 += 1 if self.positive else -1

    def updateY(self, tick):
        # return
        if self.translation == -1:
            self.theta2 -= TURN_ANGLE / 90 
        elif self.translation == 1:
            self.theta2 += TURN_ANGLE / 90
        # if self.translation != 0:
        #     self.theta2 = translate(tick, 0, 89, 0, self.translation * TURN_ANGLE)


def makeWireframe(points, offset=0):
    # x, y, z, theta1, theta2
    nodes = np.zeros((len(points) + 1, 5))
    nodes[0] = [offset, 0, offset/2, points[0].theta1, points[0].theta2]
    for i in range(1, len(points)):
        prev = nodes[i - 1]
        prevTheta1 = math.radians(prev[3])
        prevTheta2 = math.radians(prev[4])
        nodes[i] = [
            prev[0] + math.cos(prevTheta1),
            prev[1] + math.sin(prevTheta1),
            prev[2] + math.sin(prevTheta2),
            prev[3] + points[i].theta1,
            points[i].theta2,
        ]
    nodes[-1] = nodes[0]
    return nodes


class xSolver:
    def __init__(self, points):
        self.points = points

    def update(self, tick):
        if tick % 90 == 0:
            self.points = shift(self.points, -1)
        for point in self.points:
            point.updateX(tick)

    def plot(self):
        figure = plt.figure()

        minX, maxX = 100, 0
        minY, maxY = 100, 0

        def plotState(i):
            nonlocal minX, maxX, minY, maxY
            plt.cla()
            nodes = makeWireframe(self.points, i // 90)
            xs = nodes[:, 0]
            ys = nodes[:, 1]

            minX, maxX = min(min(xs), minX), max(max(xs), maxX)
            minY, maxY = min(min(ys), minY), max(max(ys), maxY)

            plt.xlim(minX - 0.5, maxX + 0.5)
            plt.ylim(minY - 0.5, maxY + 0.5)

            counter = 0
            for x, y in zip(xs, ys):
                plt.scatter(
                    x,
                    y,
                    label="{}".format(counter),
                    color=self.points[counter % len(self.points)].color,
                )
                counter += 1
            plt.plot(xs, ys)
            plt.grid()
            plt.pause(0.05)

        for i in range(361):
            self.update(i)
            if i % 4 == 0:
                plotState(i)

        plt.show()


class ySolver:
    def __init__(self, points):
        self.points = points
        self.assignTranslations()

    def assignTranslations(self):
        for i, point in enumerate(self.points):
            point.assignTranslation(TRANSLATION[i])

    def update(self, tick):
        if tick % 90 == 0:
            self.points = shift(self.points, 1)
            self.assignTranslations()
        for point in self.points:
            point.updateY(tick)


class Solver:
    def __init__(self):
        self.points = [
            Point(theta2=TURN_ANGLE),
            Point(theta1=90),
            Point(),
            Point(theta1=90, theta2=-TURN_ANGLE),
            Point(),
            Point(theta1=90),
            Point(),
            Point(theta1=90),
        ]
        # self.points = [
        #     Point(),
        #     Point(theta1=90, theta2=TURN_ANGLE),
        #     Point(),
        #     Point(theta1=90),
        #     Point(theta2=-TURN_ANGLE),
        #     Point(theta1=90),
        #     Point(),
        #     Point(theta1=90),
        # ]
        # self.points = [
        #     Point(),
        #     Point(theta1=90),
        #     Point(theta2=TURN_ANGLE),
        #     Point(theta1=90),
        #     Point(),
        #     Point(theta1=90, theta2=-TURN_ANGLE),
        #     Point(),
        #     Point(theta1=90),
        # ]
        self.xSolver = xSolver(self.points)
        self.ySolver = ySolver(self.points)

    def update(self, tick):
        if tick % 90 == 0:
            self.points = shift(self.points, -1)
            if tick != 0:
                global TRANSLATION
                TRANSLATION = shift(TRANSLATION, 2)
        self.xSolver.update(tick)
        self.ySolver.update(tick)

    def showX(self):
        self.xSolver.plot()

    def showY(self):
        figure = plt.figure()
        ax = figure.gca(projection="3d")

        minX, maxX = 100, 0
        minY, maxY = 100, 0
        minZ, maxZ = -1, 1

        def plotState(i):
            nonlocal minX, maxX, minY, maxY, minZ, maxZ
            plt.cla()
            nodes = makeWireframe(self.points, i // 90)
            xs = nodes[:, 0]
            ys = nodes[:, 1]
            zs = nodes[:, 2]

            minX, maxX = min(min(xs), minX), max(max(xs), maxX)
            minY, maxY = min(min(ys), minY), max(max(ys), maxY)
            minZ, maxZ = min(min(zs), minZ), max(max(zs), maxZ)

            plt.xlim(minX, maxX)
            plt.ylim(minZ, maxZ)
            ax.set_zlim(minY, maxY)

            counter = 0
            for x, y, z in zip(xs, ys, zs):
                ax.scatter(
                    x,
                    z,
                    y,
                    label="{}".format(counter),
                    color=self.points[counter % len(self.points)].color,
                )
                counter += 1
            ax.plot(xs, zs, ys)
            # plt.legend()
            plt.pause(0.01)

        print(makeWireframe(self.points))
        # plotState(0)

        for i in range(270):
            self.update(i)
            if i % 3 == 0:
                plotState(i)
            if i % 90 == 0 and i != 0:
                print(makeWireframe(self.points))
        print(makeWireframe(self.points))

        plt.show()


if __name__ == "__main__":
    solver = Solver()
    # solver.showX()
    solver.showY()
