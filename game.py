import pygame
from pygame.locals import *
import numpy
import random
import time
from config import *
from classes import *

# starts pygame
pygame.init()


#defines player, makes the all_sprites_list, makes the sublists for the other classes
player = Player(PLAYER, 5, False)

all_sprites_list = pygame.sprite.Group()

all_sprites_list.add(player)

guards_list = pygame.sprite.Group()

bushes_list = pygame.sprite.Group()

powerups_list = pygame.sprite.Group()


# minimum helper function
def min(a, b):
    if a < b:
        return a
    else:
        return b

#generate level helper function
def generate_level(level):              
        player.rect.x = 1200
        player.rect.y = 650

        player.speed = 5

        player.jugged = False

        for i in range(min(level + 2, 5)):
            bush = Bush(BUSH)
            bush.rect.x = random.randint(200, 1000)
            bush.rect.y = random.randint(100, 500)
            all_sprites_list.add(bush)
            bushes_list.add(bush)

        for i in range(level + 2):
            guard = Guard(GUARD, 0)
            guard.rect.x = random.randint(0, 1000)
            if i < (level + 3)/2:
                guard.rect.y = random.randint(360, 500)
            else:
                guard.rect.y = random.randint(50, 360)
            guards_list.add(guard)
            all_sprites_list.add(guard)

        for i in range(2):
            if i == 0:
                powerup = Powerup(FIRENIP, "nip")
                powerup.rect.x = random.randint(690, 1100)
                powerup.rect.y = random.randint(360, 670)
            else:
                powerup = Powerup(FIREJUG, "jug")
                powerup.rect.x = random.randint(160, 690)
                powerup.rect.y = random.randint(160, 360)
            powerups_list.add(powerup)
            all_sprites_list.add(powerup)

#sets initial state of the game, such as the number of jumps the player has,
#whether the player is hidden, the level, the score, the time, and the initial sprites, etc
jumps = 1

is_hidden = False

move = {}
move["up"] = False
move["down"] = False
move["left"] = False
move["right"] = False

level = 1

generate_level(level)

score = 0

clock = pygame.time.Clock()

screen = pygame.display.set_mode(SCREEN_SIZE)

time = 0
jug_time = 0

#initializes font variables for later text
font1 = pygame.font.SysFont(pygame.font.get_default_font(), 100)
font2 = pygame.font.SysFont(pygame.font.get_default_font(), 50)
font3 = pygame.font.SysFont(pygame.font.get_default_font(), 150)

#sets directions to true so that the directions page is displayed
#sets running and End to false so the game does not display
directions = True
running = False
End = False


#Directions text page; loops over directions list and displays each member at new line.  
#Exit if you press the exit button, transitions to actual game if you press any key
while directions:
    screen.fill((0, 0, 0))
    pygame.font.init() 
    for i in range(len(instructions)):
        if i == 0:
            text_surface = font1.render(instructions[i], False, (0, 255, 0))
            screen.blit(text_surface, (500, 0))
        elif i == 1:
            text_surface = font2.render(instructions[i], False, (0, 255, 0))
            screen.blit(text_surface, (0, 100))
        elif i < len(instructions) - 1:
            text_surface = font2.render(instructions[i], False, (0, 255, 0))
            screen.blit(text_surface, (0, 50 + 50 * i))
        else:
            text_surface = font1.render(instructions[i], False, (0, 255, 0))
            screen.blit(text_surface, (300, 100 + 50 * i))


    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            running = True
            directions = False
        if event.type == pygame.QUIT:
            directions = False
            running = False
            End = False
    pygame.display.update()


