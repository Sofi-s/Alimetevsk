import pygame
import math
from bd import  *
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
            if scale:
                self.init_img = pygame.transform.scale(self.init_img, (w, h))
            else:
                self.init_img = tile(self.init_img, w, h)
        self.image = self.init_img
        self.rect = self.image.get_rect()


class AnimatedImageSpriteBody(SpriteBody):
    image = None

    def __init__(self, group, body, img=None, columns=1, rows=1, scale=False):
        super().__init__(group, body)
        if img is not None:
            self.init_img = img
        else:
            self.init_img = self.__class__.image
        if columns * rows == 1:
            self.frames = [self.init_img]
        else:
            self.frames = self.cut_sheet(img, columns, rows)
        self.cur_frame = 0
        w, h = self.get_size()
        if scale:
            for i in range(len(self.frames)):
                # self.init_img = pygame.transform.scale(self.init_img, (w, h))
                self.frames[i] = pygame.transform.scale(self.frames[i], (w, h))
        else:
            for i in range(len(self.frames)):
                # self.init_img = tile(self.init_img, w, h)
                self.frames[i] = tile(self.frames[i], w, h)
        # self.image = self.init_img
        self.init_img = self.frames[self.cur_frame]
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()

    def cut_sheet(self, sheet, columns, rows):
        rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        frames = []
        for j in range(rows):
            for i in range(columns):
                frame_location = (rect.w * i, rect.h * j)
                frames.append(sheet.subsurface(pygame.Rect(frame_location, rect.size)))
        return frames

    def get_size(self):
        w, h = self.init_img.get_size()
        if isinstance(self.body.fixtures[0].shape, b2CircleShape):
            w = h = self.body.fixtures[0].shape.radius * PPM * 2
        if isinstance(self.body.fixtures[0].shape, b2PolygonShape):
            vertices = self.body.fixtures[0].shape.vertices
            w = int((vertices[2][0] - vertices[0][0]) * PPM)
            h = int((vertices[2][1] - vertices[0][1]) * PPM)
        return w, h

    def update(self, anim=False):
        # print(len(self.frames))
        if anim:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.init_img = self.frames[self.cur_frame]
        super().update()
