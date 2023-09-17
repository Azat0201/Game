import pygame
from random import randint

pygame.init()
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 1000
WINDOW_COLOR = 'black'
FPS = 60
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Rain')

WATER_SPEED = 1
RAIN_WIDTH = 2
RAIN_HEIGHT = 7
RAIN_COLOR = '#11438B'
MIN_RAIN_SPEED = 3
MAX_RAINS_SPEED = 10
DROPS_IN_WATER = 50

drops = -WINDOW_HEIGHT // 8
water_y = 0
rain = []

while True:
    pygame.time.Clock().tick(FPS)
    window.fill(WINDOW_COLOR)

    if water_y == WINDOW_HEIGHT:
        drops = -WINDOW_HEIGHT // 4
        water_y = 0
        rain = []

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    rain.append((pygame.Rect(randint(0, WINDOW_WIDTH), 0, RAIN_WIDTH, RAIN_HEIGHT),
                 randint(MIN_RAIN_SPEED, MAX_RAINS_SPEED)))
    drops += 1

    for drop in list(rain):
        if drop[0].y >= WINDOW_HEIGHT:
            rain.remove(drop)
        pygame.draw.rect(window, RAIN_COLOR, drop[0])
        drop[0].y += drop[1]
    
    if drops >= DROPS_IN_WATER:
        drops = 0
        water_y += WATER_SPEED

    pygame.draw.rect(window, RAIN_COLOR, (0, WINDOW_HEIGHT - water_y, WINDOW_WIDTH, water_y))

    pygame.display.update()
