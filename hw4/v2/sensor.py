from threading import Thread
from time import sleep
from adafruit_mpu6050 import MPU6050
from adafruit_bno055 import BNO055_I2C
from fusion import Fusion
from scipy.spatial.transform import Rotation
import board
import busio


# print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (mpu.acceleration))
# print("Gyro X:%.2f, Y: %.2f, Z: %.2f degrees/s" % (mpu.gyro))
# print("Temperature: %.2f C" % mpu.temperature)

MPU_1 = 0x68
MPU_2 = 0x69

BNO_WEIGHT = 0.5
MPU_WEIGHT = 1 - BNO_WEIGHT

SLEEP_TIME = 0.05


def averageTwoVectors(list1, list2, weight1=0.5, weight2=0.5):
    averages = []
    for i1, i2 in zip(list1, list2):
        averages.append((i1 * weight1) + (i2 * weight2))
    return averages


class Sensor:
    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.mpus = [MPU6050(i2c, address=MPU_1), MPU6050(i2c, address=MPU_2)]
        self.fusions = [Fusion() for item in self.mpus]
        self.bno = BNO055_I2C(i2c)
        self.euler = None
        self.stopped = False

    def start(self):
        Thread(target=self.run, args=()).start()

    def run(self):
        while not self.stopped:
            [
                fusion.update_nomag(mpu.acceleration, mpu.gyro)
                for fusion, mpu in zip(self.fusions, self.mpus)
            ]
            mpuOrientations = [sensor.q for sensor in self.mpus]

            mpuOrientation = averageTwoVectors(mpuOrientations[0], mpuOrientations[1])
            bnoOrientation = self.bno.quaternion

            quaternion = averageTwoVectors(
                bnoOrientation, mpuOrientation, BNO_WEIGHT, MPU_WEIGHT
            )

            self.euler = Rotation(quaternion).as_rotvec()

            sleep(SLEEP_TIME)

    def stop(self):
        self.stopped = True
