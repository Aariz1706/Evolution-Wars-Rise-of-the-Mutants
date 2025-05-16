import pygame
import random
import os
pygame.init()
width, height = 800, 800
FPS = 15
speed_bullet = -10
speed_rocket = 20
speed_rock = 10
speed_enemy_bullet = 20
score = 0
bullets = []
rocks = []
enemy_bullets = []
bonuses = []
power_up = False
power_time = 0
bullet_cooldown = 250
shot_time = 0
level = 1
levelup_score = 100
show_level_time = 2000
level_text = True
font_over = pygame.font.SysFont("impact", 50)
font_menu = pygame.font.SysFont("impact" , 50)
start_time_level = pygame.time.get_ticks()

highscore_file = "highscore.txt"
if os.path.exists(highscore_file):
    with open(highscore_file, "r") as f:
        high_score = int(f.read())
else:
    high_score = 0
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Rocket Laucher")


clock=pygame.time.Clock()
enemy_delay = 1000
last_enemy = pygame.time.get_ticks()

def tint(surface, color):
    tinted = surface.copy()
    tinted.fill(color + (0,), None , pygame.BLEND_RGBA_ADD) # None for filling entire screen
    return tinted

rocket_img = pygame.image.load("rocket_image.png").convert_alpha()
rocket = pygame.transform.scale(rocket_img , (120,120))
rocket_rect = rocket.get_rect(center = (width//2, height-70))
rocket_mask = pygame.mask.from_surface(rocket)

enemy_img = pygame.image.load("enemy_image.png")
enemy = pygame.transform.scale(enemy_img, (100,100))
enemy_rect = enemy.get_rect(topleft = (100,100))
enemy_mask = pygame.mask.from_surface(enemy)

bullet_img = pygame.image.load("bullet_image.png").convert_alpha()
bullet_img = pygame.transform.scale(bullet_img, (30,45))
bullet_img = tint(bullet_img, (255, 255, 0))
bullet_mask = pygame.mask.from_surface(bullet_img)

enemy_bullet_img = pygame.image.load("enemy_bullet.png").convert_alpha()
enemy_bullet_img = pygame.transform.scale(enemy_bullet_img , (25,40))
enemy_bullet_img = tint(enemy_bullet_img , (255,0,0))
enemy_bullet_mask = pygame.mask.from_surface(enemy_bullet_img)

background_img = pygame.image.load("background.jpg").convert()
background_img = pygame.transform.scale(background_img, (width, height))

bonus_img = pygame.image.load("bonus.png").convert_alpha()
bonus_img = pygame.transform.scale(bonus_img, (40, 40))

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

def show_level(level):
    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    font_color = (255,255,255)
    bar_color = (0,0,0,180)
    text = font_over.render(f"---------------Level {level}---------------" , True , font_color)
    text_rect = text.get_rect(center = (width//2 , height//2))
    bar_rect = pygame.Rect(0 , 0 , text_rect.width + 40 , text_rect.height + 20)
    bar_rect.center = text_rect.center
    for alpha in range(0, 256, 15):
        overlay.fill((0, 0, 0, 0))
        pygame.draw.rect(overlay, bar_color, bar_rect, border_radius=15)
        overlay.blit(text, text_rect)
        overlay.set_alpha(alpha)
        screen.blit(background_img, (0, 0))
        screen.blit(overlay, (0, 0))
        pygame.display.flip()
        pygame.time.delay(30)
    pygame.time.delay(1000)
    for alpha in range(255, -1, -15):
        overlay.fill((0, 0, 0, 0))
        pygame.draw.rect(overlay, bar_color, bar_rect, border_radius=15)
        overlay.blit(text , text_rect)
        overlay.set_alpha(alpha)
        screen.blit(background_img, (0, 0))
        screen.blit(overlay, (0, 0))
        pygame.display.flip()
        pygame.time.delay(30)

show_level(level)
running = True
while running:

    clock.tick(FPS)
    screen.blit(background_img, (0,0))
    dark_background = pygame.Surface((width,height))
    dark_background.set_alpha(80)
    dark_background.fill((0,0,0))
    screen.blit(dark_background ,(0,0))

    pause = font_menu.render("Press P to Pause", True, (255, 255, 255))
    screen.blit(pause, (10, 10))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if  event.key == pygame.K_p:
                pause_menu()
    current = pygame.time.get_ticks()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and rocket_rect.left>0:
        rocket_rect.x -= speed_rocket
    if keys[pygame.K_RIGHT] and rocket_rect.right< width:
        rocket_rect.x += speed_rocket
    if keys[pygame.K_SPACE] and current - shot_time > bullet_cooldown:

        if len(bullets)<10: 
            if power_up:
                left_rect = bullet_img.get_rect(center = (rocket_rect.left + 10, rocket_rect.top))
                bullets.append({"rect": left_rect, "dx": -3, "dy": speed_bullet})
                center_rect = bullet_img.get_rect(center=(rocket_rect.centerx, rocket_rect.top))
                bullets.append({"rect": center_rect, "dx": 0, "dy": speed_bullet})
                right_rect = bullet_img.get_rect(center=(rocket_rect.right - 10, rocket_rect.top))
                bullets.append({"rect": right_rect, "dx": 3, "dy": speed_bullet})
            else:
                center_rect = bullet_img.get_rect(center=(rocket_rect.centerx, rocket_rect.top))
                bullets.append({"rect": center_rect, "dx": 0, "dy": speed_bullet})
        shot_time = current
                

    for bullet in bullets[:]:
        bullet["rect"].x += bullet["dx"]
        bullet["rect"].y += bullet["dy"]
        if bullet["rect"].bottom < 0 or bullet["rect"].right < 0 or bullet["rect"].left > width:
            bullets.remove(bullet)
        else:
            screen.blit(bullet_img , bullet["rect"])

    for ebullet in enemy_bullets[:]:
        ebullet.y += speed_enemy_bullet
        if ebullet.top > height:
            enemy_bullets.remove(ebullet)
        else:
            screen.blit(enemy_bullet_img , ebullet)
    for bonus_rect in bonuses[:]:
        bonus_rect.y += 5
        if bonus_rect.top >height:
            bonuses.remove(bonus_rect)
        elif bonus_rect.colliderect(rocket_rect):
            bonuses.remove(bonus_rect)
            power_up = True
            power_time = pygame.time.get_ticks()
            print("BONUSES COLLECTED! DOUBLE UP SPEED")
        screen.blit(bonus_img , bonus_rect)

    if current - last_enemy > enemy_delay:
        rock_rect = enemy.get_rect(topleft = (random.randint(0, width-100), 0))
        rocks.append(rock_rect)
        last_enemy = current
        if level >= 3 and random.randint(1,10) == 1:
            bonus_rect = bonus_img.get_rect(center = (rock_rect.centerx , rock_rect.centery))
            bonuses.append(bonus_rect)  
    for rock in rocks[:]:
        rock.y += speed_rock 
        if level >= 2 and random.randint(1,100) == 1:
            enemy_bullet_rect = enemy_bullet_img.get_rect(midtop = (rock.centerx ,rock.bottom))
            enemy_bullets.append(enemy_bullet_rect)
        if rock.top>height:
            rocks.remove(rock)
        elif rock.colliderect(rocket_rect):
            offset = (rocket_rect.x - rock.x , rocket_rect.y - rock.y)
            if enemy_mask.overlap(rocket_mask , offset):
                running = False
        screen.blit(enemy , rock)
    
    for ebullet in enemy_bullets[:]:
        if ebullet.colliderect(rocket_rect):
            offset = (rocket_rect.x - ebullet.x , rocket_rect.y - ebullet.y)
            if enemy_bullet_mask.overlap(rocket_mask , offset):
                running = False
                enemy_bullets.remove(ebullet) 

    for rock in rocks[:]:
        for bullet in bullets[:]:
            if bullet["rect"].colliderect(rock):
                offset = (bullet["rect"].x - rock.x , bullet["rect"].y - rock.y)
                if enemy_mask.overlap(bullet_mask , offset):
                    rocks.remove(rock)
                    bullets.remove(bullet)
                    score += 10
                    if score >= level * levelup_score:
                        level +=1
                        show_level(level)
                        if level >= 4:
                            speed_rock += 1
                        if enemy_delay > 400:
                            enemy_delay -= 100
                    enemy_delay = max(300 , enemy_delay-10)
                    break

    screen.blit(rocket, rocket_rect)
    score_checker = font_over.render(f"Score: {score}" , True , (255,255,255))   
    score_rect = score_checker.get_rect(topright = (width -10 , 10))
    screen.blit(score_checker , score_rect) 
    high_score_text = font_over.render(f"High Score: {high_score}", True, (255, 215, 0))
    high_score_rect = high_score_text.get_rect(topright=(width - 10, 60))
    screen.blit(high_score_text, high_score_rect)
    if power_up:
        if pygame.time.get_ticks() -power_time > 5000:
            power_up = False
            print("POWER-UP ENDED")
    pygame.display.flip()

def game_over(score):
#     window = pygame.display.set_mode((width , height))
#     window.fill((0,0,0))
#     text_game = font_over.render(f"GAME OVER" , True , (255,255,255))
#     text_score = font_over.render(f"SCORE: {score}" , True , (255,255,255))
#     text_game_rect = text_game.get_rect( center = (width//2 , height//2))
#     text_score_rect = text_game.get_rect( center = (width//2 , height//2 -100))
#     window.blit(text_game , text_game_rect)
#     window.blit(text_score , text_score_rect)
#     pygame.display.flip()
#     pygame.time.wait(3000)
# game_over(score)
    global high_score
    if score > high_score:
        high_score = score
        with open(highscore_file, "w") as f:
            f.write(str(high_score))

    window = pygame.display.set_mode((width , height))
    window.fill((0,0,0))

    text_game = font_over.render("GAME OVER", True, (255, 0, 0))
    text_score = font_over.render(f"SCORE: {score}", True, (255, 255, 255))
    text_high = font_over.render(f"HIGH SCORE: {high_score}", True, (255, 215, 0))

    text_game_rect = text_game.get_rect(center = (width // 2, height // 2 - 60))
    text_score_rect = text_score.get_rect(center = (width // 2, height // 2))
    text_high_rect = text_high.get_rect(center = (width // 2, height // 2 + 60))

    window.blit(text_game, text_game_rect)
    window.blit(text_score, text_score_rect)
    window.blit(text_high, text_high_rect)
    pygame.display.flip()
    pygame.time.wait(3000)  
game_over(score)
pygame.quit()
