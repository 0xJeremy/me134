import board, busio
from adafruit_mpu6050 import MPU6050
from adafruit_bno055 import BNO055_I2C
from threading import Thread

# print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (mpu.acceleration))
# print("Gyro X:%.2f, Y: %.2f, Z: %.2f degrees/s" % (mpu.gyro))
# print("Temperature: %.2f C" % mpu.temperature)

MPU_1 = 0x68
MPU_2 = 0x69


class Sensor:
    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.mpus = [MPU6050(i2c, address=MPU_1), MPU6050(i2c, address=MPU_2)]
        self.bno = BNO055_I2C(i2c)
        self.stopped = False

    def start(self):
        Thread(target=self.run, args=()).start()

    def run(self):
        while not self.stopped:
            pass

    def stop(self):
        self.stopped = True
