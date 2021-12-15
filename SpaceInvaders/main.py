import pygame
from pygame import mixer
import random
import math

#Constants/options
PLAYER_SPEED = 3.5
ENEMY_SPEED = 3
BULLET_SPEED = 10
NUM_OF_ENEMIES = 5


#important vars
score = 0

# Initializing Pygame
pygame.init()


# Creating Screen
screen = pygame.display.set_mode((800,600)) #tuple argument, width x height

# Background Image
background = pygame.image.load('./images/background.png')

# Background Music
mixer.music.load('./sounds/background_music.wav')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('./images/icon.png')
pygame.display.set_icon(icon) #why is this not working? looks like it is not supported on UNIX systems

# Score display
score_font = pygame.font.Font('freesansbold.ttf', 32)
scoreX = 10
scoreY = 10

def show_score(x, y):
    score_text = score_font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (x,y))

# Game Over Text
game_over_font = pygame.font.Font('freesansbold.ttf', 64)

def game_over_text():
    game_over_text = game_over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(game_over_text, (200, 250))

# Player
playerImg = pygame.image.load('./images/player.png')
playerX = 400 - 32
playerY = 480
playerX_change = 0
playerY_change = 0

def player(x, y):
    #boundaries
    if x <= 0:
        x = 0
    elif x >= 800 - 64:
        x = 800 - 64
    
    if y <= 0:
        y = 0
    elif y >= 600 - 64:
        y = 600 - 64
    
    screen.blit(playerImg, (x, y))



# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

for i in range(NUM_OF_ENEMIES):
    enemyImg.append(pygame.image.load('./images/enemy.png'))
    enemyX.append(random.randint(1, 800 - 64))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(ENEMY_SPEED)
    enemyY_change.append(ENEMY_SPEED * 10)

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))



# Bullet
bulletImg = pygame.image.load('./images/bullet.png')
bulletX = 0
bulletY = 480
bulletY_change = BULLET_SPEED
bullet_fired = False

def fire_bullet(x, y):
    global bullet_fired
    bullet_fired = True
    screen.blit(bulletImg, ((x+16, y+10)))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2))))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True

while running:

    #background
    # screen.fill((1, 21, 66)) #color tuple, RGB
    screen.blit(background, (0,0))

    #events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            #right and  left
            if event.key == pygame.K_RIGHT:
                playerX_change = PLAYER_SPEED
            if event.key == pygame.K_LEFT:
                playerX_change = -PLAYER_SPEED

            #up and down
            if event.key == pygame.K_UP:
                playerY_change = -PLAYER_SPEED
            if event.key == pygame.K_DOWN:
                playerY_change = PLAYER_SPEED

            #fire bullet
            if event.key == pygame.K_SPACE and not bullet_fired:
                    bulletX = playerX
                    bulletY = playerY
                    fire_bullet(bulletX, bulletY)
                    
                    #sound effect
                    bullet_sound = mixer.Sound('./sounds/laser.wav')
                    bullet_sound.play()

        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                playerX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0



    #player movement
    playerX += playerX_change
    playerY += playerY_change



    #enemy movement
    for i in range(NUM_OF_ENEMIES):

        #if enemy reaches end line or collides with player
        #clear or reset all entities (moving them out of screen)
        #and display game over text
        if enemyY[i] > 440 or isCollision(enemyX[i], enemyY[i], playerX, playerY):
            for j in range(NUM_OF_ENEMIES):
                enemyY[j] = 2000
            game_over_text()
            playerX = 400 - 32
            playerY = 480
            break

        enemyX[i] += enemyX_change[i] * random.uniform(0.5, 1.5) #randomize enemy speed a bit
    
        #boundaries
        if enemyX[i] <= 0:
            enemyX_change[i] = ENEMY_SPEED
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 800 - 64:
            enemyX_change[i] = -ENEMY_SPEED
            enemyY[i] += enemyY_change[i]

    #collision detection betweem bullet and enemy
        if isCollision(enemyX[i], enemyY[i], bulletX, bulletY):
            bullet_fired = False
            bulletY = 480
            score += 100
            enemyX[i] = random.randint(1, 800 - 64)
            enemyY[i] = random.randint(50,150)

            #sound effect
            explosion_sound = mixer.Sound('./sounds/explosion.wav')
            explosion_sound.play()
        
        #draw enemy
        enemy(enemyX[i], enemyY[i], i)



    #bullet movement
    if bulletY <= 0:
        bullet_fired = False
        bulletY = 480

    if bullet_fired:
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change


    #draw player
    player(playerX, playerY)

    #show score
    show_score(scoreX, scoreY)
    
    pygame.draw.line(screen,(245,230,20),(0,440+64),(800,440+64), 3)

    #update screen
    pygame.display.update() #Run this to update display