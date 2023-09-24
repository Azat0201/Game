import pygame
from random import randint, random

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 900
FPS = 60
WINDOW_COLOR = 'black'
TEXT_COLOR = 'white'

pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Game')
FONT = pygame.font.SysFont('Verdana', 20)
RADIUS = 15
SIZE_SQUARE = RADIUS * 2 ** 0.5
HALF_SIZE_TRIANGLE = (RADIUS * 3 ** 0.5) / 2
POINTS = ((0, -RADIUS), (HALF_SIZE_TRIANGLE, RADIUS / 2), (-HALF_SIZE_TRIANGLE, RADIUS / 2))
BOMB_COLOR = 'red'
PRIZE_COLOR = 'blue'
PLAYER_COLOR = 'green'
SPEED = 5
SPEED_PLAYER = 4


def new_loop():
    bombs = []
    prizes = []
    count = 0
    player_pos = [WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3 * 2]
    while True:
        pygame.time.Clock().tick(FPS)
        window.fill(WINDOW_COLOR)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and RADIUS <= player_pos[0]:
            player_pos[0] -= SPEED_PLAYER
        if keys[pygame.K_d] and player_pos[0] <= WINDOW_WIDTH - RADIUS:
            player_pos[0] += SPEED_PLAYER
        if keys[pygame.K_w] and RADIUS <= player_pos[1]:
            player_pos[1] -= SPEED_PLAYER * 3 / 4
        if keys[pygame.K_s] and player_pos[1] <= WINDOW_HEIGHT - RADIUS:
            player_pos[1] += SPEED_PLAYER * 4 / 3
        player_rect = pygame.rect.Rect(player_pos[0] - SIZE_SQUARE / 2, player_pos[1] - SIZE_SQUARE / 2, SIZE_SQUARE,
                                       SIZE_SQUARE)

        if random() < 0.17:
            if random() >= 0.3:
                bombs.append([randint(RADIUS, WINDOW_WIDTH - RADIUS), 0])
            else:
                prizes.append([randint(RADIUS, WINDOW_WIDTH - RADIUS), 0])

        for pos in bombs:
            pygame.draw.circle(window, BOMB_COLOR, pos, RADIUS)
            pos[1] += SPEED
            rect = pygame.rect.Rect(pos[0] - SIZE_SQUARE / 2, pos[1] - SIZE_SQUARE / 2, SIZE_SQUARE, SIZE_SQUARE)
            if rect.colliderect(player_rect):
                new_loop()
            elif not (0 <= pos[1] <= WINDOW_HEIGHT):
                bombs.remove(pos)

        for pos in prizes:
            points = list(map(lambda x: (x[0] + pos[0], x[1] + pos[1]), POINTS))
            pygame.draw.polygon(window, PRIZE_COLOR, points)
            pos[1] += SPEED
            rect = pygame.rect.Rect(pos[0] - SIZE_SQUARE / 2, pos[1] - SIZE_SQUARE / 2, SIZE_SQUARE, SIZE_SQUARE)
            if rect.colliderect(player_rect):
                count += 1
                prizes.remove(pos)
            elif not (0 <= pos[1] <= WINDOW_HEIGHT):
                prizes.remove(pos)

        pygame.draw.circle(window, PLAYER_COLOR, player_pos, RADIUS)
        text = FONT.render(f'Счёт: {count}', True, TEXT_COLOR)
        window.blit(text, (10, 10))

        pygame.display.update()


new_loop()
