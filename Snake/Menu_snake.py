import pygame
import os
import ctypes


class Button:
    def __init__(self, x, y, function, title="", width=150, height=75, font='Verdana', size_font=15,
                 button_color=(150, 150, 150), text_color='black'):
        self.font = pygame.font.SysFont(font, size_font)
        self.function = function
        self.button_color = button_color
        self.text_color = text_color
        self.width = width
        self.heigth = height
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
x = MONITOR_WIDTH // 2 - WINDOW_WIDTH // 2
y = MONITOR_HEIGHT // 2 - WINDOW_HEIGHT // 2
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)


def start_game():
    import Snake
    Snake.new_loop()


BUTTON_WIDTH = WINDOW_WIDTH // 5
BUTTON_HEIGHT = WINDOW_HEIGHT // 10
TEXT_COLOR = 'black'


def new_loop():
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Menu')
    button_start = Button(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 8, start_game, 'Начать игру', BUTTON_WIDTH, BUTTON_HEIGHT)
    button_exit = Button(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 8 * 2, quit, 'Выйти', BUTTON_WIDTH, BUTTON_HEIGHT)
    buttons = (button_start, button_exit)

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
                        button.function()

        for button in buttons:
            pygame.draw.rect(window, button.button_color, button.rect)
            window.blit(button.text, button.get_rect_center())

        pygame.display.update()


new_loop()
