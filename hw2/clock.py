from adafruit_servokit import ServoKit

# Channel -> (On location, off location)
MAP = {
    # Hours (tens)
    0: (0, 120),
    1: (100, 0),
    2: (75, 0),
    3: (100, 0),
    4: (115, 0),
    5: (10, 130),
    6: (140, 0),
    # Hours (ones)
    7: (130, 0),
    8: (0, 120),
    9: (140, 0),
    10: (0, 140),
    11: (110, 0),
    12: (10, 100),
    13: (0, 120),
    # Minutes (tens)
    14: (20, 120),
    15: (0, 130),
    16: (120, 0),
    17: (110, 0),
    18: (135, 5),
    19: (10, 120),
    20: (100, 0),
    # Minutes (ones)
    21: (120, 0),
    22: (0, 120),
    23: (120, 0),
    24: (140, 10),
    25: (130, 0),
    26: (130, 10),
    27: (10, 130),
}


class Digit:
    def __init__(self, driver, offset):
        self.driver = driver
        self.offset = 7 * offset

    def set(self, binaryArray):
        for i, segmentState in enumerate(binaryArray):
            offset = self.offset + i
            segment = MAP[offset]
            self.driver.servo[offset % 14].angle = (
                segment[0] if segmentState else segment[1]
            )


class Clock:
    def __init__(self):
        self.driverHours = ServoKit(channels=16, address=0x40)
        self.driverMinutes = ServoKit(channels=16, address=0x41)
        self.tensHour = Digit(self.driverHours, 0)
        self.onesHour = Digit(self.driverHours, 1)
        self.tensMinute = Digit(self.driverMinutes, 2)
        self.onesMinute = Digit(self.driverMinutes, 3)

    def set(self, binaryArray):
        self.tensHour.set(binaryArray[0:7])
        self.onesHour.set(binaryArray[7:14])
        self.tensMinute.set(binaryArray[14:21])
        self.onesMinute.set(binaryArray[21:28])
