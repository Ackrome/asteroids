import pygame
import random
import os
import time
import math
import inspect
import os
import sys

def get_script_dir(follow_symlinks=True):
    if getattr(sys, 'frozen', False): # py2exe, PyInstaller, cx_Freeze
        path = os.path.abspath(sys.executable)
    else:
        path = inspect.getabsfile(get_script_dir)
    if follow_symlinks:
        path = os.path.realpath(path)
    return os.path.dirname(path)

os.chdir(get_script_dir())
###############################################################################################################
###############################################################################################################
WIDTH = 920
HEIGHT = 580
FPS = 60
max_mob_speed = 2


bullet_live = 0.7
check_hits_now = 1
time_for_escape = 1.5
rotator_time = 100

lifes = 3
score = 0

n_mobs = 8

use_death_star = 1

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255,204,0)
###############################################################################################################
###############################################################################################################
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.original_image = pygame.image.load('images//'+'pngfind.com-xwing-png-6101995.png')
        self.original_image = pygame.transform.scale(self.original_image, (50, 40))
        self.original_image = pygame.transform.rotate(self.original_image, -90)
        
        self.fly_image =  pygame.image.load('images//'+'xwing_fly.png')
        self.fly_image = pygame.transform.scale(self.fly_image, (50, 45))
        self.fly_image = pygame.transform.rotate(self.fly_image, -90)
        
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.angle = 0
        self.speed = 0
        self.time_shot = time.time()
        self.delay = 150
        
        self.fly=0

    def update(self):
        keys = pygame.key.get_pressed()

        # Вращение
        if keys[pygame.K_LEFT]:
            self.angle += 5
        if keys[pygame.K_RIGHT]:
            self.angle -= 5

        # Движение вперед/назад
        if keys[pygame.K_UP]:
            self.fly =1
            self.speed += 0.5
        elif keys[pygame.K_DOWN]:
            self.speed -= 0.5
            self.fly =1
        else:
            self.fly = 0

        if self.speed > 0:
            self.speed -=0.3
        elif self.speed < 0:
            self.speed +=0.3
        
        

        # Обновление позиции игрока
        rad_angle = math.radians(self.angle)
        self.rect.x += self.speed * math.cos(rad_angle)
        self.rect.y -= self.speed * math.sin(rad_angle)  # "-" из-за инверсии оси Y в Pygame

        if self.rect.left > WIDTH:
            self.rect.right = 0
            
        if self.rect.right < 0:
            self.rect.left = WIDTH
            
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0
            
        if self.rect.bottom < 0:
            self.rect.top = HEIGHT
        
        
        # Поворот изображения
        if self.fly==0:
            self.image = pygame.transform.rotate(self.original_image, self.angle)
            self.rect = self.image.get_rect(center=self.rect.center)
        else:
            self.image = pygame.transform.rotate(self.fly_image, self.angle)
            self.rect = self.image.get_rect(center=self.rect.center)

        # Выстрел
        if keys[pygame.K_SPACE]:
            self.shoot()

    def shoot(self):
        if time.time() - self.time_shot >= self.delay / 1000:
            self.time_shot = time.time()

            # Позиция носа корабля
            rad_angle = math.radians(self.angle)
            nose_x = self.rect.centerx + 25 * math.cos(rad_angle)
            nose_y = self.rect.centery - 25 * math.sin(rad_angle)

            # Создание ракеты
            bullet = Bullet(nose_x, nose_y, self.angle)
            all_sprites.add(bullet)
            bullets.add(bullet)
            shoot_sound.play()
            
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((5, 5))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.angle = angle
        self.speed = 10

        # Поворот ракеты
        self.image = pygame.transform.rotate(self.image, -self.angle)

        # Вычисление направления движения
        self.rad_angle = math.radians(self.angle)
        self.vel_x = self.speed * math.cos(self.rad_angle)
        self.vel_y = -self.speed * math.sin(self.rad_angle)
        
        self.live = bullet_live
        self.born = time.time()

    def update(self):
        # Движение ракеты
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        if time.time() - self.born >= self.live:
            self.kill()
        
        
        # Удаление ракеты, если она выходит за экран
        if (
            self.rect.bottom < 0
            or self.rect.top > HEIGHT
            or self.rect.right < 0
            or self.rect.left > WIDTH
        ):
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
                
                

