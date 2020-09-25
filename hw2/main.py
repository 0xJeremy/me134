# 172.20.10.2 on iPhone

from clock import Clock
import time_conversion as tc
import numpy as np
import time

def init():
    clock = Clock()
    time_binary_array = tc.get_binary_array()
    clock.set(time_binary_array)

    return clock, time_binary_array

def main():
    clock, previous_binary_array = init()

    # Main loop
    try:
        while True:
            time_binary_array = tc.get_binary_array()
            if (np.array_equal(previous_binary_array, time_binary_array)):
                pass
            else:
                clock.set(time_binary_array)
                previous_binary_array = time_binary_array
            time.sleep(5)
    except KeyboardInterrupt:
        print("Closing program...")
    finally:
        print("Done.")

# Loop through every value the clock can display
def demonstrate(period=3):
    clock, _ = init()

    # Main loop
    try:
        # loop through all possible combinations with *period* pause between changes
        for hour in range(24):
            for minute in range(60):
                binary_array = tc.time_to_binary_arrays(hour,minute)
                print(tc.time_to_string(hour, minute))
                print(binary_array)
                clock.set(binary_array)
                time.sleep(period)
    except KeyboardInterrupt:
        print("Closing program...")
    finally:
        print("Done.")


if __name__ == "__main__":
    # main()
    demonstrate() 