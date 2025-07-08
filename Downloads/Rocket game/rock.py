import pygame
import sys
import random

pygame.init()
pygame.font.init()

# Constants and Setup
font = pygame.font.SysFont(None, 60)
width, height = 800, 600
score = 0
bullets = []  
rocks = []
rock_speed = 5
bullet_speed = -15

# Setup the game window
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("ROCKET SHOOTER")
clock = pygame.time.Clock()
FPS = 20

# Load images
rocket = pygame.image.load("rocket_image.png").convert_alpha()
rocket = pygame.transform.scale(rocket, (200, 200))
rocket_rect = rocket.get_rect(center=(width // 2, height - 70))
rocket_mask = pygame.mask.from_surface(rocket)

opponent = pygame.image.load("enemy.jpg").convert()
opponent.set_colorkey((255, 255, 255))
opponent = pygame.transform.scale(opponent, (100, 100))
opponent_mask = pygame.mask.from_surface(opponent)

background = pygame.image.load("space_background.jpg").convert()
background = pygame.transform.scale(background, (width, height))

# Create bullet image and mask
bullet_image = pygame.Surface((4, 10), pygame.SRCALPHA)
bullet_image.fill((255, 255, 0))  # Yellow bullet
bullet_mask = pygame.mask.from_surface(bullet_image)

# Main game loop
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle user input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and rocket_rect.left > 0:
        rocket_rect.x -= 10
    if keys[pygame.K_RIGHT] and rocket_rect.right < width:
        rocket_rect.x += 10

    # Bullet firing logic
    if keys[pygame.K_SPACE]:
        if len(bullets) < 5:
            bullet_rect = bullet_image.get_rect(center=(rocket_rect.centerx, rocket_rect.top))
            bullets.append(bullet_rect)

    # Update bullet positions
    for bullet in bullets[:]:
        bullet.y += bullet_speed
        if bullet.bottom < 0:
            bullets.remove(bullet)

    # Create new falling enemy (rock)
    if random.randint(1, 10) == 1:
        rock_rect = opponent.get_rect(topleft=(random.randint(0, width - 100), 0))
        rocks.append(rock_rect)

    # Move rocks
    for rock in rocks[:]:
        rock.y += rock_speed
        if rock.top > height:
            rocks.remove(rock)
        elif rock.colliderect(rocket_rect):
            # Pixel-perfect collision detection
            offset = (rocket_rect.x - rock.x, rocket_rect.y - rock.y)
            if opponent_mask.overlap(rocket_mask, offset):
                running = False  # Game over

    # Bullet-enemy collision
    for rock in rocks[:]:
        for bullet in bullets[:]:
            if rock.colliderect(bullet):
                # Pixel-perfect collision detection
                offset = (bullet.x - rock.x, bullet.y - rock.y)
                if opponent_mask.overlap(bullet_mask, offset):
                    rocks.remove(rock)
                    bullets.remove(bullet)
                    score += 1
                    break

    # Drawing everything
    window.blit(background, (0, 0))
    window.blit(rocket, rocket_rect)
    for bullet in bullets:
        window.blit(bullet_image, bullet)
    for rock in rocks:
        window.blit(opponent, rock)

    pygame.display.flip()

# Game over screen
def show_game_over_screen(score):
    game_over_window = pygame.display.set_mode((width, height))
    game_over_window.fill((0, 0, 0))
    text = font.render(f"Game Over! Score: {score}", True, (255, 255, 255))
    text_rect = text.get_rect(center=(width // 2, height // 2))
    game_over_window.blit(text, text_rect)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                waiting = False

show_game_over_screen(score)
pygame.quit()


