import board
from busio import I2C
from adafruit_bno055 import BNO055_I2C
from adafruit_vl6180x import VL6180X

i2c = I2C(board.SCL, board.SDA)
bno = BNO055_I2C(i2c)
tof = VL6180X(i2c)


def getAbsoluteOrientation():
    # If you want quaternion output
    # return bno.quaternion

    # If you want euler output
    return bno.euler


def getTimeOfFlight():
    # Returns the distance in mm
    return tof.range
