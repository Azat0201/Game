import pygame
from random import randint

pygame.init()
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 1000
WINDOW_COLOR = '#10A031'
FPS = 60
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Traffic')

TRAFFIC_LIGHTS_WIDTH = 100
TRAFFIC_LIGHTS_HEIGHT = 300
TRAFFIC_LIGHTS_TRACING_WIDTH = 5
TRAFFIC_LIGHTS_X = WINDOW_WIDTH // 2 - TRAFFIC_LIGHTS_WIDTH // 2
TRAFFIC_LIGHTS_Y = WINDOW_HEIGHT // 2 - TRAFFIC_LIGHTS_HEIGHT // 2
TRAFFIC_LIGHTS_COLOR = '#9D9D9D'
TRAFFIC_LIGHTS_COLOR_TRACING = '#757575'
LIGHT_RADIUS = 40
traffic_lights = pygame.rect.Rect(TRAFFIC_LIGHTS_X + TRAFFIC_LIGHTS_TRACING_WIDTH,
                                  TRAFFIC_LIGHTS_Y + TRAFFIC_LIGHTS_TRACING_WIDTH,
                                  TRAFFIC_LIGHTS_WIDTH - TRAFFIC_LIGHTS_TRACING_WIDTH * 2,
                                  TRAFFIC_LIGHTS_HEIGHT - TRAFFIC_LIGHTS_TRACING_WIDTH * 2)
traffic_lights_tracing = pygame.rect.Rect(TRAFFIC_LIGHTS_X, TRAFFIC_LIGHTS_Y,
                                          TRAFFIC_LIGHTS_WIDTH, TRAFFIC_LIGHTS_HEIGHT)

LIGHTS_POSITIONS = (
    (TRAFFIC_LIGHTS_X + TRAFFIC_LIGHTS_WIDTH // 2, TRAFFIC_LIGHTS_Y + TRAFFIC_LIGHTS_HEIGHT // 3 * 2.5),
    (TRAFFIC_LIGHTS_X + TRAFFIC_LIGHTS_WIDTH // 2, TRAFFIC_LIGHTS_Y + TRAFFIC_LIGHTS_HEIGHT // 3 * 0.5),
    (TRAFFIC_LIGHTS_X + TRAFFIC_LIGHTS_WIDTH // 2, TRAFFIC_LIGHTS_Y + TRAFFIC_LIGHTS_HEIGHT // 3 * 1.5)
)
LIGHTS = (('green', 6), ('red', 2), ('yellow', 2))
current_light = 0

COUNT_ROADS = 5 * 2
ROAD_WIDTH = (WINDOW_WIDTH - TRAFFIC_LIGHTS_WIDTH) // COUNT_ROADS
ROAD_COLOR = 'black'
CAR_WIDTH = ROAD_WIDTH // 2
CAR_HEIGHT = 40
ROAD_X = ROAD_WIDTH // 2 - CAR_WIDTH // 2
CAR_COLOR = 'blue'
CAR_CAN_MOVE_LIGHT = 0
RIGHT_ROADS = (ROAD_WIDTH * (COUNT_ROADS // 2 - 1) + ROAD_X, ROAD_WIDTH * (COUNT_ROADS - 1) + ROAD_X + TRAFFIC_LIGHTS_WIDTH)
LEFT_ROADS = (ROAD_WIDTH * COUNT_ROADS // 2 + ROAD_X + TRAFFIC_LIGHTS_WIDTH, ROAD_X)
cars = []

for _ in range(3):
    car_x = randint(0, COUNT_ROADS - 1) * ROAD_WIDTH + ROAD_X
    if car_x > ROAD_WIDTH * COUNT_ROADS // 2:
        car_x += TRAFFIC_LIGHTS_WIDTH
    cars.append((pygame.rect.Rect(car_x, WINDOW_HEIGHT, CAR_WIDTH, CAR_HEIGHT), randint(2, 5)))

time_spawn_car = 0
last_switch = pygame.time.get_ticks()
interval = LIGHTS[current_light][1] * 1000

while True:
    window.fill(WINDOW_COLOR)
    pygame.Clock().tick(FPS)
    time_spawn_car += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    for i in range(COUNT_ROADS):
        road_x = i * ROAD_WIDTH + (TRAFFIC_LIGHTS_WIDTH if i >= COUNT_ROADS // 2 else 0)
        pygame.draw.rect(window, ROAD_COLOR, pygame.rect.Rect(road_x + ROAD_WIDTH // 10, 0,
                                                                        ROAD_WIDTH - ROAD_WIDTH // 5, WINDOW_HEIGHT))

    now = pygame.time.get_ticks()
    if now - last_switch >= interval:
        current_light = (current_light + 1) % 3
        last_switch = now

    interval = LIGHTS[current_light][1] * 1000

    if time_spawn_car >= 100:
        time_spawn_car = 0
        car_x = randint(0, COUNT_ROADS - 1) * ROAD_WIDTH + ROAD_X
        if car_x > ROAD_WIDTH * COUNT_ROADS // 2:
            car_x += TRAFFIC_LIGHTS_WIDTH
        cars.append((pygame.rect.Rect(car_x, WINDOW_HEIGHT, CAR_WIDTH, CAR_HEIGHT), randint(2, 5)))

    for car in list(cars):
        pygame.draw.rect(window, CAR_COLOR, car[0])
        if current_light == CAR_CAN_MOVE_LIGHT:
            car[0].y -= car[1]
            if randint(0, 100) == 0 and car[0].x not in RIGHT_ROADS:
                car[0].x += ROAD_WIDTH
            if randint(0, 100) == 0 and car[0].x not in LEFT_ROADS:
                car[0].x -= ROAD_WIDTH
        if car[0].y > WINDOW_HEIGHT:
            cars.remove(car)

    pygame.draw.rect(window, TRAFFIC_LIGHTS_COLOR_TRACING, traffic_lights_tracing)
    pygame.draw.rect(window, TRAFFIC_LIGHTS_COLOR, traffic_lights)

    for i in range(3):
        color = TRAFFIC_LIGHTS_COLOR_TRACING if current_light != i else LIGHTS[i][0]
        pygame.draw.circle(window, color, LIGHTS_POSITIONS[i], LIGHT_RADIUS)

    pygame.display.update()
