# 172.20.10.2 on iPhone

import math
import time
from sensor import Sensor, applyDeadzone
from robot import Robot, boundSpeed
from pid import PID

DEADZONE = 5  # degrees

# Too small = runs away, too big = jitters
P = 6

I = 2

# Too small = jitters
D = 0.8


WEIGHTS = [(-math.sqrt(3) / 2, 0.5), (0, -1), (math.sqrt(3) / 2, 0.5)]

pidX = PID(P=P, I=I, D=D)
pidY = PID(P=P, I=I, D=D)

sensor = Sensor().start()
robot = Robot()

try:
    while True:
        angles = sensor.euler

        speedX = boundSpeed(pidX.update(angles[0]))
        speedY = boundSpeed(pidY.update(angles[1]))

        print("Angles: {}, Speeds: ({}, {})".format(angles, speedX, speedY))

        for i, weight in enumerate(WEIGHTS):
            motorSpeed = weight[0] * speedX + weight[1] * speedY
            robot.speed(i, motorSpeed)

        time.sleep(0.005)

except KeyboardInterrupt:
    robot.stop()
    sensor.stop()
