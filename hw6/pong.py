import numpy as np
import random
# from display import WIDTH, HEIGHT

def setRange(value, minimum, maximum):
    return min(max(value, minimum), maximum)

WIDTH = 20
HEIGHT = 15

PADDLE_COLOR = (0, 255, 0)
BALL_COLOR = (0, 0, 255)

PADDLE = 1
BALL = 2

PADDLE_LENGTH = 5

class Ball:
    def __init__(self):
        self.reset()

    def reset(self):
        self.position = (WIDTH/2, HEIGHT/2)
        self.velocity = (random.choice([-1, 1]), random.choice([-1, 0, 1]))

    def flipXDirection(self):
        self.velocity = (-self.velocity[0], self.velocity[1])

    def step(self):
        self.position = (self.position[0]+self.velocity[0], self.position[1]+self.velocity[1])
        if self.position[1] in [0, HEIGHT-1]:
            self.velocity = (self.velocity[0], -self.velocity[1])
        if self.position[0] == 0:
            return 0
        if self.position[1] == WIDTH-1:
            return 1
        return None

class Pong:
    def __init__(self):
        self.paddles = [0, 0]
        self.ball = Ball()
        self.generateBoard()

    def generateBoard(self):
        self.board = np.zeros((WIDTH, HEIGHT))
        self.board[0] = np.array([PADDLE if i >= self.paddles[0] and i < self.paddles[0]+PADDLE_LENGTH else 0 for i in range(HEIGHT)])
        self.board[WIDTH-1] = np.array([PADDLE if i >= self.paddles[1] and i < self.paddles[1]+PADDLE_LENGTH else 0 for i in range(HEIGHT)])

    def step(self):
        atEnd = self.ball.step()
        if atEnd is None:
            return
        isBlocked = self.checkPaddleBlock(atEnd)
        if isBlocked:
            self.ball.flipXDirection()
        else:
            print("SCOREEEEEEE")

    def checkPaddleBlock(self, paddleNum):
        ballPosition = self.ball.position[1]
        return ballPosition >= self.paddles[paddleNum] and ballPosition < self.paddles[paddleNum]

    def setPaddle(self, paddle, position):
        self.paddles[paddle] = setRange(position, 0, HEIGHT-PADDLE_LENGTH)

    def plot(self):
        toShow = np.copy(self.board)
        np.rot90(toShow)
        x, y = self.ball.position
        toShow[int(x)][int(y)] = BALL
        plt.imshow(toShow, interpolation="nearest")
        plt.show()


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    pong = Pong()
    for i in range(10):
        pong.step()
        pong.plot()


