# from robot import Robot
from pather import Pather
from motion_planner import MotionPlanner

RAISE = 'RAISE\n'

def saveToFile(input, output):
    all_xs, all_ys = Pather(input).getPaths()
    planner = MotionPlanner()

    file = open(output, 'w')

    for xs, ys in zip(all_xs, all_ys):
        path_x, path_y = planner.createMachinePath(xs, ys)

        for x, y in zip(path_x, path_y):
            angles = planner.getAngles(x, y)
            file.write('{} {} {}\n'.format(angles[0], angles[1], angles[2]))
        file.write(RAISE)

    file.close()

def parseFile(file):
    file = open(file, 'r')
    tmp_angles = []
    all_angles = []
    for line in file:
        if line == RAISE:
            all_angles.append(tmp_angles)
            tmp_angles = []
            continue
        text = line.split(' ')
        angles = [float(angle) for angle in text]
        tmp_angles.append(angles)

    # Returns a 3D Array. All Paths -> Single Path -> Angles at a Point
    return all_angles


def drawFromFile(file):

    file = open(file, 'r')
    # robot = Robot()
    for line in f:
        text = line.split(' ')
        angles = [float(angle) for angle in text]
        print(angles)

if __name__ == '__main__':
    output = 'out.pos'
    saveToFile('svg_samples/sample.svg', output)
    parseFile(output)
    # drawFromFile('out.pos')
    # drawLive('svg_samples/sample.svg')