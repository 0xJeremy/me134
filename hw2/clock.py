from adafruit_servokit import ServoKit

# class ServoKit:
#   def __init__(self, channels=16, address=0x40):
#       self.servo = [i for i in range(14)]

class Segment:
    def __init__(self, on, off, requirements=[]):
        self.on = on
        self.off = off
        self.requirements = requirements

# Channel -> (On location, off location)
MAP = {
    # Hours (tens)
    0: Segment(0, 120),
    1: Segment(100, 0),
    2: Segment(75, 0),
    3: Segment(100, 0),
    4: Segment(115, 0),
    5: Segment(10, 130),
    6: Segment(140, 0),
    # Hours (ones)
    7: Segment(130, 0),
    8: Segment(0, 120),
    9: Segment(140, 0),
    10: Segment(0, 140),
    11: Segment(110, 0),
    12: Segment(10, 100),
    13: Segment(0, 120),

    # Minutes (tens)
    14: Segment(20, 120),
    15: Segment(0, 130),
    16: Segment(120, 0),
    17: Segment(110, 0),
    18: Segment(135, 5),
    19: Segment(10, 120),
    20: Segment(100, 0),
    # Minutes (ones)
    21: Segment(120, 0),
    22: Segment(0, 120),
    23: Segment(120, 0),
    24: Segment(140, 10),
    25: Segment(130, 0),
    26: Segment(130, 10),
    27: Segment(10, 130)
}

class Digit:
    def __init__(self, driver, offset):
        self.driver = driver
        self.offset = 7 * offset

    def set(self, binaryArray):
        for i, segmentState in enumerate(binaryArray):
            offset = self.offset + i
            segment = MAP[offset]
            for requirement in segment.requirements:
                # add logic to meet hardware requirements
                pass
            self.driver.servo[offset % 14].angle = segment.on if segmentState else segment.off


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
