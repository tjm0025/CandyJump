import pygame
from pygame.locals import *
import pickle
from os import path

pygame.init()

# screen variables
screen_width = 1000
screen_height = 1000

# set clock speed
clock = pygame.time.Clock()

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Candy Jump')

# define variables (global)
tile_size = 50
game_over = 0
menu = True
level = 1
max_levels = 3

# image sizes
default_image_sz = (100, 100)

# load images into window
background = pygame.image.load('assets/Backgrounds/PinkBG.jpg')
background = pygame.transform.smoothscale(background, screen.get_size())
restart_image = pygame.image.load('assets/Characters/restart_btn.png')
play_image = pygame.image.load('assets/Characters/play-button.png')
exit_image = pygame.image.load('assets/Characters/exit-button.png')

# resize buttons
play_image = pygame.transform.scale(play_image, default_image_sz)
exit_image = pygame.transform.scale(exit_image, default_image_sz)


# functions
def reset_level(level):
    player.restart(100, screen_height - 130)
    angryBlock_group.empty()
    spikeGroup.empty()
    exitGroup.empty()

    if path.exists(f'level{level}_data'):
        pickle_in = open(f'level{level}_data', 'rb')
        world_data = pickle.load(pickle_in)
    world = World(world_data)

    return world



class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False

        position = pygame.mouse.get_pos()

        if self.rect.collidepoint(position):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # button draw
        screen.blit(self.image, self.rect)

        return action


# player class for player sprite
class Player:
    def __init__(self, x, y):
        self.restart(x, y)

    def player_update(self, game_over):
        dx = 0
        dy = 0

        if game_over == 0:
            # user input to get movement
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jumped == False and self.limit_jump == False:
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
            self.limit_jump = True
            for tile in world.tileList:
                # check for x collision
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                # check y direction collisions
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    # check if below the ground (jumping)
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    # check if above the ground (jumping)
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.limit_jump = False

            # check for collision with enemies
            if pygame.sprite.spritecollide(self, angryBlock_group, False):
                game_over = -1

            # check collision with spikes
            if pygame.sprite.spritecollide(self, spikeGroup, False):
                game_over = -1

            # check collision with exit
            if pygame.sprite.spritecollide(self, exitGroup, False):
                game_over = 1

            # update player coordinates
            self.rect.x += dx
            self.rect.y += dy

        elif game_over == -1:
            self.image = self.dead_image
            if self.rect.y > 200:
                self.rect.y -= 5

        # draws the player onto the screen
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

        return game_over

    def restart(self, x, y):
        player_image = pygame.image.load('assets/Characters/tile_0003.png')
        self.image = pygame.transform.scale(player_image, (40, 80))
        self.dead_image = pygame.image.load('assets/Characters/ghost.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        # new variable for gravity/jump
        self.vel_y = 0
        self.jumped = False
        self.limit_jump = True


class World:
    def __init__(self, data):
        self.tileList = []

        # set images
        ground = pygame.image.load('assets/Tiles/tile_0002.png')
        cakeimg = pygame.image.load('assets/Tiles/tile_0037.png')
        candycane = pygame.image.load('assets/Tiles/tile_0041.png')

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
                if tile == 3:
                    angryBlock = Enemies(column_count * tile_size, row_count * tile_size + 15)
                    angryBlock_group.add(angryBlock)
                if tile == 5:
                    image = pygame.transform.scale(candycane, (tile_size, tile_size))
                    image_rect = image.get_rect()
                    image_rect.x = column_count * tile_size
                    image_rect.y = row_count * tile_size
                    tile = (image, image_rect)
                    self.tileList.append(tile)
                if tile == 6:
                    spike = WhippedSpike(column_count * tile_size, row_count * tile_size + (tile_size // 2))
                    spikeGroup.add(spike)
                if tile == 8:
                    exit = Exit(column_count * tile_size, row_count * tile_size - (tile_size // 2))
                    exitGroup.add(exit)
                column_count += 1
            row_count += 1

    def draw_world(self):
        for tile in self.tileList:
            screen.blit(tile[0], tile[1])
            pygame.draw.rect(screen, (255, 255, 255), tile[1], 2)


class Enemies(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/Characters/tile_0011.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1


class WhippedSpike(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('assets/Tiles/tile_0107.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('assets/Characters/exit.png')
        self.image = pygame.transform.scale(img, (tile_size, int(tile_size * 1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


player = Player(100, screen_height - 130)

angryBlock_group = pygame.sprite.Group()
spikeGroup = pygame.sprite.Group()
exitGroup = pygame.sprite.Group()

# loading level info
if path.exists(f'level{level}_data'):
    pickle_in = open(f'level{level}_data', 'rb')
    world_data = pickle.load(pickle_in)
world = World(world_data)

# create buttons
restart_button = Button(screen_width // 2 - 50, screen_height // 2 + 100, restart_image)
play_button = Button(screen_width // 2 - 350, screen_height // 2, play_image)
exit_button = Button(screen_width // 2 + 350, screen_height // 2, exit_image)

run = True
while run:

    # set FPS limit
    clock.tick(60)
    fps = str(int(clock.get_fps()))
    # SET BACKGROUND IMAGE
    screen.blit(background, (0, 0))

    if menu == True:
        if exit_button.draw():
            run = False
        if play_button.draw():
            menu = False
    else:
        # draw world
        world.draw_world()

        if game_over == 0:
            # draw enemies/update enemies
            angryBlock_group.update()

        angryBlock_group.draw(screen)
        spikeGroup.draw(screen)
        exitGroup.draw(screen)
        # update player location, status, etc
        game_over = player.player_update(game_over)

        # if players dies
        if game_over == -1:
            if restart_button.draw():
                player.restart(100, screen_height - 130)
                game_over = 0
        # if player beats level
        if game_over == 1:
            # got to next level
            level += 1
            if level <= max_levels:
                # reset
                world_data = []
                world = reset_level(level)
                game_over = 0
            else:
                # restart
                pass
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False  # quit game
    pygame.display.update()

pygame.quit()
