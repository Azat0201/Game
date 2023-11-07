import pygame
import ctypes
from Button import Button

with open('Colors') as colors:
    WINDOW_COLOR, TEXT_COLOR, BUTTON_COLOR, BUTTON_TEXT_COLOR, ACTIVATED_BUTTON_COLOR = (colors.readline().split()[0] for _ in range(5))

DIFFICULTIES = ('Лёгкий', 'Средний', 'Сложный')
current_difficult = 1
current_size = 0
increase_food_time = True
can_crash_wall = False
can_crash_self = False
is_button_visible = False
user32 = ctypes.windll.user32
MONITOR_WIDTH = user32.GetSystemMetrics(0)
MONITOR_HEIGHT = user32.GetSystemMetrics(1)
MONITOR_SIZE = ((MONITOR_WIDTH, MONITOR_HEIGHT),)
WINDOWS_SIZES = ((3840, 2160), (2560, 1440), (1920, 1080), (1680, 1050), (1600, 1200), (1600, 900), (1440, 900),
                 (1400, 1050), (1366, 768), (1366, 760), (1280, 1024), (1280, 960), (1280, 800), (1280, 768),
                 (1280, 720), (1280, 600), (1152, 864), (1024, 768), (800, 600), (720, 576), (720, 480), (640, 480),
                 (680, 400), (512, 384), (400, 300), (320, 240), (320, 200), (100, 100))
WINDOWS_SIZES = MONITOR_SIZE + tuple(filter(lambda x: x[0] <= MONITOR_WIDTH and x[1] <= MONITOR_HEIGHT and
                                                      x != MONITOR_SIZE[0], WINDOWS_SIZES))
FPS = 60


def start_game():
    import Snake
    global is_button_visible
    is_button_visible = False
    Snake.new_loop(WINDOWS_SIZES[current_size], current_difficult, increase_food_time, can_crash_wall, can_crash_self)


def change_difficult(button):
    global current_difficult
    current_difficult = (current_difficult + 1) % len(DIFFICULTIES)
    button._text = DIFFICULTIES[current_difficult]


def settings():
    global is_button_visible
    is_button_visible = not is_button_visible


def increase_food_time_function(button):
    global increase_food_time
    increase_food_time = not increase_food_time
    button._activator = increase_food_time


def can_crash_wall_function(button):
    global can_crash_wall
    can_crash_wall = not can_crash_wall
    button._activator = can_crash_wall


def can_crash_self_function(button):
    global can_crash_self
    can_crash_self = not can_crash_self
    button._activator = can_crash_self


def change_size_window(button):
    global current_size
    current_size = (current_size + 1) % len(WINDOWS_SIZES)
    button.title = f'{WINDOWS_SIZES[current_size][0]}x{WINDOWS_SIZES[current_size][1]}'
    new_loop()


def increase_size_window(button):
    global current_size
    current_size = (current_size - 1) % len(WINDOWS_SIZES)
    button.title = f'{WINDOWS_SIZES[current_size][0]}x{WINDOWS_SIZES[current_size][1]}'
    new_loop()


def move_window(x, y):
    size = pygame.display.get_wm_info()['window']
    ctypes.windll.user32.MoveWindow(size, x - 8, y - 31, WINDOWS_SIZES[current_size][0], WINDOWS_SIZES[current_size][1], False)


