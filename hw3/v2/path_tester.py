from pather import Pather
from motion_planner import MotionPlanner, mapValue

import matplotlib.pyplot as plt


def getMinMax(list2d):
    minVal, maxVal = min(list2d[0]), max(list2d[0])

    for array in list2d:
        minVal = min(minVal, min(array))
        maxVal = max(maxVal, max(array))

    return minVal, maxVal


def saveToFile(input):
    all_xs, all_ys = Pather(input).getPaths()
    planner = MotionPlanner()

    offset = 0

    x_min, x_max = getMinMax(all_xs)
    y_min, y_max = getMinMax(all_ys)

    accX = []
    accY = []

    tipX = []
    tipY = []

    for path_x, path_y in zip(all_xs, all_ys):

        for x, y in zip(path_x, path_y):

            x -= x_min
            y -= y_min

            x = mapValue(x, 0, x_max - x_min, 20, 100)
            y = mapValue(y, 0, y_max - y_min, 20, 100)

            accX.append(x)
            accY.append(y)

            angles = planner.getAngles(x, y + offset)

            tips = planner.links[-1].tip()
            tipX.append(tips[0])
            tipY.append(tips[1])

            angles[0] -= 90

        # offset += (y_max - y_min) / len(all_ys)

    # plt.scatter(accX, accY)
    plt.scatter(tipX, tipY)
    plt.show()


saveToFile("svg_samples/sample.svg")
