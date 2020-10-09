from adafruit_servokit import ServoKit

class Robot:
	def __init__(self):
		self.kit = ServoKit(channels=16)
		self.lower()

		self.kit.servo[1].angle = 90
		self.kit.servo[2].angle = 90

	def goto(self, angle1, angle2):
		self.kit.servo[1].angle = angle1
		self.kit.servo[2].angle = angle2

	def lift(self):
		self.kit.servo[0].angle = 100

	def lower(self):
		self.kit.servo[0].angle = 90
		from adafruit_servokit import ServoKit
		from time import sleep

		class Robot:
			def __init__(self):
				self.kit = ServoKit(channels=16)
				self.lowered = False

				self.kit.servo[1].angle = 90
				self.kit.servo[2].angle = 90
				self.lastPos = (90, 90)

			def goto(self, angle1, angle2):
				min_angle = 0.125
				t = 0.01

				if not (-1 * min_angle < self.kit.servo[1].angle - angle1 < min_angle):
					self.goto((self.kit.servo[1].angle + angle1) / 2, (self.kit.servo[2].angle + angle2) / 2)
				elif not (-1 * min_angle < self.kit.servo[2].angle - angle2 < min_angle):
					self.goto((self.kit.servo[1].angle + angle1) / 2, (self.kit.servo[2].angle + angle2) / 2)
				sleep(t)

		#		self.kit.servo[1].angle = angle1
		#		self.kit.servo[2].angle = angle2

		#		sleep(t)

		#		self.kit.servo[1].angle = angle1 + 5
		#		self.kit.servo[2].angle = angle2 + 5

		#		sleep(t)

		#		self.kit.servo[1].angle = angle1 - 5
		#		self.kit.servo[2].angle = angle2 - 5

		#		sleep(t)

				self.kit.servo[1].angle = angle1 + 1.2345 * 3.1415
				self.kit.servo[2].angle = angle2 + 1.2345 * 3.1415
				#self.kit.servo[1].angle = angle1 + 5
				#self.kit.servo[2].angle = angle2 
				#sleep(t)
				#self.kit.servo[1].angle = angle1 - 5

			def lift(self):
				if self.lowered:
					self.kit.servo[0].angle = 100
					self.lowered = False

			def lower(self):
				if not self.lowered:
					self.kit.servo[0].angle = 0
					self.lowered = True
