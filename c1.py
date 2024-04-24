import pygame
import sys

from functions import screen_to_world, world_to_screen
# from catapult import Catapult
# from Box2D.b2 import world as box2d_world, polygonShape, circleShape, staticBody, dynamicBody
from Box2D.b2 import world, polygonShape, circleShape
from elips2 import EllipseObject
import settings
import util
from settings import *
from primetivs import *
from catapulta import FlyBird

pygame.init()
world = world(gravity=(0, -0.5))


class NewWindow1:
    def __init__(self):
        self.screen = screen
        self.fon = pygame.image.load("data/space.jpg")
        self.planet = EllipseObject('data/Earth.png', (int(WIDTH / 1.8), int(WIDTH / 1.8)))
        self.planet.rect.topleft = (WIDTH * -0.1, HEIGHT / 2.5)
        # список для хранения ссылок на спрайты
        self.all_sprites = pygame.sprite.Group()  # создаем группу спрайтов для всех спрайтов
        self.level = 2
        self.c = 0
        self.running = True
        bar_body = world.CreateStaticBody(position=(29, -28), shapes=polygonShape(box=(20, 1)))

    def run(self):
        # bar_body = world.CreateStaticBody(position=(29, -28), shapes=polygonShape(box=(20, 1)))

        self.bricks = []
        self.fon = pygame.transform.scale(self.fon, (1300, 750))
        self.width, self.height = self.fon.get_width(), self.fon.get_height()
        # screen = pygame.display.set_mode((self.width, self.height))
        screen = self.screen
        pygame.display.set_caption("New Window")
        print(1)

        MYEVENTTYPE = pygame.USEREVENT + 1
        pygame.time.set_timer(MYEVENTTYPE, 4)

        create_bird_event = pygame.USEREVENT + 24
        pygame.time.set_timer(create_bird_event, 10000)

        all_sprites = pygame.sprite.Group()

        util.screen = screen
        polygonShape.draw = util.my_draw_polygon
        circleShape.draw = util.my_draw_circle

        center_body = world.CreateStaticBody(
            position=(-40, -20),
            shapes=polygonShape(box=(0.2, 0.2)))

        bird_sprites = pygame.sprite.Group()
        # rom catapulta import FlyBird
        people = pygame.image.load('data/11.png')
        # image =
        people = pygame.transform.scale(people, (100, 100))
        bird = FlyBird(world, bird_sprites, center_body, people)

        flag1 = False
        running = True
        moving = 0
        kill_bird = False
        line = True
        died = False

        # pygame.mixer.music.load('data/chiken_music.mp3')
        # pygame.mixer.music.play()

        catapult = pygame.image.load('data/catapult.png')
        scale = pygame.transform.scale(
            catapult, (catapult.get_width() // 2,
                       catapult.get_height() // 2))
        scale_rect = scale.get_rect(center=(world_to_screen((-40, -26))))
        screen.blit(scale, scale_rect)

        while running:
            # print(RAT.rect.center)
            # if died:
            #     RAT.kill()
            #     world.DestroyBody(RAT.body)
            #     died = False
            # NewWindow2().run2()
            # if RAT.rect.center[1] > settings.SCREEN_HEIGHT:
            # died = True
            #   print('died')# почему не выводится?

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == MYEVENTTYPE:
                    bird_sprites.update()
                    all_sprites.update()

                # if event.type == create_bird_event and kill_bird:
                #     bird.sprite.kill()
                #     world.DestroyBody(bird.sprite.body)
                #     center_body = world.CreateStaticBody(
                #         position=(-40, -20),
                #         shapes=polygonShape(box=(0.2, 0.2)))
                #
                # bird = FlyBird(world, bird_sprites, center_body, "data/cosmonaut.png")
                #     kill_bird = False
                #     line = True
                #     moving = 0

                # реализация катапульты (удаление всех джоинтов для полета птицы)
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
                        kill_bird = True

            screen.fill((0, 0, 0, 0))
            util.draw_bodies(world)
            screen.blit(self.fon, (0, 0))

            catapult = pygame.image.load('data/catapult.png')
            scale = pygame.transform.scale(
                catapult, (catapult.get_width() // 2,
                           catapult.get_height() // 2))
            scale_rect = scale.get_rect(center=(world_to_screen((-40, -26))))
            screen.blit(scale, scale_rect)

            if line:
                pygame.draw.line(screen, (53, 23, 12), (world_to_screen((-38, -18))), bird.sprite.rect.center, 8)
                pygame.draw.line(screen, (53, 23, 12), (world_to_screen((-42, -18))), bird.sprite.rect.center, 8)

            # world.Step(TIME_STEP, 10, 10)

            world.Step(settings.TIME_STEP, 10, 10)
            all_sprites.update()
            all_sprites.draw(screen)
            bird_sprites.draw(screen)
            self.planet.draw(self.screen)
            pygame.display.flip()
            # if self.c == 3 and died:
            #     NewWindow2().run2()
            #     self.level = 2
            # elif self.c == 3 and died == False:

            # clock.tick(TARGET_FPS)


if __name__ == "__main__":
    window = NewWindow1()
    window.run()
