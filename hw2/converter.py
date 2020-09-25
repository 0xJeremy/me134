import time
import datetime

# The binary array indicates with of the seven segments are on or off. We're using a convention where the top segment is index 0, then clockwise around with the middle segment being last.
'''
 __0__
|     |
1     2
|__3__|
|     |
4     5
|__6__|
'''
ZERO = [1,1,1,0,1,1,1]
ONE = [0,0,1,1,0,0,0]
TWO = [1,0,1,1,1,0,1]
THREE = [1,0,1,1,0,1,1]
FOUR = [0,1,1,1,0,1,0]
FIVE = [1,1,0,1,0,1,1]
SIX = [0,1,0,1,1,1,1]
SEVEN = [1,0,1,0,0,1,0]
EIGHT = [1,1,1,1,1,1,1]
NINE = [1,1,1,1,0,1,0]

Integer_To_Binary = {0:ZERO, 1:ONE, 2:TWO, 3:THREE, 4:FOUR, 5:FIVE, 6:SIX, 7:SEVEN, 8:EIGHT, 9:NINE}

def get_binary_array():
    now = datetime.datetime.now()
    hours = now.hour
    minutes = now.minute

    return time_to_binary_arrays(hours, minutes)

def time_to_string(hours, minutes):
    return "{}:{}".format(str(hours).zfill(2), str(minutes).zfill(2))

def time_to_binary_arrays(hours, minutes):
    # ugly but we have no speed requirements
    time_string = time_to_string(hours,minutes)

    hour0 = int(time_string[0])
    hour1 = int(time_string[1])
    min0 = int(time_string[3])
    min1 = int(time_string[4])

    toConvert = [hour0, hour1, min0, min1]
    ret = []
    for entry in toConvert:
        ret.extend(Integer_To_Binary[entry])

    return ret
