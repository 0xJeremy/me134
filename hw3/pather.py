from svgpathtools import svg2paths, Path, Line, CubicBezier, Arc, QuadraticBezier
import numpy as np


# https://en.wikipedia.org/wiki/B%C3%A9zier_curve#Quadratic_B%C3%A9zier_curves
def quadraticBezier(t, p):
    return p[1] + ((1 - t) ** 2 * (p[0] - p[1])) + (t ** 2 * (p[2] - p[1]))


# https://en.wikipedia.org/wiki/B%C3%A9zier_curve#Cubic_B%C3%A9zier_curves
def cubicBezier(t, p):
    return (
        (((1 - t) ** 3) * p[0])
        + ((3 * (1 - t) ** 2) * t * p[1])
        + (3 * (1 - t) * t ** 2 * p[2])
        + (t ** 3 * p[3])
    )


NUM_POINTS = 10


class Pather:
    def __init__(self, filePath):
        paths, attributes = svg2paths(filePath)
        self.xs = []
        self.ys = []
        self.all_xs = []
        self.all_ys = []
        for path in paths:
            self.parseSVG(path)
            self.all_xs.append(self.xs)
            self.all_ys.append(self.ys)
            self.xs = []
            self.ys = []

    def append(self, thing):
        if not isinstance(thing, list):
            thing = [thing]
        for item in thing:
            self.xs.append(item.real)
            self.ys.append(item.imag)

    def parseSVG(self, path):
        if isinstance(path, Path):
            for item in path:
                self.parseSVG(item)
        elif isinstance(path, Line):
            self.append([path.start, path.end])
        elif isinstance(path, QuadraticBezier):
            for point in np.linspace(0, 1, NUM_POINTS):
                interpolated_x = quadraticBezier(
                    point, [path.start.real, path.control.real, path.end.real]
                )
                interpolated_y = quadraticBezier(
                    point, [path.start.imag, path.control.imag, path.end.imag]
                )
                self.append(complex(interpolated_x, interpolated_y))
        elif isinstance(path, CubicBezier):
            for point in np.linspace(0, 1, NUM_POINTS):
                interpolated_x = cubicBezier(
                    point,
                    [
                        path.start.real,
                        path.control1.real,
                        path.control2.real,
                        path.end.real,
                    ],
                )
                interpolated_y = cubicBezier(
                    point,
                    [
                        path.start.imag,
                        path.control1.imag,
                        path.control2.imag,
                        path.end.imag,
                    ],
                )
                self.append(complex(interpolated_x, interpolated_y))
        elif isinstance(path, Arc):
            raise RuntimeError("Encountered arc path...", path)
        else:
            raise RuntimeError("Encountered unexpected path type...", path)

    def getPaths(self):
        return self.all_xs, self.all_ys


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    all_xs, all_ys = Pather("svg_samples/sample.svg").getPaths()

    for xs, ys in zip(all_xs, all_ys):
        plt.scatter(xs, ys)
        plt.plot(xs, ys)
    plt.gca().invert_yaxis()
    plt.show()
