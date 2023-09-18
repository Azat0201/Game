import pygame
from math import ceil
from random import shuffle, choices


WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 900
FPS = 60
WINDOW_COLOR = 'black'

pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Memory game')

COUNT_COUPLES = 6
COUNT_ROWS = ceil(COUNT_COUPLES / (WINDOW_WIDTH // 250))
COUNT_CIRCLES_IN_ROW = COUNT_COUPLES * 2 // COUNT_ROWS
RADIUS = WINDOW_WIDTH // (COUNT_CIRCLES_IN_ROW * 3)
STRIP = 10 + RADIUS
GAP = (WINDOW_WIDTH - STRIP * 2) // (COUNT_CIRCLES_IN_ROW - 1)
POSITIONS_X = tuple(STRIP + GAP * i for i in range(COUNT_CIRCLES_IN_ROW))
POSITIONS_Y = tuple(GAP * i + STRIP for i in range(COUNT_ROWS))

TIME = 3
FONT = pygame.font.SysFont('Verdana', 20)
TEXT_COLOR = 'white'

while True:
    colors = ['#' + ''.join(choices('1234567890ABCDEF', k=6)) for _ in range(COUNT_COUPLES)] * 2
    shuffle(colors)
    color_circles = tuple(color for color in colors)
    game = True
    prev_couple = None
    score = 0

    circles_pos = []
    for x in POSITIONS_X:
        for y in POSITIONS_Y:
            circles_pos.append((x, y))

    while True:
        pygame.time.Clock().tick(FPS)
        window.fill(WINDOW_COLOR)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, circle in enumerate(circles_pos):
                    if pygame.rect.Rect(circle[0] - RADIUS, circle[1] - RADIUS,
                                        RADIUS * 2, RADIUS * 2).collidepoint(event.pos):
                        current_color = color_circles[i]
                        colors[i] = current_color
                        if prev_couple is None:
                            prev_couple = current_color
                        else:
                            if prev_couple == current_color:
                                score += 1
                            prev_couple = None

        for color, circle in zip(colors, circles_pos):
            pygame.draw.circle(window, color, circle, RADIUS)

        text = FONT.render(f'Счёт: {score}', True, TEXT_COLOR)
        window.blit(text, (10, WINDOW_HEIGHT - text.get_height() - 10))

        pygame.Clock().tick(FPS)
        pygame.display.update()

        if colors.count('gray') == 0:
            if game:
                pygame.time.wait(TIME * 1000)
                colors = ['gray'] * (COUNT_COUPLES * 2)
                game = False
            else:
                pygame.time.wait(TIME * 500)
                break
