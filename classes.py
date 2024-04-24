import math
from functions import *
from Box2D.Box2D import b2CircleShape, b2PolygonShape


class SpriteBody(pygame.sprite.Sprite):

    def __init__(self, group, body=None):
        super().__init__(group)
        self.body = body
        self.image = None
        self.init_img = None
        self.rect = None

    def update(self):
        if self.body is not None and self.image is not None:
            self.image = pygame.transform.rotate(self.init_img, math.degrees(self.body.angle))
            self.rect = self.image.get_rect()
            self.rect.center = world_to_screen(self.body.position)


class ImageSpriteBody(SpriteBody):
    image = None

    def __init__(self, group, body, img=None, scale=True):
        super().__init__(group, body)
        if img is not None:
            self.init_img = img
        else:
            self.init_img = self.__class__.image
        if isinstance(self.body.fixtures[0].shape, b2CircleShape):
            w = h = self.body.fixtures[0].shape.radius * PPM * 2
            if scale:
                self.init_img = pygame.transform.scale(self.init_img, (w, h))
            else:
                self.init_img = tile(self.init_img, w, h)
        if isinstance(self.body.fixtures[0].shape, b2PolygonShape):
            vertices = self.body.fixtures[0].shape.vertices
            w = int((vertices[2][0] - vertices[0][0]) * PPM)
            h = int((vertices[2][1] - vertices[0][1]) * PPM)
            self.init_img = pygame.transform.scale(self.init_img, (w, h))
        self.image = self.init_img
        self.rect = self.image.get_rect()

