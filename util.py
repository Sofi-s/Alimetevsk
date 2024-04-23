# import b2
from settings import *
import pygame
from functions import *

from Box2D.b2 import world, polygonShape, circleShape, staticBody, dynamicBody


def create_bound(w):
    world_top = HEIGHT / (2 * PPM)
    world_bottom = -world_top
    world_right = WIDTH / (2 * PPM)
    world_left = -world_right

    bottom_body = w.CreateStaticBody(
        position=(0, world_bottom + 2),
        shapes=polygonShape(box=(world_right - 1, 1))
    )
    top_body = w.CreateStaticBody(
        position=(0, world_top - 2),
        shapes=polygonShape(box=(world_right - 1, 1))
    )
    left_body = w.CreateStaticBody(
        position=(world_left + 2, 0),
        shapes=polygonShape(box=(1, world_top - 1))
    )
    right_body = w.CreateStaticBody(
        position=(world_right - 2, 0),
        shapes=polygonShape(box=(1, world_top - 1))
    )


colors = {
    staticBody: (255, 255, 255, 255),
    dynamicBody: (127, 127, 127, 255)
}
screen = None


def my_draw_polygon(polygon, body, fixture):
    vertices = [(body.transform * v) for v in polygon.vertices]
    vertices = list(map(world_to_screen, vertices))
    pygame.draw.polygon(screen, colors[body.type], vertices)


def my_draw_circle(circle, body, fixture):
    position = body.transform * circle.pos
    position = world_to_screen(position)
    pygame.draw.circle(screen, colors[body.type], [int(x) for x in position],
                       int(circle.radius * PPM))


def draw_bodies(world):
    for body in world.bodies:
        for fixture in body.fixtures:
            fixture.shape.draw(body, fixture)