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
       
    def __walkWall(self, angle, direction, set, runtime):
        self.walkTick += 1

        # walk with middle & back legs
        if set==0:
            self.legsOdd.remove(self.legs[3])
            self.legsEven.remove(self.legs[0])
            for leg in self.legsMiddle: 
                leg.shoulder.targetAngle = leg.shoulder.minAngle+angle
            for leg in self.legsBack:
                leg.shoulder.targetAngle = leg.shoulder.minAngle+angle
            actuate(self.legs,runtime=runtime) # set shoulder angles so that the legs won't hit the wall while walking

        # walk with front & back legs
        elif set==1:
            self.legsOdd.remove(self.legs[1])
            self.legsEven.remove(self.legs[4])
            for leg in self.legsFront:
                leg.shoulder.targetAngle = leg.shoulder.maxAngle-angle
            for leg in self.legsBack:
                leg.shoulder.targetAngle = leg.shoulder.minAngle+angle
            actuate(self.legs,runtime=runtime)

        # walk with front & middle legs
        else:
            self.legsOdd.remove(self.legs[5])
            self.legsEven.remove(self.legs[2])
            for leg in self.legsFront:
                leg.shoulder.targetAngle = leg.shoulder.maxAngle-angle
            for leg in self.legsMiddle:
                leg.shoulder.targetAngle = leg.shoulder.maxAngle-angle
            actuate(self.legs,runtime=runtime)

        moveLegs = self.legsOdd if self.walkTick % 2 == 0 else self.legsEven
        standLegs = self.legsEven if self.walkTick % 2 == 0 else self.legsOdd

        # raise
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

        # Reset
        for leg in moveLegs:
            leg.shoulder.addAngle(-angle)
        for leg in standLegs:
            leg.shoulder.addAngle(angle)
        actuate(self.legs, runtime=runtime)

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
            actuate(moveLegs, runtime=runtime)

            for leg in moveLegs:
                leg.shoulder.addAngle(angle * direction, ignoreInverted=True)
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
       
    def wall(self):
        # pass front legs
        self.raiseLeg(0)
        self.raiseLeg(3)
        for i in range(step=10): # assume that the remaining four legs need to move 10 steps to get to the wall
            self.__walkWall(angle=10,direction=1,set=0,runtime=0.03) # walk with the remaining four legs for one step
            self.lowerLeg(leg=0,angle=10,runtime=0.35) # lower leg0 on the other side of the wall 10 degress at a time
            self.lowerLeg(leg=3,angle=10,runtime=0.35) # lower leg3 on the other side of the wall

        # repeat for the middle and back sets of legs
        # pass middle legs
        self.raiseLeg(1)
        self.raiseLeg(4)
        for i in range(step=10):
            self.__walkWall(angle=10, direction=1, set=1, runtime=0.03)
            self.lowerLeg(leg=1, angle=10, runtime=0.35)
            self.lowerLeg(leg=4, angle=10, runtime=0.35)

        # pass back legs
        self.raiseLeg(2)
        self.raiseLeg(5)
        for i in range(step=10):
            self.__walkWall(angle=10, direction=1, set=2, runtime=0.03)
            self.lowerLeg(leg=2, angle=10, runtime=0.35)
            self.lowerLeg(leg=5, angle=10, runtime=0.35)
        self.reset

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
   
    def reset(self,runtime=0.35):
        for leg in self.legs:
            leg.shoulder.targetAngle=leg.shoulder.startAngle
            leg.knee.targetAngle=leg.knee.startAngle
            leg.foot.targetAngle=leg.foot.startAngle
        actuate(self.legs,runtime=runtime)

    def raiseLeg(self,leg,runtime=0.35):
        # prevent the leg from hitting the wall
        self.legs[leg].shoulder.targetAngle=self.legs[leg].shoulder.minAngle
        actuate(self.legs[leg],runtime=runtime)

        # raise leg to its minAngle (or to a specific angle that's sufficient to skip the wall)
        self.legs[leg].knee.targetAngle=self.legs[leg].knee.minAngle
        self.legs[leg].foot.targetAngle = self.legs[leg].foot.minAngle
        actuate(self.legs[leg],runtime=runtime)

        # skip wall
        self.legs[leg].shoulder.targetAngle=self.legs[leg].shoulder.maxAngle
        actuate(self.legs[leg],runtime=runtime)

        # bend leg
        self.legs[leg].foot.targetAngle = self.legs[leg].foot.startAngle
        actuate(self.legs[leg], runtime=runtime)

    def lowerLeg(self,leg,angle,runtime=0.35):
        # lower the leg(that is skipping the wall) for 'angle' angles each time called
        if self.legs[leg].foot.currentAngle<=85: # assume foot=85 will give us max height
            self.legs[leg].foot.addAngle(angle)
        if self.legs[leg].knee.currentAngle<=180: # assume knee=180 will give us max height
            self.legs[leg].knee.addAngle(angle)
        actuate(self.legs[leg],runtime=runtime)


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
