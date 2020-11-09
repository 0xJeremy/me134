import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import argparse

##################
### PARAMETERS ###
##################

R = 1
P1 = np.array([0.5, 0.5, 0.707])
P2 = np.array([0, 1, 0])
SPHERE_RESOLUTION = 40
PATH_RESOLUTION = 10

#######################################
### VISUALIZATION AND INTERPOLATION ###
#######################################


def getSphereSurface(resolution):
    """
    Given a resolution (int), returns an arrays of x, y, and z points
    respectively where resolution = len(x) = len(y) = len(z).
    """
    res = complex(0, resolution)
    u, v = np.mgrid[0 : 2 * np.pi : res, 0 : np.pi : res]
    x = np.cos(u) * np.sin(v) * R
    y = np.sin(u) * np.sin(v) * R
    z = np.cos(v) * R
    return x, y, z


def slerp(p1, p2, t):
    """
    Performs a spherical linear interpolation from P1 to P2 with t number
    of points.
    """
    omega = np.arccos(p1.dot(p2))
    sinOmega = np.sin(omega)
    t = t[:, np.newaxis]
    return (np.sin((1 - t) * omega) * p1 + np.sin(t * omega) * p2) / sinOmega


def plot():
    """
    Plots the sphere and interpolated points from P1 to P2.
    """
    ax = plt.figure().add_subplot(111, projection="3d")
    x, y, z = getSphereSurface(SPHERE_RESOLUTION)
    ax.plot_surface(x, y, z, color="c", alpha=0.2, linewidth=0)
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")
    ax.set_zlabel("Z-axis")

    arc = slerp(P1, P2, np.linspace(0, 1, PATH_RESOLUTION))

    for point in arc:
        ax.scatter(
            *point,
            color="b",
            label="Interpolated Point" if np.array_equal(point, arc[0]) else None
        )
    ax.plot(arc[:, 0], arc[:, 1], arc[:, 2])
    ax.scatter(*P1, color="g", label="Starting Position")
    ax.scatter(*P2, color="r", label="Ending Position")
    plt.legend()


def generateRandom():
    """
    Generates a random sampling of points along a sphere and tests the
    interpolation algorithm.
    """
    vec = np.random.randn(3, 10)
    vec /= np.linalg.norm(vec, axis=0)
    xs, ys, zs = vec
    global P1, P2
    for i in range(1, len(xs)):
        P1 = np.array([xs[i - 1], ys[i - 1], zs[i - 1]])
        P2 = np.array([xs[i], ys[i], zs[i]])
        plot()
    plt.show()


########################################
### ARGUMENT PARSING AND ENTRY POINT ###
########################################

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Processes a path along a sphere for a robotic end-effector."
    )
    parser.add_argument(
        "-r",
        "--radius",
        type=float,
        help="Sets the radius for the sphere used, default={}".format(R),
    )
    parser.add_argument(
        "-sr",
        "--sphere_resolution",
        type=int,
        help="Sets the resolution of the sphere overlay, default={}".format(
            SPHERE_RESOLUTION
        ),
    )
    parser.add_argument(
        "-pr",
        "--path_resolution",
        type=int,
        help="Sets the resolution of the path interpolation, default={}".format(
            PATH_RESOLUTION
        ),
    )
    parser.add_argument(
        "-p1",
        "--point1",
        nargs="+",
        help="Sets the point for P1[x, y, z], default={}".format(P1),
    )
    parser.add_argument(
        "-p2",
        "--point2",
        nargs="+",
        help="Sets the point for P2[x, y, z], default={}".format(P2),
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Automatically tests the program with a sample of randomly generated points",
    )
    args = parser.parse_args()

    # Sets the global parameters according to the command line arguments
    if args.radius:
        R = args.radius
    if args.sphere_resolution:
        SPHERE_RESOLUTION = args.sphere_resolution
    if args.path_resolution:
        PATH_RESOLUTION = args.path_resolution
    if args.point1:
        P1 = np.array([float(point) for point in args.point1])
    if args.point2:
        P2 = np.array([float(point) for point in args.point2])

    if args.test:
        generateRandom()
    else:
        plot()
        plt.show()
