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
NIP_COLOR = (150, 90, 0)
JUG_COLOR = (255, 150, 0)
FIRELORD_COLOR = (255, 150, 0)
WIDTH = 500
HEIGHT = 500

def min(a, b):
    if a < b:
        return a
    else:
        return b

class Player(pygame.sprite.Sprite):
    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, color, width, height, speed, jugged):
       # Call the parent class (Sprite) constructor
       pygame.sprite.Sprite.__init__(self)
       # Create an image of the block, and fill it with a color.
       # This could also be an image loaded from the disk.
       self.image = pygame.Surface([width, height])
       self.image.fill(color)
       self.speed = speed
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
    def __init__(self, color, width, height, type):
       # Call the parent class (Sprite) constructor
       pygame.sprite.Sprite.__init__(self)
       # Create an image of the block, and fill it with a color.
       # This could also be an image loaded from the disk.
       self.image = pygame.Surface([width, height])
       self.image.fill(color)
       self.type = type

       # Fetch the rectangle object that has the dimensions of the image
       # Update the position of this object by setting the values of rect.x and rect.y
       self.rect = self.image.get_rect()

jumps = 1

is_hidden = False

level = 1

score = 0

size = (WIDTH, HEIGHT)

clock = pygame.time.Clock()

screen = pygame.display.set_mode(size)

time = 0


all_sprites_list = pygame.sprite.Group()

guards_list = pygame.sprite.Group()

bushes_list = pygame.sprite.Group()

powerups_list = pygame.sprite.Group()

player = Player(PLAYER_COLOR, 10, 10, 3, False)

for i in range(3):
    if i < 2:
        guard = Guard(GUARD_COLOR, 10, 10, 0)
        guard.rect.x = random.randint(200, 350)
        guard.rect.y = random.randint(200, 350)
    else:
        guard = Guard(GUARD_COLOR, 10, 10, 0)
        guard.rect.x = random.randint(50, 200)
        guard.rect.y = random.randint(50, 200)
    guards_list.add(guard)
    all_sprites_list.add(guard)

for i in range(2):
    if i == 0:
        powerup = Popwerup(NIP_COLOR, 20, 20, "nip")
        powerup.rect.x = random.randint(200, 350)
        powerup.rect.y = random.randint(200, 350)
    else:
        powerup = Popwerup(JUG_COLOR, 20, 20, "jug")
        powerup.rect.x = random.randint(50, 200)
        powerup.rect.y = random.randint(50, 200)
    powerups_list.add(powerup)
    all_sprites_list.add(powerup)

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

jug_time = 0

while running:
    pygame.display.set_caption(f'Level: {level}           Jumps: {jumps}          Score: {score}        Firelord Mode: {str(player.jugged)}')
    clock.tick(30)
    time += 1
    jug_time += 1
    
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
        player.rect.y -= player.speed
    if (move["down"]):
        player.rect.y += player.speed
    if (move["right"]):
        player.rect.x += player.speed
    if (move["left"]):
        player.rect.x -= player.speed


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
                
        if pygame.sprite.collide_rect(guard, player) and not player.jugged:
            running = False

        if pygame.sprite.collide_rect(guard, player) and player.jugged:
            pygame.sprite.Sprite.kill(guard)
            score += 1


    for powerup in powerups_list:
        if pygame.sprite.collide_rect(player, powerup):
            if powerup.type == "jug":
                jug_time = 1
                player.jugged = True
            else:
                player.speed = 5
            pygame.sprite.Sprite.kill(powerup)

    if time % 350 == 0 and jumps == 0:
        jumps += 1
        
    if jug_time % 150 == 0:
        player.jugged = False

    if player.jugged:
        player.image = pygame.Surface([10, 10])
        player.image.fill(FIRELORD_COLOR)

    if player.rect.x < 50 and player.rect.y < 50:
        player.rect.x = 450
        player.rect.y = 450
            
        player.speed = 3
        player.jugged = False

        level += 1

        score += 1

        for guard in guards_list:
            pygame.sprite.Sprite.kill(guard)
    
        for bush in bushes_list:
            pygame.sprite.Sprite.kill(bush)

        for powerup in powerups_list:
            pygame.sprite.Sprite.kill(powerup)

        for i in range(min(level, 3)):
            bush = Bush(BUSH_COLOR, 30, 30)
            bush.rect.x = random.randint(50, 350)
            bush.rect.y = random.randint(50, 350)
            all_sprites_list.add(bush)
            bushes_list.add(bush)

        for i in range(level + 2):
            if i < (level + 3)/2:
                guard = Guard(GUARD_COLOR, 10, 10, 0)
                guard.rect.x = random.randint(200, 350)
                guard.rect.y = random.randint(200, 350)
            else:
                guard = Guard(GUARD_COLOR, 10, 10, 0)
                guard.rect.x = random.randint(50, 200)
                guard.rect.y = random.randint(50, 200)
            guards_list.add(guard)
            all_sprites_list.add(guard)

        for i in range(2):
            if i == 0:
                powerup = Popwerup(NIP_COLOR, 20, 20, "nip")
                powerup.rect.x = random.randint(200, 350)
                powerup.rect.y = random.randint(200, 350)
            else:
                powerup = Popwerup(JUG_COLOR, 20, 20, "jug")
                powerup.rect.x = random.randint(50, 200)
                powerup.rect.y = random.randint(50, 200)
            powerups_list.add(powerup)
            all_sprites_list.add(powerup)


    pygame.draw.circle(screen, (0, 0, 255), (25, 25), 50)

    for sprite in all_sprites_list:
        screen.blit(sprite.image, sprite.rect)

    pygame.display.update()

pygame.quit()
    

