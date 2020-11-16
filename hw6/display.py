import numpy as np
import time
import board
import neopixel

PIN = board.D18
LENGTH = 300
ORDER = neopixel.GRB
BRIGHTNESS = 0.5

WIDTH = 20
HEIGHT = 15


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)


class Display:
    def __init__(self, brightness=BRIGHTNESS):
        self.pixels = neopixel.NeoPixel(
            PIN, LENGTH, brightness=brightness, auto_write=False, pixel_order=ORDER
        )
        self.reset()

    def set(self, values):
        values = np.flipud(values)
        for i in range(HEIGHT):
            for j in range(WIDTH):
                if i % 2 != 0:
                    self.pixels[int(i * WIDTH + j)] = values[i][j]
                else:
                    self.pixels[int((i + 1) * WIDTH - j - 1)] = values[i][j]
        self.pixels.show()

    def reset(self):
        self.pixels.fill((0, 0, 0))
        self.pixels.show()

    def fill(self, color):
        self.pixels.fill(color)
        self.pixels.show()

    def rainbow(self, runs=10, wait=0.01):
        for run in range(runs):
            for j in range(255):
                for i in range(LENGTH):
                    pixel_index = (i * 256 // LENGTH) + j
                    self.pixels[i] = wheel(pixel_index & 255)
                self.pixels.show()
                time.sleep(wait)


if __name__ == "__main__":
    display = Display()

    toShow = np.full((HEIGHT, WIDTH, 3), (0, 0, 0))
    toShow[1][0] = (255, 255, 255)

    display.set(toShow)
