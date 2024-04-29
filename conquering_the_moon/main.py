import pygame
import sys
import math
from Box2D.b2 import world, polygonShape, circleShape, staticBody, dynamicBody
from catapulta import FlyAstronaut
from settings import *
from catapulta import *
from functions import screen_to_world, world_to_screen


def start_end():
    running_frame = True
    while running_frame:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                running_frame = False


pygame.init()

world = world(gravity=(0, -0.5))
pygame.display.set_caption("Покорение Луны")
all_sprites = pygame.sprite.Group()  # создаем группу спрайтов
background_image = pygame.image.load('data/space.jpg')
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
# загружаем музыку
pygame.mixer.music.load('data/musik.mp3')
pygame.mixer.music.play()

planet_sprites = pygame.sprite.Group()
one_planet = pygame.image.load(f'data/Earth.png')
one_planet = pygame.transform.scale(one_planet, (WIDTH // 1.8, WIDTH // 1.8))

# Параметры эллипса
ellipse_center = [WIDTH // 5.6, HEIGHT // 1.5]
ellipse_width = WIDTH * 1.6
ellipse_height = HEIGHT // 1.05
# Угол поворота
angle = 0
MYEVENTTYPE = pygame.USEREVENT + 1
pygame.time.set_timer(MYEVENTTYPE, 12)

create_fly_event = pygame.USEREVENT + 24
pygame.time.set_timer(create_fly_event, 10000)

angular_speed = 0.0000000000000000001  # Скорость вращения (радианы за кадр)
fly_sprites = pygame.sprite.Group()
clock = pygame.time.Clock()


# класс для загрузки и создания спрайтов
class Images(pygame.sprite.Sprite):
    def __init__(self, filename, width, height):
        pygame.sprite.Sprite.__init__(self)
        im = pygame.image.load(filename)
        self.image = pygame.transform.scale(im, (width, height))
        self.rect = self.image.get_rect()


people = Images('data/cosmonaut1.png', 60, 60)
moon = Images('data/moon.png', 150, 150)
all_sprites.add(moon)

while True:
    # Основной игровой цикл
    flag1 = False
    moving = 0
    count = 0
    line = True
    running = True

    center_body = world.CreateStaticBody(
        position=(-40, -20),
        shapes=polygonShape(box=(0.2, 0.2)))
    im = pygame.image.load("data/cosmonaut1.png")
    fly = FlyAstronaut(world, fly_sprites, center_body, im)

    collections = 0
    catapult = pygame.image.load('data/catapult.png')
    scale = pygame.transform.scale(
        catapult, (catapult.get_width() // 2,
                   catapult.get_height() // 2))
    scale_rect = scale.get_rect(center=(world_to_screen((-40, -26))))

    # start window
    fons = pygame.image.load("data/fons.jfif")
    fons = pygame.transform.scale(fons, (WIDTH, HEIGHT))
    screen.blit(fons, (0, 0))
    pygame.display.flip()
    start_end()

    screen.blit(scale, scale_rect)

    # основной цикл
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MYEVENTTYPE:
                fly_sprites.update()
                all_sprites.update()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and moving == 0:
                moving = 1

            if event.type == pygame.MOUSEMOTION:
                if moving == 1:
                    fly.mJoint.target = screen_to_world(pygame.mouse.get_pos())

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and moving == 1:
                moving = 2
                world.DestroyJoint(fly.rope)
                world.DestroyJoint(fly.mJoint)
                flag1 = True

            if flag1:
                if (fly.ball_body.position.x - fly.center_body.position.x) ** 2 + (
                        fly.ball_body.position.y - fly.center_body.position.y) ** 2 < 4:
                    world.DestroyJoint(fly.joint)
                    world.DestroyBody(center_body)
                    angular_speed += 0.005
                    count += 1
                    flag1 = False
                    line = False

        screen.fill((0, 0, 0, 0))
        screen.blit(background_image, (0, 0))

        # Рисуем эллипс
        pygame.draw.ellipse(screen, (210, 255, 255),
                            (ellipse_center[0] - ellipse_width // 2,
                             ellipse_center[1] - ellipse_height // 2, ellipse_width, ellipse_height), 1)

        # Вычисляем новые координаты объекта
        x = ellipse_center[0] + ellipse_width // 2 * math.cos(angle)
        y = ellipse_center[1] + ellipse_height // 2 * math.sin(angle)

        moon.rect.center = x, y
        coll = fly.sprite.rect.colliderect(moon.rect)
        if coll:
            running = False
            fly.sprite.kill()
            world.DestroyBody(fly.sprite.body)

        # действия при промахе
        if (fly.sprite.rect.y < - HEIGHT or fly.sprite.rect.y > HEIGHT or
                fly.sprite.rect.x < - WIDTH or fly.sprite.rect.x > WIDTH):
            center_body = world.CreateStaticBody(
                position=(-40, -20),
                shapes=polygonShape(box=(0.2, 0.2)))
            flag1 = False
            moving = 0
            line = True
            fly = FlyAstronaut(world, fly_sprites, center_body, people.image)

        screen.blit(one_planet, (WIDTH * (-0.1), HEIGHT // 2.5))
        # Обновляем угол поворота
        angle += angular_speed

        # Если угол  больше 2*pi, то уменьшаем его на 2*pi
        if angle > 2 * math.pi:
            angle -= 2 * math.pi

        screen.blit(scale, scale_rect)

        if line:
            pygame.draw.line(screen, (53, 23, 12), (world_to_screen((-38, -18))), fly.sprite.rect.center, 8)
            pygame.draw.line(screen, (53, 23, 12), (world_to_screen((-42, -18))), fly.sprite.rect.center, 8)

        world.Step(TIME_STEP, 10, 10)
        all_sprites.update()
        all_sprites.draw(screen)
        fly_sprites.draw(screen)

        pygame.display.flip()

        # Ограничиваем частоту кадров
        clock.tick(60)

    # реализация финального окна
    fons = pygame.image.load("data/end.jpg")
    fons = pygame.transform.scale(fons, (WIDTH, HEIGHT))
    t = (f'c {count} попытки, чтобы пройти заново, кликните по экрану')
    myFont = pygame.font.SysFont('tahoma', 33)
    myText = myFont.render(t, 1, 'white')
    screen.blit(fons, (0, 0))
    screen.blit(myText, (WIDTH // 4.75, HEIGHT // 1.12))
    pygame.display.flip()

    start_end()
    pygame.display.flip()

    start_end()

# Выход
pygame.quit()
sys.exit()
