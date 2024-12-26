import math

import pygame
from pygame import mixer
import random
# initialize the pygame
pygame.init()
# fps
clock = pygame.time.Clock()
# creating the screen
screen = pygame.display.set_mode((800,600))
# Title and icon
pygame.display.set_caption("Space Invaders")
# background
background = pygame.image.load("space.png")
# background sound
mixer.music.load("bg.mp3")
mixer.music.play(-1)
# Player
playerImgImport = pygame.image.load("spaceship_yellow.png")
playerImage = pygame.transform.scale(playerImgImport, (40,55))
playerX = 370
playerY = 480
playerX_change = 0
# Enemy
enemyImgImport = []
enemyImage = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyImgImport.append(pygame.image.load("spaceship_red.png"))
    enemyImage.append(pygame.transform.rotate(pygame.transform.scale(playerImgImport, (40,55)), 180))
    enemyX.append(random.randint(0,730))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(5)
    enemyY_change.append(30)
# Bullet
bulletImage = pygame.image.load("bullet.png")
# bulletImage = pygame.transform.scale(bulletImgImport, (20,30)),
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 15
bullet_state = "ready"
# score
score_value =0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

def showplayer(x,y):
    screen.blit(playerImage, (x,y))
def showenemy(x,y, i):
    screen.blit(enemyImage[i], (x,y))
def firebullet(x,y):
    global  bullet_state
    bullet_state = "fire"
    screen.blit(bulletImage, (x + 4 , y))
def iscollided(enemyX,enemyY,bulletX,bulletY):
    magnitude = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY- bulletY,2)))
    if magnitude < 27:
        return True
    else:
        return False
def showscore(x,y):
    score = font.render("Score :" + str(score_value), True, (0,255,0))
    screen.blit(score, (x,y))
# gameover text
gameoverfont = pygame.font.Font('freesansbold.ttf', 64)
def gameovertext():
    overtext = gameoverfont.render("Game over", True, (255,255,255))
    screen.blit(overtext,(210,250))
# Game loop
running = True
while running:
    clock.tick(70)
    screen.fill((0,0,0))
    screen.blit(background, (0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -15
            if event.key == pygame.K_RIGHT:
                playerX_change = 15
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletsound = mixer.Sound("Gun+Silencer.mp3")
                    bulletsound.play()
                    bulletX = playerX
                    firebullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    playerX += playerX_change
    if playerX <= 0:
        playerX =0
    elif playerX >= 760:
        playerX = 760
    # enemy movement
    for i in range(num_of_enemies):
        # Game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            gameovertext()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 760:
            enemyX_change[i] = -5
            enemyY[i] += enemyY_change[i]

        # collision
        collided = iscollided(enemyX[i], enemyY[i], bulletX, bulletY)
        if collided:
            collisionsound = mixer.Sound("Grenade+1.mp3")
            collisionsound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 730)
            enemyY[i] = random.randint(50, 150)
        showenemy(enemyX[i], enemyY[i], i)

    if bulletY <=0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        firebullet(bulletX,bulletY)
        bulletY -= bulletY_change
    showscore(textX,textY)
    showplayer(playerX,playerY)


    pygame.display.update()