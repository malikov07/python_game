import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Load and resize images
player_image = pygame.image.load("img/rocket.png")
player_image = pygame.transform.scale(player_image, (150, 100))
enemy_image = pygame.image.load("img/enemy.png")
enemy_image = pygame.transform.scale(enemy_image, (70, 100))
bullet_image = pygame.image.load("img/bullet.png")
bullet_image = pygame.transform.scale(bullet_image, (30, 40))

# Background image
background_image = pygame.image.load("img/background.jpg")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Sizes for collision detection and positioning
player_size = player_image.get_size()
enemy_size = enemy_image.get_size()
bullet_size = bullet_image.get_size()

# Player settings
player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150]
player_speed = 7

# Bullet settings
bullets = []

# Enemy settings
enemies = []

# FPS controller
clock = pygame.time.Clock()
FPS = 90

def draw_background():
    screen.blit(background_image, (0, 0))

def draw_player(pos):
    screen.blit(player_image, pos)

def draw_bullet(pos):
    screen.blit(bullet_image, pos)

def draw_enemy(pos):
    screen.blit(enemy_image, pos)

def create_enemy():
    enemy_x = random.randint(0, SCREEN_WIDTH - enemy_size[0])
    enemy_y = random.randint(-200, -50)
    return [enemy_x, enemy_y]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet_x = player_pos[0] + player_size[0] // 2 - bullet_size[0] // 2
                bullet_y = player_pos[1]
                bullets.append([bullet_x, bullet_y])

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT] and player_pos[0] < SCREEN_WIDTH - player_size[0]:
        player_pos[0] += player_speed

    bullets = [[x, y - 7] for x, y in bullets if y > 0]

    enemies = [[x, y + 3] for x, y in enemies if y < SCREEN_HEIGHT]
    if random.randint(0, 100) < 3:
        enemies.append(create_enemy())

    bullets_to_remove = []
    enemies_to_remove = []
    for bullet in bullets:
        for enemy in enemies:
            if (bullet[0] < enemy[0] + enemy_size[0] and bullet[0] + bullet_size[0] > enemy[0] and
                    bullet[1] < enemy[1] + enemy_size[1] and bullet[1] + bullet_size[1] > enemy[1]):
                bullets_to_remove.append(bullet)
                enemies_to_remove.append(enemy)
    bullets = [b for b in bullets if b not in bullets_to_remove]
    enemies = [e for e in enemies if e not in enemies_to_remove]

    screen.fill((0, 0, 0))  # Fill the screen with black
    draw_background()
    for bullet in bullets:
        draw_bullet(bullet)
    for enemy in enemies:
        draw_enemy(enemy)
    draw_player(player_pos)

    pygame.display.flip()
    clock.tick(FPS)
