from pygame import *
class GameSprite(sprite.Sprite):
    def __init__ (self, player_image, player_x, player_y,size_x, size_y):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image),(size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y,size_x, size_y, player_x_speed, player_y_speed):
        GameSprite.__init__(self, player_image, player_x, player_y,size_x, size_y)
        self.x_speed = player_x_speed
        self.y_speed = player_y_speed
        self.size_x = size_x
        self.size_y = size_y
    def update(self):
        if packman.rect.x <=win_width-80 and packman.x_speed>0 or packman.rect.x >=0 and packman.x_speed <0:
            self.rect.x += self.x_speed
        platforms_touched = sprite.spritecollide(self, walls,False)
        if self.x_speed>0:
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.x_speed<0:
            for p in platforms_touched:
                self.rect.left= max(self.rect.left, p.rect.right)
        if packman.rect.y <= win_height - 80 and packman.y_speed >0 or packman.rect.y >=0 and packman.y_speed < 0:
            self.rect.y += self.y_speed
        platforms_touched = sprite.spritecollide(self, walls,False)
        if self.y_speed > 0:
            for p in platforms_touched:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
        if self.y_speed < 0:
            for p in platforms_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom)
    def fire(self):
        bullet = Bullet('prov.jpg', self.rect.right, self.rect.centery,15,20,15, _direction)    
        bullets.add(bullet)    
class Knopka(GameSprite):
    def collidepoint(self, x, y):
        return self.rect.collidepoint(x,y)
class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y,size_x, size_y, speed,enemy_life ='yes' ,direction = 'right'):
        super().__init__(player_image, player_x, player_y,size_x, size_y)
        self.player_x = player_x
        self.speed = speed
        self.size_x = size_x
        self.direction=direction
        self.life = enemy_life
    def update(self):
        self.life = enemy_life
        if self.direction =='right':
            speed = self.speed
        if self.direction =='left':
            speed = -1*  self.speed
        if self.rect.x>=win_width-self.size_x:
            self.direction  = 'left'
        if self.rect.x<=420:
            self.direction = 'right'
        self.rect.x += speed
class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y,size_x, size_y,bull_speed,direction = 'up'):
        GameSprite.__init__(self, player_image, player_x, player_y,size_x, size_y)
        self.speed=5
        self.direction = _direction
    def update(self):
        self.reset()
        if self.direction =='right':
            if self.rect.x > win_width+10:
                self.kill()
            self.rect.x+=self.speed
        if self.direction =='left':
            if self.rect.x < -10:
                self.kill()
            self.rect.x-= self.speed
        if self.direction =='up':
            if self.rect.y < -10:
                self.kill()
            self.rect.y -=self.speed
        if self.direction =='down':
            if self.rect.y > win_height+10:
                self.kill()
            self.rect.y +=self.speed
knop = Knopka('knop.png', 670,10, 20, 20)
win_width = 700
win_height = 500
window = display.set_mode((win_width,win_height))#Задаём размер окна
back = (119,210,223)
GREEN = (0, 255, 0)
display.set_caption('Лабиринт')#Назване окна
w1 = GameSprite('platform2.png', win_width/2-win_width/3, win_height/2,300,50)
w2 = GameSprite('platform2_v.png', 370, 100, 50, 400)
packman = Player('hero.png', 5,  win_height-80, 80, 80,0,0)
enemy =Enemy('bennet.png',420,180,80,80,5)
final = GameSprite('finish.png',win_width-80,win_height-80,80,80)
walls = sprite.Group()
walls.add(w1)
walls.add(w2)
bullets = sprite.Group()
enemis =   sprite.Group()
enemis.add(enemy)
fin_pic =transform.scale(image.load('fin_pic.jpg'),(700,500))
run = True
finish = False
_direction ='right'
enemy_life = True
while run:
    time.delay(50)#Задержка обновления, чтоб не лагало
    for e in event.get():#Если нажали на закрыть окно...
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key ==K_LEFT:
                packman.x_speed =-5
                _direction = 'left'
            elif e.key == K_RIGHT:
                packman.x_speed =5
                _direction ='right'
            elif e.key == K_UP:
                packman.y_speed =-5
                _direction = 'up'
            elif e.key == K_DOWN:
                packman.y_speed =5
                _direction ='down'
            elif e.key == K_SPACE:
                packman.fire()   
        elif e.type == KEYUP:
            if e.key ==K_LEFT:
                packman.x_speed =0
            elif e.key == K_RIGHT:
                packman.x_speed =0
            elif e.key == K_UP:
                packman.y_speed =0
            elif e.key == K_DOWN:
                packman.y_speed =0       
    if not finish:
        window.fill(back)  
        walls.draw(window)
        final.reset()
        packman.reset()
        packman.update()
        bullets.update()
        sprite.groupcollide(enemis,bullets, True, True)
        enemis.update()
        enemis.draw(window)
        sprite.groupcollide(bullets, walls, True, False)
        if sprite.groupcollide(enemis,bullets, True, True):
            enemy_life = False
            enemy.kill()
            #enemis.remove(enemy)
        if enemy_life:
            if sprite.collide_rect(packman, enemy):
                finish = True
                lose_pic = image.load('finish_1.jpg')
                d=lose_pic.get_width()//lose_pic.get_height()
                window.fill((255,255,255))
                window.blit(transform.scale(lose_pic, (win_height*d, win_height)),(90,0))
        if sprite.collide_rect(packman, final):
            finish =True
            window.fill((255,255,255))
            window.blit(fin_pic,(0,0))
    if finish:
        knop.reset()
        for ev in event.get():
            if ev.type == KEYDOWN:
                if ev.key ==K_RETURN:
                    x, y = event.pos
                    if knop.collidepoint(x, y):
                        finish =False
                        window.fill((255, 255,0))
                        finish =False
                    
    display.update()