# from primitives_v2 import Ball
from functions import *
import util
import pygame
from settings import screen
from classes import ImageSpriteBody

from Box2D.b2 import world, polygonShape, circleShape
from Box2D import b2RopeJointDef


class Ball(ImageSpriteBody, pygame.sprite.Sprite):
    image = pygame.image.load("data/cosmonaut.png")

# class Bird1(AnimatedImageSpriteBody):
#     image = pygame.image.load("data/litle_red_bird.png")

class FlyBird:
    def __init__(self, world, sprite_group, center_body, image):
        self.ball_body = world.CreateDynamicBody(position=(-40, -20))
        self.ball_body.CreateCircleFixture(radius=3, density=10, friction=0.5, restitution=0)

        self.center_body = center_body

        self.sprite = None

        self.joint = world.CreateMotorJoint(bodyA=self.ball_body, bodyB=self.center_body, maxForce=1000,
                                            maxTorque=1000000)

        self.mJoint = world.CreateMouseJoint(bodyA=self.center_body,
                                             bodyB=self.ball_body,
                                             target=self.ball_body.position,
                                             maxForce=50000.0)

        self.rope = world.CreateJoint(b2RopeJointDef(
            bodyA=self.ball_body,
            bodyB=self.center_body,
            maxLength=20,
            localAnchorA=(0, 0),
            localAnchorB=(0, 0)))

        self.sprite = Ball(sprite_group, self.ball_body, img=image)

    def create_ball(position):
        ball_body = world.CreateDynamicBody(position=position)
        ball_body.CreateCircleFixture(radius=5, density=1, friction=0.3, restitution=1)
        Ball(all_sprites, ball_body, scale=True)





def create_ball(position):
    ball_body = world.CreateDynamicBody(position=position)
    ball_body.CreateCircleFixture(radius=5, density=1, friction=0.3, restitution=1)
    Ball(all_sprites, ball_body, scale=True)


if __name__ == "__main__":

    # screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Catapult")
    print(2)
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()

    world = world(gravity=(0, -25))

    util.screen = screen
    polygonShape.draw = util.my_draw_polygon
    circleShape.draw = util.my_draw_circle

    ball_body = world.CreateDynamicBody(position=(-15, -15))
    ball_body.CreateCircleFixture(radius=5, density=1, friction=0.3, restitution=0)

    Ball(all_sprites, ball_body, scale=True)

    center_body = world.CreateStaticBody(
        position=(0, 0),
        shapes=polygonShape(box=(1, 1))
    )
    center_body1 = world.CreateStaticBody(position=(0, 0))
    center_body1.CreateCircleFixture(radius=3, density=1, friction=0.3)

    joint = world.CreateMotorJoint(bodyA=ball_body, bodyB=center_body, maxForce=10000, maxTorque=1000000)

    mJoint = world.CreateMouseJoint(bodyA=center_body,
                                    bodyB=ball_body,
                                    target=ball_body.position,
                                    maxForce=5000000.0)

    rope = world.CreateJoint(b2RopeJointDef(
        bodyA=ball_body,
        bodyB=center_body,
        maxLength=20,
        localAnchorA=(0, 0),
        localAnchorB=(0, 0)))

    flag = True

    running = True
    moving = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                moving = True
            if event.type == pygame.MOUSEMOTION:
                if moving:
                    mJoint.target = screen_to_world(pygame.mouse.get_pos())
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                moving = False
                world.DestroyBody(center_body1)
                world.DestroyJoint(rope)
                world.DestroyJoint(mJoint)

        if flag:
            print(ball_body.position, center_body.position)
            if (ball_body.position.x - center_body.position.x) ** 2 + (
                    ball_body.position.y - center_body.position.y) ** 2 < 4:
                print(1)
                world.DestroyJoint(joint)
                world.DestroyBody(center_body)
                flag = False
        screen.fill((0, 0, 0, 0))
        world.Step(TIME_STEP, 10, 10)
        util.draw_bodies(world)
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(TARGET_FPS)
    pygame.quit()
