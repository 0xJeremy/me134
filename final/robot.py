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
        self.legsFront = [self.legs[0], self.legs[3]]
        self.legsMiddle = [self.legs[1], self.legs[4]]
        self.legsBack = [self.legs[2], self.legs[5]]
        self.legsRight = [self.legs[0], self.legs[1], self.legs[2]]
        self.legsLeft = [self.legs[3], self.legs[4], self.legs[5]]
        setup(self.legs)
        self.forwardCount = 0
        self.forwardTallCount = 0
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
        if moveLegs is None and standLegs is None:
            if not self.isTall:
                self.forwardCount += 1
                if self.forwardCount % 3:
                    self.turnLeft()
            else:
                self.forwardTallCount += 1
                if self.forwardTallCount % 3 == 1:
                    self.turnLeft()

    def backward(self, raiseAngle=34, turnAngle=14, runtime=0.03):
        for i in range(2):
            self.__walk(
                raiseAngle=raiseAngle,
                turnAngle=turnAngle,
                direction=1,
                runtime=runtime,
            )
        if not self.isTall:
            self.forwardCount += 1
            if self.forwardCount % 3:
                self.turnRight()
        else:
            self.forwardTallCount += 1
            if self.forwardTallCount % 3 == 1:
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
        
    def __adjust(self,angle,direction,runtime=0.03):

        if direction==0: #body facing right
            # front legs (leg 0 and leg 3) need to move to the left, and back legs(leg2 and leg 5) need to move to the right
            # leg 0 need to add positive foot angle to move to the left,
            # leg 3 need to add neg foot angle to move to the left

            # leg 2 need to add negative foot angle to move to the right,
            # leg 5 need to add positive foot angle to move to the right.
            setA = [self.legs[0], self.legs[5]]
            setB = [self.legs[3], self.legs[2]]

        else:
            setB = [self.legs[0], self.legs[5]]
            setA = [self.legs[3], self.legs[2]]
        #raise
        for leg in setA:
            leg.knee.addAngle(-10)
        actuate(setA, runtime=runtime)

        #stretch
        for leg in setA:
            leg.foot.addAngle(angle)
        actuate(setA, runtime=runtime)

        #lower
        for leg in setA:
            leg.knee.addAngle(10)
        actuate(setA, runtime=runtime)

        #reset
        for leg in setA:
            leg.foot.addAngle(-angle)
        actuate(setA, runtime=runtime)

        #raise
        for leg in setB:
            leg.knee.addAngle(-10)
        actuate(setB, runtime=runtime)

        #fold
        for leg in setB:
            leg.foot.addAngle(-angle)
        actuate(setA, runtime=runtime)

        #lower
        for leg in setB:
            leg.knee.addAngle(10)
        actuate(setB, runtime=runtime)

        #reset
        for leg in setB:
            leg.foot.addAngle(angle)
        actuate(setB, runtime=runtime)
        
    def __balance(self,runtime=0.03):
        heading=sensing.getAbsoluteOrientation()[0]/2.0 #about z-axis
        roll=sensing.getAbsoluteOrientation()[1]/2.0 #about y-axix
        pitch=sensing.getAbsoluteOrientation()[2]/2.0 #about x-axis

        thresh=5

        if math.abs(heading)>thresh:
            if heading>0:
                self.__adjust(heading,0)
            else:
                self.__adjust(heading,1)
        if math.abs(roll)>thresh: # tilt to the right
            for leg in legsRight:
                self.leg.knee.addAngle(roll)
            for leg in legsLeft:
                self.leg.knee.addAngle(-roll)
            actuate(self.legs,runtime=runtime)
        else:
            for leg in legsRight:
                self.leg.knee.addAngle(-roll)
            for leg in legsLeft:
                self.leg.knee.addAngle(roll)
            actuate(self.legs, runtime=runtime)
        if math.abs(pitch)>thresh: # tilt to the back
            for leg in legsBack:
                self.leg.knee.addAngle(pitch)
            for leg in legsFront:
                self.leg.knee.addAngle(-pitch)
            actuate(self.legs, runtime=runtime)
        else:
            for leg in legsBack:
                self.leg.knee.addAngle(-pitch)
            for leg in legsFront:
                self.leg.knee.addAngle(pitch)
            actuate(self.legs, runtime=runtime)
    
    def debris(self):
        self.__walk(angle * 2, 1, runtime=runtime)
        self.__balance()

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

    def leg(self, legNum, shoulder=None, knee=None, foot=None, runtime=0.05):
        leg = self.legs[legNum]
        if shoulder is not None:
            leg.shoulder.targetAngle = shoulder
        if knee is not None:
            leg.knee.targetAngle = knee
        if foot is not None:
            leg.foot.targetAngle = foot
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
