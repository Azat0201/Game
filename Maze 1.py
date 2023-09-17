import pygame

pygame.init()
STRING_MAZE = '''\
-   
1

11
-\
'''

def new_game():
    global maze, x, y, score
    maze = [list(line) for line in STRING_MAZE.split('\n')]
    x, y = 2, 0
    score = 0

new_game()

RECT = '-'
COIN = '1'
RADIUS = 20
WIDTH = RADIUS * 2
WINDOW_WIDTH = WIDTH * len(maze[0])
WINDOW_HEIGHT = WIDTH * len(maze) + RADIUS

WINDOW_COLOR = 'black'
RECT_COLOR = 'white'
CIRCLE_COLOR = 'red'
TEXT_COLOR = 'blue'
COIN_COLOR = 'yellow'

FONT = pygame.font.SysFont('Verdana', 10)
window = pygame.display.set_mode((WINDOW_WIDTH,  WINDOW_HEIGHT))
pygame.display.set_caption('Maze')

while True:
    window.fill(WINDOW_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                x -= 1
            if event.key == pygame.K_s:
                x += 1
            if event.key == pygame.K_a:
                y -= 1
            if event.key == pygame.K_d:
                y += 1

    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == RECT:
                rect = pygame.Rect(WIDTH * j, WIDTH * i, WIDTH, WIDTH)
                pygame.draw.rect(window, RECT_COLOR, rect)
                if pygame.Rect(WIDTH * y, WIDTH * x, WIDTH, WIDTH).colliderect(rect):
                    new_game()
            if maze[i][j] == COIN:
                if pygame.Rect(WIDTH * y, WIDTH * x, WIDTH, WIDTH).colliderect(
                        pygame.Rect(WIDTH * j, WIDTH * i, WIDTH, WIDTH)):
                    score += 1
                    maze[i][j] = None
                else:
                    pygame.draw.circle(window, COIN_COLOR, (WIDTH * j + RADIUS, WIDTH * i + RADIUS), RADIUS // 2)

    if not (0 <= x * WIDTH <= WINDOW_HEIGHT - WIDTH and 0 <= y * WIDTH <= WINDOW_WIDTH - WIDTH):
        new_game()

    pygame.draw.circle(window, CIRCLE_COLOR, (WIDTH * y + RADIUS, WIDTH * x + RADIUS), RADIUS)
    window.blit(FONT.render("Очки: " + str(score), True, TEXT_COLOR), (0, WINDOW_HEIGHT - RADIUS))
    pygame.display.update()
