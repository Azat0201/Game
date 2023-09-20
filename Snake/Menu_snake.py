import pygame
import os
import ctypes


WINDOW_WIDTH = 900
WINDOW_HEIGHT = 900
WINDOW_COLOR = 'black'
user32 = ctypes.windll.user32
MONITOR_WIDTH, MONITOR_HEIGHT = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
FPS = 60
WINDOW_X = MONITOR_WIDTH // 2 - WINDOW_WIDTH // 5
WINDOW_Y = MONITOR_HEIGHT // 2 - WINDOW_HEIGHT // 2
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (WINDOW_X, WINDOW_Y)

BUTTON_WIDTH = WINDOW_WIDTH // 4
BUTTON_HEIGHT = WINDOW_HEIGHT // 8
BUTTON_X = WINDOW_WIDTH // 2
BUTTON_Y = BUTTON_HEIGHT + 15
TEXT_COLOR = 'black'


class Button:
    def __init__(self, x, y, function, title="", font=None, width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                 text_color='black', button_color='#969696', parameters=None, activated_button_color='#646464', activator='0'):
        self.rect = pygame.Rect(x - width // 2, y - height // 2, width, height)
        self.function = function
        self.font = font
        self.text_color = text_color
        self.text = self.font.render(title, True, self.text_color)
        self.button_color = button_color
        self.parameters = parameters
        self.activated_button_color = activated_button_color
        self.activator = activator

    def get_rect_center(self):
        return self.text.get_rect(center=self.rect.center)
    
    def use_function(self):
        if self.parameters is None:
            self.function()
        else:
            self.function(self.parameters)
            
    def get_button_color(self):
        return self.activated_button_color if eval(self.activator) else self.button_color


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
    FONT = pygame.font.SysFont('Verdana', 18)

    button_start = Button(BUTTON_X, BUTTON_Y, start_game, 'Начать игру', FONT)
    button_difficulty = Button(BUTTON_X, BUTTON_Y * 2, change_difficult, DIFFICULTIES[current_difficult], FONT)
    button_difficulty.parameters = button_difficulty
    button_settings = Button(BUTTON_X, BUTTON_Y * 3, settings, 'Настройки', FONT)

    buttons_data = (
        (increase_food_time_function, 'Увеличение времени\nеды от количества еды', 'increase_food_time'),
        (can_crash_wall_function, 'Врезаться в стены', 'can_crash_wall'),
        (can_crash_self_function, 'Врезаться в себя', 'can_crash_self')
    )
    button_increase = Button(BUTTON_X + BUTTON_WIDTH + 15, BUTTON_Y * 2, buttons_data[0][0], buttons_data[0][1], FONT,
                             activator=buttons_data[0][2])
    button_increase.parameters = button_increase

    button_can_wall = Button(BUTTON_X + BUTTON_WIDTH + 15, BUTTON_Y * 3, buttons_data[1][0], buttons_data[1][1], FONT,
                             activator=buttons_data[1][2])
    button_can_wall.parameters = button_can_wall

    button_can_self = Button(BUTTON_X + BUTTON_WIDTH + 15, BUTTON_Y * 4, buttons_data[2][0], buttons_data[2][1], FONT,
                             activator=buttons_data[2][2])
    button_can_self.parameters = button_can_self

    button_exit = Button(BUTTON_X, BUTTON_Y * 4, quit, 'Выйти', FONT)
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
                        button.use_function()

        for button in buttons:
            pygame.draw.rect(window, button.get_button_color(), button.rect)
            window.blit(button.text, button.text.get_rect(center=button.rect.center))

        pygame.display.update()
