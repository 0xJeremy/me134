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
        self.forwardCount = 0
        self.isTall = False

    def __walk(self, raiseAngle, turnAngle, direction, runtime):
        self.walkTick += 1

        moveLegs = self.legsOdd if self.walkTick % 2 == 0 else self.legsEven
        standLegs = self.legsEven if self.walkTick % 2 == 0 else self.legsOdd

        # Raise
        for leg in moveLegs:
            leg.knee.addAngle(-raiseAngle)
            leg.foot.addAngle(-raiseAngle)
        actuate(moveLegs, runtime=runtime)

        # Forward
        for leg in moveLegs:
            leg.shoulder.addAngle(turnAngle * direction)

        for leg in standLegs:
            leg.shoulder.addAngle(-turnAngle * direction)

        actuate(self.legs, runtime=runtime)

        # Lower
        stopOffset = 10
        for leg in moveLegs:
            leg.knee.addAngle(raiseAngle - stopOffset)
            leg.foot.addAngle(raiseAngle)
        actuate(moveLegs, runtime=runtime)

        for leg in moveLegs:
            leg.knee.addAngle(stopOffset)
        actuate(moveLegs, runtime=runtime)

    def raiseLegPair(self, pairNumber):
        legPair = [pairNumber, pairNumber+3]

        for leg in legPair:
            self.leg(leg, knee=115, foot=20)
            self.leg(leg, knee=135, foot=135)
            # self.leg(leg, knee=135, foot=135)

            if leg == 0 or leg == 5:
                self.leg(leg, shoulder=30)

            if leg == 2 or leg == 3:
                self.leg(leg, shoulder=150)

    def wallWalk(self, pairRaised, raiseAngle=34, turnAngle=14, runtime=0.07):
        legSequence = {
            0: [self.legs[1], self.legs[5], self.legs[2], self.legs[4]],
            1: [self.legs[0], self.legs[5], self.legs[2], self.legs[3]],
            2: [self.legs[0], self.legs[4], self.legs[1], self.legs[3]],
        }[pairRaised]

        for i in range(2):
            for leg in legSequence:
                # Raise leg
                leg.knee.addAngle(-raiseAngle)
                leg.foot.addAngle(-raiseAngle)
                actuate([leg], runtime=runtime)

                # Move forward
                leg.shoulder.addAngle(turnAngle)
                actuate([leg], runtime=runtime)

                # Lower leg
                leg.knee.addAngle(raiseAngle)
                leg.foot.addAngle(raiseAngle)
                actuate([leg], runtime=runtime)

            for leg in legSequence:
                leg.shoulder.addAngle(-turnAngle)
                actuate([leg], runtime=runtime)

    def __turn(self, angle, direction, runtime):
        self.turnTick += 1

        # Re-orient body
        if self.turnTick % 3 == 0:
            for leg in self.legs:
                leg.shoulder.addAngle(angle * -direction, ignoreInverted=True)
            actuate(self.legs, runtime=runtime)

        # Move the legs
        else:
            moveLegs = self.legsEven if self.turnTick % 2 == 0 else self.legsOdd

            for leg in moveLegs:
                leg.knee.addAngle(-angle)
                leg.foot.addAngle(-angle)
            actuate(moveLegs, runtime=runtime)

            for leg in moveLegs:
                leg.shoulder.addAngle(angle * direction, ignoreInverted=True)
            actuate(self.legs, runtime=runtime)

            for leg in moveLegs:
                leg.knee.addAngle(angle)
                leg.foot.addAngle(angle)
            actuate(moveLegs, runtime=runtime)

    def forward(self, raiseAngle=34, turnAngle=14, runtime=0.03):
        for i in range(2):
            self.__walk(
                raiseAngle=raiseAngle,
                turnAngle=turnAngle,
                direction=-1,
                runtime=runtime,
            )
        self.forwardCount += 1
        if self.forwardCount % 3 == 2:
            self.turnLeft()

    def backward(self, raiseAngle=34, turnAngle=14, runtime=0.03):
        for i in range(2):
            self.__walk(
                raiseAngle=raiseAngle,
                turnAngle=turnAngle,
                direction=1,
                runtime=runtime,
            )
        self.forwardCount += 1
        if self.forwardCount % 3:
            self.turnRight()

    def turnRight(self, angle=20, runtime=0.05):
        for i in range(3):
            self.__turn(angle, direction=-1, runtime=runtime)

    def turnLeft(self, angle=20, runtime=0.05):
        for i in range(3):
            self.__turn(angle, direction=1, runtime=runtime)

    def goTall(self):
        self.stand(knee=210, foot=115, runtime=0.1)
        self.isTall = True

    def goShort(self):
        self.stand(knee=90, foot=0, runtime=0.1)
        self.isTall = False

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

    def leg(self, legNum, shoulder=None, knee=None, foot=None, runtime=0.05, actuation=True):
        leg = self.legs[legNum]
        if shoulder is not None:
            leg.shoulder.targetAngle = shoulder
        if knee is not None:
            leg.knee.targetAngle = knee
        if foot is not None:
            leg.foot.targetAngle = foot
        if actuation:
            actuate(self.legs, runtime=runtime)


if __name__ == "__main__":
    import time

    robot = Robot()
    # robot.stand(runtime=0.1)
    # time.sleep(0.1)
    robot.stand(knee=155, foot=65, runtime=0.060)

    def demo(sleeptime=0.5):
        for i in range(5):
            robot.stand(knee=115, runtime=0.065)
            time.sleep(sleeptime)
            robot.stand(knee=185, runtime=0.065)
            time.sleep(sleeptime)
