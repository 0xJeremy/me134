# try:
from adafruit_servokit import ServoKit

boards = [ServoKit(channels=16, address=0x40), ServoKit(channels=16, address=0x41)]


def setup(legs):
    for leg in legs:
        for joint in leg.joints:
            boards[joint.board].servo[joint.channel].set_pulse_width_range(
                joint.minPulse, joint.maxPulse
            )
            boards[joint.board].servo[joint.channel].angle = joint.startAngle


def actuate(legs):
    for leg in legs:
        for joint in leg.joints:
            boards[joint.board].servo[joint.channel].angle = joint.currAngle


# except:
#     import matplotlib.pyplot as plt
#     from mpl_toolkits.mplot3d import Axes3D
#     from math import cos, sin, radians

#     ax = plt.figure().gca(projection="3d")
#     xBodyPoints = [1, 1, 2, 3, 3, 2, 1]
#     yBodyPoints = [0, 0.5, 0.5, 0.5, 0, 0, 0]
#     zBodyPoints = [0] * 7
#     shoulderAngle = 35
#     shoulderLength = 1
#     kneeLength = 1
#     footLength = 1
#     color = "green"

#     def setup(legs):
#         pass

#     def actuate(legs):
#         ax.cla()
#         ax.scatter(xBodyPoints, yBodyPoints, zBodyPoints, color="blue")
#         ax.plot(xBodyPoints, yBodyPoints, zBodyPoints, color="red")

#         bp1 = [xBodyPoints[0], yBodyPoints[0]]
#         leg1 = legs[0]
#         shoulder1 = shoulderLength * cos(
#             radians(leg1.shoulder.currAngle + shoulderAngle)
#         )
#         knee1 = kneeLength * cos(radians(leg1.knee.currAngle))
#         foot1 = footLength * cos(radians(leg1.foot.currAngle))

#         ax.scatter(bp1[0], shoulder1, zBodyPoints[0], color=color)
#         ax.scatter(shoulder1, knee1, zBodyPoints[0], color=color)
#         ax.scatter(knee1, foot1, zBodyPoints[0], color=color)


# if __name__ == "__main__":
#     from robot import LEGS

#     actuate(LEGS)
#     plt.show()
