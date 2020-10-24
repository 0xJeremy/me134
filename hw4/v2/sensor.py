from threading import Thread
from time import sleep, time
from adafruit_mpu6050 import MPU6050, GyroRange
from adafruit_bno055 import BNO055_I2C
from fusion import Fusion
from scipy.spatial.transform import Rotation
import board
import busio
import numpy as np

# https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/i2c-clock-stretching

MPU_1 = 0x68
MPU_2 = 0x69

BNO_WEIGHT = 0.5
MPU_WEIGHT = 1 - BNO_WEIGHT

SLEEP_TIME = 0.01


def applyDeadzone(angles, deadzone=5):
    return [0 if angle < deadzone else angle for angle in angles]


def averageTwoVectors(list1, list2, weight1=0.5, weight2=0.5):
    averages = []
    for i1, i2 in zip(list1, list2):
        averages.append((i1 * weight1) + (i2 * weight2))
    return averages


def mpuOrientationToBnoOrientation(axes):
    # Flips the x and y dimensions, and inverts the new x
    return (-axes[1], axes[0], axes[2])


def timeDiff(start, end):
    return end - start


class Sensor:
    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.mpus = [MPU6050(i2c, address=MPU_1), MPU6050(i2c, address=MPU_2)]
        for mpu in self.mpus:
            mpu.gyro_range = GyroRange.RANGE_2000_DPS
            
        self.fusions = [Fusion(timediff=timeDiff) for item in self.mpus]
        self.bno = BNO055_I2C(i2c)
        self.euler = None
        self.eulerOffset = None
        self.stopped = False

    def start(self):
        Thread(target=self.run, args=()).start()
        while self.euler == None:
            sleep(1)
        print("Initialization Complete!\nSensor Running...")
        return self

    def run(self):
        while not self.stopped:
            # currTime = time()

            # [
            #     fusion.update_nomag(mpu.acceleration, mpu.gyro, currTime)
            #     for fusion, mpu in zip(self.fusions, self.mpus)
            # ]

            # mpuOrientations = [fusion.q for fusion in self.fusions]

            # mpuOrientation = averageTwoVectors(mpuOrientations[0], mpuOrientations[1])
            # bnoOrientation = self.bno.quaternion

            # quaternion = bnoOrientation

            # quaternion = averageTwoVectors(
            #     bnoOrientation, mpuOrientation, BNO_WEIGHT, MPU_WEIGHT
            # )

            try:
                # angles = np.rad2deg(Rotation.from_quat(quaternion).as_rotvec())
                angles1 = mpuOrientationToBnoOrientation(self.mpus[0].gyro)
                angles2 = mpuOrientationToBnoOrientation(self.mpus[1].gyro)
                self.euler = averageTwoVectors(angles1, angles2)

                # if self.eulerOffset is None:
                #     self.eulerOffset = angles

                # self.euler = (angles[1]-self.eulerOffset[1], angles[2]-self.eulerOffset[2], angles[0]-self.eulerOffset[0])
                # self.euler = (angles[1], angles[2], angles[0])
            except ValueError:
                print("Booting up sensors...")

            sleep(SLEEP_TIME)

    def stop(self):
        self.stopped = True
