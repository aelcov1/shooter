from pygame import *
from random import randint

font.init()
font = font.Font(None, 36)

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_d] and self.rect.x < 640:
            self.rect.x += 5
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= 5
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 10)
        bullets.add(bullet)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < -50:
            self.kill()



lost = 0
score = 0

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= win_height:
            self.rect.x = randint(80, win_height - 80)
            self.rect.y = 0
            lost = lost + 1

class asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= win_height:
            self.rect.x = randint(80, win_height - 80)
            self.rect.y = 0
        

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Shooter")
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))

player = Player('rocket.png', 8, 430, 4)
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy('ufo.png', randint(80, win_width - 80), 0, randint(1, 5))
    monsters.add(monster)

steroids = sprite.Group()
steroid = asteroid('asteroid.png', randint(80, win_width - 80), 0, randint(1, 5))
steroids.add(steroid)

bullets = sprite.Group()


text_lost = font.render('YOU LOSE', True, (255, 215, 0))
text_finish = font.render('YOU WIN', True, (255, 215, 0))
text_score = font.render('Счет: ' + str(score), 1, (255, 255 , 255))

text_lose = font.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
window.blit(text_lose, (6, 42))
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
game = True
clock = time.Clock()
FPS = 60

finish = False
while game:
    for e in event.get():
        if e.type == QUIT:
           game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()

    if finish != True:
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy('ufo.png', randint(80, win_width - 80),0, randint(1, 5))
            monsters.add(monster)



        text_score = font.render('Счет: ' + str(score), 1, (255, 255 , 255))
        text_lose = font.render('Пропущено: ' + str(lost), 1, (255, 255, 255))      

        

        window.blit(background,(0, 0))
        window.blit(text_score, (10, 25))
        window.blit(text_lose, (10, 50))
        player.update()
        monsters.update()
        bullets.update()
        steroids.update()

        steroids.draw(window)
        monsters.draw(window)
        player.reset()
        bullets.draw(window)
        if score == 15:
            finish = True
            window.blit(text_finish, (6, 15))
        if lost >= 5:
            finish = True
            window.blit(text_lost, (6, 15))

        collides2 = sprite.spritecollide(player, steroids, True)
        for c in collides2:
            steroid = asteroid('asteroid.png', randint(80, win_width - 80), 0, randint(1, 5))
            steroids.add(steroid)
            finish = True
            window.blit(text_lost, (10,50))            

    clock.tick(FPS)
    display.update()
