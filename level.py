import pygame
from pygame.locals import *

pygame.init()

# global variables
screen_width = 1000
screen_height = 1000

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Candy Jump')

# define variables for tiles
tile_size = 50

# load images into window
background = pygame.image.load('assets/Backgrounds/PinkBG.jpg')
background = pygame.transform.smoothscale(background, screen.get_size())


# player class for player sprite
class Player:
    def __init__(self, x, y):
        player_image = pygame.image.load('assets/Characters/tile_0003.png')
        self.image = pygame.transform.scale(player_image, (40, 80))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # new variable for gravity/jump
        self.vel_y = 0
        self.jumped = False

    def player_update(self):
        dx = 0
        dy = 0

        # user input to get movement
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and self.jumped == False:
            self.vel_y = -15
            self.jumped = True
        if not key[pygame.K_SPACE]:
            self.jumped = False
        if key[pygame.K_LEFT]:
            dx -= 5
        if key[pygame.K_RIGHT]:
            dx += 5

        # gravity
        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y
        # check for collisions

        # update player coordinates
        self.rect.x += dx
        self.rect.y += dy

        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
            dy = 0

        # draws the player onto the screen
        screen.blit(self.image, self.rect)


class World:
    def __init__(self, data):
        self.tileList = []

        # set images
        ground = pygame.image.load('assets/Tiles/tile_0002.png')
        cakeimg = pygame.image.load('assets/Tiles/tile_0037.png')

        row_count = 0
        for row in data:
            column_count = 0
            for tile in row:
                if tile == 1:
                    image = pygame.transform.scale(ground, (tile_size, tile_size))
                    image_rect = image.get_rect()
                    image_rect.x = column_count * tile_size
                    image_rect.y = row_count * tile_size
                    tile = (image, image_rect)
                    self.tileList.append(tile)
                if tile == 2:
                    image = pygame.transform.scale(cakeimg, (tile_size, tile_size))
                    image_rect = image.get_rect()
                    image_rect.x = column_count * tile_size
                    image_rect.y = row_count * tile_size
                    tile = (image, image_rect)
                    self.tileList.append(tile)
                column_count += 1
            row_count += 1

    def draw_world(self):
        for tile in self.tileList:
            screen.blit(tile[0], tile[1])


world_data = [

    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 1],
    [1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 2, 2, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 7, 0, 5, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 1],
    [1, 7, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7, 0, 0, 0, 0, 1],
    [1, 0, 2, 0, 0, 7, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 2, 0, 0, 4, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 7, 0, 0, 0, 0, 2, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 1],
    [1, 0, 0, 0, 0, 0, 2, 2, 2, 6, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

player = Player(100, screen_height - 130)
world = World(world_data)

run = True
while run:

    screen.blit(background, (0, 0))

    world.draw_world()

    player.player_update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()

pygame.quit()
