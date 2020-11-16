# 172.20.10.2 on iPhone

import time
import sys

RAISE = "RAISE\n"
HOP_HEIGHT = 0.5
TRAVEL_TIME = 0.5
DEFAULT_FILE = "out.pos"
DEFAULT_STYLE = 1.2345 * 3.1415


def getMinMax(list2d):
    minVal, maxVal = min(list2d[0]), max(list2d[0])

    for array in list2d:
        minVal = min(minVal, min(array))
        maxVal = max(maxVal, max(array))

    return minVal, maxVal


def saveToFile(input, output, arm):
    from pather import Pather
    from motion_planner import MotionPlanner, mapValue
    import matplotlib.pyplot as plt

    all_xs, all_ys = Pather(input).getPaths()
    planner = MotionPlanner(arm)

    file = open(output, "w")
    offset = 0

    x_min, x_max = getMinMax(all_xs)
    y_min, y_max = getMinMax(all_ys)

    x_avg = x_max - x_min
    y_avg = y_max - y_min

    accX = []
    accY = []

    for path_x, path_y in zip(all_xs, all_ys):

        for x, y in zip(path_x, path_y):

            y = y_avg - y

            x = mapValue(x, x_min, x_max, 44, 84)
            y = mapValue(y, y_min, y_max, 40, 80)

            accX.append(x)
            accY.append(y)

            angles = planner.getAngles(x, y + offset)

            angles[0] -= 90

            file.write("{} {}\n".format(angles[0], angles[1]))

        file.write(RAISE)

    file.close()

    plt.scatter(accX, accY)
    plt.show()


def parseFile(file):
    file = open(file, "r")
    all_angles = []
    angles = []
    for line in file:
        text = line.split(" ")
        if text[0] == RAISE:
            all_angles.append(angles)
            angles = []
        else:
            angles.append([float(text[0]), float(text[1])])

    return all_angles


def drawFromFile(file, style_factor=DEFAULT_STYLE):
    from robot import Robot

    robot = Robot(style_factor)

    all_angles = parseFile(file)

    for path in all_angles:
        robot.lower()
        for angles in path:
            robot.goto(angles[1], angles[0])
            time.sleep(0.1)
        robot.lift()
        time.sleep(0.5)


def readCmdLine(argv):
    infile = DEFAULT_FILE
    outfile = DEFAULT_FILE
    style_factor = DEFAULT_STYLE
    arm = "short"
    draw_live = False

    if len(sys.argv) > 1:
        if "-h" in sys.argv or "--help" in sys.argv:
            print(
                "usage: main.py [-h] [-i] input_file [-o] output_file [-s] style_factor [-a] arm [-dl]\n\n"
                "Create and/or execute robot path\n\n"
                "optional arguments:\n"
                "-h, --help\tshow help message and exit\n"
                "-i, --infile\tinput .svg or .pos file\n"
                "-o, --outfile\toutput .pos file to save to\n"
                "-s, --style\tthe desired robot arm style factor\n"
                "-a, --arm\tthe arm set-up, 'short' or 'long'\n"
                "-dl, --drawlive\tcompiles .svg and runs path"
            )
            sys.exit()

        for arg, val in zip(sys.argv[1::2], sys.argv[2::2]):
            if arg in ("-i", "--infile"):
                infile = val
            elif arg in ("-o", "--outfile"):
                outfile = val
            elif arg in ("-s", "--style"):
                style_factor = val

        draw_live = "-dl" in sys.argv or "--drawlive" in sys.argv

    return [infile, outfile, style_factor, arm, draw_live]


if __name__ == "__main__":
    [infile, outfile, style_factor, arm, draw_live] = readCmdLine(sys.argv)

    if ".svg" in infile:
        saveToFile(infile, outfile, arm)
        if draw_live:
            infile = outfile

    if ".pos" in infile:
        drawFromFile(infile, style_factor)
