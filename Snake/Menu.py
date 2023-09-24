import pygame
import ctypes


with open('Colors') as colors:
    WINDOW_COLOR, _, BUTTON_COLOR, TEXT_COLOR, ACTIVATED_BUTTON_COLOR = (colors.readline().split()[0] for _ in range(5))

DIFFICULTIES = ('Лёгкий', 'Средний', 'Сложный')
WINDOWS_SIZES = ((900, 900), (1920, 1080))
current_difficult = 0
current_size = 0
increase_food_time = True
can_crash_wall = False
can_crash_self = False
FPS = 60


def get_parameters():
    global WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_X, WINDOW_Y, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_X, BUTTON_X2, BUTTON_Y
    user32 = ctypes.windll.user32
    WINDOW_WIDTH, WINDOW_HEIGHT = WINDOWS_SIZES[current_size]
    MONITOR_WIDTH, MONITOR_HEIGHT = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    WINDOW_X = MONITOR_WIDTH // 2 - WINDOW_WIDTH // 2
    WINDOW_Y = MONITOR_HEIGHT // 2 - WINDOW_HEIGHT // 2
    BUTTON_WIDTH = WINDOW_WIDTH // 4
    BUTTON_HEIGHT = WINDOW_HEIGHT // 8
    BUTTON_X = WINDOW_WIDTH // 2
    BUTTON_X2 = BUTTON_X + BUTTON_WIDTH + 15
    BUTTON_Y = BUTTON_HEIGHT + 15


def start_game():
    import Snake
    Snake.new_loop(WINDOWS_SIZES[current_size][0], WINDOWS_SIZES[current_size][1], current_difficult, increase_food_time, can_crash_wall, can_crash_self)


def change_difficult(button):
    global current_difficult
    current_difficult = (current_difficult + 1) % len(DIFFICULTIES)
    button.title = DIFFICULTIES[current_difficult]


def settings():
    global buttons, visible_buttons, setting_buttons
    buttons = buttons + setting_buttons if buttons == visible_buttons else visible_buttons


def increase_food_time_function():
    global increase_food_time
    increase_food_time = not increase_food_time


def can_crash_wall_function():
    global can_crash_wall
    can_crash_wall = not can_crash_wall


def can_crash_self_function():
    global can_crash_self
    can_crash_self = not can_crash_self
    
    
def change_size_window(button):
    global current_size
    current_size = (current_size + 1) % len(WINDOWS_SIZES)
    button.title = f'{WINDOWS_SIZES[current_size][0]}x{WINDOWS_SIZES[current_size][1]}'
    new_loop()


def move_window(x, y):
    size = pygame.display.get_wm_info()['window']
    width, height = pygame.display.get_surface().get_size()
    ctypes.windll.user32.MoveWindow(size, x - 8, y - 31, width, height, False)


def new_loop():
    global current_difficult, buttons, visible_buttons, setting_buttons
    get_parameters()
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    move_window(WINDOW_X, WINDOW_Y)
    pygame.display.set_caption('Menu')
    FONT = pygame.font.SysFont('Verdana', 18)

    class Button:
        def __init__(self, x, y, function, title="", activator='0', parameters=None):
            self.activate = False
            self.rect = pygame.Rect(x - BUTTON_WIDTH // 2, y - BUTTON_HEIGHT // 2, BUTTON_WIDTH, BUTTON_HEIGHT)
            self.function = function
            self.title = title
            self.parameters = parameters
            self.activator = activator

        def use_function(self):
            if self.parameters is None:
                self.function()
            else:
                self.function(self.parameters)

        def get_button_color(self):
            activate = self.activate
            self.activate = False
            return ACTIVATED_BUTTON_COLOR if eval(self.activator) or activate else BUTTON_COLOR

    BUTTONS_DATA = (
        (increase_food_time_function, 'Увеличение времени\nеды от количества еды', 'increase_food_time'),
        (can_crash_wall_function, 'Врезаться в стены', 'can_crash_wall'),
        (can_crash_self_function, 'Врезаться в себя', 'can_crash_self'),
        (change_size_window, f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')
    )

    button_start = Button(BUTTON_X, BUTTON_Y, start_game, 'Начать игру')
    button_difficulty = Button(BUTTON_X, BUTTON_Y * 2, change_difficult, DIFFICULTIES[current_difficult])
    button_difficulty.parameters = button_difficulty
    button_settings = Button(BUTTON_X, BUTTON_Y * 3, settings, 'Настройки')
    button_exit = Button(BUTTON_X, BUTTON_Y * 4, quit, 'Выйти')

    button_increase = Button(BUTTON_X2, BUTTON_Y * 1, BUTTONS_DATA[0][0], BUTTONS_DATA[0][1], BUTTONS_DATA[0][2])
    button_can_wall = Button(BUTTON_X2, BUTTON_Y * 2, BUTTONS_DATA[1][0], BUTTONS_DATA[1][1], BUTTONS_DATA[1][2])
    button_can_self = Button(BUTTON_X2, BUTTON_Y * 3, BUTTONS_DATA[2][0], BUTTONS_DATA[2][1], BUTTONS_DATA[2][2])
    button_change_size = Button(BUTTON_X2, BUTTON_Y * 4, BUTTONS_DATA[3][0], BUTTONS_DATA[3][1])
    button_change_size.parameters = button_change_size


    visible_buttons = (button_start, button_difficulty, button_settings, button_exit)
    setting_buttons = (button_increase, button_can_wall, button_can_self, button_change_size)
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
            if button.rect.collidepoint(pygame.mouse.get_pos()):
                button.activate = True
            text = FONT.render(button.title, True, TEXT_COLOR)
            pygame.draw.rect(window, button.get_button_color(), button.rect)
            window.blit(text, text.get_rect(center=button.rect.center))

        pygame.display.update()
