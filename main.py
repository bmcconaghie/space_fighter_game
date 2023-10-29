import pygame
import random
import math
from pygame import mixer

# Initializes pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Background Image
background = pygame.image.load('background.jpg')

# Background Sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption('Space Fighter')
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('Fighter.png')
playerX = 370
playerY = 525
playerX_Change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_Change = []
enemyY_Change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('Enemy.png'))
    enemyX.append(random.randint(0, 752))
    enemyY.append(random.randint(50, 150))
    enemyX_Change.append(0.5)
    enemyY_Change.append(48)

# Laser
LaserImg = pygame.image.load('Laser.png')
LaserX = 0
LaserY = 525
LaserX_Change = 0
laserY_Change = 5
laser_state = "ready"

# Score

score_value = 0
font = pygame.font.Font(None, 32)  # Use the default font

textX = 10
textY = 10

# Game Over Text
game_over_font = pygame.font.Font(None, 128)  # Use the default font

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 0))
    screen.blit(score, (x, y))

def game_over_text():
    game_over = game_over_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(game_over, (150, 250))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_laser(x, y):
    global laser_state
    laser_state = "fire"
    screen.blit(LaserImg, (x, y + 10))

def isCollision(enemyX, enemyY, laserX, laserY):
    distance = math.sqrt((enemyX - laserX) ** 2 + (enemyY - laserY) ** 2)
    if distance < 27:
        return True
    else:
        return False

# Game Loop
running = True
while running:

    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle player input
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_Change = -1
            if event.key == pygame.K_RIGHT:
                playerX_Change = 1
            if event.key == pygame.K_SPACE:
                if laser_state == "ready":
                    laser_sound = mixer.Sound('laser.wav')
                    laser_sound.play()
                    LaserX = playerX
                    fire_laser(LaserX, LaserY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_Change = 0

    playerX += playerX_Change

    # Ensure the player stays within the screen boundaries
    if playerX <= 0:
        playerX = 0
    elif playerX >= 752:
        playerX = 752

    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_Change[i]

        # Handle enemy movement and screen boundaries
        if enemyX[i] <= 0:
            enemyX_Change[i] = 0.5
            enemyY[i] += enemyY_Change[i]
        elif enemyX[i] >= 752:
            enemyX_Change[i] = -0.5
            enemyY[i] += enemyY_Change[i]

        # Handle collision
        collision = isCollision(enemyX[i], enemyY[i], LaserX, LaserY)
        if collision:
            explosion_sound = mixer.Sound('explosion.mp3')
            explosion_sound.play()
            LaserY = 525  # Reset laser position
            laser_state = 'ready'
            score_value += 1
            enemyX[i] = random.randint(0, 752)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Handle laser movement
    if LaserY <= 0:
        LaserY = 525
        laser_state = "ready"

    if laser_state == "fire":
        fire_laser(LaserX, LaserY)
        LaserY -= laserY_Change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()