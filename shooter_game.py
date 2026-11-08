from pygame import *
from random import randint
from time import time as timer

mixer.init()
mixer.music.load('Warning.mp3')
mixer.music.play(-1)
fire_sound = mixer.Sound('shooting.mp3')

font.init()
font1 = font.Font(None, 80)
win = font1.render('Victory!', True, (0,255,0))
lose = font1.render('FATE LOST', True, (255, 0 , 0))
font2 = font.Font(None, 36)

img_back = "BGR.png"
img_hero_raw = image.load("player1.png")
img_hero = transform.rotate(img_hero_raw, 90)
img_bullet = "bullet.png"
img_enemy = "ENEMY.png"

num_fire = 0 
rel_time  = False


score = 0
goal = 10
lost = 0
max_lost = 14


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)

        if isinstance(player_image, str):
            loaded_image = image.load(player_image)
        else:
            loaded_image = player_image

        self.image = transform.scale(loaded_image, (size_x,size_y))
        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image , (self.rect.x, self.rect.y))

class Player (GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 30, 25, -15)
        bullets.add(bullet)


class Enemy(GameSprite):
    def __init__(
        self, player_image, player_x, player_y,
        size_x, size_y, player_speed, count_miss=True
    ):
        super().__init__(
            player_image, player_x, player_y,
            size_x, size_y, player_speed
        )
        self.count_miss = count_miss

    def update(self):
        self.rect.y += self.speed

        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0

            if self.count_miss:
                global lost
                lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
        





win_width = 700
win_height = 500
display.set_caption("SUPPRESSION")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width,win_height))

ship = Player(img_hero, 5, win_height - 80, 40, 80, 20)

abnormalities = sprite.Group()
for i in range(1,5):
    abnormality = Enemy(img_enemy, randint(80, win_width - 80), -40, 20, 80, randint(3,5) )
    abnormalities.add(abnormality) 

bullets = sprite.Group()

rocks = sprite.Group()
for i in range(3):
    rock = Enemy('falling.png', randint(30, win_width - 30), -40, 50, 30, 6, False)
    rocks.add(rock)

finish = False
run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN and e.key == K_SPACE:
            if num_fire < 6 and not rel_time:
                num_fire += 1
                fire_sound.play()
                ship.fire()
            if num_fire >= 5 and  not rel_time:
                rel_time = True
                last_time = timer()

    if not finish:
            
        window.blit(background,(0,0))

        text = font2.render("Score: " + str(score), 1, (12, 232, 12))
        window.blit(text, (10,20))

        text_lose = font2.render("Missed: " + str(lost), 1, (209, 31, 31))
        window.blit(text_lose, (10,50))

        ship.update()
        abnormalities.update()
        bullets.update()
        rocks.update()


        ship.reset()
        abnormalities.draw(window)
        bullets.draw(window)
        rocks.draw(window)

        if rel_time:
            now_time = timer()
            if now_time - last_time < 2:
                reload = font2.render("Reloading...", 1, (150, 0 , 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False
    

        collides = sprite.groupcollide(abnormalities , bullets, True, True)
        for c in collides:
            score = score + 1
            abnormality = Enemy(img_enemy, randint(80, win_width - 80), -40, 20, 80, randint(3,5) )
            abnormalities.add(abnormality)

        if sprite.spritecollide(ship, abnormalities ,False) or sprite.spritecollide(ship, rocks, False)  or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))
        
        if score >= goal:
            finish = True
            window.blit(win, (200,200))
        




        display.update()

    time.delay(50)
