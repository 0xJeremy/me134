import numpy as np
import random
# from display import wheel

def setRange(value, minimum, maximum):
    return min(max(value, minimum), maximum)


HEIGHT = 15
WIDTH = 20

PADDLE_COLOR = (0, 255, 0)
BALL_COLOR = (0, 0, 255)

PADDLE = 1
BALL = 2

PADDLE_LENGTH = 5

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

SPEED_REDUCER = 6


class Ball:
    def __init__(self):
        self.reset()

    def reset(self):
        global SPEED_REDUCER
        SPEED_REDUCER -= 1
        SPEED_REDUCER = max(SPEED_REDUCER, 2)
        self.position = (int(HEIGHT / 2), int(WIDTH / 2))
        self.velocity = (random.choice([-1, 0, 1]), random.choice([-1/SPEED_REDUCER, 1/SPEED_REDUCER]))

    def flipXDirection(self):
        self.velocity = (self.velocity[0], -self.velocity[1])

    def step(self):
        self.position = (
            self.position[0] + self.velocity[0],
            self.position[1] + self.velocity[1],
        )
        if self.position[0] in [0, HEIGHT - 1]:
            self.velocity = (-self.velocity[0], self.velocity[1])
        if int(self.position[1]) == 1:
            return 0
        if int(self.position[1]) == WIDTH - 2:
            return 1
        return None


class Pong:
    def __init__(self):
        self.reset()
        self.tick = 0

    def reset(self):
        self.paddles = [0, 0]
        self.ball = Ball()
        self.generateBoard()
        self.scored = False

    def generateBoard(self):
        self.board = np.full((HEIGHT, WIDTH, 3), (0, 0, 0))
        self.invBoard = np.full((HEIGHT, WIDTH, 3), (255, 255, 255))
        # for i in range(HEIGHT):
        #     if self.paddles[0] <= i and self.paddles[0] + PADDLE_LENGTH > i:
        #         self.board[i][0] = PADDLE
        #     if self.paddles[1] <= i and self.paddles[1] + PADDLE_LENGTH > i:
        #         self.board[i][WIDTH - 1] = PADDLE

    def step(self):
        atEnd = self.ball.step()
        if atEnd is None or self.scored > 0:
            return
        isBlocked = self.checkPaddleBlock(atEnd)
        if isBlocked:
            self.ball.flipXDirection()
        else:
            print("SCOREEEEEEE")
            self.ball.velocity = [0, 0]
            # self.ball.reset()
            self.scored = 4

    def checkPaddleBlock(self, paddleNum):
        yBall = self.ball.position[0]

        return (
            yBall >= self.paddles[paddleNum]
            and yBall < self.paddles[paddleNum] + PADDLE_LENGTH
        )

    def setPaddle(self, paddle, position):
        self.paddles[paddle] = setRange(position, 0, WIDTH - PADDLE_LENGTH)

    def getBoard(self):
        self.tick += 2
        if self.scored > 0:
            color = (0, 0, 0)
            toShow = np.copy(self.invBoard)
            self.scored -= 1
            if self.scored == 0:
                self.ball.reset()
        else:
            color = wheel(self.tick & 255)
            toShow = np.copy(self.board)
        for i in range(HEIGHT):
            if self.paddles[0] <= i and self.paddles[0] + PADDLE_LENGTH > i:
                # toShow[i][0] = PADDLE_COLOR
                toShow[i][0] = color
            if self.paddles[1] <= i and self.paddles[1] + PADDLE_LENGTH > i:
                # toShow[i][WIDTH - 1] = PADDLE_COLOR
                toShow[i][WIDTH - 1] = color
        x, y = self.ball.position
        # toShow[int(x)][int(y)] = BALL_COLOR
        toShow[int(x)][int(y)] = color
        return toShow

    # def plot(self):
    #     board = self.getBoard()
    #     cv2.imshow('Pong!', board)
    #     cv2.waitKey(5)


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    pong = Pong()
    for i in range(10):
        pong.step()
        if pong.scored:
            # pong.reset()
            break
        pong.plot()
