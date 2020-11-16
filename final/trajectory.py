import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

num_steps = 10
YS = np.linspace(-2, 2, num_steps)
LEG_DISTANCE = 3.5
BODY_WIDTH = 3


def gait_trajectory(y, height):
    z = np.zeros(num_steps)
    for i, value in enumerate(y):
        z[i] = math.sqrt(height ** 2 - value ** 2)
    return z


def generateWireframe(ax, trajectory, pointOffset, legSide=0):
    counter = 0
    for side in range(2):
        x = np.full(num_steps, side * BODY_WIDTH)
        for leg in range(0, 3):
            counter += 1
            if (counter % 2 == 0 and legSide == 0) or (
                counter % 2 != 0 and legSide == 1
            ):
                continue
            yValues = YS + np.full(YS.shape, leg * LEG_DISTANCE)
            ax.plot(x, yValues, trajectory, color="orange")
            ax.scatter(
                x[pointOffset],
                yValues[pointOffset],
                trajectory[pointOffset],
                color="blue",
            )


def animate():
    fig = plt.figure()
    ax = fig.gca(projection="3d")
    ax.set_xlabel("$X$")
    ax.set_ylabel("$Y$")
    ax.set_zlabel("$Z$")

    trajectory = gait_trajectory(YS, 2)

    for i in range(10):
        for j in range(num_steps):
            generateWireframe(ax, trajectory, j, legSide=i % 2)
            plt.pause(0.2)
        ax.cla()

    plt.show()


if __name__ == "__main__":
    animate()
