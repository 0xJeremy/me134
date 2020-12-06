import time


def __extend(robot, legNum):
    robot.leg(legNum, knee=135, foot=135)


def wall(robot):
    robotLegs = robot.legs
    __extend(robot, 0)  # raise front right
    time.sleep(1)
    robot.leg(0, shoulder=30)  # move front right forward

    __extend(robot, 3)  # raise front left
    time.sleep(1)
    robot.leg(3, shoulder=150)  # move front left forward

    robot.forward(
        moveLegs=[robotLegs[1], robotLegs[5]], standLegs=[robotLegs[2], robotLegs[4]]
    )


if __name__ == "__main__":
    from robot import Robot

    robot = Robot()
    robot.goTall()

    wall(robot)
