import numpy as np
import math

# secondsPerDegree = 0.00233333333
secondsPerDegree = 0.003
INTERVAL = 4


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def interpolate(start, end, runtime, points):
    x = np.linspace(-INTERVAL, INTERVAL, points)
    y = sigmoid(x)
    y = (y - y[0]) * (end - start) + start
    x = ((x + INTERVAL) / (2 * INTERVAL)) * runtime
    return x, y


def generatePoints(start, end, runtime, points):
    times, angles = interpolate(start, end, runtime, points)
    return angles[1:], np.diff(times)


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    start = 100
    end = 150
    runtime = 0.3
    points = 10

    x, y = interpolate(start, end, runtime, points)

    angles, timeDiffs = generatePoints(start, end, runtime, points)

    for angle, time in zip(angles, timeDiffs):
        print("{} {}".format(angle, time))

    plt.plot(x, y, label="Sigmoid")
    plt.scatter(x[1:], angles, color="orange", label="Command Points")
    plt.xlabel("Time")
    plt.ylabel("Command Angle")
    plt.legend()

    plt.show()
