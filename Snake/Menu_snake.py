import pygame
import os
import ctypes


class Button:
    def __init__(self, x, y, function, title="", width=150, height=75, font='Verdana', size_font=15,
                 button_color=(150, 150, 150), text_color='black', parameters=None):
        self.font = pygame.font.SysFont(font, size_font)
        self.function = function
        self.parameters = parameters
        self.button_color = button_color
        self.text_color = text_color
        self.title = title
        self.rect = pygame.Rect(x - width // 2, y - height // 2, width, height)
        self.text = self.font.render(title, True, text_color)

    def get_rect_center(self):
        return self.text.get_rect(center=self.rect.center)



WINDOW_WIDTH = 900
WINDOW_HEIGHT = 900
WINDOW_COLOR = 'black'
user32 = ctypes.windll.user32
MONITOR_WIDTH, MONITOR_HEIGHT = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
FPS = 60
WINDOW_X = MONITOR_WIDTH // 2 - WINDOW_WIDTH // 2
WINDOW_Y = MONITOR_HEIGHT // 2 - WINDOW_HEIGHT // 2
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (WINDOW_X, WINDOW_Y)

DIFFICULTIES = ('Лёгкий', 'Средний', 'Сложный')
current_difficult = 0


def start_game():
    import Snake
    Snake.new_loop(current_difficult)


def change_difficult(button):
    global current_difficult
    current_difficult = (current_difficult + 1) % len(DIFFICULTIES)
    button.text = button.font.render(DIFFICULTIES[current_difficult], True, button.text_color)


BUTTON_WIDTH = WINDOW_WIDTH // 5
BUTTON_HEIGHT = WINDOW_HEIGHT // 10
TEXT_COLOR = 'black'


def new_loop():
    global current_difficult
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Menu')
    button_start = Button(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 8, start_game, 'Начать игру', BUTTON_WIDTH, BUTTON_HEIGHT)
    button_difficulty = Button(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 8 * 2,
                               change_difficult, DIFFICULTIES[current_difficult], BUTTON_WIDTH, BUTTON_HEIGHT)
    button_difficulty.parameters = button_difficulty
    button_exit = Button(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 8 * 3, quit, 'Выйти', BUTTON_WIDTH, BUTTON_HEIGHT)
    buttons = (button_start, button_difficulty, button_exit)

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
            pygame.draw.rect(window, button.button_color, button.rect)
            window.blit(button.text, button.text.get_rect(center=button.rect.center))

        pygame.display.update()
