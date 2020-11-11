def shift(seq, n=0):
    a = n % len(seq)
    return seq[-a:] + seq[:-a]


def setRange(value, minimum, maximum):
    return min(max(value, minimum), maximum)


ANGLE_STEP = 15


class Point:
    def __init__(self, theta1=0, theta2=90, isTurningLink=True):
        self.theta1 = theta1
        self.theta2 = theta2
        self.isTurningLink = isTurningLink

    # angle between -3 and 3 (-90 and 90)
    # theta2 maps between 0 and 180
    def update(self, angle):
        if self.isTurningLink:
            self.theta2 = 90 + (angle * ANGLE_STEP)


class Solver:
    def __init__(self):
        self.points = [
            Point(),
            Point(),
            Point(theta1=90),
            Point(theta1=90),
            Point(),
            Point(),
            Point(theta1=90),
            Point(theta1=90),
        ]
        self.angleSteps = 0

    def step(self, direction):
        self.points = shift(self.points, direction)

    def turn(self, direction):
        self.angleSteps += direction
        self.angleSteps = setRange(self.angleSteps, -3, 3)
        for point in self.points:
            point.update(self.angleSteps)

    def getPoints(self):
        return self.points


if __name__ == "__main__":
    solver = Solver()
    print([point.theta2 for point in solver.points])
    solver.turn(1)
    print([point.theta2 for point in solver.points])
    solver.turn(1)
    print([point.theta2 for point in solver.points])
    solver.turn(-1)
    print([point.theta2 for point in solver.points])
    solver.turn(-1)
    print([point.theta2 for point in solver.points])
    solver.turn(1)
    solver.step(1)
    print([point.theta2 for point in solver.points])
