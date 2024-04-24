# from primitives_v2 import Ball
from functions import *
import util
import pygame
from settings import screen
from classes import ImageSpriteBody

from Box2D.b2 import world, polygonShape, circleShape
from Box2D import b2RopeJointDef


class Ball(ImageSpriteBody, pygame.sprite.Sprite):
    pass

class FlyBird:
    def __init__(self, world, sprite_group, center_body, image):
        self.ball_body = world.CreateDynamicBody(position=(-40, -20))
        self.ball_body.CreateCircleFixture(radius=3, density=1, friction=0.5, restitution=0)

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


