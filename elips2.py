import pygame
import sys
import math
from settings import WIDTH, HEIGHT, screen


class EllipseObject:
    def __init__(self, image_file, size):
        self.image = pygame.image.load(image_file)
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()
        self.angle = 0
        self.angular_speed = 0.008
        self.ellipse_center = [WIDTH // 5.6, HEIGHT // 1.5]
        self.running = True
        self.ellipse_width = WIDTH * 1.6
        self.ellipse_height = HEIGHT // 1.05

    def update(self):
        self.angle += self.angular_speed
        if self.angle > 2 * math.pi:
            self.angle -= 2 * math.pi
        x = self.ellipse_center[0] + self.ellipse_width // 2 * math.cos(self.angle)
        y = self.ellipse_center[1] + self.ellipse_height // 2 * math.sin(self.angle)
        self.rect.center = (x, y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False


EllipseObject('data/moon.png', (1000, 1000)).run()
