import pygame
import sys
import random

screenWidth = 400
screenHeight = 400
gridSize = 20
gridWidth = screenWidth/gridSize
gridHeight = screenHeight/gridSize
up, down = (0, -1), (0, 1)
left, right = (-1, 0), (1, 0)

class Snake():
    def __init__(self):
        self.length = 1
        self.positions = [((screenWidth/2), (screenHeight/2))]
        self.direction = random.choice([up, down, left, right])
        self.color = (17, 24, 47)
        self.score = 0

    def get_head_position(self):
        return self.position[0]

class Food():
    def __init__(self):
        self.position = (0, 0)
        self.color = (223, 163, 49)
        self.randomisePosition()

    def randomisePosition(self):

    def draw(self, surface):

def drawGrid(surface):
    for y in range(int(gridHeight)):
        for x in range(int(gridWidth)):
            if (x+y)%2 == 0:
            else:
