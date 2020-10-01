import tinyik
import numpy as np

# https://stackoverflow.com/questions/1969240/mapping-a-range-of-values-to-another
def mapValue(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)


def normalizeJoint0(angle):
    if angle > 180:
        angle -= 360
    elif angle < -180:
        angle += 360
    return angle


def normalizeJoint1(angle):
    if angle < 0:
        angle += 360
    elif angle > 180:
        raise RuntimeError("Unable to normalize joint 1:", angle)
    return angle


def normalizeJoint2(angle):
    return abs(angle)


def mapToMachineAngles(angles):
    angles[0] = normalizeJoint0(angles[0])
    angles[1] = normalizeJoint1(angles[1])
    angles[2] = normalizeJoint2(angles[2])
    return angles


class MotionPlanner:
    def __init__(self):
        self.min_x = 0.3
        self.min_y = 0.3
        self.max_x = 2.1
        self.max_y = 2.1
        self.arm = tinyik.Actuator(
            [
                "z",
                [1e-10, 0.0, 0.32],
                "x",
                [0.0, 1.4745, 0.0],
                "x",
                [0.0, 1.5566, 0.0],
                # "x", [0.0, 0.355,  0.0],
            ]
        )

    def createMachinePath(self, xs, ys):
        # Expects 1D array of points
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)

        x_points = []
        y_points = []

        for x, y in zip(xs, ys):
            x_points.append(mapValue(x, min_x, max_x, self.min_x, self.max_x))
            y_points.append(mapValue(y, min_y, max_y, self.min_y, self.max_y))

        return x_points, y_points

    def getAngles(self, x, y, z=0):
        # min: [0.3, 0.3, 0]
        # max: [2.1, 2.1, 0]
        self.arm.ee = [x, y, z]
        angles = np.degrees(self.arm.angles)
        return mapToMachineAngles(angles)


if __name__ == "__main__":
    planner = MotionPlanner()
    position = 2.1
    angles = planner.getAngles(position, position, 0)
    print(position, angles)
    tinyik.visualize(planner.arm)
