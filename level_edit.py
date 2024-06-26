import pygame
import pickle
from os import path

pygame.init()

clock = pygame.time.Clock()
fps = 60

# game window
tile_size = 50
cols = 20
margin = 100
screen_width = tile_size * cols
screen_height = (tile_size * cols) + margin

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Level Editor')

# load images into window
background = pygame.image.load('assets/Backgrounds/PinkBG.jpg')
background = pygame.transform.smoothscale(background, screen.get_size())
restart_image = pygame.image.load('assets/Characters/restart_btn.png')
play_image = pygame.image.load('assets/Characters/play-button.png')
exit_image = pygame.image.load('assets/Characters/exit-button.png')
ground = pygame.image.load('assets/Tiles/tile_0002.png')
cakeimg = pygame.image.load('assets/Tiles/tile_0037.png')
candycane = pygame.image.load('assets/Tiles/tile_0041.png')
angryBlock = pygame.image.load('assets/Characters/tile_0011.png')
spike = pygame.image.load('assets/Tiles/tile_0107.png')
exit_image = pygame.image.load('assets/Characters/exit.png')
save_image = pygame.image.load('assets/Characters/save_btn.png')
load_image = pygame.image.load('assets/Characters/load_btn.png')

# define game variables
clicked = False
level = 1

# define colours
white = (255, 255, 255)
green = (144, 201, 120)

font = pygame.font.SysFont('Futura', 24)

# create empty tile list
world_data = []
for row in range(20):
    r = [0] * 20
    world_data.append(r)

# set boundary
for tile in range(0, 20):
    world_data[19][tile] = 2
    world_data[0][tile] = 1
    world_data[tile][0] = 1
    world_data[tile][19] = 1


# function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def draw_grid():
    for c in range(21):
        # vertical lines
        pygame.draw.line(screen, white, (c * tile_size, 0), (c * tile_size, screen_height - margin))
        # horizontal lines
        pygame.draw.line(screen, white, (0, c * tile_size), (screen_width, c * tile_size))


def draw_world():
    for row in range(20):
        for col in range(20):
            if world_data[row][col] > 0:
                if world_data[row][col] == 1:
                    # dirt blocks
                    img = pygame.transform.scale(ground, (tile_size, tile_size))
                    screen.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 2:
                    # grass blocks
                    img = pygame.transform.scale(cakeimg, (tile_size, tile_size))
                    screen.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 3:
                    # enemy blocks
                    img = pygame.transform.scale(angryBlock, (tile_size, int(tile_size * 0.75)))
                    screen.blit(img, (col * tile_size, row * tile_size + (tile_size * 0.25)))
                if world_data[row][col] == 5:
                    # enemy blocks
                    img = pygame.transform.scale(candycane, (tile_size, int(tile_size * 0.75)))
                    screen.blit(img, (col * tile_size, row * tile_size + (tile_size * 0.25)))
                if world_data[row][col] == 6:
                    # lava
                    img = pygame.transform.scale(spike, (tile_size, tile_size // 2))
                    screen.blit(img, (col * tile_size, row * tile_size + (tile_size // 2)))
                if world_data[row][col] == 8:
                    # exit
                    img = pygame.transform.scale(exit_image, (tile_size, int(tile_size * 1.5)))
                    screen.blit(img, (col * tile_size, row * tile_size - (tile_size // 2)))


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self):
        action = False

        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action


# create load and save buttons
save_button = Button(screen_width // 2 - 150, screen_height - 80, save_image)
load_button = Button(screen_width // 2 + 50, screen_height - 80, load_image)

run = True
while run:

    clock.tick(fps)

    # draw background
    screen.fill(green)
    screen.blit(background, (0, 0))


    # load and save level
    if save_button.draw():
        # save level data
        pickle_out = open(f'level{level}_data', 'wb')
        pickle.dump(world_data, pickle_out)
        pickle_out.close()
    if load_button.draw():
        # load in level data
        if path.exists(f'level{level}_data'):
            pickle_in = open(f'level{level}_data', 'rb')
            world_data = pickle.load(pickle_in)

    # show the grid and draw the level tiles
    draw_grid()
    draw_world()

    # text showing current level
    draw_text(f'Level: {level}', font, white, tile_size, screen_height - 60)
    draw_text('Press UP or DOWN to change level', font, white, tile_size, screen_height - 40)

    # event handler
    for event in pygame.event.get():
        # quit game
        if event.type == pygame.QUIT:
            run = False
        # mouseclicks to change tiles
        if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
            clicked = True
            pos = pygame.mouse.get_pos()
            x = pos[0] // tile_size
            y = pos[1] // tile_size
            # check that the coordinates are within the tile area
            if x < 20 and y < 20:
                # update tile value
                if pygame.mouse.get_pressed()[0] == 1:
                    world_data[y][x] += 1
                    if world_data[y][x] > 8:
                        world_data[y][x] = 0
                elif pygame.mouse.get_pressed()[2] == 1:
                    world_data[y][x] -= 1
                    if world_data[y][x] < 0:
                        world_data[y][x] = 8
        if event.type == pygame.MOUSEBUTTONUP:
            clicked = False
        # up and down key presses to change level number
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                level += 1
            elif event.key == pygame.K_DOWN and level > 1:
                level -= 1

    # update game display window
    pygame.display.update()

pygame.quit()
