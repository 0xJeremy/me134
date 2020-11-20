import numpy as np
import random

HEIGHT = 15
WIDTH = 20

HEAD_COLOR = (255, 255, 255)
TAIL_COLOR = (255, 255, 255)
FOOD_COLOR = (0, 255, 0)


class Snake:
    def __init__(self):
        self.board = np.full((HEIGHT, WIDTH, 3), (0, 0, 0))
        self.reset()

    def reset(self):
        self.head = (int(HEIGHT / 2), int(WIDTH / 2))
        self.velocity = [0, 0]
        self.tail = []
        self.lost = False
        self.generateFood()

    def generateFood(self):
        while True:
            self.food = [random.randint(0, HEIGHT - 1), random.randint(0, WIDTH - 1)]
            if self.food not in self.tail:
                return

    def setVelocity(self, x=0, y=0):
        self.velocity = [x, y]

    def step(self):
        self.tail.append(self.head)
        self.head = (self.head[0] + self.velocity[0], self.head[1] + self.velocity[1])
        if self.head[0] == HEIGHT:
            self.lost = True
            self.head = (self.head[0] - 1, self.head[1])
        elif self.head[0] == -1:
            self.lost = True
            self.head = (self.head[0] + 1, self.head[1])
        if self.head[1] == -1:
            self.lost = True
            self.head = (self.head[0], self.head[1] + 1)
        if self.head[1] == WIDTH:
            self.lost = True
            self.head = (self.head[0], self.head[1] - 1)
        if self.head[0] == self.food[0] and self.head[1] == self.food[1]:
            self.generateFood()
        else:
            self.tail.pop(0)
        for position in self.tail:
            if self.head[0] == position[0] and self.head[1] == position[1]:
                self.lost = True

    def generateBoard(self):
        if self.lost:
            return np.full((HEIGHT, WIDTH, 3), (0, 255, 0), "uint8")
        toShow = np.copy(self.board)
        for position in self.tail:
            toShow[position[0]][position[1]] = TAIL_COLOR
        toShow[self.head[0]][self.head[1]] = HEAD_COLOR
        toShow[self.food[0]][self.food[1]] = FOOD_COLOR
        return toShow.astype("uint8")


if __name__ == "__main__":
    import cv2
    import time

    snake = Snake()
    while True:
        board = snake.generateBoard()
        # board = cv2.resize(board, (300, 400))
        cv2.imshow("Snake", board)
        key = cv2.waitKey(200) & 0xFF
        if key == ord("q"):
            break
        elif key == ord("w"):
            snake.setVelocity(x=-1, y=0)
        elif key == ord("a"):
            snake.setVelocity(x=0, y=-1)
        elif key == ord("s"):
            snake.setVelocity(x=1, y=0)
        elif key == ord("d"):
            snake.setVelocity(x=0, y=1)
        snake.step()
