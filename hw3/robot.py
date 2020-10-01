import tinyik
import numpy as np
try:
	from adafruit_servokit import ServoKit
except:
	class ServoKit:
		def __init__(self, channels):
			pass
	pass

SCALAR = 1000

class Robot:
	def __init__(self):
		self.kit = ServoKit(channels=16)
		self.arm = tinyik.Actuator([
		    "z", [1e-10, 0.0, 0.32],
		    "x", [0.0, 1.4745, 0.0],
		    "x", [0.0, 1.5566, 0.0],
		    "x", [0.0, 0.355,  0.0],
		])

	def getAngles(self, x, y, z=0):
		self.arm.ee = [x, y, z]
		return self.arm.angles

	def goto(self, x, y, z=0):
		angles = np.degrees(self.getAngles(x, y, z))
		x /= SCALAR
		y /= SCALAR
		z /= SCALAR
		self.kit.servo[0].angle = angles[0]
		self.kit.servo[1].angle = angles[1]
		self.kit.servo[2].angle = angles[2]
		self.kit.servo[3].angle = angles[3]

if __name__ == '__main__':
	robot = Robot()
	tinyik.visualize(robot.arm, target=[0.8, 0.8, 0])
