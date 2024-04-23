import pygame
import sys
from settings import WIDTH, HEIGHT, screen
from buttons import Button
from x import NewWindow1


# from button import Button
# from level import NewWindow
# import b2.settings
# from b2.settings import SCREEN_HEIGHT, SCREEN_WIDTH, LEVEL_COMPLETED
# from finish_window import FinalWindow


class StartWindow:
    def __init__(self):
        pygame.init()
        self.fon = pygame.image.load("data/fons.jpg")

    def background_image(self):
        self.fon = pygame.transform.scale(self.fon, (WIDTH, HEIGHT))
        self.image = self.fon
        self.width, self.height = self.image.get_width(), self.image.get_height()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("space conquerors")
        self.screen.blit(self.image, (0, 0))

        col_grey = '#C7C7C7'
        y = 80
        y2 = 480
        t = ''
        pygame.mixer.music.load('data/musik.mp3')
        pygame.mixer.music.play()
        #
        # if b2.settings.COUNT == 0:
        #     t = 'Go Return Eggs!'
        # elif b2.settings.COUNT == 1:
        #     t = f'First win & You were able to steal an 1 egg'
        # else:
        #     t = f'Youre the real hen`s killer & You have already returned {b2.settings.COUNT}eggs!'

        # text = t.split('&')
        # for i in text:
        #     i = i.strip()
        #     myFont = pygame.font.SysFont('maiandragd', 33)
        #     myText = myFont.render(i, 1, '#FFEA28')
        #     self.screen.blit(myText, (50, y2))
        #     y2 += 30
        #
        # myFont = pygame.font.SysFont('maiandragd', 17)
        # myText = myFont.render(f'returns eggs: {b2.settings.COUNT}', 1, '#6E5023')
        # self.screen.blit(myText, (1120, 10))

        with open("data/story.txt") as f:
            for i in f:
                i = i.strip()
                myFont = pygame.font.SysFont('maiandragd', 27)
                myText = myFont.render(i, 1, '#f9f7fa')
                self.screen.blit(myText, (0.8*WIDTH, y))
                y += 30
        # pygame.display.update()
        button_level_1 = Button()
        button_level_1.create_button(self.screen, '#F5F5DC', WIDTH/2, (HEIGHT/1.5), WIDTH/7, HEIGHT/15, 1000, "forward to conquer space!", "#1E90FF")
        #
        # button_level_2 = Button()
        # if b2.settings.LEVEL_COMPLETED[0] == 1:
        #     button_level_2.create_button(self.screen, '#FFF9BA', 1133, 160, 100, 50, 0, "level_2", "#1E90FF")
        # else:
        #     button_level_2.create_button(self.screen, col_grey, 1133, 160, 100, 50, 0, "level_2", "#1E90FF")
        #
        # button_level_3 = Button()
        # if b2.settings.LEVEL_COMPLETED[1] == 1:
        #     button_level_3.create_button(self.screen, '#FFF590', 1133, 240, 100, 50, 0, "level_3", "#1E90FF")
        # else:
        #     button_level_3.create_button(self.screen, col_grey, 1133, 240, 100, 50, 0, "level_3", "#1E90FF")
        #
        # button_level_4 = Button()
        # if b2.settings.LEVEL_COMPLETED[2] == 1:
        #     button_level_4.create_button(self.screen, '#FFEE4E', 1133, 320, 100, 50, 0, "level_4", "#1E90FF")
        # else:
        #     button_level_4.create_button(self.screen, col_grey, 1133, 320, 100, 50, 0, "level_4", "#1E90FF")
        #
        # button_level_5 = Button()
        # if b2.settings.LEVEL_COMPLETED[3] == 1:
        #     button_level_5.create_button(self.screen, '#FFEA28', 1133, 400, 100, 50, 0, "level_5", "#1E90FF")
        # else:
        #     button_level_5.create_button(self.screen, col_grey, 1133, 400, 100, 50, 0, "level_5", "#1E90FF")
        #

        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if button_level_1.pressed(pygame.mouse.get_pos()):
                        from main import Game
                        new_window = Game()
                        new_window.run()
                        self.background_image()
        #             elif button_level_2.pressed(pygame.mouse.get_pos()):
        #                 new_window = NewWindow(2, "level 2")
        #                 new_window.run()
        #                 self.background_image()
        #             elif button_level_3.pressed(pygame.mouse.get_pos()):
        #                 new_window = NewWindow(3, "level 3")
        #                 new_window.run()
        #                 self.background_image()
        #             elif button_level_4.pressed(pygame.mouse.get_pos()):
        #                 new_window = NewWindow(4, "level 4")
        #                 new_window.run()
        #                 self.background_image()
        #             elif button_level_5.pressed(pygame.mouse.get_pos()):
        #                 new_window = NewWindow(5, "level 5")
        #                 new_window.run()
        #                 self.background_image()
        #         if sum(LEVEL_COMPLETED) == 5:
        #             print(LEVEL_COMPLETED)
        #             fwindow = FinalWindow()
        #             fwindow.run()
        #             self.background_image()
        #


if __name__ == "__main__":
    window = StartWindow()
    window.background_image()
