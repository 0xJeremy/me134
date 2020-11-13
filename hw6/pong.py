import numpy as np
import random
# import cv2

# from display import HEIGHT, WIDTH


def setRange(value, minimum, maximum):
    return min(max(value, minimum), maximum)


HEIGHT = 15
WIDTH = 20

PADDLE_COLOR = (0, 255, 0)
BALL_COLOR = (0, 0, 255)

PADDLE = 1
BALL = 2

PADDLE_LENGTH = 5


class Ball:
    def __init__(self):
        self.reset()

    def reset(self):
        self.position = (int(HEIGHT / 2), int(WIDTH / 2))
        self.velocity = (random.choice([-1, 0, 1]), random.choice([-1, 1]))

    def flipXDirection(self):
        self.velocity = (self.velocity[0], -self.velocity[1])

    def step(self):
        self.position = (
            self.position[0] + self.velocity[0],
            self.position[1] + self.velocity[1],
        )
        if self.position[0] in [0, HEIGHT - 1]:
            self.velocity = (-self.velocity[0], self.velocity[1])
        if self.position[1] == 1:
            return 0
        if self.position[1] == WIDTH - 2:
            return 1
        return None


class Pong:
    def __init__(self):
        self.reset()

    def reset(self):
        self.paddles = [0, 0]
        self.ball = Ball()
        self.generateBoard()
        self.scored = False

    def generateBoard(self):
        self.board = np.full((HEIGHT, WIDTH, 3), (0, 0, 0))
        # for i in range(HEIGHT):
        #     if self.paddles[0] <= i and self.paddles[0] + PADDLE_LENGTH > i:
        #         self.board[i][0] = PADDLE
        #     if self.paddles[1] <= i and self.paddles[1] + PADDLE_LENGTH > i:
        #         self.board[i][WIDTH - 1] = PADDLE

    def step(self):
        atEnd = self.ball.step()
        if atEnd is None:
            return
        isBlocked = self.checkPaddleBlock(atEnd)
        if isBlocked:
            self.ball.flipXDirection()
        else:
            print("SCOREEEEEEE")
            self.scored = True

    def checkPaddleBlock(self, paddleNum):
        yBall = self.ball.position[0]

        return (
            yBall >= self.paddles[paddleNum]
            and yBall < self.paddles[paddleNum] + PADDLE_LENGTH
        )

    def setPaddle(self, paddle, position):
        self.paddles[paddle] = setRange(position, 0, WIDTH - PADDLE_LENGTH)

    def getBoard(self):
        toShow = np.copy(self.board)
        for i in range(HEIGHT):
            if self.paddles[0] <= i and self.paddles[0] + PADDLE_LENGTH > i:
                toShow[i][0] = PADDLE_COLOR
            if self.paddles[1] <= i and self.paddles[1] + PADDLE_LENGTH > i:
                toShow[i][WIDTH - 1] = PADDLE_COLOR
        x, y = self.ball.position
        toShow[int(x)][int(y)] = BALL_COLOR
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
