
# import pygame
# import sys
# import random
# pygame.init()
# pygame.font.init()
# font = pygame.font.SysFont(None, 60)
# width, height= 800,600
# score=0
# bullets=[]  
# rocks=[]
# rock_speed=5
# window=pygame.display.set_mode((width, height))
# pygame.display.set_caption("ROCKET SHOOTER")
# clock=pygame.time.Clock()
# FPS=20
# # def select():
# #     rockets = ["rocket1.png", "rocket2.png", "rocket3.png"]
# #     enemies = ["enemy1.png", "enemy2.png", "enemy3.png"]
# #     rocket_image=[]
# #     for img in rockets:
# #         load_img = pygame.image.load(img)
# #         scale_img = pygame.transform.scale(load_img, (100,100))
# #         rocket_image.append(scale_img)
    
# #     enemy_image=[]
# #     for img in enemies:
# #         load_img = pygame.image.load(img)
# #         scale_img = pygame.transform.scale(load_img, (100,100))
# #         enemy_image.append(scale_img)
# # chosen_rocket_img, chosen_enemy_img = select()
# rocket = pygame.image.load("rocket_image.png").convert_alpha()
# rocket = pygame.transform.scale(rocket,(200,200))
# opponent = pygame.image.load("enemy.jpg").convert()
# opponent.set_colorkey((255,255,255))
# opponent = pygame.transform.scale(opponent, (100,100))
# # rocket.fill((255, 0, 0))
# background = pygame.image.load("space_background.jpg").convert_alpha()
# background= pygame.transform.scale(background,(width, height))
# rocket_rect = rocket.get_rect(center=(width // 2, height - 70))
# running = True


# while running:
#     clock.tick(FPS)
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#     keys = pygame.key.get_pressed()
#     if keys[pygame.K_LEFT] and rocket_rect.left > 0:
#         rocket_rect.x -= 10
#     if keys[pygame.K_RIGHT] and rocket_rect.right < width:
#         rocket_rect.x += 10 
    
#     bullet_speed=-15
#     if keys[pygame.K_SPACE]:
#         if len(bullets) < 5:
#             bullet = pygame.Rect(rocket_rect.centerx - 2, rocket_rect.top, 4, 10)
#             bullets.append(bullet)
#     for bullet in bullets:
#         bullet.y += bullet_speed
#         if bullet.bottom < 0:
#             bullets.remove(bullet)

#     if random.randint(1, 10) == 1:
#         rock = pygame.Rect(random.randint(0, width - 40), 0, 40, 40)
#         rocks.append(rock)

#     for rock in rocks[:]:
#         rock.y += rock_speed
#         if rock.top > height:
#             rocks.remove(rock)
#         elif rock.colliderect(rocket_rect):
#             running=False
#     for rock in rocks[:]:
#         for bullet in bullets[:]:
#             if rock.colliderect(bullet):
#                 rocks.remove(rock)
#                 bullets.remove(bullet)
#                 score=score+1
#                 break

#     window.fill((0, 0, 0))
  
#     window.blit(background,(0,0))
#     window.blit(rocket, rocket_rect)

#     for bullet in bullets:
#         pygame.draw.rect(window, (255, 255, 0), bullet)

#     for rock in rocks:
#         window.blit(opponent, rock)

#     pygame.display.flip()


# def show_game_over_screen(score):
#     game_over_window = pygame.display.set_mode((width, height))
#     game_over_window.fill((0, 0, 0))
#     text = font.render(f"Game Over! Score: {score}", True, (255, 255, 255))
#     text_rect = text.get_rect(center=(width // 2, height // 2))
#     game_over_window.blit(text, text_rect)
#     pygame.display.flip()

#     waiting = True
#     while waiting:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
#                 waiting = False

# show_game_over_screen(score)

# pygame.quit()



def calculate_but_only_addition(num1,num2):
    return num1+num2
 

def adding_three_numbers(num1,num2,num3):
    return calculate_but_only_addition(calculate_but_only_addition(num1,num2), num3)

print(adding_three_numbers(1,2,3))
