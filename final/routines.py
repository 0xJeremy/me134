import time

def swimFrontLegs(robot):
    robot.leg(0, knee=176, foot=101)
    robot.leg(0, shoulder=30)
    robot.leg(0, knee=210, foot=115)

    robot.leg(3, knee=176, foot=101)
    robot.leg(3, shoulder=150)
    robot.leg(3, knee=210, foot=115)

    robot.leg(0, shoulder=90, actuation=False)
    robot.leg(3, shoulder=90)

def swimBackLegs(robot):
    robot.leg(2, shoulder=150, actuation=False)
    robot.leg(5, shoulder=30)

    robot.leg(2, knee=176, foot=101)
    robot.leg(2, shoulder=90)
    robot.leg(2, knee=210, foot=115)

    robot.leg(5, knee=176, foot=101)
    robot.leg(5, shoulder=90)
    robot.leg(5, knee=210, foot=115)

    robot.leg(2, shoulder=150, actuation=False)
    robot.leg(5, shoulder=30)

def frontLegsForward(robot):
    robot.leg(0, shoulder=30, actuation=False)
    robot.leg(3, shoulder=150)

def frontLegsBack(robot):
    robot.leg(0, shoulder=90, actuation=False)
    robot.leg(3, shoulder=90)

def raiseFrontLegs(robot):
    robot.leg(0, knee=176, foot=101, actuation=False)
    robot.leg(3, knee=176, foot=101)

def lowerFrontLegs(robot):
    robot.leg(0, knee=210, foot=115, actuation=False)
    robot.leg(3, knee=210, foot=115)

def backLegsBack(robot):
    robot.leg(2, shoulder=150, actuation=False)
    robot.leg(5, shoulder=30)

def backLegsForward(robot):
    robot.leg(2, shoulder=90, actuation=False)
    robot.leg(5, shoulder=90)

def raiseBackLegs(robot):
    robot.leg(2, knee=176, foot=101, actuation=False)
    robot.leg(5, knee=176, foot=101)

def lowerBackLegs(robot):
    robot.leg(0, knee=210, foot=115, actuation=False)
    robot.leg(3, knee=210, foot=115)


def walkTall(robot):
    pass

def wall(robot):
    robot.goTall()

    # Raise front legs and brace on wall
    robot.raiseLegPair(0)
    time.sleep(1)
    robot.raiseLegPair(1)
    for leg in [0, 3]:
        robot.leg(leg, knee=210, foot=115)

    time.sleep(0.1)

    # Push forward from wall
    robot.leg(0, shoulder=90, actuation=False)
    robot.leg(3, shoulder=90)

    robot.leg(2, shoulder=150, actuation=False)
    robot.leg(5, shoulder=30)

    swimFrontLegs(robot)
    swimBackLegs(robot)

    # robot.leg(0, shoulder=30, actuation=False)
    # robot.leg(3, shoulder=150)


    # Move middle legs forward
    # robot.leg(1, shoulder=70, actuation=False)
    # robot.leg(4, shoulder=110)

    # robot.raiseLegPair(2)

    # robot.leg(1, knee=210, foot=115, actuation=False)
    # robot.leg(4, knee=210, foot=115)

    # robot.leg(1, shoulder=90, actuation=False)
    # robot.leg(4, shoulder=90)

    # for i in range(3):
    #     robot.raiseLegPair(0)
    #     robot.wallWalk(0)

    #     time.sleep(2)

    # robot.wallWalk(2)
    # robot.wallWalk(2)

    # robot.goTall()


if __name__ == "__main__":
    from robot import Robot

    robot = Robot()
    robot.goTall()

    wall(robot)
