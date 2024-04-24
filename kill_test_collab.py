import pygame
import sys
import math
from Box2D.b2 import world, polygonShape, circleShape
from Box2D.b2 import world as box2d_world, polygonShape, circleShape, staticBody, dynamicBody
from catapulta import FlyBird
from settings import *

from functions import screen_to_world, world_to_screen
from primetivs import *
from bd import *
import util

pygame.init()

world = world(gravity=(0, -0.5))

pygame.display.set_caption("Вращение объекта по оси эллипса")
all_sprites = pygame.sprite.Group()  # создаем группу спрайтов
background_image = pygame.image.load('data/space.jpg')
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
WHITE = (255, 255, 255)

planet_sprites = pygame.sprite.Group()
one_planet = pygame.image.load(f'data/{planet}.png')
one_planet = pygame.transform.scale(one_planet, (WIDTH // 1.8, WIDTH // 1.8))

# Параметры эллипса
ellipse_center = [WIDTH // 5.6, HEIGHT // 1.5]
ellipse_width = WIDTH * 1.6
ellipse_height = HEIGHT // 1.05

# image = pygame.image.load('data/moon.png')
# image = pygame.transform.scale(image, (100, 100))
# Угол поворота
angle = 0
MYEVENTTYPE = pygame.USEREVENT + 1
pygame.time.set_timer(MYEVENTTYPE, 12)

create_bird_event = pygame.USEREVENT + 24
pygame.time.set_timer(create_bird_event, 10000)

# all_sprites = pygame.sprite.Group()
angular_speed = 0.000001  # Скорость вращения (радианы за кадр)
bird_sprites = pygame.sprite.Group()
clock = pygame.time.Clock()

class Images(pygame.sprite.Sprite):
    def __init__(self, filename, width, height):
        pygame.sprite.Sprite.__init__(self)
        im = pygame.image.load(filename)
        self.image = pygame.transform.scale(im, (width, height))
        self.rect = self.image.get_rect()


people = Images('data/cosmonaut1.png', 150, 150)
moon = Images('data/moon.png', 150, 150)

all_sprites.add(moon)

# Основной игровой цикл
flag1 = False
moving = 0
line = True
running = True

util.screen = screen
polygonShape.draw = util.my_draw_polygon
circleShape.draw = util.my_draw_circle

center_body = world.CreateStaticBody(
    position=(-40, -20),
    shapes=polygonShape(box=(0.2, 0.2)))
bird = FlyBird(world, bird_sprites, center_body, people.image)

# rect_2 = image.get_rect().center
# rect_1 = bird.center_body()
# collide = rect_2.collidepoint(rect_1)

collections = 0
catapult = pygame.image.load('data/catapult.png')
scale = pygame.transform.scale(
    catapult, (catapult.get_width() // 2,
               catapult.get_height() // 2))
scale_rect = scale.get_rect(center=(world_to_screen((-40, -26))))
screen.blit(scale, scale_rect)

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == MYEVENTTYPE:
            bird_sprites.update()

            all_sprites.update()


        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and moving == 0:
            moving = 1

        if event.type == pygame.MOUSEMOTION:
            if moving == 1:
                bird.mJoint.target = screen_to_world(pygame.mouse.get_pos())

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and moving == 1:
            moving = 2
            world.DestroyJoint(bird.rope)
            world.DestroyJoint(bird.mJoint)
            flag1 = True


        if flag1:
            if (bird.ball_body.position.x - bird.center_body.position.x) ** 2 + (
                    bird.ball_body.position.y - bird.center_body.position.y) ** 2 < 4:
                world.DestroyJoint(bird.joint)
                world.DestroyBody(center_body)
                flag1 = False
                line = False

    screen.fill((0, 0, 0, 0))
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
    # if not collisions:
    moon.rect.center = x, y
    # print(moon.rect, bird.sprite.rect)
    coll = bird.sprite.rect.colliderect(moon.rect)
    # print(coll)

    if coll:
        exit()
    print(bird.sprite.rect)
    if bird.sprite.rect.y < -1000 or bird.sprite.rect.y > 1000:
        center_body = world.CreateStaticBody(
            position=(-40, -20),
            shapes=polygonShape(box=(0.2, 0.2)))
        flag1 = False
        moving = 0
        line = True
        bird = FlyBird(world, bird_sprites, center_body, people.image)
    # #     # screen.blit(moon.image, (x - moon.image.get_width() // 2, y - moon.image.get_height() // 2))
    #     screen.blit(moon.image, 100, 100)


    screen.blit(one_planet, (WIDTH * (-0.1), HEIGHT // 2.5))
    # Обновляем угол поворота
    angle += angular_speed

    # Если угол стал больше 2*pi, то уменьшаем его на 2*pi
    if angle > 2 * math.pi:
        angle -= 2 * math.pi

    util.screen = screen
    polygonShape.draw = util.my_draw_polygon
    circleShape.draw = util.my_draw_circle

    # center_body = world.CreateStaticBody(
    #     position=(-40, -20),
    #     shapes=polygonShape(box=(0.2, 0.2)))
    #
    # bird_sprites = pygame.sprite.Group()
    # # rom catapulta import FlyBird
    # people = pygame.image.load('data/11.png')
    # # image =
    # people = pygame.transform.scale(people, (100, 100))
    # bird = FlyBird(world, bird_sprites, center_body, people)

    # screen.blit(background_image, (0, 0))

    # catapult = pygame.image.load('data/catapult.png')
    # scale = pygame.transform.scale(
    #     catapult, (catapult.get_width() // 2,
    #                catapult.get_height() // 2))
    # scale_rect = scale.get_rect(center=(world_to_screen((-40, -26))))
    screen.blit(scale, scale_rect)

    if line:
        pygame.draw.line(screen, (53, 23, 12), (world_to_screen((-38, -18))), bird.sprite.rect.center, 8)
        pygame.draw.line(screen, (53, 23, 12), (world_to_screen((-42, -18))), bird.sprite.rect.center, 8)

    # world.Step(TIME_STEP, 10, 10)

    world.Step(TIME_STEP, 10, 10)
    all_sprites.update()
    all_sprites.draw(screen)
    bird_sprites.draw(screen)

    # util.draw_bodies(world)
    # Обновляем экран
    pygame.display.flip()

    # Ограничиваем частоту кадров
    clock.tick(60)
# Выход из Pygame
pygame.quit()
sys.exit()
