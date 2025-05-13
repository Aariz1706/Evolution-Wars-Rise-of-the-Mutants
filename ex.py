import pygame
import random

pygame.init()
width, height = 800, 800
FPS = 15
speed_bullet = -10
speed_rock = 10
score = 0
bullets = []
rocks = []
font_over = pygame.font.SysFont(None, 50)
font_menu = pygame.font.SysFont(None , 50)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Rocket Laucher")


clock=pygame.time.Clock()

rocket_img = pygame.image.load("rocket_image.png").convert_alpha()
rocket = pygame.transform.scale(rocket_img , (100,100))
rocket_rect = rocket.get_rect(center=(width//2, height-70))
rocket_mask = pygame.mask.from_surface(rocket)

enemy_img = pygame.image.load("enemy.jpg")
enemy = pygame.transform.scale(enemy_img, (80,80))
enemy_rect = enemy.get_rect(topleft = (100,100))
enemy_mask = pygame.mask.from_surface(enemy)

bullet_img = pygame.Surface((8,10), pygame.SRCALPHA)
bullet_img.fill((255,255,0))
bullet_mask = pygame.mask.from_surface(bullet_img)

# pause = pygame.Rect(width - 120, 60, 120, 120)


# def pause_function():
#     pygame.draw.rect(screen , (120,120,120) , pause)
#     text = font_menu.render("Pause" , True , (255,255,255))
#     screen.blit(text , (pause.x + (pause.width - text.get_width()) // 2, pause.y + (pause.height - text.get_height()) // 2))

def pause_menu():
    while True:
        screen.fill((0,0,0))
        text_for_pause = font_menu.render(f"Game Paused" , True , (255,255,255))
        text_for_resume = font_menu.render(f" R for Resume Game" , True , (255,255,255))
        text_for_quit = font_menu.render(f"Q for Quit Game" , True , (255,255,255))

        screen.blit(text_for_pause, (width//2 - text_for_pause.get_width()//2, height//2 - 100))
        screen.blit(text_for_resume, (width//2 - text_for_resume.get_width()//2, height//2))
        screen.blit(text_for_quit, (width//2 - text_for_quit.get_width()//2, height//2 + 100))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return
                elif event.key == pygame.K_q:
                    pygame.quit()
running = True
while running:

    clock.tick(FPS)
    screen.fill((0,0,0))
    pause = font_menu.render("Press P to Pause", True, (255, 255, 255))
    screen.blit(pause, (10, 10))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running =False
        elif event.type == pygame.KEYDOWN:
            if  event.key == pygame.K_p:
                pause_menu()
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and rocket_rect.left>0:
        rocket_rect.x -= 10
    if keys[pygame.K_RIGHT] and rocket_rect.right< width:
        rocket_rect.x += 10
    if keys[pygame.K_SPACE]:
        if len(bullets)<10:
            bullet_rect = bullet_img.get_rect(center = (rocket_rect.centerx,rocket_rect.top))
            bullets.append(bullet_rect)

    for bullet in bullets[:]:
        bullet.y += speed_bullet
        if bullet.bottom<0:
            bullets.remove(bullet)
        else:
            screen.blit(bullet_img , bullet)

    if random.randint(1,60) == 1:
        rock_rect = enemy.get_rect(topleft = (random.randint(0, width-100) , 0))
        rocks.append(rock_rect)
    for rock in rocks[:]:
        rock.y += speed_rock
        if rock.top>height:
            rocks.remove(rock)
        elif rock.colliderect(rocket_rect):
            offset = (rocket_rect.x - rock.x , rocket_rect.y - rock.y)
            if enemy_mask.overlap(rocket_mask , offset):
                running = False
        screen.blit(enemy , rock)
    for rock in rocks[:]:
        for bullet in bullets[:]:
            if bullet.colliderect(rock):
                offset = (bullet.x - rock.x , bullet.y - rock.y)
                if enemy_mask.overlap(bullet_mask , offset):
                    rocks.remove(rock)
                    bullets.remove(bullet)
                    score += 10
                    break

    screen.blit(rocket, rocket_rect)
    score_checker = font_over.render(f"Score: {score}" , True , (255,255,255))   
    score_rect = score_checker.get_rect(topright = (width -10 , 10))
    screen.blit(score_checker , score_rect)
    pygame.display.flip()

def game_over(score):
    window = pygame.display.set_mode((width , height))
    window.fill((0,0,0))
    text_game = font_over.render(f"GAME OVER" , True , (255,255,255))
    text_score = font_over.render(f"SCORE: {score}" , True , (255,255,255))
    text_game_rect = text_game.get_rect( center = (width//2 , height//2))
    text_score_rect = text_game.get_rect( center = (width//2 , height//2 -100))
    window.blit(text_game , text_game_rect)
    window.blit(text_score , text_score_rect)
    pygame.display.flip()
    pygame.time.wait(3000)
game_over(score)
pygame.quit()