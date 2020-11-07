def shift(seq, n=0):
    a = n % len(seq)
    return seq[-a:] + seq[:-a]

class Point:
    def __init__(self, theta1=0):
        self.theta1 = theta1

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

    def step(self, direction):
        self.points = shift(self.points, direction)
        return [point.theta1 for point in self.points]

if __name__ == '__main__':
    solver = Solver()
    print([point.theta1 for point in solver.points])
    print(solver.step(1))
    print(solver.step(1))
    print(solver.step(1))
