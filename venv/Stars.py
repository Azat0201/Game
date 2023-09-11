import pygame
from random import randint

pygame.init()

WIDTH = 640
HEIGHT = 480
WINDOW_COLOR = (0, 0, 0)
TEXT_COLOR = (255, 255, 255)
STAR_COLOR = (255, 192, 203)
SPEED = 0
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Звезды падают вниз")

FONT = pygame.font.SysFont("Verdana", 15)

star_list = []
for i in range(50):
    x = randint(0, WIDTH)
    y = randint(-200, -50)
    speed = randint(1, 5) + SPEED
    size = randint(1, 4)
    star_list.append([x, y, speed, size])
score = 0

freeze = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            freeze = not freeze
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                freeze = not freeze

    window.fill(WINDOW_COLOR)

    if not freeze:
        for star in star_list:
            star[1] += star[2]
            if star[1] > HEIGHT:
                star[0] = randint(0, WIDTH)
                star[1] = randint(-200, -50)
                score += 1
            pygame.draw.circle(window, STAR_COLOR, (star[0], star[1]), star[3])

    score_text = FONT.render("Упало звезд: " + str(score), True, TEXT_COLOR)
    window.blit(score_text, (10, 10))

    pygame.display.update()

    # устанавливаем частоту обновления экрана
    pygame.time.Clock().tick(60)
