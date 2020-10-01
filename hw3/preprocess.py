from pather import Pather
from robot import Robot
from tqdm import tqdm
import numpy as np
import argparse

OUTPUT = 'out.pos'
RAISE = 'RAISE'

def parse(filename, pointCallback, raiseCallback):
	planner = Pather(filename)
	robot = Robot()

	all_xs, all_ys = planner.getPaths()
	lastPoint = None

	for xs, ys in zip(all_xs, all_ys):
		for x, y in tqdm(zip(xs, ys), total=len(xs)):
			pointCallback(np.degrees(robot.getAngles(x, y)))
			lastPoint = (x, y)
		raiseCallback(lastPoint)
	

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Preprocess the motion of a robot arm.')
	parser.add_argument('filename', help='Path to the file to process')
	outputFile = open(OUTPUT, 'w')

	def pointCallback(angle):
		outputFile.write('{:.2f} {:.2f} {:.2f} {:.2f}\n'.format(angle[0], angle[1], angle[2], angle[3]))
		
	def raiseCallback(lastPoint):
		outputFile.write('{}\n'.format(RAISE))

	parse(parser.parse_args().filename, pointCallback, raiseCallback)

	outputFile.close()
