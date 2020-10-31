import matplotlib.pyplot as plt
import math

NUM_SEGMENTS = 8
SEGMENT_LENGTH = 1


class Oscillator:
    def __init__(self, initial):
        self.state = initial
        self.speed = 0

    def setSpeed(self, speed):
        self.speed = speed

    def next(self):
        pass


class Solver:
    def __init__(self):
        self.xTarget = 0
        self.yTarget = 0
        self.xs = [0, 90] * int(NUM_SEGMENTS / 2)
        self.ys = [0] * NUM_SEGMENTS

    # Accepts values of -100 to 100
    def setXTarget(self):

        pass

    # Accepts values of -100 to 100
    def setYTarget(self):
        pass

    def solveX(self):
        pass

    def solveY(self):
        pass

    def plot(self):
        figure = plt.figure()
        # (x, y, theta)

        def makeFigure():
            points = [(0, 0, 0)]
            for joint in self.xs:

                prev = points[-1]
                newAngle = prev[2] + joint
                radiansAngle = math.radians(newAngle)

                points.append(
                    (
                        prev[0] + math.cos(radiansAngle) * SEGMENT_LENGTH,
                        prev[1] + math.sin(radiansAngle) * SEGMENT_LENGTH,
                        newAngle,
                    )
                )

                # xs = [prev[0], points[-1][0]]
                # ys = [prev[1], points[-1][1]]
            figure.clf()
            xs = [point[0] for point in points]
            ys = [point[1] for point in points]
            plt.plot(xs, ys, linewidth=4)
            plt.pause(0.01)

        for i in range(500):
            angle = i % 90
            self.xs = [90-angle, angle] * int(NUM_SEGMENTS / 2)
            makeFigure()
        plt.show()


if __name__ == "__main__":
    solver = Solver()
    solver.plot()
