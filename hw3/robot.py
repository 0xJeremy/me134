import tinyik
import numpy as np
try:
	from adafruit_servokit import ServoKit
except:
	class ServoKit:
		def __init__(self, channels):
			pass
	pass

RANGES = {
	0: (0, 270)
	1: (30, 270)
	2: (20, 270)
	3: (0, 180)
}

# https://stackoverflow.com/questions/1969240/mapping-a-range-of-values-to-another
def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

SCALAR = 1000

class Robot:
	def __init__(self):
		self.kit = ServoKit(channels=16)
		self.kit.servo[0].set_pulse_width_range(500, 2500)
		self.kit.servo[1].set_pulse_width_range(500, 2500)
		self.kit.servo[2].set_pulse_width_range(500, 2500)
		self.kit.servo[0].angle = 135
		self.kit.servo[1].angle = 135
		self.kit.servo[2].angle = 135
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
		x /= SCALAR
		y /= SCALAR
		z /= SCALAR
		angles = np.degrees(self.getAngles(x, y, z))
		self.kit.servo[0].angle = angles[0]
		self.kit.servo[1].angle = angles[1]
		self.kit.servo[2].angle = angles[2]
		self.kit.servo[3].angle = angles[3]

if __name__ == '__main__':
	robot = Robot()
	tinyik.visualize(robot.arm, target=[0.8, 0.8, 0])
