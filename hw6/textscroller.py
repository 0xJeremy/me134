import string
from PIL import Image, ImageFont, ImageDraw
import numpy as np
import time

WIDTH = 20
HEIGHT = 15

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

def cut(textArray, offset=0):
    zeros = np.zeros((HEIGHT, WIDTH, 3))
    vertOffset = int((HEIGHT - textArray.shape[0]) / 2)
    for i in range(zeros.shape[0]):
        if i >= textArray.shape[0]:
            break
        for j in range(zeros.shape[1]):
            if j >= textArray.shape[1]:
                break
            zeros[i+vertOffset][j] = textArray[i][j+offset]
    return zeros.astype('uint8')

class TextScroller:
    def __init__(self):
        pass

    def stringToPixels(self, text, color=(0, 0, 255)):
        arr = charToPixels(text, fontsize=12)
        result = np.expand_dims(arr, axis=2)
        result = np.where(result, color, (0, 0, 0))
        return result.astype('uint8')

    def displayTextScroll(self, display, text):
        text = self.stringToPixels(text)
        for i in range(text.shape[1] - WIDTH):
            display.set(cut(text, offset=i))
            time.sleep(0.1)
        time.sleep(0.4)
        display.reset()



if __name__ == '__main__':
    import time
    from display import Display
    scroller = TextScroller()
    disp = Display()
    time.sleep(1)
    scroller.displayTextScroll(disp, 'This is PONG!')
