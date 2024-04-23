# from primitives_v2 import Ball
from functions import *
import util
import pygame
from settings import screen

from Box2D.b2 import world, polygonShape, circleShape
from Box2D import b2RopeJointDef


image = pygame.image.load("data/cosmonaut.png")


# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Catapult")
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


def create_ball(position):
    ball_body = world.CreateDynamicBody(position=position)
    ball_body.CreateCircleFixture(radius=5, density=1, friction=0.3, restitution=1)
    Ball(all_sprites, ball_body, scale=True)


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
