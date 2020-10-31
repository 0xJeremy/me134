import matplotlib.pyplot as plt
import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from collections import deque

# TRANSITIONS = deque([0, 1, 0, 1, -1, 0, 0, -1])
TRANSITIONS = deque([-1, 0, -1, 1, 0, 0, 0, -0.5])
# TRANSITIONS.rotate(-1)
print(TRANSITIONS)
TURN_ANGLE = 40


def translate(value, leftMin, leftMax, rightMin, rightMax):
    return rightMin + (
        (float(value - leftMin) / float(leftMax - leftMin)) * (rightMax - rightMin)
    )


class Point:
    def __init__(self, theta1=0, theta2=0):
        self.theta1 = theta1
        self.theta2 = theta2
        self.positive = self.theta1 != 90
        self.transition = 0

    def setTranslation(self, value):
        self.transition = value

    def update(self, size, tick):
        self.theta1 = 90 - tick if self.positive else tick
        if self.transition != 0:
            self.theta2 = translate(tick, 0, 90, 0, self.transition*TURN_ANGLE)


def makeWireframe(points, offsetX=0):
    # x, y, z, theta1, theta2
    nodes = np.zeros((len(points) + 1, 5))
    nodes[0] = [offsetX, 0, 0, points[0].theta1, points[0].theta2]
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


class Solver:
    def __init__(self):
        self.translationCounter = 0
        self.stepSize = 1
        self.points = [
            Point(theta2=TURN_ANGLE),
            Point(theta1=90),
            Point(),
            Point(theta1=90, theta2=-TURN_ANGLE),
            Point(),
            Point(theta1=90),
            Point(),
            Point(theta1=90, theta2=TURN_ANGLE),
        ]
        self.setTranslations()

    def setTranslations(self):
        for i, point in enumerate(self.points):
            point.setTranslation(TRANSITIONS[i])

    def update(self):
        self.translationCounter -= self.stepSize
        # if self.translationCounter == 90:
        #     TRANSITIONS.rotate(-1)
        #     self.setTranslations()
        #     print(TRANSITIONS)
        for point in self.points:
            point.update(self.stepSize, self.translationCounter % 90)

    def plot(self):
        figure = plt.figure()
        ax = figure.gca(projection="3d")

        minX, maxX = 100, 0
        minY, maxY = 100, 0
        minZ, maxZ = -1, 1

        def plotState():
            nonlocal minX, maxX, minY, maxY, minZ, maxZ
            plt.cla()
            nodes = makeWireframe(self.points, self.translationCounter // 90)
            xs = nodes[:, 0]
            ys = nodes[:, 1]
            zs = nodes[:, 2]

            minX, maxX = min(min(xs), minX), max(max(xs), maxX)
            minY, maxY = min(min(ys), minY), max(max(ys), maxY)
            minZ, maxZ = min(min(zs), minZ), max(max(zs), maxZ)

            plt.xlim(minX, maxX)
            plt.ylim(minZ, maxZ)
            ax.set_zlim(minY, maxY)

            # print(nodes)
            counter = 0
            for x, y, z in zip(xs, ys, zs):
                ax.scatter(x, z, y, label="{}".format(counter))
                counter += 1
            ax.plot(xs, zs, ys)
            plt.legend()
            plt.pause(0.01)

        plotState()

        for i in range(90):
            self.update()
            plotState()

        plt.show()

    def debug(self):
        points1 = [
            Point(theta2=TURN_ANGLE),
            Point(theta1=90),
            Point(),
            Point(theta1=90, theta2=-TURN_ANGLE),
            Point(),
            Point(theta1=90),
            Point(),
            Point(theta1=90, theta2=TURN_ANGLE),
        ]
        points2 = [
            Point(theta1=90),
            Point(),
            Point(theta1=90, theta2=-TURN_ANGLE),
            Point(),
            Point(theta1=90),
            Point(),
            Point(theta1=90),
            Point(theta2=TURN_ANGLE/2),
        ]
        points3 = [
            Point(),
            Point(theta1=90),
            Point(theta2=TURN_ANGLE),
            Point(theta1=90),
            Point(),
            Point(theta1=90, theta2=-TURN_ANGLE),
            Point(),
            Point(theta1=90),
        ]

        TRANSITIONS = deque([0, 1, 0, 1, -1, 0, 0, -1])

        figure = plt.figure()
        ax = figure.gca(projection="3d")

        nodes = makeWireframe(points1, self.translationCounter // 90)

        xs = nodes[:, 0]
        ys = nodes[:, 1]
        zs = nodes[:, 2]

        counter = 0
        for x, y, z in zip(xs, ys, zs):
            ax.scatter(x, z, y, label="{}".format(counter))
            counter += 1
        ax.plot(xs, zs, ys)
        plt.legend()


        nodes = makeWireframe(points2, self.translationCounter // 90)

        xs = nodes[:, 0]
        ys = nodes[:, 1]
        zs = nodes[:, 2]


        figure = plt.figure()
        ax = figure.gca(projection="3d")

        counter = 0
        for x, y, z in zip(xs, ys, zs):
            ax.scatter(x, z, y, label="rot {}".format(counter))
            counter += 1
        ax.plot(xs, zs, ys)
        plt.legend()




        nodes = makeWireframe(points3, self.translationCounter // 90)

        xs = nodes[:, 0]
        ys = nodes[:, 1]
        zs = nodes[:, 2]


        figure = plt.figure()
        ax = figure.gca(projection="3d")

        counter = 0
        for x, y, z in zip(xs, ys, zs):
            ax.scatter(x, z, y, label="full {}".format(counter))
            counter += 1
        ax.plot(xs, zs, ys)
        plt.legend()

        plt.show()
        




if __name__ == "__main__":
    solver = Solver()
    solver.plot()
    # solver.debug()
