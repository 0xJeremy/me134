import math
from collections import deque

NUM_SEGMENTS = 8
SEGMENT_LENGTH = 1

CONTROL_ORIENTATIONS = {
    1: [0, 1, 0, 0, 1, 1, 0, 0],
    2: [0, 1] * 4,
    3: [0, 0, 1, 1, 0, 0, 1, 1],
}

Y_CONTROL_ORIENTATIONS = {1: [], 2: [1, -1, 0, -1, 2, -1, 0, -1, 0], 3: []}


class Solver:
    def __init__(self, startingPosition=2):
        self.xCounter = 0
        self.xStep = 1
        self.yCounter = 0
        self.yStep = 1
        self.orientation = CONTROL_ORIENTATIONS[startingPosition]
        self.yOrientation = Y_CONTROL_ORIENTATIONS[2]
        self.xs = [90 * i for i in self.orientation]
        self.ys = [5 * i for i in self.yOrientation]

    def setControlOrientation(self, formation):
        self.orientation = CONTROL_ORIENTATIONS[formation]

    def setXStep(self, value):
        self.xStep = value

    def setYStep(self, value):
        self.yStep = value

    def getX(self):
        return self.xs

    def getY(self):
        return self.ys

    def stepX(self):
        self.xCounter += self.xStep
        angle = self.xCounter % 90
        self.xs = [
            90 - angle if self.orientation[j] else angle for j, x in enumerate(self.xs)
        ]
        return self.xs

    def stepY(self):
        offset = self.xCounter // 90
        angle = self.xCounter % 90
        items = deque(self.yOrientation)
        items.rotate(offset)
        ys = []
        for j, y in enumerate(self.ys):
            ys.append(y + (angle * items[j]))
            # ys.append(target-angle if self.yOrientation[j] else angle)
        self.ys = ys
        return self.ys

    def plotX(self):
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D

        figure = plt.figure()
        ax = figure.gca(projection="3d")
        boundary = 0.5

        def makeFigure():
            points = [(0, 0, 0, 0, 0)]
            for jointX, jointY in zip(self.xs, self.ys):

                prev = points[-1]
                newAngleX = prev[3] + jointX
                newAngleY = prev[4] + jointY
                radiansAngleX = math.radians(newAngleX)
                radiansAngleY = math.radians(newAngleY)

                points.append(
                    (
                        prev[0] + math.cos(radiansAngleX) * SEGMENT_LENGTH,
                        prev[1] + math.sin(radiansAngleX) * SEGMENT_LENGTH,
                        prev[2] + math.sin(radiansAngleY) * SEGMENT_LENGTH,
                        newAngleX,
                        newAngleY,
                    )
                )

            plt.cla()
            xs = [point[0] for point in points]
            ys = [point[1] for point in points]
            zs = [point[2] for point in points]
            # plt.xlim(-1, 1)
            # plt.ylim(-0.1, 0.2)
            # ax.set_zlim(0, 2)
            # plt.grid()
            # ax.plot(xs, ys,  linewidth=4)
            counter = 0
            for x, y, z in zip(xs, ys, zs):
                ax.scatter(x, z, y, label="{}".format(counter))
                counter += 1
            plt.legend()
            ax.plot(xs, zs, ys)
            plt.pause(1)

        self.setXStep(10)
        self.setYStep(10)
        for i in range(3):
            self.stepX()
            self.stepY()
            makeFigure()
        # makeFigure()
        plt.show()

    # def plotY(self):
    #     import matplotlib.pyplot as plt
    #     figure = plt.figure()

    #     def makeFigure():
    #         points = [(0, 0, 0)]
    #         for joint in self.ys:


if __name__ == "__main__":
    Solver().plotX()
