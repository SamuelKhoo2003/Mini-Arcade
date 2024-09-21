import pygame
import sys

pygame.init()
window = pygame.display.set_mode((300, 300))
clock = pygame.time.Clock()

rect = pygame.Rect(0, 0, 20, 20)
rect.center = window.get_rect().center
speed = 5

run = True
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            print(pygame.key.name(event.key))

    keys = pygame.key.get_pressed()
    rect.x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * speed
    rect.y += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * speed

    rect.centerx %= window.get_width()
    rect.centery %= window.get_height()

    window.fill(0)
    pygame.draw.rect(window, (255, 0, 0), rect)
    # we flip because everything is animated on the last buffer, so show the new latest updated state
    pygame.display.flip()

pygame.quit()
sys.exit()