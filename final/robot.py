from actuation import setup, actuate
import time

class Joint:
    def __init__(self, board, channel, minPulse, maxPulse, startAngle, inverted=False):
        self.board = board
        self.channel = channel
        self.minPulse = minPulse
        self.maxPulse = maxPulse
        self.startAngle = startAngle
        self.currAngle = self.startAngle
        self.inverted = inverted

    def addAngle(self, angle, ignoreInverted=False):
        inverted = False if ignoreInverted else self.inverted
        if inverted:
            self.currAngle -= angle
        else:
            self.currAngle += angle


JOINT1 = Joint(0, 0, 600, 2500, 135)
JOINT2 = Joint(0, 1, 575, 2500, 135)
JOINT3 = Joint(0, 2, 600, 2500, 90)
JOINT4 = Joint(0, 3, 550, 2500, 135)
JOINT5 = Joint(0, 4, 550, 2500, 135)
JOINT6 = Joint(0, 5, 700, 2500, 90)
JOINT7 = Joint(0, 6, 700, 2500, 135)
JOINT8 = Joint(0, 7, 600, 2500, 135)
JOINT9 = Joint(0, 8, 500, 2500, 90)
JOINT10 = Joint(1, 0, 750, 2500, 135)
JOINT11 = Joint(1, 1, 700, 2500, 135)
JOINT12 = Joint(1, 2, 500, 2600, 90, inverted=True)
JOINT13 = Joint(1, 3, 500, 2500, 135)
JOINT14 = Joint(1, 4, 700, 2500, 135)
JOINT15 = Joint(1, 5, 500, 2500, 90, inverted=True)
JOINT16 = Joint(1, 6, 500, 2500, 135)
JOINT17 = Joint(1, 7, 600, 2500, 135)
JOINT18 = Joint(1, 8, 600, 2500, 90, inverted=True)


class Leg:
    def __init__(self, foot, knee, shoulder):
        self.foot = foot
        self.knee = knee
        self.shoulder = shoulder
        self.joints = [foot, knee, shoulder]


LEG1 = Leg(JOINT1, JOINT2, JOINT3)
LEG2 = Leg(JOINT4, JOINT5, JOINT6)
LEG3 = Leg(JOINT7, JOINT8, JOINT9)
LEG4 = Leg(JOINT10, JOINT11, JOINT12)
LEG5 = Leg(JOINT13, JOINT14, JOINT15)
LEG6 = Leg(JOINT16, JOINT17, JOINT18)

LEGS = [LEG1, LEG2, LEG3, LEG4, LEG5, LEG6]

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
        for i in range(angle+1):
            for leg in moveLegs:
                leg.shoulder.addAngle(direction)

            for leg in standLegs:
                leg.shoulder.addAngle(-direction)

            actuate(self.legs, sleep=0.05)

        # Lower
        for leg in moveLegs:
            leg.knee.addAngle(10)
        actuate(moveLegs)

    def forward(self, angle=10):
        self.__walk(angle, 1)

    def backward(self, angle=10):
        self.__walk(angle, -1)

    def __turn(self, angle, direction):
        self.turnTick += 1

        if self.turnTick % 3 == 0:
            for i in range(angle+1):
                for leg in self.legs:
                    leg.shoulder.addAngle(-direction, ignoreInverted=True)
                actuate(self.legs, sleep=0.05)

        else:
            moveLegs = self.legsEven if self.turnTick % 2 == 0 else self.legsOdd

            for leg in moveLegs:
                leg.knee.addAngle(-angle)
            actuate(moveLegs)

            for i in range(angle+1):
                for leg in moveLegs:
                    leg.shoulder.addAngle(direction, ignoreInverted=True)
                actuate(self.legs, sleep=0.05)

            for leg in moveLegs:
                leg.knee.addAngle(angle)
            actuate(moveLegs)

    def turnRight(self, angle=10):
        self.__turn(angle, direction=-1)

    def turnLeft(self, angle=10):
        self.__turn(angle, direction=1)

    def __changeHeight(self, targetKnee, targetFoot):
        steps = 10
        diffKnee = (targetKnee - self.currKnee) / steps
        diffFoot = (targetFoot - self.currFoot) / steps
        for i in range(steps):
            self.stand(knee=self.currKnee + diffKnee, foot=self.currFoot + diffFoot)
            actuate(self.legs, sleep=0.01)

    def goTall(self):
        self.__changeHeight(targetKnee=130, targetFoot=70)

    def goShort(self):
        self.__changeHeight(targetKnee=90, targetFoot=20)

    def stand(self, shoulder=None, knee=90, foot=20):
        self.currKnee = knee
        self.currFoot = foot
        for leg in self.legs:
            leg.shoulder.currAngle = shoulder or leg.shoulder.startAngle
            leg.knee.currAngle = knee
            leg.foot.currAngle = foot
        actuate(self.legs)

if __name__ == '__main__':
    robot = Robot()
    robot.stand()


