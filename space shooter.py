import pygame as pg
from sys import exit
from random import randint,choice
pg.init()

#variables declaration
clock = pg.time.Clock()
running = False
font=pg.font.Font("Font/Pixeltype.ttf",72)
height=width=600

#Setting the screen
screen = pg.display.set_mode((width,height))
pg.display.set_caption('Space shooter')

#Setting the background
background = pg.image.load("Graphics/background.jpg").convert()
background = pg.transform.scale(background,(600,600))

#The spaceship class
class Spaceship(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pg.image.load("Graphics/spaceship.png").convert()
        self.image=pg.transform.rotozoom(self.image,0,0.65)
        self.image.set_colorkey(self.image.get_at((0, 0)))
        self.rect=self.image.get_rect(bottom=height-50)
        self.sh=0
        self.health=100
        self.die=False
        self.w=0
        
    #input method
    def input(self):
        keys=pg.key.get_pressed()
        #Movement
        if keys[pg.K_LEFT] and self.rect.left>0:
            self.rect.x-=vel_pl
        if keys[pg.K_RIGHT] and self.rect.right<600:
            self.rect.x+=vel_pl
        if keys[pg.K_UP] and self.rect.top>0:
            self.rect.y-=vel_pl
        if keys[pg.K_DOWN] and self.rect.bottom<600:
            self.rect.y+=vel_pl
        #Shooting
        if keys[pg.K_SPACE]:
            self.sh+=0.2
    
    #Configure the shooting timing
    def shoot(self):
        if self.sh==1:
            bullets.add(Bullet())
            self.sh=0
            
    #damage method(instant death!!!)
    def damage(self):
        for a in pg.sprite.spritecollide(self,aliens,False):
            self.health-=10
            a.anim()
            if self.health<=0:
                self.die=True
                running=False

    #death animation
    def crash(self):
        if self.die:
            if self.w==0:
                self.frames=[pg.image.load("Graphics/explosion1.png").convert(),pg.image.load("Graphics/explosion2.png").convert()]
                self.frames=[pg.transform.scale(x,(self.rect.bottom-self.rect.top,self.rect.right-self.rect.left)) for x in self.frames]
                for x in self.frames:
                    x.set_colorkey(x.get_at((0,0)))
            self.image=self.frames[ind%2]
            self.w+=0.2
            if self.w>=1:
                running=False
    
    def update(self):
        self.input()
        self.shoot()
        self.damage()
        self.crash()


#The bullets class
class Bullet(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load("Graphics/bullet.png").convert()
        self.image = pg.transform.rotozoom(self.image, -45, 1.5)
        self.image.set_colorkey(self.image.get_at((0, 0)))
        self.rect = self.image.get_rect(midbottom=player.sprite.rect.midtop)

    #input movement method
    def move(self):
        self.rect.y -= vel_bul

    #bullets out of screen
    def destroy(self):
        if self.rect.bottom<0:
            self.kill()

    def update(self):
        self.move()
        self.destroy()
#the alien class
class Alien(pg.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.hit=False
        self.w=0
        self.die=False
        self.pos=pos
        self.frames=[pg.image.load("Graphics/alien1.png").convert(),pg.image.load("Graphics/alien2.png").convert()]
        self.frames=[pg.transform.scale(x,((width-130-col_nb*between)//col_nb,int(((width-130-col_nb*between)//col_nb)*1.25))) for x in self.frames]
        for x in self.frames:
            x.set_colorkey(x.get_at((0,0)))
        self.health=100
        self.image=self.frames[(self.pos+ind)%2]
        self.rect=self.image.get_rect(bottomleft=(self.pos*((width-130-col_nb*between)//col_nb+between)+72,0))

    #movement method
    def move(self):
        self.rect.y += vel_al
    
    #aliens out of screen
    def destroy(self):
        if self.rect.top==height:
            self.kill()

    #collision with bullets
    def damage(self):
        for b in pg.sprite.spritecollide(self,bullets,False):
            self.health-=15
            if self.health>0:
                self.hit=True
            else:
                self.die=True
            b.kill()
        for _ in pg.sprite.spritecollide(self,player,False):
            self.die=True
    
    #push back animation
    def push(self):
        if self.hit:
            if not self.w:
                self.rect.y-=10
            self.w+=0.2
            if self.w>=1:
                self.rect.y+=10
                self.w=0
                self.hit=False

    #death animation
    def anim(self):
        if self.die:
            if not self.w:
                self.frames=[pg.image.load("Graphics/explosion1.png").convert(),pg.image.load("Graphics/explosion2.png").convert()]
                self.frames=[pg.transform.scale(x,((width-130-col_nb*between)//col_nb,int(((width-130-col_nb*between)//col_nb)*1.25))) for x in self.frames]
                for x in self.frames:
                    x.set_colorkey(x.get_at((0,0)))
            self.w+=0.2
            if self.w==1:
                self.kill()
        
    def update(self):
        self.image=self.frames[(self.pos+ind)%2]
        self.move()
        self.destroy()
        self.damage()
        self.push()
        self.anim()

#initialize spaceship
player = pg.sprite.GroupSingle()
player.add(Spaceship())
vel_pl=5

#setting bullets
bullets = pg.sprite.Group()
vel_bul=10

#setting aliens
between=40
col_nb=6
dt=1000
vel_al=1
ind=0
aliens=pg.sprite.Group()
alien_timer_wave=pg.USEREVENT+1
alien_timer_anim=pg.USEREVENT+2
pg.time.set_timer(alien_timer_wave,dt)
pg.time.set_timer(alien_timer_anim,500)

#While loop
while True:
    #Checking big events
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type==pg.KEYDOWN and event.key == pg.K_ESCAPE):
            pg.quit()
            exit()
        if running:
            if event.type==alien_timer_wave:
                x=randint(0,2**col_nb)
                for i in range(col_nb):
                    if x%2==1:
                        aliens.add(Alien(pos=i))
                    x//=2
            if event.type==alien_timer_anim:
                ind=1-ind
        else:
            #starting or restarting
            if event.type==pg.KEYUP and event.key==pg.K_SPACE:
                running=True
    screen.blit(background, (0, 0))
    if running:
        bullets.update()
        player.update()
        aliens.update()
        player.draw(screen)
        bullets.draw(screen)
        aliens.draw(screen)
    else:
        #Setting the welcoming message
        welcom_txt=font.render("SPACE SHOOTER", False, '#ffffff')
        txt_rect=welcom_txt.get_rect(midtop=(width//2,50))
        border=pg.rect.Rect(txt_rect.left-6,txt_rect.top-6,txt_rect.width+12,txt_rect.height+10)
        pg.draw.rect(screen,'#0066cc',border)
        screen.blit(welcom_txt, txt_rect)
        
        #guide
        welcom_txt=font.render("Press 'space' to take off!!", False, '#ffffff')
        txt_rect=welcom_txt.get_rect(midbottom=(width//2,height-50))
        border=pg.rect.Rect(txt_rect.left-6,txt_rect.top-6,txt_rect.width+12,txt_rect.height+10)
        pg.draw.rect(screen,'#0066cc',border)
        screen.blit(welcom_txt, txt_rect)

        #logo
        logo=pg.image.load('Graphics/logo.png').convert()
        logo=pg.transform.rotozoom(logo,0,0.65)
        logo.set_colorkey(logo.get_at((0, 0)))
        screen.blit(logo,logo.get_rect(center=(width//2,height//2)))
        
    pg.display.update()
    clock.tick(60)
#todo list: collision detection /score/ health bar/ sound effects/win-lose conditions
#extansions: spaceship movement animation/accord timer to aliens' size/add special attacks/add personal soundtracks
