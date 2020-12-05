from interpolator import generatePoints

try:
    from adafruit_servokit import ServoKit
    import time

    boards = [ServoKit(channels=16, address=0x40), ServoKit(channels=16, address=0x41)]

    numInterpolationPoints = 10

    def setup(legs):
        for leg in legs:
            for joint in leg.joints:
                servo = boards[joint.board].servo[joint.channel]
                servo.actuation_range = joint.actuationRange
                servo.set_pulse_width_range(joint.minPulse, joint.maxPulse)

    def __validateMotionPlan(legs):
        for leg in legs:
            for joint in leg.joints:
                if joint.minAngle is not None and joint.targetAngle < joint.minAngle:
                    raise RuntimeError(
                        "Unable to actuate; commanded angle is less than hardware range. Commanded={}, minAngle={}".format(
                            joint.targetAngle, joint.minAngle
                        )
                    )
                if joint.maxAngle is not None and joint.targetAngle > joint.maxAngle:
                    raise RuntimeError(
                        "Unable to actuate; commanded angle is greater than hardware range. Commanded={}, maxAngle={}".format(
                            joint.targetAngle, joint.maxAngle
                        )
                    )

    def __generateActuationPlan(legs, runtime=0.5):
        sleepTime = None
        for leg in legs:
            for joint in leg.joints:
                angles, timeDiffs = generatePoints(
                    joint.currentAngle,
                    joint.targetAngle,
                    runtime=runtime,
                    points=numInterpolationPoints,
                )
                joint.interpolatedPoints = angles
                if sleepTime is None:
                    sleepTime = timeDiffs[0]
        return sleepTime

    def __performActuation(legs, sleepTime):
        for i in range(numInterpolationPoints - 1):
            for leg in legs:
                for joint in leg.joints:
                    boards[joint.board].servo[
                        joint.channel
                    ].angle = joint.interpolatedPoints[i]
                    joint.currentAngle = joint.interpolatedPoints[i]
                time.sleep(sleepTime)

    def actuate(legs, runtime=0.35):
        __validateMotionPlan(legs)
        sleepTime = __generateActuationPlan(legs, runtime=runtime)
        __performActuation(legs, sleepTime)


except:
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    from math import cos, sin, radians

    ax = plt.figure().gca(projection="3d")
    xBodyPoints = [3, 3, 3, -3, -3, -3]
    yBodyPoints = [-3, 0, 3, -3, 0, 3]
    zBodyPoints = [10, 10, 10, 10, 10, 10]
    xLegPoints = [3, 3, 3, -3, -3, -3]
    yLegPoints = [-3, 0, 3, -3, 0, 3]
    zLegPoints = [10, 10, 10, 10, 10, 10]
    shoulderLength = 1
    kneeLength = 1
    footLength = 1
    base_shoulder_distance = 1

    def setup(legs):
        pass

    def actuate(legs, sleep=0.2):
        ax.cla()
        i = -1
        for leg in legs:
            i += 1
            shoulderAng = leg.shoulder.currAngle
            alpha = leg.knee.currAngle - 90
            add_arg = 180 - 90 - alpha
            beta = leg.foot.currAngle - add_arg
            heightcomp2 = footLength * sin(radians(beta))
            widthcomp2 = footLength * cos(radians(beta))
            height = kneeLength * cos(radians(alpha)) + heightcomp2
            width = kneeLength * sin(radians(alpha)) - widthcomp2
            if xBodyPoints[i] < 0:
                xLegPoints[i] = xBodyPoints[i] - width
            else:
                xLegPoints[i] = xBodyPoints[i] + width

            zLegPoints[i] = zBodyPoints[i] - height
            if shoulderAng < 90:
                yLegPoints[i] = yBodyPoints[i] - width * sin(radians(shoulderAng))
            else:
                yLegPoints[i] = yBodyPoints[i] - width * sin(radians(shoulderAng))

        ax.scatter(xBodyPoints, yBodyPoints, zBodyPoints, color="green")
        ax.scatter(xLegPoints, yLegPoints, zLegPoints, color="red")

        plt.pause(sleep)


if __name__ == "__main__":
    from hardware import LEGS

    actuate(LEGS)
    plt.show()
