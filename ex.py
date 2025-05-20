import pygame
import random
import os
import pygame.mixer
import sys
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
endless_start_time = 0
diff_increase_interval = 10000
last_diff_increase = 0
enemy_delay = 1000
endless_rockspeed = speed_rock
endless_enemydelay = enemy_delay
wave_timer = 0
wave = 1
wave_threshold = 1000
wave_mutation = None

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
game_modes = ["Classic", "Challenge", "Survival", "Endless", "Target Practice", "One Life"]
start_time_level = pygame.time.get_ticks()

pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.play(-1)
shoot_sound = pygame.mixer.Sound("bullet_shoot.wav")
hit_sound = pygame.mixer.Sound("hit_enemy.wav")

highscore_file = "highscore.txt"
if os.path.exists(highscore_file):
    with open(highscore_file, "r") as f:
        high_score = int(f.read())
else:
    high_score = 0
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Rocket Laucher")


clock=pygame.time.Clock()
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

boss_enemy_img = pygame.image.load("boss_enemy.png").convert_alpha()
boss_enemy = None

background_img = pygame.image.load("background.jpg").convert()
background_img = pygame.transform.scale(background_img, (width, height))

bonus_img = pygame.image.load("bonus.png").convert_alpha()
bonus_img = pygame.transform.scale(bonus_img, (40, 40))

