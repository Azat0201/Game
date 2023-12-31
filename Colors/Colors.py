import random
import pygame


WIDTH = 1200
HEIGTH = 707
window_SIZE = (WIDTH, HEIGTH)
IMAGE_WIDTH = 400
IMAGE_HEIGTH = 400
IMAGE_SIZE = (IMAGE_WIDTH, IMAGE_HEIGTH)
FPS = 30

BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
ORANGE = (255, 150, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
LIGHT_BLUE = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 255)

COLORS = ()
for color in (RED, ORANGE, YELLOW, GREEN, LIGHT_BLUE, BLUE, PURPLE):
    COLORS += (color, )

pygame.init()
window = pygame.display.set_mode(window_SIZE)
background = pygame.Surface(window_SIZE)
background.fill(pygame.Color(COLORS[0]))
pygame.display.set_caption("Game")
clock = pygame.time.Clock()

image = pygame.image.load("image.jpg")
image = pygame.transform.scale(image, IMAGE_SIZE)
window.blit(image, (0, 0))


class Button:
    def __init__(self, x, y, title="", width=150, height=75, font='Verdana', size_font=12, button_color=GRAY, text_color=BLACK):
        self.font = pygame.font.SysFont(font, size_font)
        self.button_color = button_color
        self.text_color = text_color
        self.width = width
        self.heigth = height
        self.rect = pygame.Rect(x - width // 2, y - height // 2, width, height)
        self.text = self.font.render(title, True, text_color)

    def get_rect_center(self):
        return self.text.get_rect(center=self.rect.center)


button1 = Button(WIDTH // 2 - 100, HEIGTH // 2, title='Вперёд!')
button2 = Button(WIDTH // 2 + 100, HEIGTH // 2, title='Назад!')

color = 0
while True:
    window.fill(COLORS[color % len(COLORS)])
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                color += 1
            elif event.key == pygame.K_s:
                color -= 1
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if button1.rect.collidepoint(event.pos):
                color += 1
            if button2.rect.collidepoint(event.pos):
                color -= 1

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        color += 1
    if keys[pygame.K_s]:
        color -= 1

    window.blit(image, (WIDTH // 2 - IMAGE_WIDTH // 2, HEIGTH // 2 - IMAGE_HEIGTH // 2))

    pygame.draw.rect(window, button1.button_color, button1.rect)
    window.blit(button1.text, button1.get_rect_center())

    pygame.draw.rect(window, button2.button_color, button2.rect)
    window.blit(button2.text, button2.get_rect_center())

    pygame.display.update()
