# 172.20.10.2 on iPhone

import math
import time
from sensor import Sensor
from robot import Robot
from pid import PID

# Some good values:
# P = 3, D = 4
# P = 6, D = 10
# P = 2.45, D = 0.8
# P = 1.1, D = 2.5
# P = 1.1, D = 15

# Too small = runs away, too big = jitters
P = 1.1

I = 0

# Too small = jitters
D = 15


WEIGHTS = [
    (0, 1),
    (math.sqrt(3) / 2, -0.5),
    (-math.sqrt(3) / 2, -0.5)
]

pidX = PID(P=P, I=I, D=D)
pidY = PID(P=P, I=I, D=D)

sensor = Sensor().start()
robot = Robot()

try:
    while True:
        angles = sensor.euler

        speedX = pidX.update(angles[0])
        speedY = pidY.update(angles[1])

        print("Angles: {}, Speeds: ({}, {})".format(angles, speedX, speedY))

        for i, weight in enumerate(WEIGHTS):
            motorSpeed = weight[0] * speedX + weight[1] * speedY
            robot.speed(i, motorSpeed)

        time.sleep(0.005)

except KeyboardInterrupt:
    robot.stop()
    sensor.stop()
