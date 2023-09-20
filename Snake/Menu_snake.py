import pygame
import os
import ctypes


WINDOW_WIDTH = 900
WINDOW_HEIGHT = 900
WINDOW_COLOR = 'black'
user32 = ctypes.windll.user32
MONITOR_WIDTH, MONITOR_HEIGHT = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
FPS = 60
WINDOW_X = MONITOR_WIDTH // 2 - WINDOW_WIDTH // 2
WINDOW_Y = MONITOR_HEIGHT // 2 - WINDOW_HEIGHT // 2
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (WINDOW_X, WINDOW_Y)

BUTTON_WIDTH = WINDOW_WIDTH // 5
BUTTON_HEIGHT = WINDOW_HEIGHT // 10
TEXT_COLOR = 'black'


class Button:
    def __init__(self, x, y, function, title="", width=BUTTON_WIDTH, height=BUTTON_HEIGHT, font='Verdana', size_font=15, text_color='black',
                 button_color=(150, 150, 150), parameters=None, activated_button_color=(100, 100, 100), activator='0'):
        self.font = pygame.font.SysFont(font, size_font)
        self.function = function
        self.parameters = parameters
        self.button_color = button_color
        self.activator = activator
        self.activated_button_color = activated_button_color
        self.text_color = text_color
        self.title = title
        self.rect = pygame.Rect(x - width // 2, y - height // 2, width, height)
        self.text = self.font.render(title, True, text_color)

    def get_rect_center(self):
        return self.text.get_rect(center=self.rect.center)


DIFFICULTIES = ('Лёгкий', 'Средний', 'Сложный')
current_difficult = 0
increase_food_time = True
can_crash_wall = False
can_crash_self = False


def start_game():
    import Snake
    Snake.new_loop(current_difficult, increase_food_time, can_crash_wall, can_crash_self)


def change_difficult(button):
    global current_difficult
    current_difficult = (current_difficult + 1) % len(DIFFICULTIES)
    button.text = button.font.render(DIFFICULTIES[current_difficult], True, button.text_color)


def settings():
    global buttons, visible_buttons, setting_buttons
    buttons = buttons + setting_buttons if buttons == visible_buttons else visible_buttons


def increase_food_time_function(button):
    global increase_food_time
    increase_food_time = not increase_food_time
    button.activate = increase_food_time


def can_crash_wall_function(button):
    global can_crash_wall
    can_crash_wall = not can_crash_wall
    button.activate = can_crash_wall


def can_crash_self_function(button):
    global can_crash_self
    can_crash_self = not can_crash_self
    button.activate = can_crash_self


def new_loop():
    global current_difficult, buttons, visible_buttons, setting_buttons
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Menu')
    button_start = Button(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 8, start_game, 'Начать игру')

    button_difficulty = Button(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 8 * 2,
                               change_difficult, DIFFICULTIES[current_difficult])
    button_difficulty.parameters = button_difficulty

    button_settings = Button(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 8 * 3, settings, 'Настройки')

    button_increase = Button(WINDOW_WIDTH // 2 + BUTTON_WIDTH + 10, WINDOW_HEIGHT // 8 * 2, increase_food_time_function,
                             'Увеличение времени\nеды', activator='increase_food_time')
    button_increase.parameters = button_increase

    button_can_wall = Button(WINDOW_WIDTH // 2 + BUTTON_WIDTH + 10, WINDOW_HEIGHT // 8 * 3, can_crash_wall_function,
                             'Врезаться в стены', activator='can_crash_wall')
    button_can_wall.parameters = button_can_wall

    button_can_self = Button(WINDOW_WIDTH // 2 + BUTTON_WIDTH + 10, WINDOW_HEIGHT // 8 * 4, can_crash_self_function,
                             'Врезаться в себя', activator='can_crash_self')
    button_can_self.parameters = button_can_self

    button_exit = Button(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 8 * 4, quit, 'Выйти')
    visible_buttons = (button_start, button_difficulty, button_settings, button_exit)
    setting_buttons = (button_increase, button_can_wall, button_can_self)
    buttons = visible_buttons

    while True:
        pygame.time.Clock().tick(FPS)
        window.fill(WINDOW_COLOR)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.rect.collidepoint(event.pos):
                        if button.parameters is None:
                            button.function()
                        else:
                            button.function(button.parameters)

        for button in buttons:
            pygame.draw.rect(window, button.activated_button_color if eval(button.activator) else button.button_color,
                             button.rect)
            window.blit(button.text, button.text.get_rect(center=button.rect.center))

        pygame.display.update()