class MenuMob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.pn =  random.randrange(0,10)
        rn_pn = 'images//'+f'Planet{self.pn}.png'
                
        self.original_image = pygame.image.load(rn_pn)
        
        self.image = self.original_image.copy()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.image.set_colorkey(BLACK)
        
        
        self.rect = self.image.get_rect()
        # Случайное появление объекта на карте
        self.rect.y = random.randrange(HEIGHT - self.rect.height)
        self.rect.x = random.randrange(WIDTH - 20, WIDTH)
        self.speedx = random.randrange(1, 8)
        
    def update(self):
        self.rect.x -= self.speedx
        if self.rect.left <  - 10:
            self.rect.y = random.randrange(HEIGHT - self.rect.height)
            self.rect.x = random.randrange(WIDTH - 20, WIDTH)
            self.speedx = random.randrange(1, 8)


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)        
        self.identificate()
        
    def identificate(self):
        if use_death_star:
            rn_pn = 'images//'+'pngkey.com-death-star-png-142561.png'
        else:
            self.pn =  random.randrange(0,10)
            rn_pn = 'images//'+f'Planet{self.pn}.png'
                
        self.original_image = pygame.image.load(rn_pn)
        
        self.image = self.original_image.copy()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.image.set_colorkey(BLACK)
        
        
        self.rect = self.image.get_rect()
        # Случайное появление объекта на карте
        self.rect.x = random.randrange(WIDTH - self.rect.width)/WIDTH
        self.rect.y = random.randrange(HEIGHT - self.rect.height)/HEIGHT
        
        self.top = 0
        self.left = 0
        
        if self.rect.x > self.rect.y:
            self.top = random.randrange(2)
            
            if self.top:
                self.rect.x = random.randrange(WIDTH)
                self.rect.y = random.randrange(self.rect.height)
                
            else:
                self.rect.x = random.randrange(WIDTH)
                self.rect.y = random.randrange(HEIGHT - 20, HEIGHT)
                
        else:
            self.left = random.randrange(2)
            if self.left:
                self.rect.x = random.randrange(0,20)
                self.rect.y = random.randrange(HEIGHT)
                
            else:
                self.rect.x = random.randrange(WIDTH - 20, WIDTH)
                self.rect.y = random.randrange(HEIGHT)
                
                
        if self.top:
            self.speedy = random.randrange(1, max_mob_speed)
        elif not(self.top):
            self.speedy = -random.randrange(1, max_mob_speed)
            
        if self.left:
            self.speedx = random.randrange(1, max_mob_speed)
        elif not(self.left):
            self.speedx = -random.randrange(1, max_mob_speed)
        
        self.rot = 0
        self.rot_speed = random.randrange(-8,8)
        self.last_update = pygame.time.get_ticks()
    
    def rotate(self):
        now = pygame.time.get_ticks()
        
        if now -self.last_update > rotator_time:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.original_image, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.image = pygame.transform.scale(self.image, (50, 50))
            self.rect = self.image.get_rect()
            self.rect.center = old_center
        
		
        

    def update(self):
        # Вращение
        self.rotate()
        
        # Движение со сменой кадров
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        
        if self.rect.top > HEIGHT + 50 or self.rect.left < -50 or self.rect.right > WIDTH + 50 or self.rect.bottom < -50:
            self.identificate()


# Функция написания текста

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font("Bombardier-Regular.ttf", size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def show_go_screen():
    screen.blit(background, background_rect)
        
    
    
    
    
    all_sprites = pygame.sprite.Group()    
    for i in range(n_mobs):
        m = MenuMob()
        all_sprites.add(m)
        
    waiting = True
    while waiting:
        clock.tick(FPS)
        # Обновление
        all_sprites.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                for i in all_sprites:
                    i.kill()
                waiting = False
                
        
        
        screen.blit(background, background_rect)
        all_sprites.draw(screen)
        draw_text(screen, "Steroids:", 80, WIDTH / 2, HEIGHT / 4 - 40)
        draw_text(screen, "shoot the planets", 40, WIDTH / 2, HEIGHT / 4 + 20)
        draw_text(screen, "Arrows (left, right) - rotate", 22,WIDTH / 2, HEIGHT / 2-40)
        draw_text(screen, "Arrows (up, down) - initiate engine", 22,WIDTH / 2, HEIGHT / 2-10)
        draw_text(screen, "Space to fire", 22,WIDTH / 2, HEIGHT / 2+20)
        draw_text(screen, "Press a key to begin", 18, WIDTH / 2, HEIGHT * 3 / 4-20)
        pygame.display.flip()

# Загрузка музыки
pygame.mixer.init()

shoot_sound = pygame.mixer.Sound('sounds//'+"blast-101soundboards (mp3cut.net).mp3")

expl_sounds = []
for snd in ['sounds//'+'expl3.wav', 'sounds//'+'expl6.wav']:
    expl_sounds.append(pygame.mixer.Sound(snd))
pygame.mixer.music.load('sounds//'+'Victory Celebration (Soundtrack from  Star Wars )   John Wil.mp3')
pygame.mixer.music.set_volume(0.2)

# Загрузка всей игровой графики

# Фон
background = pygame.image.load('images//'+'Space_1.png')
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
background_rect = background.get_rect()


# Взрывы
explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
for i in range(9):
    filename = 'images//'+f'regularExplosion0{i}.png'
    img = pygame.image.load(filename)
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)
    
    filename = 'images//'+f'sonicExplosion0{i}.png'
    img = pygame.image.load(filename)
    img.set_colorkey(BLACK)
    explosion_anim['player'].append(img)
               


# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Steroids")
pygame.font.init()
clock = pygame.time.Clock()

# Группы Спрайтов
bullets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()

# Определение объектов
player = Player()
all_sprites.add(player)
    

# Цикл игры
pygame.mixer.music.play(loops=-1)

game_over = True
running = True

while running:
    
    if game_over:
        
        show_go_screen()
        
        game_over = False
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        
        player = Player()
        all_sprites.add(player)
        
        for i in range(n_mobs):
            m = Mob()
            all_sprites.add(m)
            mobs.add(m)
        lifes = 3
        score = 0
    
    if lifes == 0:
        game_over = True
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    
    # Ввод процесса (события)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        

    # Обновление
    all_sprites.update()
    
    # Проверка, не ударил ли моб игрока
    
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    
    for hit in hits:
        score +=1

        random.choice(expl_sounds).play()
        m = Mob()
        all_sprites.add(m)
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        mobs.add(m)
    
    if check_hits_now: 
        hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle)
        
        if hits:
            for hit in hits:
                expl = Explosion(hit.rect.center, 'sm')
                all_sprites.add(expl)
                hit.kill()
                score +=1
            lifes -=1
            check_hits_now-=1
            time_start = time.time()
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            player.kill()
            player = Player()
            all_sprites.add(player)
            
    else:
        
        if time.time() - time_start >= time_for_escape:
            check_hits_now+=1
        

    
    # Рендеринг



    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, f'Score : {score}', 18, WIDTH - 50 , 10)
    draw_text(screen, f'Lifes : {lifes}', 18, 50 , 10)


    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()