import pygame
from random import randrange

pygame.init()
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1020
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
COLORS = (RED, GREEN, BLUE, YELLOW, WHITE)

WINDOW_COLOR = BLACK
WIDTH = 60
FPS = 60
speed_y = 3
speed_x = 3
rect = pygame.Rect(randrange(0, WINDOW_WIDTH), 0, WIDTH, WIDTH)
rect_color = randrange(len(COLORS))
rect_landed = False
stop = False

landed_rects = []

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                stop = not stop
            if event.key == pygame.K_w:
                speed_x += 1
            if event.key == pygame.K_s:
                speed_x -= 1
            if event.key == pygame.K_q:
                speed_y += 1
            if event.key == pygame.K_a:
                speed_y -= 1
            if event.key == pygame.K_r:
                rect_color = (rect_color + 1) % len(COLORS)
            if event.key == pygame.K_SPACE:
                landed_rects.append((rect, rect_color))
                rect_landed = True
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()

    if not stop:
        if not rect_landed:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_d]:
                rect.x -= speed_x
            if keys[pygame.K_f]:
                rect.x += speed_x
            if keys[pygame.K_DOWN]:
                rect.y += 3
            if keys[pygame.K_UP]:
                rect.y -= 3
            if keys[pygame.K_RIGHT]:
                rect.x += 3
            if keys[pygame.K_LEFT]:
                rect.x -= 3
        
            for landed_rect in landed_rects:
                if rect.colliderect(landed_rect[0]):
                    rect_landed = True
                    landed_rects.append((rect, rect_color))
                    break
        
            if not rect_landed:
                rect.y += speed_y
        
                if rect.y + WIDTH > WINDOW_HEIGHT:
                    rect.y = WINDOW_HEIGHT - WIDTH
                    rect_landed = True
                    landed_rects.append((rect, rect_color))
        
        if rect_landed:
            rect = pygame.Rect(randrange(0, WINDOW_WIDTH), 0, WIDTH, WIDTH)
            rect_color = randrange(len(COLORS))
            rect_landed = False

    window.fill(WINDOW_COLOR)
    for landed_rect in landed_rects:
        pygame.draw.rect(window, COLORS[landed_rect[1]], landed_rect[0])
    pygame.draw.rect(window, COLORS[rect_color], rect)
    pygame.display.update()

    pygame.time.Clock().tick(FPS)
