import pygame
import random
import os
import pygame.mixer
pygame.init()
pygame.mixer.init()
width, height = 800, 800
FPS = 15
lives = 3
speed_bullet = -10
speed_rocket = 20
speed_rock = 10
speed_enemy_bullet = 20
enemy_speed_increase = 0.005 
score = 0
bullets = []
rocks = []
enemy_bullets = []
bonuses = []
message = []
power_up = False
power_time = 0
bullet_cooldown = 250
shot_time = 0
boss_count = 0
level = 1
levelup_score = 100
show_level_time = 2000
level_text = True
selected = None
font_over = pygame.font.SysFont("impact", 50)
font_menu = pygame.font.SysFont("impact" , 50)
game_modes = ["Classic" , "Challenge" , "Survival" , "Target Practice" , "One Life"]
start_time_level = pygame.time.get_ticks()

pygame.mixer.music.load("assets/sounds/background_music.mp3")
pygame.mixer.music.play(-1)
shoot_sound = pygame.mixer.Sound("assets/sounds/bullet_shoot.wav")
hit_sound = pygame.mixer.Sound("assets/sounds/hit_enemy.wav")

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Rocket Laucher")


clock=pygame.time.Clock()
enemy_delay = 1000
last_enemy = pygame.time.get_ticks()

def tint(surface, color):
    tinted = surface.copy()
    tinted.fill(color + (0,), None , pygame.BLEND_RGBA_ADD) # None for filling entire screen
    return tinted

