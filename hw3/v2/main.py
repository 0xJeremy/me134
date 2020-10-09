# 172.20.10.2 on iPhone

import time

RAISE = 'RAISE\n'
HOP_HEIGHT = 0.5
TRAVEL_TIME = 0.5

def getMinMax(list2d):
    minVal, maxVal = min(list2d[0]), max(list2d[0])

    for array in list2d:
        minVal = min(minVal, min(array))
        maxVal = max(maxVal, max(array))

    return minVal, maxVal

def saveToFile(input, output):
    from pather import Pather
    from motion_planner import MotionPlanner, mapValue
    import matplotlib.pyplot as plt
    all_xs, all_ys = Pather(input).getPaths()
    planner = MotionPlanner()

    file = open(output, 'w')
    offset = 0

    x_min, x_max = getMinMax(all_xs)
    y_min, y_max = getMinMax(all_ys)

    x_avg = x_max - x_min
    y_avg = y_max - y_min

    accX = []
    accY = []

    # center: x=85, y=90 (now x=64 y=60)

    for path_x, path_y in zip(all_xs, all_ys):

        for x, y in zip(path_x, path_y):

            # x -= x_avg
            # y -= y_avg

            # x = mapValue(x, 0, x_max-x_min, 10, 120)
            # y = mapValue(y, 0, y_max-y_min, 10, 120)

            # x = mapValue(x, x_min, x_max, 55, 115)
            # y = mapValue(y, y_min, y_max, 60, 120)

            y = y_avg - y

            x = mapValue(x, x_min, x_max, 44, 84)
            y = mapValue(y, y_min, y_max, 40, 80)


            accX.append(x)
            accY.append(y)

            angles = planner.getAngles(x, y+offset)

            angles[0] -= 90

            file.write('{} {}\n'.format(angles[0], angles[1]))

        file.write(RAISE)

    file.close()

    plt.scatter(accX, accY)
    plt.show()


def parseFile(file):
    file = open(file, 'r')
    all_angles = []
    angles = []
    for line in file:
        text = line.split(' ')
        if text[0] == RAISE:
            all_angles.append(angles)
            angles = []
        else:
            angles.append([float(text[0]), float(text[1])])

    return all_angles


def drawFromFile(file):
    from robot import Robot
    robot = Robot()

    all_angles = parseFile(file)

    for path in all_angles:
        robot.lower()
        for angles in path:
            robot.goto(angles[1], angles[0])
            time.sleep(0.1)
        robot.lift()
        time.sleep(0.5)


if __name__ == '__main__':
    output = 'out.pos'
    saveToFile('svg_samples/jk.svg', output)
    # parseFile(output)
    # drawFromFile('out.pos')
    # drawLive('svg_samples/sample.svg')