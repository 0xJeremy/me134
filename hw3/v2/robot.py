from adafruit_servokit import ServoKit

class Robot:
	def __init__(self):
		kit = ServoKit(channels=16)
		self.lower()

		kit.servo[1].angle = 90
		kit.servo[2].angle = 90

	def goto(self, angle1, angle2):
		self.servo[1].angle = angle1
		self.servo[2].angle = angle2

	def lift(self):
		self.servo[0].angle = 100

	def lower(self):
		self.servo[0].angle = 90
