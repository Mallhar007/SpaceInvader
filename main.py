import math
import random

import pygame
from pygame import mixer

# initialize pygame
pygame.init()

# create screen
screen = pygame.display.set_mode((800, 600))
backgroundIMG = pygame.image.load('background.png')

# background sound
mixer.music.load('background.wav')
mixer.music.play(-1)


# Title and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('avatar.png')
pygame.display.set_icon(icon)

# Player
playerIMG = pygame.image.load('playerimage.png')
playerX = 368
playerY = 500
playerX_change = 0

# Enemy

# multiple enemies
enemyIMG = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
number_of_enemies = 10

# enemy location
for i in range(number_of_enemies):
    enemyIMG.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 200))
    enemyX_change.append(0.5)
    enemyY_change.append(45)

# Bullet

bulletIMG = pygame.image.load('bullet.png')
bulletX = 368
bulletY = 500
bulletX_change = 0
bulletY_change = 1
bullet_state = "ready"


# Player position on screen
def player(x, y):
    screen.blit(playerIMG, (x, y))


# enemy position on screen

def enemy(x, y, i):
    screen.blit(enemyIMG[i], (x, y))


# Firing bullet
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletIMG, (x + 16, y + 10))  # bullet default position with spaceship


# Collision
def is_collision(bulletX, bulletY, enemyX, enemyY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 32:
        return True


# Score
# number of times enemy killed
score = 0
font = pygame.font.Font("freesansbold.ttf", 16)
text_X = 10
text_Y = 10

def show_score(text_X, text_Y):
    score_value = font.render("SCORE: " + str(score), True, (255, 255, 0))
    screen.blit(score_value, (text_X, text_Y))

# Game Over
game_over_font = pygame.font.Font("freesansbold.ttf", 75)


def game_over():
    game_over_text = game_over_font.render("GAME OVER", True, (255, 255, 0))
    screen.blit(game_over_text, (155, 250))

# Game loop
running = True
while running:

    # screen color RGB
    screen.fill((0, 0, 30))

    # background
    screen.blit(backgroundIMG, (0, 0))



    # quit button code
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # checking keystrokes

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.4
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.4
            if event.key == pygame.K_UP:
                if bullet_state is "ready":
                    bulletX = playerX
                fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # changing player value wrt arrow keys
    playerX += playerX_change

    # enemy continuous movement

    # setting boundaries
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # enemy movement
    for i in range(number_of_enemies):

        # enemy continuous movement
        enemyX[i] += enemyX_change[i]

        if enemyY[i] > 450:
            for j in range(number_of_enemies):
                enemyY[j] = 2000
            game_over()
            break

        if enemyX[i] <= 0:
            enemyX_change[i] = 0.5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.5
            enemyY[i] += enemyY_change[i]

        # calling collision function
        if is_collision(bulletX, bulletY, enemyX[i], enemyY[i]):
            collision_sound = mixer.Sound('death.wav')
            collision_sound.play()
            score += 1
            bulletY = 500
            bullet_state = "ready"
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 200)

        # calling enemy function
        enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    if bulletY <= 0:
        bulletY = 500
        bullet_state = "ready"

    if bullet_state is "fire":
        #bullet_sound = mixer.Sound('missile.wav')
        #bullet_sound.play()
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # calling player function
    player(playerX, playerY)

    # calling score function
    show_score(text_X, text_Y)

    # permanent code to maintain and update display
    pygame.display.update()
