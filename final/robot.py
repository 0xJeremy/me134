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

    def __walk(self, angle, direction, runtime):
        self.walkTick += 1

        moveLegs = self.legsOdd if self.walkTick % 2 == 0 else self.legsEven
        standLegs = self.legsEven if self.walkTick % 2 == 0 else self.legsOdd

        # Raise
        for leg in moveLegs:
            leg.knee.addAngle(-angle)
        actuate(moveLegs, runtime=runtime)

        # Forward
        for leg in moveLegs:
            leg.shoulder.addAngle(angle)

        for leg in standLegs:
            leg.shoulder.addAngle(-angle)

        actuate(self.legs, runtime=runtime)

        # Lower
        for leg in moveLegs:
            leg.knee.addAngle(angle)
        actuate(moveLegs, runtime=runtime)

    def __turn(self, angle, direction, runtime):
        self.turnTick += 1

        # Re-orient body
        if self.turnTick % 3 == 0:
            for leg in self.legs:
                leg.shoulder.addAngle(angle*-direction, ignoreInverted=True)
            actuate(self.legs, runtime=runtime)

        # Move the legs
        else:
            moveLegs = self.legsEven if self.turnTick % 2 == 0 else self.legsOdd

            for leg in moveLegs:
                leg.knee.addAngle(-angle)
            actuate(moveLegs, runtime=runtime)

            for leg in moveLegs:
                leg.shoulder.addAngle(angle*direction, ignoreInverted=True)
            actuate(self.legs, runtime=runtime)

            for leg in moveLegs:
                leg.knee.addAngle(angle)
            actuate(moveLegs, runtime=runtime)

    def forward(self, angle=15, runtime=0.03):
        for i in range(2):
            self.__walk(angle, 1, runtime=runtime)

    def backward(self, angle=15, runtime=0.03):
        for i in range(2):
            self.__walk(angle, -1, runtime=runtime)

    def turnRight(self, angle=15, runtime=0.05):
        for i in range(3):
            self.__turn(angle, direction=-1, runtime=runtime)

    def turnLeft(self, angle=15, runtime=0.05):
        for i in range(3):
            self.__turn(angle, direction=1, runtime=runtime)

    def goTall(self):
        self.stand(knee=180, foot=85, runtime=0.1)

    def goShort(self):
        self.stand(knee=110, foot=45, runtime=0.1)

    # knee: more = higher
    # foot: more = higher
    def stand(self, shoulder=None, knee=135, foot=135, runtime=0.35):
        self.currentKnee = knee
        self.currentFoot = foot
        for leg in self.legs:
            leg.shoulder.targetAngle = shoulder or leg.shoulder.startAngle
            leg.knee.targetAngle = knee
            leg.foot.targetAngle = foot
        actuate(self.legs, runtime=runtime)


if __name__ == "__main__":
    import time
    robot = Robot()
    robot.stand(runtime=0.1)
    time.sleep(0.1)
    robot.stand(knee=155, foot=65, runtime=0.060)

    def demo(sleeptime=0.5):
        for i in range(5):
            robot.stand(knee=115, runtime=0.065)
            time.sleep(sleeptime)
            robot.stand(knee=185, runtime=0.065)
            time.sleep(sleeptime)
