import pygame
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


def new_loop(window_width, window_height, difficult, increase_food_time, can_crash_wall, can_crash_self):
    global WINDOW_WIDTH, WINDOW_HEIGHT, SPEED, DIFFERENCE_SPEED, SPEED_FOOD, INCREASE_SPEED_FOOD, \
        CAN_CRASH_WALL, CAN_CRASH_SELF, WINDOW_CENTRE_X, WINDOW_CENTRE_Y
    global WINDOW_COLOR, TEXT_COLOR, BUTTON_COLOR, BUTTON_TEXT_COLOR, ACTIVATED_BUTTON_COLOR, GAME_OVER_TEXT_COLOR, \
        SNAKE_COLOR, EYE_COLOR, FOOD_COLOR
    global FPS, RADIUS, RADIUS_FOOD, BUTTON_WIDTH, BUTTON_HEIGHT, Button, best_score

    with open('Settings') as settings, open('Colors') as colors, open('Score') as best_score:
        best_score = int(best_score.readline().split()[0])
        data = [int(settings.readline().split()[0]) for _ in range(3)]
        colors = [colors.readline().split()[0] for _ in range(9)]

    SPEED, DIFFERENCE_SPEED, SPEED_FOOD = data
    WINDOW_COLOR, TEXT_COLOR, BUTTON_COLOR, BUTTON_TEXT_COLOR, ACTIVATED_BUTTON_COLOR, GAME_OVER_TEXT_COLOR, \
     SNAKE_COLOR, EYE_COLOR, FOOD_COLOR = colors

    WINDOW_WIDTH = window_width
    WINDOW_HEIGHT = window_height

    INCREASE_SPEED_FOOD = increase_food_time
    CAN_CRASH_WALL = can_crash_wall
    CAN_CRASH_SELF = can_crash_self

    FPS = 60
    SPEED -= (difficult * DIFFERENCE_SPEED)
    RADIUS = (WINDOW_WIDTH + WINDOW_HEIGHT) // 100
    RADIUS_FOOD = RADIUS // 2
    BUTTON_WIDTH = WINDOW_WIDTH // 5
    BUTTON_HEIGHT = WINDOW_HEIGHT // 10

    WINDOW_CENTRE_X = WINDOW_WIDTH // 2 - WINDOW_WIDTH // 2 % RADIUS
    WINDOW_CENTRE_X -= RADIUS * int(not WINDOW_CENTRE_X // 2 % 2)
    WINDOW_CENTRE_Y = WINDOW_HEIGHT // 2 - WINDOW_WIDTH // 2 % RADIUS
    WINDOW_CENTRE_Y -= RADIUS * int(not WINDOW_CENTRE_Y // 2 % 2)


    class Button:
        def __init__(self, x, y, function, title="", parameters=None):
            self.activate = False
            self.rect = pygame.Rect(x - BUTTON_WIDTH // 2, y - BUTTON_HEIGHT // 2, BUTTON_WIDTH, BUTTON_HEIGHT)
            self.function = function
            self.title = title
            self.parameters = parameters

        def get_button_color(self):
            activate = self.activate
            self.activate = False
            return ACTIVATED_BUTTON_COLOR if activate else BUTTON_COLOR

    new_game()


def new_game():
    pygame.display.set_caption('Snake')
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    FONT = pygame.font.SysFont('Verdana', (WINDOW_WIDTH + WINDOW_HEIGHT) // 100)

    import Menu
    button_restart = Button(WINDOW_WIDTH // 2 - WINDOW_WIDTH // 4, WINDOW_HEIGHT // 2, new_game, 'Заново')
    button_menu = Button(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, Menu.new_loop, 'Меню')
    button_exit = Button(WINDOW_WIDTH // 2 + WINDOW_WIDTH // 4, WINDOW_HEIGHT // 2, quit, 'Выйти')
    buttons = (button_restart, button_menu, button_exit)

    global foods, game_over_Flag
    foods = [(-100, -100)]
    direction = (1, 0)
    iter_food = 0
    iter_snake = 0
    game_over_Flag = False
    snake = [(WINDOW_CENTRE_X - i * RADIUS * 2, WINDOW_CENTRE_Y) for i in range(5, 0, -1)]


    def game_over():
        global game_over_Flag, game_over_text, best_score
        score = len(snake) - 5
        if score <= best_score:
            game_over_text = FONT.render(f'Игра закончена! Счёт: {len(snake) - 5}\nРекорд: {best_score}',
                                         True, GAME_OVER_TEXT_COLOR)
        else:
            game_over_text = FONT.render(f'Игра закончена! Счёт: {len(snake) - 5}\nПредыдущий рекорд: {best_score}',
                                         True, GAME_OVER_TEXT_COLOR)
            with open('Score') as file:
                line = file.readline().split()
                line[0] = str(score)

            with open('Score', 'w') as file:
                file.write(' '.join(line) + '\n')
            best_score = score
        game_over_Flag = True


    while True:
        clock.tick(FPS)
        window.fill(WINDOW_COLOR)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        if not game_over_Flag:
            iter_food += 1
            iter_snake += 10

            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_w, pygame.K_UP) and direction[1] != 1:
                        copy_snake = list(snake[1:]) + [(snake[-1][0], snake[-1][1] + RADIUS * -2)]
                        if copy_snake[-1] == copy_snake[-3]:
                            iter_snake = 0
                            snake = snake[1:] + [(snake[-1][0] + RADIUS * 2 * direction[0],
                                                  snake[-1][1] + RADIUS * 2 * direction[1])]
                        direction = (0, -1)
                    elif event.key in (pygame.K_a, pygame.K_LEFT) and direction[0] != 1:
                        copy_snake = list(snake[1:]) + [(snake[-1][0] + RADIUS * -2, snake[-1][1])]
                        if copy_snake[-1] == copy_snake[-3]:
                            iter_snake = 0
                            snake = snake[1:] + [(snake[-1][0] + RADIUS * 2 * direction[0],
                                                  snake[-1][1] + RADIUS * 2 * direction[1])]
                        direction = (-1, 0)
                    elif event.key in (pygame.K_s, pygame.K_DOWN) and direction[1] != -1:
                        copy_snake = list(snake[1:]) + [(snake[-1][0], snake[-1][1] + RADIUS * 2)]
                        if copy_snake[-1] == copy_snake[-3]:
                            iter_snake = 0
                            snake = snake[1:] + [(snake[-1][0] + RADIUS * 2 * direction[0],
                                                  snake[-1][1] + RADIUS * 2 * direction[1])]
                        direction = (0, 1)
                    elif event.key in (pygame.K_d, pygame.K_RIGHT) and direction[0] != -1:
                        copy_snake = list(snake[1:]) + [(snake[-1][0] + RADIUS * 2, snake[-1][1])]
                        if copy_snake[-1] == copy_snake[-3]:
                            iter_snake = 0
                            snake = snake[1:] + [(snake[-1][0] + RADIUS * 2 * direction[0],
                                                  snake[-1][1] + RADIUS * 2 * direction[1])]
                        direction = (1, 0)
                    elif event.key == pygame.K_q:
                        game_over()
                        continue
                    elif event.key == pygame.K_e:
                        global SPEED
                        SPEED = 1000000

            if iter_snake >= SPEED:
                iter_snake = 0
                del snake[0]
                snake.append((snake[-1][0] + RADIUS * 2 * direction[0], snake[-1][1] + RADIUS * 2 * direction[1]))

            for food in foods:
                pygame.draw.circle(window, FOOD_COLOR, (food[0], food[1]), RADIUS_FOOD)
                if abs(food[0] - snake[-1][0]) < RADIUS * 2 and abs(food[1] - snake[-1][1]) < RADIUS * 2:
                    foods.remove(food)
                    snake.insert(0, (snake[0][0] - (snake[1][0] - snake[0][0]),
                                     snake[0][1] - (snake[1][1] - snake[0][1])))

            if not CAN_CRASH_SELF and snake[-1] in snake[:-1]:
                game_over()
                continue

            if not (0 <= snake[-1][0] <= WINDOW_WIDTH and 0 <= snake[-1][1] <= WINDOW_HEIGHT):
                if not CAN_CRASH_WALL:
                    game_over()
                    continue
                if not (0 <= snake[-1][0] <= WINDOW_WIDTH):
                    change = WINDOW_WIDTH - RADIUS if snake[-1][0] < 0 else RADIUS
                    snake[-1] = (change, snake[-1][1])
                if not (0 <= snake[-1][1] <= WINDOW_WIDTH):
                    change = WINDOW_HEIGHT - RADIUS if snake[-1][1] < 0 else RADIUS
                    snake[-1] = (snake[-1][0], change)

            for i, pos in enumerate(snake):
                pygame.draw.circle(window, SNAKE_COLOR, (pos[0], pos[1]), RADIUS)
            pygame.draw.circle(window, EYE_COLOR, (snake[-1][0], snake[-1][1]), RADIUS_FOOD)

            if iter_food >= SPEED_FOOD + (INCREASE_SPEED_FOOD * 2) ** (len(foods)):
                iter_food = 0
                create_food()

            score_text = FONT.render(f'Очки: {(len(snake) - 5)}', True, TEXT_COLOR)
            window.blit(score_text, (10, 10))
            prev_snake = list(snake)

        else:
            snake = prev_snake
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in buttons:
                        if button.rect.collidepoint(event.pos):
                            button.function()

            for food in foods:
                pygame.draw.circle(window, FOOD_COLOR, (food[0], food[1]), RADIUS_FOOD)

            for i, pos in enumerate(snake):
                pygame.draw.circle(window, SNAKE_COLOR, (pos[0], pos[1]), RADIUS)
            pygame.draw.circle(window, 'red', (snake[-1][0], snake[-1][1]), RADIUS)
            pygame.draw.circle(window, EYE_COLOR, (snake[-1][0], snake[-1][1]), RADIUS_FOOD)

            score_text = FONT.render(f'Очки: {(len(snake) - 5)}', True, TEXT_COLOR)
            window.blit(score_text, (10, 10))

            window.blit(game_over_text, (WINDOW_WIDTH // 2 - game_over_text.get_width() // 2,
                                               WINDOW_HEIGHT // 2 - game_over_text.get_width() // 2))

            for button in buttons:
                if button.rect.collidepoint(pygame.mouse.get_pos()):
                    button.activate = True
                text = FONT.render(button.title, True, BUTTON_TEXT_COLOR)
                pygame.draw.rect(window, button.get_button_color(), button.rect)
                window.blit(text, text.get_rect(center=button.rect.center))

        pygame.display.update()
        