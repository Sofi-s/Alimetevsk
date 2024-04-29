import pygame
from settings import *


def world_to_screen(point):
    return (int(point[0] * PPM + WIDTH / 2),
            int(-point[1] * PPM + HEIGHT / 2))


def screen_to_world(point):
    return ((point[0] - WIDTH / 2) / PPM,
            (-point[1] + HEIGHT / 2) / PPM)


def tile(image, w, h):
    result = pygame.Surface((w, h), pygame.SRCALPHA)
    result.fill((255, 255, 255))
    rect = image.get_rect()
    for x in range(0, int(w), int(rect[2])):
        for y in range(0, int(h), int(rect[3])):
            result.blit(image, (x, y))
    return result


if '__name__' == '__main__':
    pass
