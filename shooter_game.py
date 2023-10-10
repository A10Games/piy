from pygame import *
from random import randint
from time import time as timer
window = display.set_mode((1000,700))
display.set_caption('пиу пау')
fon = transform.scale(image.load('galaxy.jpg'),(1000,700))

mixer.init()
mixer.music.load('space.ogg')

font.init()
font = font.Font(None,35)
score = 0
miss = 0 
class Game_Sprite(sprite.Sprite):
    def __init__(self,player_image , player_x, player_y , size_x , size_y , player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(size_x , size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))
class Player(Game_Sprite):
    def update(self):
        knopky = key.get_pressed()
        if knopky[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if knopky[K_d] and self.rect.x < 920:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.x+40,self.rect.y,15,20,15)
        bullets.add(bullet)
class Enemy(Game_Sprite):
    def update(self):
        self.rect.y += self.speed
        global miss 
        if self.rect.y >700:
            miss += 1 
            self.rect.y = 0 
            self.rect.x = randint(0,920)
class Bullet(Game_Sprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
game = True
finish = False
Vaider = Player('rocket.png', 460 , 550 , 150, 150,20)
monsters = sprite.Group()
for i in range(1,5):
    monster = Enemy('ufo.png', randint(0,920), 0 , 80, 80, randint(2,7))
    monsters.add(monster)
bullets = sprite.Group()
asteroids = sprite.Group()
for i in range(1,5):
    asteroid = Enemy('asteroid.png', randint(0,920), 0 , 80, 80, randint(1,3))
    asteroids.add(asteroid)

num_bullets = 0
reload = False
life = 3


while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_bullets< 5 and reload == False:
                    num_bullets += 1
                    Vaider.fire()
                if num_bullets >= 5 and reload == False:
                    reload = True
                    reload_time = timer()

 

    if not finish:
        window.blit(fon,(0,0))
        score_text = font.render('Счет: '+str(score),True,(255,255,255))
        miss_text = font.render('Пропуск: '+str(miss),True,(255,255,255))
        window.blit(score_text,(10,10))
        window.blit(miss_text,(10,55))
        Vaider.reset()
        Vaider.update()
        monsters.draw(window)
        monsters.update()
        asteroids.draw(window)
        asteroids.update()
        bullets.draw(window)
        bullets.update()
        if reload == True:
            new_time = timer()
            if new_time - reload_time < 2:
                reload_text = font.render('Стреляй меньше!!!!', True,(255,255,255))
                window.blit(reload_text,(500,500))
            else:
                num_bullets=0
                reload = False
        collision = sprite.groupcollide(monstersa,bullets,True,True)
        for i in collision:
            score +=1
            monster = Enemy('ufo.png', randint(0,920), 0 , 80, 80, randint(2,7))
            monsters.add(monster)
        if sprite.spritecollide(Vaider,monsters,False) or sprite.spritecollide(Vaider,asteroids,False):
            life -=1
        if score >= 50:
            finish = True
            window.blit(text_win,(400,150))
        if life ==0 or miss > 3:
            finish = True
            window.blit(text_lose,(400,150))
        display.update()
    time.delay(50)
