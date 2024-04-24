import pygame
import sys
import math
from settings import WIDTH, HEIGHT, screen
from bd import *
from catapulta import FlyBird
import catapulta
from x import NewWindow1
try:
    class Background:
        def __init__(self, image_file, width, height):
            self.fon = pygame.image.load(image_file)
            self.fon = pygame.transform.scale(self.fon, (width, height))

        def draw(self, screen):
            screen.blit(self.fon, (0, 0))


    class Game:
        def __init__(self):
            pygame.init()
            pygame.display.set_caption("Вращение объекта по оси эллипса")
            self.screen = screen
            self.clock = pygame.time.Clock()
            self.background = Background('data/space.jpg', WIDTH, HEIGHT)
            from elips2 import EllipseObject
            self.ellipse_object = EllipseObject('data/moon.png', (100, 100))
            self.planet = EllipseObject('data/Earth.png', (int(WIDTH / 1.8), int(WIDTH / 1.8)))
            self.planet.rect.topleft = (WIDTH * -0.1, HEIGHT / 2.5)
            self.running = True

        def run(self):
            while self.running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
            self.screen.fill((0, 0, 0))
            self.background.draw(self.screen)
            self.ellipse_object.update()
            self.ellipse_object.draw(self.screen)
            self.planet.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)


            pygame.quit()
            sys.exit()


    if __name__ == "__main__":
        game = Game()
        game.run()
        NewWindow1(game.screen).run()
        # FlyBird()

except Exception as e:
    print(e)