heart_img = pygame.image.load("heart.png").convert()
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
        self.rect.y += 5
    def draw(self, window):
        window.blit(self.image , (self.rect.x , self.rect.y))
        if self.health > 1:
            shield = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            pygame.draw.circle(shield, (0, 100, 255, 100), (self.rect.width//2 , self.rect.height//2), self.rect.width//2)
            window.blit(shield, (self.rect.x, self.rect.y))
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

class Enemy():
    def __init__(self , x , y , speed , shape_type = "rect" , health = 1):
        self.x = x
        self.y = y
        self.speed = speed
        self.shape_type = shape_type
        self.health = health
        self.size = 40
        self.color = (255,0,0)
        self.image = pygame.Surface((self.size , self.size) , pygame.SRCALPHA)
        self.update_shape()
    def move(self):
        self.y += 5
    def draw(self , window):
        window.blit(self.image , (self.x , self.y))
    def mutate(self, mutation_type):
        if mutation_type:
            self.shape_type = mutation_type
            self.color = (255,0,0)
            self.size = 40
            if mutation_type == "fast":
                self.color = (255, 165, 0)  
                self.speed *= 1.5 
            elif mutation_type == "circle":
                self.color = (0, 255, 0)
            elif mutation_type == "split":
                self.color = (255, 0, 255)
                self.size = 60
            elif mutation_type == "small":
                self.color = (0, 255, 255)
                self.size = 20
            elif mutation_type == "shielded":
                self.color = (0, 0, 255)
                self.health = 2 
            self.update_shape()
    def get_rect(self):
        return pygame.Rect(self.x , self.y , self.size , self.size)
    def update_shape(self):
        self.image.fill((0,0,0,0))
        if self.shape_type == "rect":
            pygame.draw.rect(self.image , self.color , (0,0,self.size,self.size))
        elif self.shape_type == "circle":
            pygame.draw.circle(self.image , self.color , (self.size // 2 , self.size // 2) , self.size // 2)
        elif self.shape_type == "triangle":
            points = [(self.size // 2 , 0) , (0 , self.size) , (self.size , self.size)]
            pygame.draw.polygon(self.image , self.color , points)
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
                    sys.exit()

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

def add_message(text , duration = 8000):
    message.append({"text" : text , "time" : pygame.time.get_ticks() , 'duration' : duration})

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
    elif selected == "Endless":
        endless_start_time = pygame.time.get_ticks()
        endless_rockspeed = 7
        endless_enemydelay = 1000
    elif selected == "One Life":
        lives = 1
    elif selected == "Target Practice":
        enemy_delay = 500
    menu(selected_mode_index)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                selected_mode_index = (selected_mode_index-1) % len(game_modes)
            elif event.key == pygame.K_DOWN:
                selected_mode_index = (selected_mode_index+1) % len(game_modes)
            elif event.key == pygame.K_RETURN:
                selected = game_modes[selected_mode_index]
                options = False
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

def update_endless_mode():
    global wave, wave_timer, wave_mutation, endless_rockspeed
    
    wave_timer += 1
    if wave_timer >= wave_threshold:
        wave += 1
        wave_timer = 0
        wave_mutation = random.choice(["circle", "fast", "split", "small", "shielded"])
        add_message(f"Wave {wave}: {wave_mutation} mutation!", 3000)
    if wave_timer == 0: 
        endless_rockspeed += 0.5
        endless_enemydelay = max(300, endless_enemydelay - 50)

running = True
while running:

    clock.tick(FPS)
    if selected == "Challenge":
        elapsed = pygame.time.get_ticks() - start_duration
        remaining = max(0, 60000 - elapsed)
        timer_text = font_menu.render(f"Time Left: {remaining // 1000}s", True, (255, 255, 255))
        screen.blit(timer_text, (20, 20))
        if remaining <= 0:
            running = False

    elif selected == "Survival":
        speed_rock += enemy_speed_increase
        speed_rock = min(speed_rock, 20)
    elif selected == "Endless":
        update_endless_mode()
        if len(rocks) < 3 + wave: 
            x = random.randint(0, width - 40)
            y = random.randint(-150, -40)
            speed = endless_rockspeed
            new_enemy = Enemy(x, y, speed)
            new_enemy.mutate(wave_mutation)
            # # Apply wave mutation
            # if wave_mutation == "fast":
            #     new_enemy.speed *= 1.5
            # elif wave_mutation == "circle":
            #     new_enemy.mutate("circle")
            # elif wave_mutation == "split":
            #     new_enemy.size = 60  
            # elif wave_mutation == "small":
            #     new_enemy.size = 20 
            # elif wave_mutation == "shielded":
            #     new_enemy.health = 2 
            rocks.append(new_enemy)
    elif selected == "Target Practice":
        enemy_bullets.clear()
        boss_enemy = None

    elif selected == "One Life":
        if lives <= 0:
            running = False
    screen.blit(background_img, (0,0))
    boss_showing(level)
    if boss_enemy:
        boss_enemy.move()
        boss_enemy.draw(screen)
        boss_enemy.health_bar(screen)
    if boss_enemy is not None and boss_enemy.is_off_screen():
        boss_enemy = None
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

    if current - last_enemy > (endless_enemydelay if selected == "Endless" else enemy_delay):
        rock_rect = enemy.get_rect(topleft = (random.randint(0, width-100), 0))
        rocks.append(rock_rect)
        last_enemy = current
        if level >= 3 and random.randint(1,10) == 1:
            bonus_rect = bonus_img.get_rect(center = (rock_rect.centerx , rock_rect.centery))
            bonuses.append(bonus_rect)  
    for enemy in rocks[:]:
        
        pygame.draw.rect(screen, (128, 128, 128), enemy)
        if level >= 2 and enemy.centery < height//2 and random.randint(1,100) == 1:
            enemy_bullet_rect = enemy_bullet_img.get_rect(midtop = (enemy.x + enemy.size//2, enemy.y + enemy.size))
            enemy_bullets.append(enemy_bullet_rect)
        if enemy.y > height:
            rocks.remove(enemy)
        enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.image.get_width(), enemy.image.get_height())
        if enemy_rect.colliderect(rocket_rect):
            offset = (rocket_rect.x - enemy.x , rocket_rect.y - enemy.y)
            if enemy_mask.overlap(rocket_mask , offset):    
                rocks.remove(enemy)
                lives -= 1
                add_message(f"Lives left: {lives}")
                if lives <= 0:
                    running = False
    
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

    for enemy in rocks[:]:
        for bullet in bullets[:]:
            if bullet["rect"].colliderect(enemy.get_rect()):
                hit_sound.play()
                offset = (bullet["rect"].x - enemy.x , bullet["rect"].y - enemy.y)
                if enemy_mask.overlap(bullet_mask , offset):
                    rocks.remove(enemy)
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
        screen.blit(heart_img , (10 + i*50 , 70))

    for m in message[:]:
        passed = pygame.time.get_ticks() - m["time"]
        if passed > m["duration"]:
            message.remove(m)
        else:
            text_message = font_menu.render(m["text"] , True , (255,255,0))
            screen.blit(text_message , (width//2 - text_message.get_width() // 2 , height-100))

    if selected == "Challenge":
        elapsed = pygame.time.get_ticks() - start_time_level
        remaining = max(0 , game_duration - elapsed)
        timer_text = font_menu.render(f"Remaining time: {remaining // 1000}s" , True , (255,255,255))
        screen.blit(timer_text , (20,20))
        if remaining <= 0:
            game_over = True
            game_over()
            pygame.time.delay(3000)
            running = False
    pygame.display.flip()

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
game_over(score)
pygame.quit()
