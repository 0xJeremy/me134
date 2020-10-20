# 172.20.10.2 on iPhone

import math
import time
from sensor import Sensor
from robot import Robot


WEIGHTS = [
	(-math.sqrt(3)/2, 0.5),
	(0, -1),
	(math.sqrt(3)/2, 0.5)
]

MAX_ANGLE = 10 # degrees
MAX_SPEED = 50

kp = MAX_SPEED / MAX_ANGLE

OFFSETS = []

sensor = Sensor().start()
robot = Robot()

while sensor.euler == None:
	time.sleep(1)

try:
	while True:
		angles = sensor.euler
		
		speedX = angles[0] * kp
		speedY = angles[1] * kp

		for i, weight in enumerate(WEIGHTS):
			motorSpeed = weight[0]*speedX + weight[1]*speedY
			robot.speed(i, motorSpeed)

		time.sleep(0.01)

except KeyboardInterrupt:
	robot.stop()
	sensor.stop()