#actual game
while running:

    #clock tick
    clock.tick(30)

    #time increments
    time += 1
    jug_time += 1
    
    #fills the screen
    screen.blit(BACKGROUND, (0, 0))

    #detection of inputs
    for event in pygame.event.get():

        #exits if you press exit
        if event.type == pygame.QUIT:
            running = False
            End = False

        #Detection of keypresses, and implementation of teleport ability
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                move["up"] = True
            if event.key == pygame.K_s:
                move["down"] = True
            if event.key == pygame.K_d:
                move["right"] = True
            if event.key == pygame.K_a:
                move["left"] = True
            if event.key == pygame.K_UP and jumps > 0:
                player.rect.y -= 120
                jumps -= 1
            if event.key == pygame.K_DOWN and jumps > 0:
                player.rect.y += 120
                jumps -= 1
            if event.key == pygame.K_RIGHT and jumps > 0:
                player.rect.x += 120
                jumps -= 1
            if event.key == pygame.K_LEFT and jumps > 0:
                player.rect.x -= 120
                jumps -= 1

        #detection of key releases
        if event.type == pygame.KEYUP:
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


    #makes sure the player doesn't go off the screen
    if (player.rect.x > SCREEN_WIDTH):
        player.rect.x = SCREEN_WIDTH
    if (player.rect.x < 0):
        player.rect.x = 0
    if (player.rect.y > SCREEN_HEIGHT):
        player.rect.y = SCREEN_HEIGHT
    if (player.rect.y < 0):
        player.rect.y = 0

    #sets the hidden variable to true iff the player is in a bush
    if pygame.sprite.spritecollideany(player, bushes_list) == None:
        is_hidden = False
    else:
        is_hidden = True


    #loops over the guards, making them bounce back and forth by default 
    #guards approach the player if the player comes within a certain area of them
    #go to End screen if the guard contacts the player when player not in firelord mode
    #kills the guard and gives the player points if the player contacts them in firelord mode
    for guard in guards_list:
        if guard.rect.x > SCREEN_WIDTH or guard.rect.x < 0:
            guard.bounces += 1

        if ((abs(guard.rect.x - player.rect.x) < 150) and (abs(guard.rect.y - player.rect.y) < 150) and not is_hidden and not player.jugged):
            if guard.rect.x < player.rect.x and guard.rect.y < player.rect.y:
                guard.rect.x += 15
                guard.rect.y += 15
            elif guard.rect.x < player.rect.x and guard.rect.y > player.rect.y:
                guard.rect.x += 15
                guard.rect.y -= 15
            elif guard.rect.x > player.rect.x and guard.rect.y < player.rect.y:
                guard.rect.x -= 15
                guard.rect.y += 15
            else:
                guard.rect.x -= 15
                guard.rect.x -= 15
        else:
            if guard.bounces % 2 == 0:
                guard.rect.x += 10
            else:
                guard.rect.x -= 10
                
        if pygame.sprite.collide_rect(guard, player) and not player.jugged:
            running = False
            End = True
            

        if pygame.sprite.collide_rect(guard, player) and player.jugged:
            pygame.sprite.Sprite.kill(guard)
            score += 1


    #detects if player has gotten powerups, and if so kills them and changes the relevant variables
    for powerup in powerups_list:
        if pygame.sprite.collide_rect(player, powerup):
            if powerup.type == "jug":
                jug_time = 1
                player.jugged = True
            else:
                player.speed = 10
            pygame.sprite.Sprite.kill(powerup)

    #restores jump power after a certain duration if the player has no jumps
    if time % 350 == 0 and jumps == 0:
        jumps += 1
        
    #ends the firelord mode after a certain period of time
    if jug_time % 100 == 0:
        player.jugged = False

    #changes the player's image if in firelord mode
    if player.jugged:
        player.image = PLAYER_JUGGED
    else:
        player.image = PLAYER

    #resets the level with an additional guard if the player gets to the end
    if player.rect.x < 150 and player.rect.y < 150:

        score += level

        level += 1

        for guard in guards_list:
            pygame.sprite.Sprite.kill(guard)
    
        for bush in bushes_list:
            pygame.sprite.Sprite.kill(bush)

        for powerup in powerups_list:
            pygame.sprite.Sprite.kill(powerup)

        generate_level(level)

    #draws everything and updates everything
    screen.blit(PORTAL, (-45,-5))

    for sprite in all_sprites_list:
        screen.blit(sprite.image, sprite.rect)

    Level_display = font2.render(f"Level: {level}", False, (0, 0, 0))
    Score_display = font2.render(f"Score: {score}", False, (0, 0, 0))
    Teleports_display = font2.render(f"Teleports: {jumps}", False, (0, 0, 0))

    screen.blit(Level_display, (1125, 25))
    screen.blit(Score_display, (1125, 75))
    screen.blit(Teleports_display, (1075, 125))


    pygame.display.update()

#Defines end screen, which tells the player their final score
while End:
    screen.fill((0, 0, 0))
    for i in range(2):
        if i == 0:
            text_surface = font3.render(f"YOU LOSE", False, (255, 0, 0))
            screen.blit(text_surface, (400, 50))
        else: 
            text_surface = font3.render(f"SCORE: {score}", False, (255, 0, 0))
            screen.blit(text_surface, (400, 300))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            End = False
    pygame.display.update()

#quits game once out of loop
pygame.quit()
