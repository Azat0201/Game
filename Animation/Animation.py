import pygame

pygame.init()

WINDOW_SIZE = (640, 480)
window = pygame.display.set_mode(WINDOW_SIZE)
WINDOW_COLOR = (216, 233, 243)
window.fill(WINDOW_COLOR)
pygame.display.set_caption('Animation')
clock = pygame.time.Clock()

frame_images = []
for i in range(1, 9):
    frame_images.append(pygame.image.load(fr"frame{i}.png"))

ANIMATION_LENGTH = len(frame_images)
ANIMATION_SPEED = 15
FRAME = 1.0 / ANIMATION_SPEED
SPEED = 1
FPS = 60
current_frame_index = 0
animation_timer = 0
frame_position = [0, 0]

window_height = WINDOW_SIZE[1]
frame_height = frame_images[0].get_height()
frame_position[1] = int(window_height * 0.45) - int(frame_height / 2)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    time_delta = clock.tick(FPS) / 1000.0
    animation_timer += time_delta
    if animation_timer >= FRAME:
        current_frame_index = (current_frame_index + 1) % ANIMATION_LENGTH
        animation_timer -= FRAME

    frame_position[0] += SPEED
    current_frame = frame_images[current_frame_index]

    if frame_position[0] > WINDOW_SIZE[0]:
        frame_position = [-current_frame.get_width(), frame_position[1]]
    window.blit(current_frame, frame_position)
    pygame.display.update()
