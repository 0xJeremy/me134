import argparse
from pather import Pather
from robot import Robot

HOP_HEIGHT = 50

def main(args):
	planner = Pather(args.filename)
	robot = Robot()

	all_xs, all_ys = planner.getPaths()
	lastPoint = None

	for xs, ys in zip(all_xs, all_ys):
		for x, y in tqdm(zip(xs, ys), total=len(xs)):
			robot.goto(x, y)
			lastPoint = (x, y)
		robot.goto(lastPoint[0], lastPoint[1], HOP_HEIGHT)


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='A writing robot.')
	parser.add_argument('-f', '--filename', help='Loads and writes from a .svg file')
	args = parser.parse_args()
