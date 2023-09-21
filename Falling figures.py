import pygame
from random import randrange, choice

pygame.init()
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
SIZE_FIGURE = (WINDOW_WIDTH + WINDOW_HEIGHT) // 20
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


class Triangle:
    height = (SIZE_FIGURE * 3 ** 0.5) / 2
    points = ((0, 0), (-SIZE_FIGURE / 2, height), (SIZE_FIGURE / 2, height))

    def __init__(self, color_figure):
        self.x = randrange(SIZE_FIGURE // 2, WINDOW_WIDTH - SIZE_FIGURE // 2)
        self.y = -self.__class__.height
        self.color = color_figure

    def draw(self):
        pygame.draw.polygon(window, self.color, tuple(map(lambda pos: (pos[0] + self.x, pos[1] + self.y),
                                                          list(self.__class__.points))))


class Square:
    def __init__(self, color_figure):
        self.x = randrange(WINDOW_WIDTH - SIZE_FIGURE)
        self.y = -SIZE_FIGURE
        self.color = color_figure

    def draw(self):
        pygame.draw.rect(window, self.color, (self.x, self.y, SIZE_FIGURE, SIZE_FIGURE))


class Circle:
    def __init__(self, color_figure):
        self.x = randrange(SIZE_FIGURE // 2, WINDOW_WIDTH - SIZE_FIGURE // 2)
        self.y = -SIZE_FIGURE / 2
        self.color = color_figure

    def draw(self):
        pygame.draw.circle(window, self.color, (self.x, self.y), SIZE_FIGURE / 2)


BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
COLORS = (RED, GREEN, BLUE, YELLOW, WHITE)
FIGURES = (Triangle, Square, Circle)

WINDOW_COLOR = BLACK
WIDTH = 60
FPS = 60
SPEED = WINDOW_HEIGHT // 100
color = choice(COLORS)
current_figure = choice(FIGURES)(color)

FONT = pygame.font.SysFont('Verdana', 15)

count_triangles = (0, Triangle, 'Треугольников')
count_squares = (0, Square, 'Квадратов')
count_circles = (0, Circle, 'Кругов')
counts = [count_triangles, count_squares, count_circles]


while True:
    window.fill(WINDOW_COLOR)
    for i, count in enumerate(counts):
        text = FONT.render(f'Счётчик {count[2]}: {count[0]}', True, WHITE)
        window.blit(text, (10, 10 + 20 * i))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    current_figure.draw()
    current_figure.y += SPEED
    if current_figure.y >= WINDOW_HEIGHT + SIZE_FIGURE:
        for i, count in enumerate(counts):
            counts[i] = (count[0] + (1 if isinstance(current_figure, count[1]) else 0), *count[1:])
        color = choice(COLORS)
        current_figure = choice(FIGURES)(color)

    pygame.time.Clock().tick(FPS)
    pygame.display.update()
