# ME-134 Midterm Exam Programming Problem

### Usage
This program is intended to be run with Python3 (behavior untested in Python2).
To run, use `python main.py`. Additional command line arguments are
```
usage: main.py [-h] [-r RADIUS] [-sr SPHERE_RESOLUTION] [-pr PATH_RESOLUTION]
               [-p1 POINT1 [POINT1 ...]] [-p2 POINT2 [POINT2 ...]] [--test]

Processes a path along a sphere for a robotic end-effector.

optional arguments:
  -h, --help            show this help message and exit
  -r RADIUS, --radius RADIUS
                        Sets the radius for the sphere used, default=1
  -sr SPHERE_RESOLUTION, --sphere_resolution SPHERE_RESOLUTION
                        Sets the resolution of the sphere overlay, default=40
  -pr PATH_RESOLUTION, --path_resolution PATH_RESOLUTION
                        Sets the resolution of the path interpolation,
                        default=10
  -p1 POINT1 [POINT1 ...], --point1 POINT1 [POINT1 ...]
                        Sets the point for P1[x, y, z], default=[0.5 0.5
                        0.707]
  -p2 POINT2 [POINT2 ...], --point2 POINT2 [POINT2 ...]
                        Sets the point for P2[x, y, z], default=[0 1 0]
  --test                Automatically tests the program with a sample of
                        randomly generated points
```
Use `python main.py --help` to see this message.

NOTE: Use `python3 main.py --test` to autogenerate random points to test the program.

### Limitations
This program makes several assumptions. If the user inputs a point (for either P1 or P2), it assumes this point is a valid [x, y, z] position for the radius of the sphere. It will work independent of the sphere radius, but the visualization is poor in that case.

### To Modify Parameters
To modify the parameters of the interpolator, there are two options. The first is the adjust the parameters in the command line interface (which exposes all the functionality of the program), or they can be modified in the program itself. To do this, change the values in the `### PARAMETERS` section.

### Requirements
This program requires `numpy` and `matplotlib` (and `mpl_toolkits`, which is part of `matplotlib`).

### Sample Commands

`python main.py`
`python main.py --test`
`python main.py -r 2 -p1 2 0 0 -p2 0 2 0`
`python main.py -r 2 -p1 2 0 0 -p2 0 2 0 -pr 20`
