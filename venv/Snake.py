import pygame
from random import randint
from time import time


with open('Settings for snake', encoding='utf8') as file:
    file.readline()
    data = [int(file.readline().split()[0].strip()) for _ in range(7)]
    file.readline()
    file.readline()
    colors = [file.readline().split()[0].strip() for _ in range(5)]

colors = [tuple(map(int, color[1:-1].split(','))) if color.startswith('(') else color for color in colors]

SPEED, SPEED_FOOD, WINDOW_WIDTH, WINDOW_HEIGHT, DECREASE_SPEED_FOOD, CAN_CRASH_WALL, CAN_CRASH_SELF = data

WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
FPS = 60
RADIUS = (WINDOW_WIDTH + WINDOW_HEIGHT) // 100
RADIUS_FOOD = RADIUS // 2

window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('Snake')
pygame.init()

FONT = pygame.font.SysFont("Verdana", 15)

def init_new_game():
    global direction, foods, iter_food, iter_snake, snake
    direction = (1, 0)
    foods = [(-100, -100)]
    iter_food = 0
    iter_snake = 0
    snake = [(WINDOW_WIDTH // 2 - RADIUS * 2 * i, WINDOW_HEIGHT // 2) for i in range(5, 0, -1)]

def create_food():
    pos = foods[0]
    timeout = time() + 2
    while pos in foods:
        if time() > timeout:
            break
        pos = (randint(RADIUS, WINDOW_WIDTH - RADIUS), randint(RADIUS, WINDOW_HEIGHT - RADIUS))
        pos = (pos[0] - pos[0] % (RADIUS * 2) + RADIUS, pos[1] - pos[1] % (RADIUS * 2) + RADIUS)
    else:
        foods.append(pos)

init_new_game()
Start_ii = False

while True:
    iter_food += 1
    iter_snake += 1

    TIME_DELTA = pygame.time.Clock().tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and direction[1] != 1:
                direction = (0, -1)
            elif event.key == pygame.K_a and direction[0] != 1:
                direction = (-1, 0)
            elif event.key == pygame.K_s and direction[1] != -1:
                direction = (0, 1)
            elif event.key == pygame.K_d and direction[0] != -1:
                direction = (1, 0)

    window.fill(pygame.Color(colors[0]))
    for pos in snake:
        if not (0 <= pos[0] <= WINDOW_WIDTH and 0 <= pos[1] <= WINDOW_HEIGHT):
            if not CAN_CRASH_WALL:
                init_new_game()
                continue
            if not (0 <= pos[0] <= WINDOW_WIDTH):
                pos = (abs(pos[0] - WINDOW_WIDTH), pos[1])
            if not (0 <= pos[1] <= WINDOW_WIDTH):
                pos[1] = (pos[0], abs(pos[1] - WINDOW_WIDTH))
        pygame.draw.circle(window, colors[1], (pos[0], pos[1]), RADIUS)
        if pos == snake[-1]:
            pygame.draw.circle(window, colors[2], (pos[0], pos[1]), RADIUS_FOOD)

    for food in foods:
        pygame.draw.circle(window, colors[3], (food[0], food[1]), RADIUS_FOOD)
        if abs(food[0] - snake[-1][0]) < RADIUS * 2 and abs(food[1] - snake[-1][1]) < RADIUS * 2:
            foods.remove(food)
            snake.insert(0, (snake[0][0] - (snake[1][0] - snake[0][0]), snake[0][1] - (snake[1][1] - snake[0][1])))

    if iter_food >= SPEED_FOOD + (2 if DECREASE_SPEED_FOOD else 0) ** (len(foods)):
        iter_food = 0
        create_food()

    if iter_snake % SPEED == 0:
        del snake[0]
        snake.append((snake[-1][0] + RADIUS * 2 * direction[0], snake[-1][1] + RADIUS * 2 * direction[1]))

    if not CAN_CRASH_SELF and len(set(snake)) != len(snake):
        init_new_game()
        continue

    score_text = FONT.render("Очки: " + str(len(snake) - 5), True, colors[4])
    window.blit(score_text, (10, 10))

    pygame.display.update()
