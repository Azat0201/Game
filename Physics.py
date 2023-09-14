import pygame
import math

pygame.init()
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 480
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Dramatic crash")

circle_pos = [WINDOW_WIDTH / 2, 50]
RADIUS = 20

RECT_POS = [WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50]
RECT_WIDTH = 100
RECT_HEIGHT = 50

WINDOW_COLOR = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)

SPEED = 5
FPS = 60

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    circle_pos[1] += SPEED

    circle_x = circle_pos[0]
    circle_y = circle_pos[1]
    rect_x = RECT_POS[0]
    rect_y = RECT_POS[1]
    distance_x = abs(circle_x - rect_x)
    distance_y = abs(circle_y - rect_y)
    if distance_x <= (RECT_WIDTH / 2 + RADIUS) and distance_y <= (RECT_HEIGHT / 2 + RADIUS):
        RECT_COLOR = red
        CIRCLE_COLOR = green
    else:
        RECT_COLOR = green
        CIRCLE_COLOR = black

    window.fill(WINDOW_COLOR)
    pygame.draw.circle(window, RECT_COLOR, circle_pos, RADIUS)
    pygame.draw.rect(window, CIRCLE_COLOR, (RECT_POS[0] - RECT_WIDTH / 2, RECT_POS[1] - RECT_HEIGHT / 2,
                                            RECT_WIDTH, RECT_HEIGHT))

    pygame.display.update()

    if circle_pos[1] + RADIUS >= RECT_POS[1] - RECT_HEIGHT / 2:
        SPEED = 0

    pygame.time.Clock().tick(FPS)
