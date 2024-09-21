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

    def turn(self, point):
        if self.length > 1 and (point[0]*-1, point[1]*-1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        curr = self.get_head_position()
        x, y = self.direction
        new = (((curr[0]+(x*gridSize))%screenWidth), (curr[1]+(y*gridSize)%screenHeight))
        if len(self.position) > 2 and new in self.positions[2:]:
            self.reset() # if new is already in self.position it means its hit its tail/somepart of itself
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop() # removing the end of the tail so snake size remains the same

    def reset(self):
        self.length = 1
        self.positions = [((screenWidth/2), (screenHeight/2))]
        self.direction = random.choice([up, down, left, right])
        self.score = 0
    
    # def handle_keys(self):
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             pygame.quit()
    #             sys.exit()
    #         elif event.type == pygame.KEYDOWN:

# class Food():
#     def __init__(self):
#         self.position = (0, 0)
#         self.color = (223, 163, 49)
#         self.randomisePosition()

#     def randomisePosition(self):

    # def draw(self, surface):

def drawGrid(surface):
    for y in range(int(gridHeight)):
        for x in range(int(gridWidth)):
            if (x+y)%2 == 0:
                r = pygame.Rect((x*gridSize, y*gridSize), (gridSize, gridSize))
                pygame.draw.rect(surface, (93, 216, 228), r)
            else:
                rr = pygame.Rect((x*gridSize, y*gridSize), (gridSize, gridSize))
                pygame.draw.rect(surface, (93, 216, 228), rr)

def main():
    pygame.init()
    clock = pygame.time.Clock() # show game time/clock
    screen = pygame.display.set_mode((screenWidth, screenHeight), 0, 32)

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()

    font = pygame.font.SysFont("monospace", 16)

    snake = Snake()

    while True:
        clock.tick(10)



if __name__ == "__main__":
    main()