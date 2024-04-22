import os
import random
import math
import pygame
from os import listdir
from os.path import isfile, join

pygame.init()

pygame.display.set_caption('Candy Jump')

# global variables
BG_color = (255, 255, 255)
WIDTH, HEIGHT = 640, 480
FPS = 60
Player_Vel = 5

window = pygame.display.set_mode((WIDTH, HEIGHT))


def main(window):
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(FPS)


if __name__ == '__main__':
    main(window)
