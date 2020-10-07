# 172.20.10.2 on iPhone

from robot import Robot
from pather import Pather
from motion_planner import MotionPlanner, mapValue

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
    all_xs, all_ys = Pather(input).getPaths()
    planner = MotionPlanner()

    file = open(output, 'w')
    offset = 0

    x_min, x_max = getMinMax(all_xs)
    y_min, y_max = getMinMax(all_ys)

    for path_x, path_y in zip(all_xs, all_ys):

        for x, y in zip(path_x, path_y):

            x -= x_min
            y -= y_min

            x = mapValue(x, 0, x_max, 20, 100)
            y = mapValue(y, 0, y_max, 20, 100)

            angles = planner.getAngles(x, y+offset)

            angles[0] -= 90

            file.write('{} {}\n'.format(angles[0], angles[1]))

        file.write(RAISE)
        offset += (y_max - y_min) / len(all_ys)

    file.close()

def parseFile(file):
    file = open(file, 'r')
    all_angles = []
    for line in file:
        text = line.split(' ')
        angles = []
        for angle in text:
            if angle == RAISE:
                break;
            angles.append(float(angle))
        all_angles.append(angles)

    return all_angles


def drawFromFile(file):

    robot = Robot()

    all_angles = parseFile(file)

    for path in all_angles:
        robot.lower()
        for angle in path:
            robot.goto(angles[1], angles[0])
            time.sleep(0.1)
        robot.lift()
        time.sleep(0.5)


if __name__ == '__main__':
    output = 'out.pos'
    saveToFile('svg_samples/sample.svg', output)
    parseFile(output)
    # drawFromFile('out.pos')
    # drawLive('svg_samples/sample.svg')