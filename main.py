import pygame
import random
import math
from pygame import mixer

#Initialize the pygame
pygame.init()

#Creating screen
screen= pygame.display.set_mode((800,600))

#Title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("images/ufo.png")
pygame.display.set_icon(icon)

#Background
bg = pygame.image.load("images/bg.jpg")

# Player
playerimg = pygame.image.load("images/spaceship.png")
playerx = 370
playery = 500
x_change = 0

# Enemy
no = 6
enemyimg=[]
enemyx=[]
enemyy=[]
e_xchange=[]
e_ychange=[]
for i in range(no):    
    enemyimg.append(pygame.image.load("images/alien.png"))
    enemyx.append(random.randint(0,736))
    enemyy.append(random.randint(50,200))
    e_xchange.append(0.1)
    e_ychange.append(40)

# Bullet
bulletimg = pygame.image.load("images/bullet.png")
bulletx = 0
bullety = 500
b_xchange = 0
b_ychange = 0.5
b_state="ready"

#Score
score_value = 0
font=pygame.font.Font("freesansbold.ttf",28)
textx=10
texty=10

#Background Sound
mixer.music.load("audio/background.wav")
mixer.music.play(-1)

over_font=pygame.font.Font("freesansbold.ttf",64)

def game_over():
    over_txt=over_font.render("GAME OVER",True,"#efefef")
    screen.blit(over_txt,(200,250))

def show_score(x,y):
    score= font.render(f"Score: {score_value}",True,"#efefef")
    screen.blit(score,(x,y))

def enemy(x,y,i):
    screen.blit(enemyimg[i],(x,y))

def player(x,y):
    screen.blit(playerimg,(x,y))

def fire_bullet(x,y):
    global b_state
    b_state="fire"
    screen.blit(bulletimg,(x+16,y+10))

def iscollision(enemyx,enemyy,bulletx,bullety):
    dist=math.sqrt((math.pow(enemyx-bulletx,2))+(math.pow(enemyy-bullety,2)))
    if dist<27:
        return True
    else:
        return False

#Game loop
running=True
while running:
    
    screen.fill((20,20,20))
    screen.blit(bg,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_change-=0.3
            if event.key == pygame.K_RIGHT:
                x_change+=0.3
            if event.key == pygame.K_SPACE:
                bullet_sound=mixer.Sound("audio/lazer.mp3")
                bullet_sound.play()
                if b_state == "ready":    
                    bulletx=playerx
                    fire_bullet(bulletx,bullety)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                x_change=0

    #Player Movement
    playerx+=x_change  
        
    if playerx<0:
        playerx=0
    if playerx>(736):
        playerx=736

    #Enemy Movement
    for i in range(no):
        if enemyy[i]>440:
            for j in range(no):
                enemyy[j]=2000
            game_over()
            break

        enemyx[i]+=e_xchange[i]
        if enemyx[i]<0:
            enemyx[i]=0
            e_xchange[i]*=-1
            enemyy[i]+=e_ychange[i]
        if enemyx[i]>(740):
            enemyx[i]=740
            e_xchange[i]*=-1
            enemyy[i]+=e_ychange[i]
        collision=iscollision(enemyx[i],enemyy[i],bulletx,bullety)
        if collision:
            ex_sound=mixer.Sound("audio/explosion.wav")
            ex_sound.play()
            bullety=500
            b_state="ready"
            score_value+=1
            enemyx[i] = random.randint(0,736)
            enemyy[i] = random.randint(50,175)
        enemy(enemyx[i],enemyy[i],i)    

    #Bullet Movement
    if bullety<=0:
        bullety=500
        b_state="ready"
    if b_state =="fire":
        fire_bullet(bulletx,bullety)
        bullety-=b_ychange

    show_score(textx,texty)
    player(playerx,playery)
    pygame.display.update()