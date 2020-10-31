import matplotlib.pyplot as plt
import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from collections import deque


class Point:
    def __init__(self, theta1=0, theta2=0):
        self.theta1 = theta1
        self.theta2 = theta2
        self.positive = self.theta1 != 90

    def update(self, size=1):
        self.theta1 += size if self.positive else -1 * size


def makeWireframe(points):
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


TRANSITIONS = [-1, 0, -1, 1, 0, 0, 1, 0]


class Solver:
    def __init__(self):
        self.translationCounter = 0
        self.stepSize = 1
        angle = 20
        self.points = [
            Point(theta2=angle),
            Point(theta1=90),
            Point(),
            Point(theta1=90, theta2=-angle),
            Point(),
            Point(theta1=90),
            Point(),
            Point(theta1=90, theta2=angle),
        ]

    def update(self):
        for point in self.points:
            point.update()

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

            # print(nodes)
            ax.plot(xs, zs, ys)
            plt.pause(0.05)

        plotState()

        # for i in range(90):
        #     self.update()
        #     plotState()

        plt.show()


if __name__ == "__main__":
    solver = Solver()
    solver.plot()
