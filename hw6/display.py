import board
import neopixel

PIN = board.D18
LENGTH = 300

WIDTH = 20
HEIGHT = 15

class Display:
    def __init__(self):
        self.pixels = neopixel.NeoPixel(PIN, LENGTH)
        self.reset()

    def set(self, values):
        for i in range(WIDTH):
            for j in range(HEIGHT):
                self.pixels[i*HEIGHT + j] = values[i][j]

    def reset(self):
        self.pixels.fill((255, 255, 255))
