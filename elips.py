import pygame
import sys
import math
from settings import WIDTH, HEIGHT, screen
from bd import *

pygame.init()

pygame.display.set_caption("Вращение объекта по оси эллипса")

background_image = pygame.image.load('data/space.jpg')
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
WHITE = (255, 255, 255)

world = pygame.image.load(f'data/{planet}.png')
world = pygame.transform.scale(world, (WIDTH // 1.8, WIDTH // 1.8))

# Параметры эллипса
ellipse_center = [WIDTH // 5.6, HEIGHT // 1.5]
ellipse_width = WIDTH * 1.6
ellipse_height = HEIGHT // 1.05

image = pygame.image.load('data/moon.png')
image = pygame.transform.scale(image, (100, 100))
# Угол поворота
angle = 0
angular_speed = 0.008  # Скорость вращения (радианы за кадр)

clock = pygame.time.Clock()

# Основной игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Очистка экрана
    screen.blit(background_image, (0, 0))

    # Рисуем эллипс
    pygame.draw.ellipse(screen, WHITE, (
        ellipse_center[0] - ellipse_width // 2, ellipse_center[1] - ellipse_height // 2, ellipse_width, ellipse_height),
                        1)

    # Вычисляем новые координаты объекта
    x = ellipse_center[0] + ellipse_width // 2 * math.cos(angle)
    y = ellipse_center[1] + ellipse_height // 2 * math.sin(angle)

    # Рисуем объект (красный круг) в новых координатах
    # pygame.draw.circle(screen, RED, (int(x), int(y)), 10)
    screen.blit(image, (x - image.get_width() // 2, y - image.get_height() // 2))
    screen.blit(world, (WIDTH * (-0.1), HEIGHT // 2.5))
    # Обновляем угол поворота
    angle += angular_speed

    # Если угол стал больше 2*pi, то уменьшаем его на 2*pi
    if angle > 2 * math.pi:
        angle -= 2 * math.pi

    # Обновляем экран
    pygame.display.flip()

    # Ограничиваем частоту кадров
    clock.tick(60)

# Выход из Pygame
pygame.quit()
sys.exit()
