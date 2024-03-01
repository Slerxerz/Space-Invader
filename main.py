import pygame
import random
import math
from pygame import mixer

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_WIDTH = 64

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("images/ufo.png")
pygame.display.set_icon(icon)

# Background
bg = pygame.image.load("images/bg.jpg")

# Player
playerimg = pygame.image.load("images/spaceship.png")
playerx = 370
playery = 500
x_change = 0

# Enemy
no = 6
enemyimg = []
enemyx = []
enemyy = []
e_xchange = []
e_ychange = []
for i in range(no):
    enemyimg.append(pygame.image.load("images/alien.png"))
    enemyx.append(random.randint(0, SCREEN_WIDTH - PLAYER_WIDTH))
    enemyy.append(random.randint(50, 200))
    e_xchange.append(0.1)
    e_ychange.append(40)

# Bullet
bulletimg = pygame.image.load("images/bullet.png")
bulletx = 0
bullety = 500
b_xchange = 0
b_ychange = 0.5
b_state = "ready"

# Score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 28)
textx = 10
texty = 10

# Background Sound
mixer.music.load("audio/background.wav")
mixer.music.play(-1)

# Game Over Font
over_font = pygame.font.Font("freesansbold.ttf", 64)

# Button Images
start_button_img = pygame.image.load("images/start_button.png")
resume_button_img = pygame.image.load("images/resume_button.png")
pause_img = pygame.image.load("images/pause.png")
mute_img = pygame.image.load("images/mute.png")
unmute_img = pygame.image.load("images/unmute.png")
sound_icon = unmute_img
mute = False

# Resize the buttons
start_button_img = pygame.transform.scale(start_button_img, (160, 80))
pause_img = pygame.transform.scale(pause_img, (30, 30))
resume_img = pygame.transform.scale(resume_button_img, (160, 80))
mute_img = pygame.transform.scale(mute_img, (30, 30))
unmute_img = pygame.transform.scale(unmute_img, (30, 30))

# Button Rectangles
start_button_rect = start_button_img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
pause_rect = pause_img.get_rect(topleft=(10, 10))
resume_rect = resume_img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
mute_rect = mute_img.get_rect(topright=(SCREEN_WIDTH - 10, 10))
unmute_rect = unmute_img.get_rect(topright=(SCREEN_WIDTH - 10, 10))

def start_screen():
    global mute
    while True:
        screen.fill((20, 20, 20))
        screen.blit(bg, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    return
                elif mute_rect.collidepoint(event.pos):
                    toggle_sound()
                    mute = not mute

        # Draw start button
        screen.blit(start_button_img, start_button_rect)

        # Draw mute/unmute button based on mute status
        if mute:
            screen.blit(mute_img, mute_rect)
        else:
            screen.blit(unmute_img, unmute_rect)

        pygame.display.update()


def toggle_sound():
    if mixer.music.get_busy():
        mixer.music.pause()
    else:
        mixer.music.unpause()

def update_sound_icon():
    global sound_icon
    if mute:
        sound_icon = mute_img
    else:
        sound_icon = unmute_img

def game_over():
    over_txt = over_font.render("GAME OVER", True, "#efefef")
    screen.blit(over_txt, (200, 250))

def show_score(x, y):
    score = font.render(f"Score: {score_value}", True, "#efefef")
    screen.blit(score, (x, y))

def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))

def player(x, y):
    screen.blit(playerimg, (x, y))

def fire_bullet(x, y):
    global b_state
    b_state = "fire"
    screen.blit(bulletimg, (x + 16, y + 10))

def iscollision(enemyx, enemyy, bulletx, bullety):
    dist = math.sqrt((math.pow(enemyx - bulletx, 2)) + (math.pow(enemyy - bullety, 2)))
    return dist < 27

# Start screen
start_screen()

def pause_screen():
    global mute
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if resume_rect.collidepoint(event.pos):
                    return 'resume'
                elif mute_rect.collidepoint(event.pos):
                    toggle_sound()
                    mute = not mute
                    update_sound_icon()

        screen.fill((20, 20, 20))
        screen.blit(bg, (0, 0))

        # Draw the resume and mute button
        screen.blit(resume_img, resume_rect)

        if mute:
            screen.blit(mute_img, mute_rect)
        else:
            screen.blit(unmute_img, unmute_rect)
        pygame.display.update()

# Game loop
running = True
paused = False
while running:
    screen.fill((20, 20, 20))
    screen.blit(bg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_change -= 0.3
            elif event.key == pygame.K_RIGHT:
                x_change += 0.3
            elif event.key == pygame.K_SPACE:
                if b_state == "ready":
                    if mute==False:
                        bullet_sound = mixer.Sound("audio/lazer.mp3")
                        bullet_sound.play()
                    bulletx = playerx
                    fire_bullet(bulletx, bullety)
            elif event.key == pygame.K_p:
                    paused = not paused        
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                x_change = 0
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pause_rect.collidepoint(event.pos):
                paused = not paused
                if paused:
                    result = pause_screen()
                    if result == "resume":
                        paused = False

    if paused:
        pause_screen()
    else:
        # Player Movement
        playerx += x_change

        if playerx < 0:
            playerx = 0
        elif playerx > (SCREEN_WIDTH - PLAYER_WIDTH):
            playerx = SCREEN_WIDTH - PLAYER_WIDTH

        # Enemy Movement
        for i in range(no):
            if enemyy[i] > 440:
                for j in range(no):
                    enemyy[j] = 2000
                game_over()
                break

            enemyx[i] += e_xchange[i]
            if enemyx[i] < 0:
                enemyx[i] = 0
                e_xchange[i] *= -1
                enemyy[i] += e_ychange[i]
            elif enemyx[i] > (SCREEN_WIDTH - PLAYER_WIDTH):
                enemyx[i] = SCREEN_WIDTH - PLAYER_WIDTH
                e_xchange[i] *= -1
                enemyy[i] += e_ychange[i]

            collision = iscollision(enemyx[i], enemyy[i], bulletx, bullety)
            if collision:
                if mute==False:
                    ex_sound = mixer.Sound("audio/explosion.wav")
                    ex_sound.play()
                bullety = 500
                b_state = "ready"
                score_value += 100
                enemyx[i] = random.randint(0, SCREEN_WIDTH - PLAYER_WIDTH)
                enemyy[i] = random.randint(50, 175)
            enemy(enemyx[i], enemyy[i], i)

        # Bullet Movement
        if bullety <= 0:
            bullety = 500
            b_state = "ready"
        if b_state == "fire":
            fire_bullet(bulletx, bullety)
            bullety -= b_ychange

        show_score(SCREEN_WIDTH - 200, 10)

        screen.blit(pause_img, pause_rect)

        player(playerx, playery)
        
    pygame.display.update()
