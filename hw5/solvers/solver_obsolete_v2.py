import matplotlib.pyplot as plt
import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from collections import deque

# TRANSITIONS = deque([0, 1, 0, 1, -1, 0, 0, -1])
TRANSITIONS = deque([0, 0, 0, 1, 0, 0, -1, 0])
# TRANSITIONS.rotate(-1)
TURN_ANGLE = 40


def translate(value, leftMin, leftMax, rightMin, rightMax):
    return rightMin + (
        (float(value - leftMin) / float(leftMax - leftMin)) * (rightMax - rightMin)
    )


class Point:
    def __init__(self, joint=0, theta1=0, theta2=0):
        self.joint = joint
        self.theta1 = theta1
        self.theta2 = theta2
        self.positive = self.theta1 != 90
        self.transition = 0

    def setTranslation(self, value):
        self.transition = value

    def update(self, tick):
        # self.theta1 += tick if self.positive else -1 * tick
        self.theta1 = 90 - tick if self.positive else tick
        # if self.theta1 == 90:
        #     self.positive != self.positive
        if self.transition != 0:
            self.theta2 = translate(tick, 90, 0, 0, self.transition * TURN_ANGLE)


def makeWireframe(points, offset=0):
    # x, y, z, theta1, theta2
    nodes = np.zeros((len(points) + 1, 5))
    nodes[0] = [0, 0, 0, points[0].theta1, points[0].theta2]
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
        self.tick = 0
        self.stepSize = 1
        # self.points = [
        #     Point(joint=0, theta2=TURN_ANGLE),
        #     Point(joint=1, theta1=90),
        #     Point(joint=2),
        #     Point(joint=3, theta1=90, theta2=-TURN_ANGLE),
        #     Point(joint=4),
        #     Point(joint=5, theta1=90),
        #     Point(joint=6),
        #     Point(joint=7, theta1=90, theta2=TURN_ANGLE)
        # ]
        self.points = [
            Point(joint=0),
            Point(joint=1, theta1=90),
            Point(joint=2),
            Point(joint=3, theta1=90, theta2=-TURN_ANGLE),
            Point(joint=4),
            Point(joint=5, theta1=90),
            Point(joint=6, theta2=TURN_ANGLE),
            Point(joint=7, theta1=90),
        ]
        self.setTranslations()
        self.update()

    def setTranslations(self):
        for i, point in enumerate(self.points):
            point.setTranslation(TRANSITIONS[i])

    def update(self):
        self.tick += self.stepSize
        # if self.tick == 90:
        #     TRANSITIONS.rotate(-1)
        #     self.setTranslations()
        #     print(TRANSITIONS)
        for point in self.points:
            point.update(self.tick)

    def plot(self):
        figure = plt.figure()
        ax = figure.gca(projection="3d")

        minX, maxX = 100, 0
        minY, maxY = 100, 0
        minZ, maxZ = -1, 1

        def plotState():
            nonlocal minX, maxX, minY, maxY, minZ, maxZ
            plt.cla()
            nodes = makeWireframe(self.points)
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
                ax.scatter(x, z, y, label="{}".format(counter))
                counter += 1
            ax.plot(xs, zs, ys)
            plt.legend()
            plt.pause(0.01)

        # self.update()
        print(makeWireframe(self.points, self.tick // 90))

        plotState()

        for i in range(90):
            self.update()
            plotState()

        plt.show()

    # def debug(self):
    #     points1 = [
    #         Point(theta2=TURN_ANGLE),
    #         Point(theta1=90),
    #         Point(),
    #         Point(theta1=90, theta2=-TURN_ANGLE),
    #         Point(),
    #         Point(theta1=90),
    #         Point(),
    #         Point(theta1=90, theta2=TURN_ANGLE),
    #     ]
    #     points2 = [
    #         Point(theta1=90),
    #         Point(),
    #         Point(theta1=90, theta2=-TURN_ANGLE),
    #         Point(),
    #         Point(theta1=90),
    #         Point(),
    #         Point(theta1=90),
    #         Point(theta2=TURN_ANGLE/2),
    #     ]
    #     points3 = [
    #         Point(),
    #         Point(theta1=90),
    #         Point(theta2=TURN_ANGLE),
    #         Point(theta1=90),
    #         Point(),
    #         Point(theta1=90, theta2=-TURN_ANGLE),
    #         Point(),
    #         Point(theta1=90),
    #     ]

    #     TRANSITIONS = deque([0, 1, 0, 1, -1, 0, 0, -1])

    #     figure = plt.figure()
    #     ax = figure.gca(projection="3d")

    #     nodes = makeWireframe(points1, self.tick // 90)

    #     xs = nodes[:, 0]
    #     ys = nodes[:, 1]
    #     zs = nodes[:, 2]

    #     counter = 0
    #     for x, y, z in zip(xs, ys, zs):
    #         ax.scatter(x, z, y, label="{}".format(counter))
    #         counter += 1
    #     ax.plot(xs, zs, ys)
    #     plt.legend()

    #     nodes = makeWireframe(points2, self.tick // 90)

    #     xs = nodes[:, 0]
    #     ys = nodes[:, 1]
    #     zs = nodes[:, 2]

    #     figure = plt.figure()
    #     ax = figure.gca(projection="3d")

    #     counter = 0
    #     for x, y, z in zip(xs, ys, zs):
    #         ax.scatter(x, z, y, label="rot {}".format(counter))
    #         counter += 1
    #     ax.plot(xs, zs, ys)
    #     plt.legend()

    #     nodes = makeWireframe(points3, self.tick // 90)

    #     xs = nodes[:, 0]
    #     ys = nodes[:, 1]
    #     zs = nodes[:, 2]

    #     figure = plt.figure()
    #     ax = figure.gca(projection="3d")

    #     counter = 0
    #     for x, y, z in zip(xs, ys, zs):
    #         ax.scatter(x, z, y, label="full {}".format(counter))
    #         counter += 1
    #     ax.plot(xs, zs, ys)
    #     plt.legend()

    #     plt.show()


if __name__ == "__main__":
    solver = Solver()
    solver.plot()
    # solver.debug()