def menu(selected_index):
    screen.fill((0,0,0))
    title_font = pygame.font.SysFont("impact" , 80)
    menu_font = pygame.font.SysFont("impact" , 40)
    title_text = title_font.render("Rocket Launcher" , True , (255,255,255))
    screen.blit(title_text , (width // 2 - title_text.get_width() // 2 , 100))
    for i , mode in enumerate(game_modes):
        if i == selected_index:
            color = (255,255,0)
        else:
            color = (255,255,255)
        mode_text = menu_font.render(mode , True , color)
        screen.blit(mode_text , (width // 2 - mode_text.get_width() // 2 , 250+i*60))
    intructions = menu_font.render("Use ↑ ↓ to select mode, Enter to start" , True , (200,200,200))
    screen.blit(intructions , (width // 2 - intructions.get_width() // 2 , height - 100))
    pygame.display.flip()
rocket_img = pygame.image.load("assets/images/rocket_image.png").convert_alpha()
rocket = pygame.transform.scale(rocket_img , (120,120))
rocket_rect = rocket.get_rect(center = (width//2, height-70))
rocket_mask = pygame.mask.from_surface(rocket)

enemy_img = pygame.image.load("assets/images/enemy_image.png")
enemy = pygame.transform.scale(enemy_img, (100,100))
enemy_rect = enemy.get_rect(topleft = (100,100))
enemy_mask = pygame.mask.from_surface(enemy)

bullet_img = pygame.image.load("assets/images/bullet_image.png").convert_alpha()
bullet_img = pygame.transform.scale(bullet_img, (30,45))
bullet_img = tint(bullet_img, (255, 255, 0))
bullet_mask = pygame.mask.from_surface(bullet_img)

enemy_bullet_img = pygame.image.load("assets/images/enemy_bullet.png").convert_alpha()
enemy_bullet_img = pygame.transform.scale(enemy_bullet_img , (25,40))
enemy_bullet_img = tint(enemy_bullet_img , (255,0,0))
enemy_bullet_mask = pygame.mask.from_surface(enemy_bullet_img)

boss_enemy_img = pygame.image.load("assets/images/boss_enemy.png").convert_alpha()
boss_enemy_rect = boss_enemy_img.get_rect()
boss_enemy = None

background_img = pygame.image.load("assets/images/background.jpg").convert()
background_img = pygame.transform.scale(background_img, (width, height))

bonus_img = pygame.image.load("assets/images/bonus.png").convert_alpha()
bonus_img = pygame.transform.scale(bonus_img, (40, 40))

heart_img = pygame.image.load("assets/images/heart.png").convert()
heart_img = pygame.transform.scale(heart_img , (40,40))

class BossEnemy():
    def __init__(self):
        self.image = pygame.transform.scale(boss_enemy_img , (150,150))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(60, 650)
        self.rect.y = -150
        self.health = 4
        self.speed = 2
    def move(self):
        self.rect.y += self.speed
    def draw(self, surface):
        surface.blit(self.image , self.rect)
    def is_off_screen(self):
        return self.rect.top > height
    def health_bar(self, surface):
        width_bar = self.rect.width
        height_bar = 10
        health_ratio = self.health / 4
        bar_rect = pygame.Rect(self.rect.x  , self.rect.y - 15 , width_bar , height_bar)
        health_rect = pygame.Rect(self.rect.x , self.rect.y - 15 , int(width_bar*health_ratio), height_bar)
        pygame.draw.rect(surface , (255,0,0) , bar_rect)
        pygame.draw.rect(surface , (0,255,0) , health_rect)

def level_bosses(level):
    if level == 2:
        return 1
    elif level in [3,4]:
        return 2
    else:
        return 2 + ((level-3)//2)
    
def boss_showing(level):
    global boss_enemy ,boss_count
    maximum_boses = level_bosses(level)
    if boss_enemy is None and boss_count < maximum_boses and level >= 2:
        boss_enemy = BossEnemy()
        boss_count += 1

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

def add_message(text , duration = 8000):
    message.append({"text" : text , "time" : pygame.time.get_ticks() , 'duration' : duration})

def game_over(score):
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

selected_mode_index = 0
options = True
while options:
    clock.tick(FPS)
    if selected == "Challenge":
        game_duration = 60000
        if pygame.time.get_ticks() - start_duration > game_duration:
            running = False  
    elif selected == "Survival":
        speed_rock += enemy_speed_increase
    elif selected == "One Life":
        lives = 1
    elif selected == "Target Practice":
        enemy_delay = 500
    menu(selected_mode_index)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                selected_mode_index = (selected_mode_index-1) % len(game_modes)
            elif event.key == pygame.K_DOWN:
                selected_mode_index = (selected_mode_index+1) % len(game_modes)
            elif event.key == pygame.K_RETURN:
                selected = game_modes[selected_mode_index]
                options = False
                highscore_file = f"highscore_{selected}.txt"
                if os.path.exists(highscore_file):
                    with open(highscore_file, "r") as f:
                        high_score = int(f.read())
                else:
                    high_score = 0
                if selected == "Challenge":
                    start_duration = pygame.time.get_ticks()
                elif selected == "Survival":
                    speed_rock = 9
                    enemy_speed_increase = 0.01
                elif selected == "One Life":
                    lives = 1
                elif selected == "Target Practice":
                    enemy_delay = 500
                    speed_rock = 5  
                    boss_count = 1000
show_level(level)

running = True
while running:

    clock.tick(FPS)


    if selected == "Survival":
        speed_rock += enemy_speed_increase
        speed_rock = min(speed_rock, 20)

    elif selected == "Target Practice":
        enemy_bullets.clear()
        boss_enemy = None

    elif selected == "One Life":
        if lives <= 0:
            running = False
    screen.blit(background_img, (0,0))

    boss_showing(level)

    hud_x = 20
    hud_y = 20
    line_spacing = 10

    # Pause text
    pause = font_menu.render("Press P to Pause", True, (255, 255, 255))
    screen.blit(pause, (hud_x, hud_y))
    hud_y += pause.get_height() + line_spacing

    # Challenge Timer
    if selected == "Challenge":
        elapsed = pygame.time.get_ticks() - start_duration
        remaining = max(0, 60000 - elapsed)
        timer_text = font_menu.render(f"Time Left: {remaining // 1000}s", True, (255, 255, 255))
        screen.blit(timer_text, (hud_x, hud_y))
        hud_y += timer_text.get_height() + line_spacing

        if remaining <= 0:
            running = False
    dark_background = pygame.Surface((width,height))
    dark_background.set_alpha(80)
    dark_background.fill((0,0,0))
    screen.blit(dark_background ,(0,0))

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
                shoot_sound.play()
            else:
                center_rect = bullet_img.get_rect(center=(rocket_rect.centerx, rocket_rect.top))
                bullets.append({"rect": center_rect, "dx": 0, "dy": speed_bullet})
                shoot_sound.play()
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
            add_message("BONUSES COLLECTED! TRIPLE FIRING")
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
        if level >= 2 and rock.centery < height//2 and random.randint(1,100) == 1:
            enemy_bullet_rect = enemy_bullet_img.get_rect(midtop = (rock.centerx ,rock.bottom))
            enemy_bullets.append(enemy_bullet_rect)
        if rock.top>height:
            rocks.remove(rock)
        elif rock.colliderect(rocket_rect):
            offset = (rocket_rect.x - rock.x , rocket_rect.y - rock.y)
            if enemy_mask.overlap(rocket_mask , offset):
                rocks.remove(rock)
                lives -= 1
                add_message(f"Lives left: {lives}")
                if lives <= 0:
                    running = False
        screen.blit(enemy , rock)

    if boss_enemy:
        boss_enemy.move()
        boss_enemy.draw(screen)
        boss_enemy.health_bar(screen) 
        if boss_enemy.is_off_screen():
            boss_enemy = None

    for ebullet in enemy_bullets[:]:
        if ebullet.colliderect(rocket_rect):
            offset = (rocket_rect.x - ebullet.x , rocket_rect.y - ebullet.y)
            if enemy_bullet_mask.overlap(rocket_mask , offset):
                enemy_bullets.remove(ebullet)
                lives -= 1
                print(f"Lives left: {lives}")
                if lives <= 0:
                    running = False

    for rock in rocks[:]:
        for bullet in bullets[:]:
            if bullet["rect"].colliderect(rock):
                hit_sound.play()
                offset = (bullet["rect"].x - rock.x , bullet["rect"].y - rock.y)
                if enemy_mask.overlap(bullet_mask , offset):
                    rocks.remove(rock)
                    bullets.remove(bullet)
                    score += 10
                    if score >= level * levelup_score:
                        level += 1
                        boss_count = 0
                        show_level(level)
                        if level >= 4:
                            speed_rock += 1
                        if enemy_delay > 400:
                            enemy_delay -= 100
                    enemy_delay = max(300 , enemy_delay-10)
                    break
    if boss_enemy:
        for bullet in bullets[:]:
            if boss_enemy.rect.colliderect(bullet["rect"]):
                bullets.remove(bullet)      
                boss_enemy.health -= 1
                if boss_enemy.health <= 0:
                    score += 20
                    boss_enemy = None
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
            add_message("POWER-UP ENDED")
    for i in range(lives):
        screen.blit(heart_img , (hud_x + i * (heart_img.get_width() + 5) , hud_y))

    for m in message[:]:
        passed = pygame.time.get_ticks() - m["time"]
        if passed > m["duration"]:
            message.remove(m)
        else:
            text_message = font_menu.render(m["text"] , True , (255,255,0))
            screen.blit(text_message , (width//2 - text_message.get_width() // 2 , height-100))

    if selected == "Challenge Mode":
        elapsed = pygame.time.get_ticks() - start_time_level
        remaining = max(0 , game_duration - elapsed)
        timer_text = font_menu.render(f"Remaining time: {remaining // 1000}" , True , (255,255,255))
        screen.blit(timer_text , (20,20))
        if remaining <= 0:
            pygame.time.delay(3000)
            running = False
    pygame.display.flip()

  
game_over(score)
pygame.quit()

