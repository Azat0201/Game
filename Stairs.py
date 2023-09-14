import pygame

pygame.init()
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500
WINDOW_COLOR = (0, 0, 0)
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Stairs')

STEP_WIDTH = 20
STEP_HEIGHT = STEP_WIDTH
STEP_COLOR = (255, 255, 255)

PLAYER_RADIUS = STEP_WIDTH // 2
PLAYER_COLOR = (255, 0, 0)
FONT_SIZE = 20
FONT_COLOR = (255, 255, 255)
clock = pygame.time.Clock()

def game_loop():
    player_x = PLAYER_RADIUS
    player_y = WINDOW_HEIGHT - STEP_HEIGHT - PLAYER_RADIUS
    step_count = 0

    while True:
        window.fill(WINDOW_COLOR)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    player_x += 20
                    player_y -= 20
                    step_count += 1
                if event.key == pygame.K_LEFT:
                    player_x -= 20
                    player_y += 20
                    step_count += 1

        step_x = 0
        step_y = WINDOW_HEIGHT - STEP_HEIGHT
        while step_x <= WINDOW_WIDTH - STEP_WIDTH and 0 <= step_y:
            pygame.draw.rect(window, STEP_COLOR, pygame.Rect(step_x, step_y, STEP_WIDTH, STEP_HEIGHT))
            step_x += STEP_WIDTH
            step_y -= STEP_HEIGHT

        if not (0 <= player_x <= WINDOW_WIDTH and 0 <= player_y <= WINDOW_HEIGHT):
            break

        pygame.draw.circle(window, PLAYER_COLOR, (player_x, player_y), PLAYER_RADIUS)

        font = pygame.font.SysFont('Arial', FONT_SIZE)
        text = font.render(f'Шаг: {str(step_count)}', True, FONT_COLOR)
        window.blit(text, (10, 10))
        pygame.display.update()
        clock.tick(60)

while True:
    game_loop()