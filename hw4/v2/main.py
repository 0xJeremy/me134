# 172.20.10.2 on iPhone

import math
import time
from sensor import Sensor
from robot import Robot
from pid import PID


def boundSpeed(value):
    if value > 100:
        return 100
    if value < -100:
        return -100
    return value


WEIGHTS = [(-math.sqrt(3) / 2, 0.5), (0, -1), (math.sqrt(3) / 2, 0.5)]

# Too small = runs away, too big = jitters
P = 6

I = 0.0

# Too small = jitters
D = 0.0

pidX = PID(P, I, D)
pidY = PID(P, I, D)

sensor = Sensor().start()
robot = Robot()

try:
    while True:
        angles = sensor.euler

        pidX.update(angles[0])
        pidY.update(angles[1])

        speedX = boundSpeed(pidX.output)
        speedY = boundSpeed(pidY.output)

        print("Angles: {}, Speeds: ({}, {})".format(angles, speedX, speedY))

        for i, weight in enumerate(WEIGHTS):
            motorSpeed = weight[0] * speedX + weight[1] * speedY
            robot.speed(i, motorSpeed)

        time.sleep(0.005)

except KeyboardInterrupt:
    robot.stop()
    sensor.stop()
