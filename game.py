import pygame
import numpy
import random
import time

def min(a, b):
    if a > b:
        return a
    else:
        return b

PLAYER_COLOR = (0, 0, 0)
SURFACE_COLOR = (167, 255, 100)
GUARD_COLOR = (255, 0, 0)
BUSH_COLOR = (0, 255, 0)
WIDTH = 500
HEIGHT = 500

class Player(pygame.sprite.Sprite):
    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, color, width, height, jumps, is_hidden):
       # Call the parent class (Sprite) constructor
       pygame.sprite.Sprite.__init__(self)
       # Create an image of the block, and fill it with a color.
       # This could also be an image loaded from the disk.
       self.image = pygame.Surface([width, height])
       self.image.fill(color)

       # Fetch the rectangle object that has the dimensions of the image
       # Update the position of this object by setting the values of rect.x and rect.y
       self.rect = self.image.get_rect()

class Guard(pygame.sprite.Sprite):
    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, color, width, height, sees_player, bounces):
       # Call the parent class (Sprite) constructor
       pygame.sprite.Sprite.__init__(self)
       # Create an image of the block, and fill it with a color.
       # This could also be an image loaded from the disk.
       self.image = pygame.Surface([width, height])
       self.image.fill(color)

       # Fetch the rectangle object that has the dimensions of the image
       # Update the position of this object by setting the values of rect.x and rect.y
       self.rect = self.image.get_rect()

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

def main():
    pygame.init()
    level = 1
    size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Level: %i", level)

    all_sprites_list = pygame.sprite.Group()

    player = Player(PLAYER_COLOR, 10, 10, 1, False)
    guard1 = Guard(GUARD_COLOR, 10, 10, False, 0)
    
    player.rect.x = 450
    player.rect.y = 450
    
    guard1.rect.x = random.randint(100, 400)
    guard1.rect.y = random.randint(100, 400)

    all_sprites_list.add(player)
    all_sprites_list.add(guard1)
   
    
    screen.fill(SURFACE_COLOR)

    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.K_w and player_rect.y < 500:
                player_rect.y += 1
            elif event.type == pygame.K_s and player_rect.y > 0:
                player_rect.y -= 1
            elif event.type == pygame.K_d and player_rect.x < 500:
                player_rect.x += 1
            elif event.type == pygame.K_a and player_rect.x > 0:
                player_rect.x -= 1
            elif event.type == pygame.K_UP and player_rect.y < 470 and info_list[1][2] > 0:
                player_rect.y += 30
                info_list[1][2] -= 1
            elif event.type == pygame.K_DOWN and player_rect.y > 30 and info_list[1][2] > 0:
                player_rect.y -= 30
                info_list[1][2] -= 1
            elif event.type == pygame.K_RIGHT and player_rect.x < 470 and info_list[1][2] > 0:
                player_rect.x += 30
                info_list[1][2] -= 1
            elif event.type == pygame.K_LEFT and player_rect.x > 30 and info_list[1][2] > 0:
                player_rect.x -= 30
                info_list[1][2] -= 1
            else:
                player_rect.x += 0

        all_sprites_list.update()
        all_sprites_list.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

    
    
Notes:
    
    
    have main function

make config file for the boring stuff (screen size + linking drawings of sprites to pygame)

make classes: 1 for player, enemies, bush, and powerups

classes inherits from pygame Sprite

Screen.blit


pygame. Sprite group
