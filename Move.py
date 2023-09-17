import pygame
from random import randint

pygame.init()
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 500
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Maze 2')
clock = pygame.time.Clock()

WINDOW_COLOR = (0, 0, 0)
PLAYER_COLOR = (255, 0, 0)
WALL_COLOR = (0, 255, 0)

WALL_WIDTH = 10
GAP = 150
door_gap = 40
MIN_DOORS_IN_LINE = 2
MAX_DOORS_IN_LINE = 5

RADIUS = 10
FPS = 60
SPEED_X = 2
SPEED_Y = 10


def create_line(game_lines, y):
    num_openings = randint(MIN_DOORS_IN_LINE, MAX_DOORS_IN_LINE)
    door_width = randint(RADIUS * 5, RADIUS * 8)
    opening_positions = [0] + sorted(
        [randint(door_width, WINDOW_HEIGHT - door_width) for _ in range(num_openings - 1)]) + [WINDOW_WIDTH]
    for j in range(num_openings):
        game_lines.append(pygame.Rect(y, opening_positions[j], WALL_WIDTH,
                                      opening_positions[j + 1] - opening_positions[j] - door_width))


def new_game():
    global player_x, player_y, lines, time
    time = 0
    player_x = RADIUS * 3
    player_y = WINDOW_HEIGHT // 2
    lines = []
    for i in range(GAP + GAP // 2, WINDOW_WIDTH, GAP):
        create_line(lines, i)


new_game()

while True:
    time += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    window.fill(WINDOW_COLOR)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player_y > RADIUS:
        player_y -= SPEED_Y
    if keys[pygame.K_s] and player_y < WINDOW_HEIGHT - RADIUS:
        player_y += SPEED_Y

    player_rect = pygame.Rect(player_x, player_y, 1, 1)
    for line in lines:
        if line.colliderect(player_rect):
            new_game()

        line.x -= SPEED_X
        pygame.draw.rect(window, WALL_COLOR, pygame.Rect(line.x, line.y + (line.height if line.height < 0 else 0),
                                                         line.width, abs(line.height)))

    if time >= GAP // SPEED_X:
        create_line(lines, lines[-1].x + GAP)

        if time >= GAP // SPEED_X + 50:
            time = 0
            x = lines[0].x
            for line in list(lines):
                if line.x != x:
                    break
                lines.remove(line)

    pygame.draw.circle(window, PLAYER_COLOR, (player_x, player_y), RADIUS)
    pygame.display.update()
    clock.tick(FPS)
