from svgpathtools import svg2paths, Path, Line, CubicBezier, Arc, QuadraticBezier
import matplotlib.pyplot as plt
import numpy as np

def cubicBezier(t, p):
	first = ((1-t)**3) * p[0]
	second = (3*(1-t)**2) * t * p[1]
	third = 3*(1-t) * t**2 * p[2]
	fourth = t**3 * p[3]
	return first + second + third + fourth

NUM_POINTS = 10

class Pather:
	RAISE = 'raise'
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
		if not isinstance(thing, list): thing = [thing]
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
			self.append([path.start, path.control, path.end])
		elif isinstance(path, CubicBezier):
			self.append(path.start)
			xs_to_use = np.linspace(path.control1.real, path.control2.real, NUM_POINTS)
			ys_to_use = np.linspace(path.control1.imag, path.control2.imag, NUM_POINTS)
			points = np.linspace(0, 1, NUM_POINTS)
			for point in points:
				fancy_x = cubicBezier(point, [path.start.real, path.control1.real, path.control2.real, path.end.real])
				fancy_y = cubicBezier(point, [path.start.imag, path.control1.imag, path.control2.imag, path.end.imag])
				self.append(complex(fancy_x, fancy_y))
			self.append(path.end)
		elif isinstance(path, Arc):
			raise RuntimeError('Encountered arc path...', path)
		else:
			raise RuntimeError('Encountered unexpected path type...', path)

	def getPaths(self):
		return self.all_xs, self.all_ys


xs, ys = Pather('sample.svg').getPaths()

for x, y in zip(xs, ys):
	plt.scatter(x, y)
	plt.plot(x, y)
plt.gca().invert_yaxis()
plt.show()