def new_loop():
    global buttons, visible_buttons, setting_buttons
    pygame.init()

    WINDOW_WIDTH, WINDOW_HEIGHT = WINDOWS_SIZES[current_size]
    GAP = (WINDOW_WIDTH + WINDOW_HEIGHT) // 200
    SIZE_FONT = (WINDOW_WIDTH + WINDOW_HEIGHT) // 100

    BUTTON_WIDTH = WINDOW_WIDTH // 4
    BUTTON_HEIGHT = WINDOW_HEIGHT // 8
    BUTTON_X = WINDOW_WIDTH // 2
    BUTTON_X2 = BUTTON_X + BUTTON_WIDTH + GAP
    BUTTON_Y = BUTTON_HEIGHT + GAP
    FONT = pygame.font.SysFont('Verdana', SIZE_FONT)

    Button.width = BUTTON_WIDTH
    Button.height = BUTTON_HEIGHT
    Button.gap = GAP
    Button.button_color = BUTTON_COLOR
    Button.activated_color = ACTIVATED_BUTTON_COLOR

    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    move_window((MONITOR_WIDTH - WINDOW_WIDTH) // 2, (MONITOR_HEIGHT - WINDOW_HEIGHT) // 2)
    pygame.display.set_caption('Snake menu')

    str_sizes = '-' * 28 + '\\n' + '\\n'.join(map(lambda x: f'{x[0]} x {x[1]}{" - current size" if x == WINDOWS_SIZES[current_size] else ""}', WINDOWS_SIZES[:-1])) + '\\n' + '-' * 28


    # parameters: (x, y, func, text, activator(value at which active),
    # additional text (text which show when hovering cursor),
    # parameters (for func, in sequence, if 'self', parameter self func), width (not default width), gap (not default),
    # color(not default), activated color (not default, color when button is active))
    BUTTONS_DATA = (
        (BUTTON_X, BUTTON_Y * 1, start_game, 'Начать игру'),
        (BUTTON_X, BUTTON_Y * 2, change_difficult, DIFFICULTIES[current_difficult], None, None, 'self'),
        (BUTTON_X, BUTTON_Y * 3, settings, 'Настройки'),
        (BUTTON_X, BUTTON_Y * 4, quit, 'Выйти'),
        (BUTTON_X2, BUTTON_Y * 1, increase_food_time_function, 'Увеличение времени создание еды от количества еды',
         increase_food_time, 'Увеличивает скорость появления еды для змейки в зависимости от количества её', 'self'),
        (BUTTON_X2, BUTTON_Y * 2, can_crash_wall_function, 'Врезаться в стены', can_crash_wall,
         'Позволяет змейки проходить через стены', 'self'),
        (BUTTON_X2, BUTTON_Y * 3, can_crash_self_function, 'Врезаться в себя', can_crash_self,
         'Позволяет змейки проходить через себя', 'self'),
        (BUTTON_X2 - BUTTON_WIDTH // 8, BUTTON_Y * 4, change_size_window, f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}',
         can_crash_self, str_sizes, 'self', BUTTON_WIDTH - BUTTON_WIDTH // 4),  # [:-1] чтобы не показывать последний размер (пасхалка)
        (BUTTON_X2 + BUTTON_WIDTH / 2.5 - GAP // 2, BUTTON_Y * 4, increase_size_window, '/\\', None, str_sizes, 'self',
         BUTTON_WIDTH // 4 - GAP)
    )

    button_start = Button(*BUTTONS_DATA[0])
    button_difficulty = Button(*BUTTONS_DATA[1])
    button_settings = Button(*BUTTONS_DATA[2])
    button_exit = Button(*BUTTONS_DATA[3])
    button_increase = Button(*BUTTONS_DATA[4])
    button_can_wall = Button(*BUTTONS_DATA[5])
    button_can_self = Button(*BUTTONS_DATA[6])
    button_change_size = Button(*BUTTONS_DATA[7])
    button_increase_size = Button(*BUTTONS_DATA[8])

    visible_buttons = (button_start, button_difficulty, button_settings, button_exit)
    setting_buttons = (button_increase, button_can_wall, button_can_self, button_change_size, button_increase_size)
    buttons = visible_buttons


    def show_text(text, x, y, width, height, color=BUTTON_TEXT_COLOR, centered_x=True, centered_y=True):
        words = text.split(' ')
        lines = [[]]
        count = 0
        for word in words:
            if r'\n' in word:
                index = word.index(r'\n')
                lines[count].append(word[:index])
                count += 1
                lines.append([])
                words.insert(words.index(word) + 1, word[index + 2:])
            elif len(word) + sum(map(len, lines[count])) + len(lines[count]) > width / WINDOW_WIDTH * 100:
                count += 1
                lines.append([word])
            else:
                lines[count].append(word)
    
        gap = (height - count * SIZE_FONT) // 2
        for i, line in enumerate(lines):
            text_line = FONT.render(' '.join(line), True, color)
            pos = (x - (text_line.get_width() // 2 * centered_x), y + (gap * centered_y) - SIZE_FONT // 2 + i * SIZE_FONT)
            window.blit(text_line, pos)


    while True:
        pygame.time.Clock().tick(FPS)
        window.fill(WINDOW_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.rect.collidepoint(event.pos):
                        button.use_function()

        buttons = visible_buttons + setting_buttons if is_button_visible else visible_buttons

        for button in buttons:
            if button.rect.collidepoint(pygame.mouse.get_pos()):
                button.change_active()
                if button.additional_text is not None:
                    show_text(button.additional_text, GAP * 2, BUTTON_Y - BUTTON_HEIGHT // 2,
                              BUTTON_WIDTH, BUTTON_HEIGHT * 3, TEXT_COLOR, False, False)

            pygame.draw.rect(window, ACTIVATED_BUTTON_COLOR, button.frame)
            pygame.draw.rect(window, button.color, button.rect)
            show_text(button.text, button.rect.center[0], button.rect.y, BUTTON_WIDTH, BUTTON_HEIGHT)

        with open('Score') as file:
            score = file.readline().split()[0]

        score_text = FONT.render(f'Рекорд: {score}', True, TEXT_COLOR)
        window.blit(score_text, (GAP, GAP))

        pygame.display.update()
