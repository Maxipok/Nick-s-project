import pygame
from pygame.locals import *
import numpy
import random
import time

pygame.init()


PLAYER_COLOR = (0, 0, 0)
SURFACE_COLOR = (167, 255, 100)
GUARD_COLOR = (255, 0, 0)
BUSH_COLOR = (0, 255, 0)
WIDTH = 500
HEIGHT = 500

class Player(pygame.sprite.Sprite):
    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, color, width, height, nipped, jugged):
       # Call the parent class (Sprite) constructor
       pygame.sprite.Sprite.__init__(self)
       # Create an image of the block, and fill it with a color.
       # This could also be an image loaded from the disk.
       self.image = pygame.Surface([width, height])
       self.image.fill(color)
       self.nipped = nipped
       self.jugged = jugged

       # Fetch the rectangle object that has the dimensions of the image
       # Update the position of this object by setting the values of rect.x and rect.y
       self.rect = self.image.get_rect()

class Guard(pygame.sprite.Sprite):
    def __init__(self, color, width, height, bounces):
       pygame.sprite.Sprite.__init__(self)
       self.image = pygame.Surface([width, height])
       self.image.fill(color)

       self.rect = self.image.get_rect()
       self.bounces = bounces

class Bush(pygame.sprite.Sprite):
    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, color, width, height):
       # Call the parent class (Sprite) constructor
       pygame.sprite.Sprite.__init__(self)
       # Create an image of the block, and fill it with a color.
       # This could also be an image loaded from the disk.
       self.image = pygame.Surface([width, height])
       self.image.fill(color)

       # Fetch the rectangle object that has the dimensions of the image
       # Update the position of this object by setting the values of rect.x and rect.y
       self.rect = self.image.get_rect()

class Popwerup(pygame.sprite.Sprite):
    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, color, width, height, taken):
       # Call the parent class (Sprite) constructor
       pygame.sprite.Sprite.__init__(self)
       # Create an image of the block, and fill it with a color.
       # This could also be an image loaded from the disk.
       self.image = pygame.Surface([width, height])
       self.image.fill(color)
       self.taken = taken

       # Fetch the rectangle object that has the dimensions of the image
       # Update the position of this object by setting the values of rect.x and rect.y
       self.rect = self.image.get_rect()

jumps = 1
is_hidden = False
level = 1
size = (WIDTH, HEIGHT)

clock = pygame.time.Clock()

screen = pygame.display.set_mode(size)

time = 0

pygame.display.set_caption(f'Level: {level}, Seconds: {time/100}')

all_sprites_list = pygame.sprite.Group()

guards_list = pygame.sprite.Group()

bushes_list = pygame.sprite.Group()

powerups_list = pygame.sprite.Group()

player = Player(PLAYER_COLOR, 10, 10, False, False)
for i in range(3):
    guard = Guard(GUARD_COLOR, 10, 10, 0)
    guard.rect.x = random.randint(50, 350)
    guard.rect.y = random.randint(50, 350)
    guards_list.add(guard)
    all_sprites_list.add(guard)

bush1 = Bush(BUSH_COLOR, 30, 30)


player.rect.x = 450
player.rect.y = 450



bush1.rect.x = random.randint(50, 350)
bush1.rect.y = random.randint(50, 350)


all_sprites_list.add(player)
all_sprites_list.add(bush1)

bushes_list.add(bush1)

running = True

move = {}
move["up"] = False
move["down"] = False
move["left"] = False
move["right"] = False


while running:
    clock.tick(30)
    time = pygame.time.get_ticks()
    
    screen.fill(SURFACE_COLOR)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # if keydown event happened
            # than printing a string to output
            if event.key == pygame.K_w:
                move["up"] = True
            if event.key == pygame.K_s:
                move["down"] = True
            if event.key == pygame.K_d:
                move["right"] = True
            if event.key == pygame.K_a:
                move["left"] = True
            if event.key == pygame.K_UP and jumps > 0:
                player.rect.y -= 30
                jumps -= 1
            if event.key == pygame.K_DOWN and jumps > 0:
                player.rect.y += 30
                jumps -= 1
            if event.key == pygame.K_RIGHT and jumps > 0:
                player.rect.x += 30
                jumps -= 1
            if event.key == pygame.K_LEFT and jumps > 0:
                player.rect.x -= 30
                jumps -= 1


        if event.type == pygame.KEYUP:
            # if keydown event happened
            # than printing a string to output
            if event.key == pygame.K_w:
                move["up"] = False
            if event.key == pygame.K_s:
                move["down"] = False
            if event.key == pygame.K_d:
                move["right"] = False
            if event.key == pygame.K_a:
                move["left"] = False

    # Actually moving the player character
    if (move["up"]):
        player.rect.y -= 3
    if (move["down"]):
        player.rect.y += 3
    if (move["right"]):
        player.rect.x += 3
    if (move["left"]):
        player.rect.x -= 3


    if (player.rect.x > WIDTH):
        player.rect.x = WIDTH
    if (player.rect.x < 0):
        player.rect.x = 0
    if (player.rect.y > HEIGHT):
        player.rect.y = HEIGHT
    if (player.rect.y < 0):
        player.rect.y = 0

    for bush in bushes_list:
        if pygame.sprite.collide_rect(player, bush):
            is_hidden = True
        else:
            is_hidden = False

    for guard in guards_list:
        if guard.rect.x > 475 or guard.rect.x < 25:
            guard.bounces += 1

        if ((abs(guard.rect.x - player.rect.x) < 100) and (abs(guard.rect.y - player.rect.y) < 100) and not is_hidden):
            if guard.rect.x < player.rect.x and guard.rect.y < player.rect.y:
                guard.rect.x += 5
                guard.rect.y += 5
            elif guard.rect.x < player.rect.x and guard.rect.y > player.rect.y:
                guard.rect.x += 5
                guard.rect.y -= 5
            elif guard.rect.x > player.rect.x and guard.rect.y < player.rect.y:
                guard.rect.x -= 5
                guard.rect.y += 5
            else:
                guard.rect.x -= 5
                guard.rect.x -= 5
        else:
            if guard.bounces % 2 == 0:
                guard.rect.x += 3
            else:
                guard.rect.x -= 3

        if pygame.sprite.collide_rect(guard, player):
            running = False

        if pygame.time.get_ticks() % 1000 == 0 and jumps == 0:
            jumps += 1

        if player.rect.x < 50 and player.rect.y < 50:
            level += 1

            new_guard = Guard(GUARD_COLOR, 10, 10, 0)

            new_guard.rect.x = random.randint(50, 350)
            new_guard.rect.y = random.randint(50, 350)

            all_sprites_list.add(new_guard)

            guards_list.add(new_guard)

            if level < 4:
                new_bush = Bush(BUSH_COLOR, 30, 30)
                new_bush.rect.x = random.randint(50, 350)
                new_bush.rect.y = random.randint(50, 350)

                all_sprites_list.add(new_bush)
                bushes_list.add(new_bush)

            for guard in all_sprites_list:
                guard.rect.x = random.randint(50, 350)
                guard.rect.y = random.randint(50, 350)

            player.rect.x = 450
            player.rect.y = 450

    pygame.draw.circle(screen, (0, 0, 255), (25, 25), 50)

    for sprite in all_sprites_list:
        screen.blit(sprite.image, sprite.rect)

    pygame.display.update()

pygame.quit()
    

