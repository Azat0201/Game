import pygame
from random import randint, choice

WINDOW_WIDTH = 1920
WINDOW_HEIGTH = 1080
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGTH)
FPS = 100
SURFACE_SIZE = 500

window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('Матрица Lite')
pygame.init()

TEXT_FONT = pygame.font.SysFont('Verdana', 15)
TEXT_COLOR = pygame.Color('green')
TEXT_SYMBOLS = '1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM123456789012345678901234567890'
TEXT_POSITION = [(randint(1, WINDOW_WIDTH), randint(1, WINDOW_HEIGTH)) for i in range(SURFACE_SIZE)]
NORMAL_TEXT_SPEED = tuple((0, randint(1, 100)) for i in range(SURFACE_SIZE))
ZERO_TEXT_SPEED = tuple((0, 0) for _ in range(SURFACE_SIZE))
TEXT_SPEED = NORMAL_TEXT_SPEED
TEXT_SURFACE_LIST = []

BUTTON_WIDTH = 100
BUTTON_HEIGTH = 50
BUTTON_SIZE = (BUTTON_WIDTH, BUTTON_HEIGTH)
BUTTON_POSX = BUTTON_WIDTH
BUTTON_POSY = 0
BUTTON1_TITLE = 'Матрица!'
BUTTON2_TITLE = 'Пауза!'
BUTTON3_TITLE = 'Выход!'


def change_surface_list():
    global TEXT_SURFACE_LIST
    if TEXT_SURFACE_LIST:
        TEXT_SURFACE_LIST = []
    else:
        for i in range(SURFACE_SIZE):
            text_symbol = choice(TEXT_SYMBOLS)
            TEXT_SURFACE_LIST.append(TEXT_FONT.render(text_symbol, True, TEXT_COLOR))

def change_speed():
    global TEXT_SPEED
    if TEXT_SPEED[0][1]:
        TEXT_SPEED = ZERO_TEXT_SPEED
    else:
        TEXT_SPEED = NORMAL_TEXT_SPEED


def quitf():
    pygame.quit()
    quit()


class Butoon:
    def __init__(self, x, y, title="", width=BUTTON_WIDTH, font=TEXT_FONT, heigt=BUTTON_HEIGTH, button_color='#606065', text_color='#FFFFFF'):
        self.font = TEXT_FONT
        self.button_color = button_color
        self.text_color = text_color
        self.width = width
        self.heigth = heigt
        self.rect = pygame.Rect(x, y, self.width, self.heigth)
        self.title = self.font.render(title, True, self.text_color)

    def get_rect_center(self):
        return self.title.get_rect(center=self.rect.center)


button1 = Butoon(BUTTON_POSX + 100, BUTTON_POSY, BUTTON1_TITLE, button_color='#555555', text_color='#000000')
button2 = Butoon(BUTTON_POSX + 000, BUTTON_POSY, BUTTON2_TITLE, button_color='#555555', text_color='#000000')
button3 = Butoon(BUTTON_POSX - 100, BUTTON_POSY, BUTTON3_TITLE, button_color='#555555', text_color='#000000')

while True:
    TIME_DELTA = pygame.time.Clock().tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quitf()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if button1.rect.collidepoint(event.pos):
                change_surface_list()
            elif button2.rect.collidepoint(event.pos):
                change_speed()
            elif button3.rect.collidepoint(event.pos):
                quitf()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                change_surface_list()
            elif event.key == pygame.K_w:
                change_speed()
            elif event.key == pygame.K_q:
                quitf()

    window.fill(pygame.Color('black'))

    for i in range(SURFACE_SIZE):
        TEXT_POSITION[i] = (TEXT_POSITION[i][0], TEXT_POSITION[i][1] + TEXT_SPEED[i][1])
        if TEXT_POSITION[i][1] > WINDOW_SIZE[1]:
            TEXT_POSITION[i] = (randint(1, WINDOW_SIZE[0]), randint(-WINDOW_HEIGTH + 100, WINDOW_HEIGTH - 100))
        if len(TEXT_SURFACE_LIST) > i:
            window.blit(TEXT_SURFACE_LIST[i], TEXT_POSITION[i])

    pygame.draw.rect(window, button1.button_color, button1.rect)
    window.blit(button1.title, button1.get_rect_center())

    pygame.draw.rect(window, button2.button_color, button2.rect)
    window.blit(button2.title, button2.get_rect_center())

    pygame.draw.rect(window, button3.button_color, button3.rect)
    window.blit(button3.title, button3.get_rect_center())

    pygame.display.update()
