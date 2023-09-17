import pygame
import os
import ctypes
from random import randint
from time import time


def create_food():
    global foods
    position = foods[0]
    timeout = time() + 1
    while position in foods:
        if time() > timeout:
            break
        position = (randint(RADIUS, WINDOW_WIDTH - RADIUS), randint(RADIUS, WINDOW_HEIGHT - RADIUS))
        position = (position[0] - position[0] % (RADIUS * 2) + RADIUS,
                    position[1] - position[1] % (RADIUS * 2) + RADIUS)
    else:
        foods.append(position)


def new_loop():
    global SPEED, SPEED_FOOD, WINDOW_WIDTH, WINDOW_HEIGHT, DECREASE_SPEED_FOOD, CAN_CRASH_WALL, CAN_CRASH_SELF
    global WINDOW_COLOR, SNAKE_COLOR, EYE_COLOR, FOOD_COLOR, BUTTON_COLOR, \
        SCORE_TEXT_COLOR, GAME_OVER_TEXT_COLOR, BUTTON_TEXT_COLOR
    global FPS, RADIUS, RADIUS_FOOD, BUTTON_WIDTH, BUTTON_HEIGHT, Button, best_score

    with open(r'Settings for snake', encoding='utf8') as file:
        best_score = int(file.readline().split()[0].strip())
        file.readline()
        file.readline()
        data = [int(file.readline().split()[0].strip()) for _ in range(7)]
        file.readline()
        file.readline()
        colors = [file.readline().split()[0].strip() for _ in range(8)]

    SPEED, SPEED_FOOD, WINDOW_WIDTH, WINDOW_HEIGHT, DECREASE_SPEED_FOOD, CAN_CRASH_WALL, CAN_CRASH_SELF = data
    WINDOW_COLOR, SNAKE_COLOR, EYE_COLOR, FOOD_COLOR, BUTTON_COLOR, \
     SCORE_TEXT_COLOR, GAME_OVER_TEXT_COLOR, BUTTON_TEXT_COLOR = colors
    WINDOW_WIDTH -= WINDOW_WIDTH % 30
    WINDOW_HEIGHT -= WINDOW_HEIGHT % 30

    user32 = ctypes.windll.user32
    MONITOR_WIDTH, MONITOR_HEIGHT = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    FPS = 60
    WINDOW_X = MONITOR_WIDTH // 2 - WINDOW_WIDTH // 2
    WINDOW_Y = MONITOR_HEIGHT // 2 - WINDOW_HEIGHT // 2
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (WINDOW_X, WINDOW_Y)

    FPS = 60
    RADIUS = (WINDOW_WIDTH + WINDOW_HEIGHT) // 100
    RADIUS_FOOD = RADIUS // 2
    BUTTON_WIDTH = WINDOW_WIDTH // 5
    BUTTON_HEIGHT = WINDOW_HEIGHT // 10

    class Button:
        def __init__(self, x, y, function, title="", font=None, width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                     button_color=BUTTON_COLOR, button_text_color=BUTTON_TEXT_COLOR):
            self.font = font
            self.function = function
            self.button_color = button_color
            self.width = width
            self.heigth = height
            self.rect = pygame.Rect(x - width // 2, y - height // 2, width, height)
            self.text = self.font.render(title, True, button_text_color)

        def get_rect_center(self):
            return self.text.get_rect(center=self.rect.center)

    init_new_game()


def init_new_game():
    pygame.display.set_caption('Snake')
    pygame.init()
    snake_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    FONT = pygame.font.SysFont('Verdana', 20)

    from Menu_snake import new_loop as exit_menu
    button_restart = Button(WINDOW_WIDTH // 2 - WINDOW_WIDTH // 4, WINDOW_HEIGHT // 2, init_new_game, 'Заново', FONT)
    button_menu = Button(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, exit_menu, 'Меню', FONT)
    button_exit = Button(WINDOW_WIDTH // 2 + WINDOW_WIDTH // 4, WINDOW_HEIGHT // 2, quit, 'Выйти', FONT)
    buttons = (button_restart, button_menu, button_exit)

    global foods, game_over
    foods = [(-100, -100)]
    direction = (1, 0)
    iter_food = 0
    iter_snake = 0
    game_over = False
    snake = [(WINDOW_WIDTH // 2 - RADIUS * 2 * i, WINDOW_HEIGHT // 2) for i in range(5, 0, -1)]


    def init_game_over():
        global game_over, game_over_text, best_score
        score = len(snake) - 5
        if score <= best_score:
            game_over_text = FONT.render(f'Игра закончена! Счёт: {len(snake) - 5}\nРекорд: {best_score}', True, GAME_OVER_TEXT_COLOR)
        else:
            game_over_text = FONT.render(f'Игра закончена! Счёт: {len(snake) - 5}\nПредыдущий рекорд: {best_score}', True,
                                         GAME_OVER_TEXT_COLOR)
            with open('Settings for snake') as file:
                lines = file.readlines()
                best_score_line = lines[0].split()
                best_score_line[0] = str(score)
                lines[0] = ' '.join(best_score_line) + '\n'
            with open('Settings for snake', 'w') as file:
                file.writelines(lines)
            best_score = score
        game_over = True


    while True:
        clock.tick(FPS)
        snake_window.fill(WINDOW_COLOR)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        if not game_over:
            iter_food += 1
            iter_snake += 1

            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w and direction[1] != 1:
                        direction = (0, -1)
                    elif event.key == pygame.K_a and direction[0] != 1:
                        direction = (-1, 0)
                    elif event.key == pygame.K_s and direction[1] != -1:
                        direction = (0, 1)
                    elif event.key == pygame.K_d and direction[0] != -1:
                        direction = (1, 0)
                    elif event.key == pygame.K_q:
                        init_game_over()
                        continue

            for food in foods:
                pygame.draw.circle(snake_window, FOOD_COLOR, (food[0], food[1]), RADIUS_FOOD)
                if abs(food[0] - snake[-1][0]) < RADIUS * 2 and abs(food[1] - snake[-1][1]) < RADIUS * 2:
                    foods.remove(food)
                    snake.insert(0, (snake[0][0] - (snake[1][0] - snake[0][0]),
                                     snake[0][1] - (snake[1][1] - snake[0][1])))

            for i, pos in enumerate(snake):
                pygame.draw.circle(snake_window, SNAKE_COLOR, (pos[0], pos[1]), RADIUS)

            if not CAN_CRASH_SELF and snake[-1] in snake[:-1]:
                init_game_over()
                continue

            pygame.draw.circle(snake_window, EYE_COLOR, (snake[-1][0], snake[-1][1]), RADIUS_FOOD)

            if not (0 <= snake[-1][0] <= WINDOW_WIDTH and 0 <= snake[-1][1] <= WINDOW_HEIGHT):
                if not CAN_CRASH_WALL:
                    init_game_over()
                    continue
                if not (0 <= snake[-1][0] <= WINDOW_WIDTH):
                    change = WINDOW_WIDTH - RADIUS if snake[-1][0] < 0 else RADIUS
                    snake[-1] = (change, snake[-1][1])
                if not (0 <= snake[-1][1] <= WINDOW_WIDTH):
                    change = WINDOW_HEIGHT - RADIUS if snake[-1][1] < 0 else RADIUS
                    snake[-1] = (snake[-1][0], change)

            if iter_food >= SPEED_FOOD + (DECREASE_SPEED_FOOD * 2) ** (len(foods)):
                iter_food = 0
                create_food()

            if iter_snake % SPEED == 0:
                del snake[0]
                snake.append((snake[-1][0] + RADIUS * 2 * direction[0], snake[-1][1] + RADIUS * 2 * direction[1]))

            score_text = FONT.render(f'Очки: {(len(snake) - 5)}', True, SCORE_TEXT_COLOR)
            snake_window.blit(score_text, (10, 10))

        else:
            snake_window.blit(game_over_text, (WINDOW_WIDTH // 2 - game_over_text.get_width() // 2,
                                               WINDOW_HEIGHT // 2 - game_over_text.get_width() // 2))
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in buttons:
                        if button.rect.collidepoint(event.pos):
                            button.function()

            for button in buttons:
                pygame.draw.rect(snake_window, button.button_color, button.rect)
                snake_window.blit(button.text, button.get_rect_center())

        pygame.display.update()


new_loop()
        