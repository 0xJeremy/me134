from actuation import setup, actuate
import time
from hardware import LEGS


class Robot:
    def __init__(self):
        self.legs = LEGS
        self.walkTick = 0
        self.turnTick = 0
        self.legsOdd = [self.legs[0], self.legs[2], self.legs[4]]
        self.legsEven = [self.legs[1], self.legs[3], self.legs[5]]
        setup(self.legs)

    def __walk(self, angle, direction):
        self.walkTick += 1

        moveLegs = self.legsOdd if self.walkTick % 2 == 0 else self.legsEven
        standLegs = self.legsEven if self.walkTick % 2 == 0 else self.legsOdd

        # Raise
        for leg in moveLegs:
            leg.knee.addAngle(-angle)
        actuate(moveLegs)

        # Forward
        for i in range(angle + 1):
            for leg in moveLegs:
                leg.shoulder.addAngle(direction)

            for leg in standLegs:
                leg.shoulder.addAngle(-direction)

            actuate(self.legs, sleep=0.05)

        # Lower
        for leg in moveLegs:
            leg.knee.addAngle(10)
        actuate(moveLegs)

    def __turn(self, angle, direction):
        self.turnTick += 1

        # Re-orient body
        if self.turnTick % 3 == 0:
            for i in range(angle + 1):
                for leg in self.legs:
                    leg.shoulder.addAngle(-direction, ignoreInverted=True)
                actuate(self.legs, sleep=0.05)

        # Move the legs
        else:
            moveLegs = self.legsEven if self.turnTick % 2 == 0 else self.legsOdd

            for leg in moveLegs:
                leg.knee.addAngle(-angle)
            actuate(moveLegs)

            for i in range(angle + 1):
                for leg in moveLegs:
                    leg.shoulder.addAngle(direction, ignoreInverted=True)
                actuate(self.legs, sleep=0.05)

            for leg in moveLegs:
                leg.knee.addAngle(angle)
            actuate(moveLegs)

    def __changeHeight(self, targetKnee, targetFoot):
        steps = 10
        diffKnee = (targetKnee - self.currKnee) / steps
        diffFoot = (targetFoot - self.currFoot) / steps
        for i in range(steps):
            self.stand(knee=self.currKnee + diffKnee, foot=self.currFoot + diffFoot)
            actuate(self.legs, sleep=0.01)

    def forward(self, angle=10):
        self.__walk(angle, 1)

    def backward(self, angle=10):
        self.__walk(angle, -1)

    def turnRight(self, angle=10):
        self.__turn(angle, direction=-1)

    def turnLeft(self, angle=10):
        self.__turn(angle, direction=1)

    def goTall(self):
        self.__changeHeight(targetKnee=130, targetFoot=70)

    def goShort(self):
        self.__changeHeight(targetKnee=90, targetFoot=20)

    # knee: more = higher
    # foot: more = higher
    def stand(self, shoulder=None, knee=135, foot=135):
        self.currKnee = knee
        self.currFoot = foot
        for leg in self.legs:
            leg.shoulder.currAngle = shoulder or leg.shoulder.startAngle
            leg.knee.currAngle = knee
            leg.foot.currAngle = foot
        actuate(self.legs)


if __name__ == "__main__":
    robot = Robot()
    robot.stand()
