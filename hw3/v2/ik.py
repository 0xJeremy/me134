import numpy as np
import math
import sympy as sym
import matplotlib.pyplot as plt


class Linkage:
    length = 0
    angle = 0
    origin = [0, 0]

    def __init__(self, length, angle, origin):
        self.length = length
        self.angle = angle
        self.origin = np.array(origin)

    def tip(self):
        return self.length * np.array([math.cos(math.radians(self.angle)), math.sin(math.radians(self.angle))]) + self.origin


def drive_A(links, delta_angle):
    links[0].angle += delta_angle
    links[2].origin = links[0].tip()

    return resolve_movement(links)


def resolve_movement(links):
    theta2 = sym.Symbol('theta2', real=True)
    theta3 = sym.Symbol('theta3', real=True)
    x3 = sym.Symbol('x3', real=True)
    y3 = sym.Symbol('y3', real=True)

    e1 = sym.Eq(x3, links[2].origin[0] + links[2].length * sym.cos(theta2))
    e2 = sym.Eq(y3, links[2].origin[1] + links[2].length * sym.sin(theta2))
    e3 = sym.Eq(x3, links[1].tip()[0] - links[3].length * sym.cos(theta3))
    e4 = sym.Eq(y3, links[1].tip()[1] - links[3].length * sym.sin(theta3))

    solution = sym.nsolve([e1, e2, e3, e4], [theta2, theta3, x3, y3], [math.radians(links[2].angle), math.radians(links[3].angle), links[3].origin[0], links[3].origin[1]])

    links[2].angle = math.degrees(solution[0])
    links[3].angle = math.degrees(solution[1])
    links[3].origin = [solution[2], solution[3]]
    links[4].angle = links[3].angle
    links[4].origin = links[3].tip()

    return links


def go_to_point(links, x4, y4):
    theta0 = sym.Symbol('theta0', real=True)
    theta1 = sym.Symbol('theta1', real=True)
    theta2 = sym.Symbol('theta2', real=True)
    theta3 = sym.Symbol('theta3', real=True)
    x2 = sym.Symbol('x2', real=True)
    y2 = sym.Symbol('y2', real=True)
    x3 = sym.Symbol('x3', real=True)
    y3 = sym.Symbol('y3', real=True)

    e1 = sym.Eq(x3, x2 + links[2].length * sym.cos(theta2))
    e2 = sym.Eq(y3, y2 + links[2].length * sym.sin(theta2))
    e3 = sym.Eq(x3, links[1].length * sym.cos(theta1) - links[3].length * sym.cos(theta3))
    e4 = sym.Eq(y3, links[1].length * sym.sin(theta1) - links[3].length * sym.sin(theta3))
    e5 = sym.Eq(x2, links[0].length * sym.cos(theta0))
    e6 = sym.Eq(y2, links[0].length * sym.sin(theta0))
    e7 = sym.Eq(x4, links[1].length * sym.cos(theta1) + links[4].length * sym.cos(theta3))
    e8 = sym.Eq(y4, links[1].length * sym.sin(theta1) + links[4].length * sym.sin(theta3))

    solution = sym.nsolve([e1, e2, e3, e4, e5, e6, e7, e8],
                          [theta0, theta1, theta2, theta3, x2, y2, x3, y3],
                          [math.radians(links[0].angle), math.radians(links[1].angle), math.radians(links[2].angle),
                           math.radians(links[3].angle), links[2].origin[0], links[2].origin[1], links[3].origin[0],
                           links[3].origin[1]])

    links[0].angle = math.degrees(solution[0])
    links[1].angle = math.degrees(solution[1])
    links[2].angle = math.degrees(solution[2])
    links[3].angle = math.degrees(solution[3])
    links[2].origin = [solution[4], solution[5]]
    links[3].origin = [solution[6], solution[7]]
    links[4].angle = links[3].angle
    links[4].origin = links[3].tip()

    return [math.degrees(solution[0]), math.degrees(solution[1])]


def drive_B(links, delta_angle):
    links[1].angle += delta_angle

    return resolve_movement(links)


def plot_system(links):
    plt.figure()
    for link in links:
        plt.plot([link.origin[0], link.tip()[0]],
                 [link.origin[1], link.tip()[1]])


if __name__ == '__main__':
    links = [
        Linkage(65, 180, [0, 0]), # Driver A
        Linkage(85, 90, [0, 0]), # Driver B
        Linkage(85, 90, [-65,0]), # Link A to lever arm
        Linkage(65, 0, [-65,85]), # First section of lever arm
        Linkage(90, 0, [0,85]), # End effector of lever arm
    ]

    plot_system(links)
    print(go_to_point(links, 90, 90))
    plot_system(links)
    print(go_to_point(links, 90, 95))
    plot_system(links)
    print(go_to_point(links, 95, 92.5))
    plot_system(links)
    print(go_to_point(links, 100, 95))
    plot_system(links)
    print(go_to_point(links, 100, 90))
    plot_system(links)
    plt.show()