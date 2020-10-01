from pather import Pather

all_xs, all_ys = Pather("svg_samples/sample.svg").getPaths()
xs = all_xs[0]
ys = all_ys[0]
from motion_planner import MotionPlanner

planner = MotionPlanner()

path_x, path_y = planner.createMachinePath(xs, ys)

print(path_x)
print(path_y)

all_angles = []
for x, y in zip(path_x, path_y):
    all_angles.append(planner.getAngles(x, y))

print(all_angles)
