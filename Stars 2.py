import pygame
from random import randint, choice

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 900
WINDOW_COLOR = 'black'
FPS = 60
MAX_STAR_SIZE = 3
MIN_STAR_SIZE = 1
STAR_SPEED = 3
STAR_CHANGE_SIZE_SPEED = 1
STAR_COLOR = 'white'
count_stars = randint(100, 200)

pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Stars')

stars = []
for _ in range(count_stars):
    x = randint(MAX_STAR_SIZE, WINDOW_WIDTH - MAX_STAR_SIZE)
    y = randint(MAX_STAR_SIZE, WINDOW_HEIGHT - MAX_STAR_SIZE)
    stars.append((x, y, randint(MIN_STAR_SIZE, MAX_STAR_SIZE), choice((1, -1)), randint(1, STAR_SPEED)))

while True:
    pygame.Clock().tick(FPS)
    window.fill(WINDOW_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    for i, star in enumerate(stars):
        pygame.draw.circle(window, STAR_COLOR, (star[0], star[1]), star[2])
        stars[i] = (*star[:4], star[4] + 1)

        if star[4] >= STAR_SPEED:
            if star[2] < MIN_STAR_SIZE or star[2] > MAX_STAR_SIZE:
                stars[i] = (*star[:3], star[3] * -1, 1)

            stars[i] = (*star[:2], star[2] + STAR_CHANGE_SIZE_SPEED * stars[i][3], stars[i][3], 1)

    pygame.display.update()
