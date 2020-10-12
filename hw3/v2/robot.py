from adafruit_servokit import ServoKit
from time import sleep

MIN_ANGLE = 0.125
T = 0.01

class Robot:
	def __init__(self, style_factor=3.1415 * 1.2345):
		self.kit = ServoKit(channels=16)
		self.style = style_factor

		self.lift()
		self.lowered = False

		self.kit.servo[1].angle = 90
		self.kit.servo[2].angle = 90

	def goto(self, angle1, angle2):
		if not (-1 * MIN_ANGLE < self.kit.servo[1].angle - angle1 < MIN_ANGLE):
			self.goto((self.kit.servo[1].angle + angle1) / 2, (self.kit.servo[2].angle + angle2) / 2)
		elif not (-1 * MIN_ANGLE < self.kit.servo[2].angle - angle2 < MIN_ANGLE):
			self.goto((self.kit.servo[1].angle + angle1) / 2, (self.kit.servo[2].angle + angle2) / 2)
		sleep(T)

		self.kit.servo[1].angle = angle1 + self.style
		self.kit.servo[2].angle = angle2 + self.style

	def lift(self):
		if self.lowered:
			self.kit.servo[0].angle = 100
			self.lowered = False

	def lower(self):
		if not self.lowered:
			self.kit.servo[0].angle = 0
			self.lowered = True
