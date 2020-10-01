# from robot import Robot
from pather import Pather
from motion_planner import MotionPlanner

RAISE = 'RAISE\n'
HOP_HEIGHT = 0.5
TRAVEL_TIME = 0.5

def saveToFile(input, output):
    all_xs, all_ys = Pather(input).getPaths()
    planner = MotionPlanner()

    file = open(output, 'w')

    for xs, ys in zip(all_xs, all_ys):
        path_x, path_y = planner.createMachinePath(xs, ys)

        startingPosition = planner.getAngles(xs[0], ys[0], HOP_HEIGHT)
        file.write('{} {} {}\n'.format(startingPosition[0], startingPosition[1], startingPosition[2]))

        for x, y in zip(path_x, path_y):
            angles = planner.getAngles(x, y)
            file.write('{} {} {}\n'.format(angles[0], angles[1], angles[2]))

        endingPosition = planner.getAngles(xs[0], ys[0], HOP_HEIGHT)
        file.write('{} {} {}\n'.format(endingPosition[0], endingPosition[1], endingPosition[2]))

    file.close()

def parseFile(file):
    file = open(file, 'r')
    all_angles = []
    for line in file:
        text = line.split(' ')
        angles = [float(angle) for angle in text]
        all_angles.append(angles)

    return all_angles


def drawFromFile(file):

    robot = Robot()

    all_angles = parseFile(file)

    for angles in all_angles:
        robot.goto(angles[0], angles[1], angles[2])

if __name__ == '__main__':
    output = 'out.pos'
    saveToFile('svg_samples/sample.svg', output)
    parseFile(output)
    # drawFromFile('out.pos')
    # drawLive('svg_samples/sample.svg')