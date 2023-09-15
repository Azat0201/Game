import pygame

pygame.init()
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 500
WINDOW_COLOR = '#187193'
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Колобок')

COUNT_IMAGES = 8

images = []
for i in range(1, COUNT_IMAGES + 1):
    images.append(pygame.image.load(f"fox{i}.png"))

kolobok_image = pygame.image.load(f"kolobok.png")

ANIMATION_SPEED = 15
FRAME = 1.0 / ANIMATION_SPEED
SPEED = 10
FPS = 60
current_frame_index = 0
animation_timer = 0

frame_position = [0, 0]
frame_height = images[0].get_height()
frame_position[1] = WINDOW_HEIGHT // 2 - images[0].get_height() // 2

kolobok_position = [400, 0]
kolobok_height = kolobok_image.get_height()
kolobok_position[1] = WINDOW_HEIGHT // 2 + kolobok_image.get_height() // 4
kolobok_angle = 0
KOLOBOK_ROTATION_SPEED = 5

while True:
    pygame.Clock().tick(FPS)
    window.fill(WINDOW_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    time_delta = pygame.Clock().tick(FPS) / 1000.0
    animation_timer += time_delta
    if animation_timer >= FRAME:
        current_frame_index = (current_frame_index + 1) % COUNT_IMAGES
        animation_timer -= FRAME

    frame_position[0] += SPEED
    kolobok_position[0] += SPEED

    current_frame = images[current_frame_index]
    if frame_position[0] > WINDOW_WIDTH:
        frame_position = [-current_frame.get_width(), frame_position[1]]

    if kolobok_position[0] > WINDOW_WIDTH:
        kolobok_position = [-current_frame.get_width(), kolobok_position[1]]

    kolobok_angle += KOLOBOK_ROTATION_SPEED
    if kolobok_angle >= 360:
        kolobok_angle = 0
    kolobok = pygame.transform.rotate(kolobok_image, kolobok_angle)

    window.blit(current_frame, frame_position)
    window.blit(kolobok, kolobok_position)

    pygame.display.update()
