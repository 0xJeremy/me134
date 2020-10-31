from solver import Solver


class Robot:
    def __init__(self):
        self.solver = Solver()
        startingXs = self.solver.getX()
        startingYs = self.solver.getY()
        self.goto(startingXs, startingYs)

    def goto(self, xs, ys):
        pass
