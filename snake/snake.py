import pygame
import sys
import random

class Snake():
    def __init__(self):
        self.length = 1
        self.positions = [((screenWidth/2), (screenHeight/2))]
        self.direction = random.choice([up, down, left, right])
        self.color = (17, 24, 47)
        self.score = 0

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0]*-1, point[1]*-1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        curr = self.get_head_position()
        x, y = self.direction
        new = (((curr[0]+(x*gridSize))%screenWidth), (curr[1]+(y*gridSize)%screenHeight))
        if len(self.positions) > 2 and new in self.positions[2:]:
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

    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (gridSize, gridSize))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, (93, 216, 228), r, 1)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(up)
                elif event.key == pygame.K_DOWN:
                    self.turn(down)
                elif event.key == pygame.K_LEFT:
                    self.turn(left)
                elif event.key == pygame.K_RIGHT:
                    self.turn(right)

class Food():
    def __init__(self):
        self.position = (0, 0)
        self.color = (223, 163, 49)
        self.randomisePosition()

    def randomisePosition(self):
        self.position = (random.randint(0, gridWidth - 1) * gridSize, random.randint(0, gridHeight - 1) * gridSize)

    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (gridSize, gridSize))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, (93, 216, 228), r, 1)

def drawGrid(surface):
    for y in range(int(gridHeight)):
        for x in range(int(gridWidth)):
            if (x+y)%2 == 0:
                r = pygame.Rect((x*gridSize, y*gridSize), (gridSize, gridSize))
                pygame.draw.rect(surface, (93, 216, 228), r)
            else:
                rr = pygame.Rect((x*gridSize, y*gridSize), (gridSize, gridSize))
                pygame.draw.rect(surface, (84, 194, 205), rr)

screenWidth = 480
screenHeight = 480
gridSize = 20
gridWidth = screenWidth/gridSize
gridHeight = screenHeight/gridSize
up = (0, -1)
down = (0, 1)
left = (-1, 0)
right = (1, 0)

def main():
    pygame.init()
    clock = pygame.time.Clock() # show game time/clock
    screen = pygame.display.set_mode((screenWidth, screenHeight), 0, 32)

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()

    scoreFont = pygame.font.SysFont("monospace", 16)

    drawGrid(surface)

    snake = Snake()
    food = Food()

    while True:
        clock.tick(10)
        snake.handle_keys()
        drawGrid(surface)
        snake.move()
        if snake.get_head_position() == food.position:
            snake.length += 1
            snake.score += 1
            food.randomisePosition()
        snake.draw(surface)
        food.draw(surface)
        screen.blit(surface, (0, 0))
        text = scoreFont.render("Score {0}".format(snake.score), 1, (0, 0, 0))
        screen.blit(text, (5, 10))
        pygame.display.update()
if __name__ == "__main__":
    main()

