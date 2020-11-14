import string
from PIL import Image, ImageFont, ImageDraw
import numpy as np
import time

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
    return (r, g, b)

def charToPixels(text, path='/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf', fontsize=14):
    font = ImageFont.truetype(path, fontsize) 
    w, h = font.getsize(text)  
    h *= 2
    image = Image.new('L', (w, h), 1)  
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), text, font=font) 
    arr = np.asarray(image)
    arr = np.where(arr, 0, 1)
    arr = arr[(arr != 0).any(axis=1)]
    return arr

def display(arr):
    result = np.where(arr, '#', ' ')
    print('\n'.join([''.join(row) for row in result]))

def cut(textArray, offset=0, color=(0, 0, 255)):
    zeros = np.zeros((HEIGHT, WIDTH, 3))
    vertOffset = int((HEIGHT - textArray.shape[0]) / 2)
    for i in range(zeros.shape[0]):
        if i >= textArray.shape[0]:
            break
        for j in range(zeros.shape[1]):
            if j >= textArray.shape[1]:
                break
            if np.any(textArray[i][j+offset]):
                # zeros[i+vertOffset][j] = color
                zeros[i+vertOffset][j] = wheel(j * 8)
            else:
                zeros[i+vertOffset][j] = (0, 0, 0)
            # zeros[i+vertOffset][j] = textArray[i][j+offset]
    return zeros.astype('uint8')

class TextScroller:
    def __init__(self):
        pass

    def stringToPixels(self, text):
        arr = charToPixels(text, fontsize=12)
        result = np.expand_dims(arr, axis=2)
        result = np.where(result, (1, 1, 1), (0, 0, 0))
        return result.astype('uint8')

    def displayTextScroll(self, display, text, color=(0, 0, 255)):
        text = self.stringToPixels(text)
        for i in range(text.shape[1] - WIDTH):
            display.set(cut(text, offset=i, color=color))
            time.sleep(0.1)
        time.sleep(0.4)
        display.reset()



if __name__ == '__main__':
    import time
    from display import Display
    scroller = TextScroller()
    disp = Display(0.8)
    time.sleep(1)
    scroller.displayTextScroll(disp, 'This is PONG!')
