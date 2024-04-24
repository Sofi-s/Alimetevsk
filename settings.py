import pygame
pygame.init()

info = pygame.display.Info()
monitor_width, monitor_height = info.current_w, info.current_h
WIDTH, HEIGHT = monitor_width // 1.2, monitor_height // 1.2
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
PPM = 10.0
TARGET_FPS = 60
TIME_STEP = 0.02