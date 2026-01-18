import pygame as pg
from sys import exit
from random import choice
pg.init()

#variables declaration
clock = pg.time.Clock()
running = False
font=pg.font.Font("Font/Pixeltype.ttf",72)
height=width=600
score=0
cross=0
level=1

#Setting the screen
screen = pg.display.set_mode((width,height))
pg.display.set_caption('Space shooter')

#Setting the background
background = pg.image.load("Graphics/background.jpg").convert()
background = pg.transform.scale(background,(600,600))

#Setting the healthbar rect
hb_rect=pg.rect.Rect(0,height-20,width,20)

#adjust the health-bar's color with health
def set_color(health):
    if health>=60:
        return '#00ff00'
    elif health>=30:
        return '#ff8800'
    else:
        return '#ff0000'

#the spaceship class
class Spaceship(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load("Graphics/spaceship.png").convert()
        self.image = pg.transform.rotozoom(self.image,0,0.75)
        self.image.set_colorkey(self.image.get_at((0,0)))
        self.rect1 = self.image.get_rect(midbottom=hb_rect.midtop)
        self.rect=pg.rect.Rect((2*self.rect1.centerx+self.rect1.left)//3,(2*self.rect1.centery+self.rect1.top)//3,self.rect1.width//3,self.rect1.height//3)
        self.health=100
        self.die=False
        self.cool_down=0
        self.w=0

    #changing the draw method
    def draw1(self):
        screen.blit(self.image,self.rect1)

    #input method
    def input(self):
        keys=pg.key.get_pressed()
        if keys[pg.K_LEFT] and self.rect1.left>-50 and not self.die and cross<3:
            self.rect.x -= vel_pl
            self.rect1.x -= vel_pl
        if keys[pg.K_RIGHT] and self.rect1.right<width+50 and not self.die and cross<3:
            self.rect.x += vel_pl
            self.rect1.x += vel_pl
        if keys[pg.K_UP] and self.rect1.top>0 and not self.die and cross<3:
            self.rect.y -= vel_pl
            self.rect1.y -= vel_pl
        if keys[pg.K_DOWN] and self.rect1.bottom<height-20 and not self.die and cross<3:
            self.rect.y += vel_pl
            self.rect1.y += vel_pl
        if keys[pg.K_SPACE] and self.cool_down<=0 and not self.die and cross<3 :
            if level==2:
                bullets.add(Bullet(order=0))
            else:
                bullets.add(Bullet(order=1))
                bullets.add(Bullet(order=2 ))
            self.cool_down=1

    #cool down configuration
    def hold(self):
        if self.cool_down>0:
            self.cool_down-=recharge

    #damage method
    def damage(self):
        if self.health<=0:
            self.die=True

    #death animation
    def anim(self):
        global running,cross,score,level
        if self.die or cross>=3:
            if self.w<=0:
                self.frames=[pg.image.load("Graphics/explosion1.png").convert(),pg.image.load("Graphics/explosion2.png").convert()]
                self.frames=[pg.transform.scale(x,(self.rect1.width,self.rect1.width*1.2)) for x in self.frames]
                for x in self.frames:
                    x.set_colorkey(x.get_at((0,0)))
            self.image=self.frames[ind]
            self.w+=0.01
            if self.w>=1:
                running=False

    def update(self):
        self.input()
        self.hold()
        self.damage()
        self.anim()
        self.draw1()

#The bullets class
class Bullet(pg.sprite.Sprite):
    def __init__(self,order):
        super().__init__()
        if level==2:
            self.image = pg.image.load("Graphics/Projectile.png").convert()
            self.image = pg.transform.rotozoom(self.image,90,0.4)
            self.rect = self.image.get_rect(midbottom=player.sprite.rect1.midtop)
            self.damage=60
        if level==1:
            self.image = pg.image.load("Graphics/bullet.png").convert()
            self.image = pg.transform.rotozoom(self.image, -45, 1.5)
            if order==1:
                self.rect = self.image.get_rect(bottomright=player.sprite.rect1.midtop)
            elif order==2:
                self.rect = self.image.get_rect(bottomleft=player.sprite.rect1.midtop)
            self.damage=25
        self.image.set_colorkey(self.image.get_at((0, 0)))

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
        if level==1:
            self.frames=[pg.image.load("Graphics/alien1.png").convert(),pg.image.load("Graphics/alien2.png").convert()]
            self.frames=[pg.transform.scale(x,((width-70-col_nb*between)//col_nb,int(((width-70-col_nb*between)//col_nb)*1.25))) for x in self.frames]
        elif level==2:
            self.frames=[pg.image.load("Graphics/alien3.png").convert(),pg.image.load("Graphics/alien4.png").convert()]
            self.frames=[pg.transform.scale(x,((width-70-col_nb*between)//col_nb,int(((width-70-col_nb*between)//col_nb)*1.25))) for x in self.frames]
        for x in self.frames:
            x.set_colorkey(x.get_at((0,0)))
        self.health=75+25*level
        self.image=self.frames[(self.pos+ind)%2]
        self.rect=self.image.get_rect(bottomleft=(self.pos*((width-70-col_nb*between)//col_nb+between)+42,0))

    #movement method
    def move(self):
        self.rect.y += vel_al
    
    #aliens out of screen
    def destroy(self):
        global cross
        if self.rect.top==height-20:
            cross+=1
            self.kill()

    #collision with bullets/the player
    def damage(self):
        global score
        for b in pg.sprite.spritecollide(self,bullets,True):
            self.health-=b.damage
            if self.health>0:
                self.hit=True
            else:
                if not self.die:
                    score+=1
                self.die = True
        for p in pg.sprite.spritecollide(self,player,False):
            p.health-=20
            boom.add(Boom(self.rect.center))
            self.kill()

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
                self.frames=[pg.transform.scale(x,((width-70-col_nb*between)//col_nb,int(((width-70-col_nb*between)//col_nb)*1.25))) for x in self.frames]
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

#explosion class
class Boom(pg.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.frames = [pg.image.load("Graphics/explosion1.png").convert(), pg.image.load("Graphics/explosion2.png").convert()]
        self.frames = [pg.transform.scale(x, ((width - 130 - col_nb * between) // col_nb,int(((width - 130 - col_nb * between) // col_nb) * 1.25))) for x in self.frames]
        for x in self.frames:
            x.set_colorkey(x.get_at((0, 0)))
        self.image=self.frames[(pos[0]+ind)%2]
        self.rect = self.image.get_rect(center=pos)
        self.w=0
        self.pos=pos

    #waiting
    def anim(self):
        self.w += 0.2
        if self.w == 1:
            self.kill()

    def update(self):
        self.image=self.frames[(self.pos[0]+ind)%2]
        self.anim()

#initialize spaceship
player = pg.sprite.GroupSingle()
player.add(Spaceship())
vel_pl=5
recharge=0.2

#setting bullets
bullets = pg.sprite.Group()
vel_bul=10

#setting aliens
between=50
col_nb=5
dt=int((width-70-col_nb*between)//col_nb*20)+100
vel_al=1
ind=0
aliens=pg.sprite.Group()
alien_timer_wave=pg.USEREVENT+1
alien_timer_anim=pg.USEREVENT+2
pg.time.set_timer(alien_timer_wave,dt)
pg.time.set_timer(alien_timer_anim,500)
randomizer1=[x for x in range(0,2**col_nb) if str(bin(x)).count("1")<=4]
randomizer2=[x for x in range(0,2**(col_nb+2)) if str(bin(x)).count("1")<=4]+[x for x in range(0,2**(col_nb+2)) if str(bin(x)).count("1")<=3]

#Setting explosion group
boom=pg.sprite.Group()

#While loop
while True:
    #Checking big events
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type==pg.KEYDOWN and event.key == pg.K_ESCAPE):
            pg.quit()
            exit()
        if running :
            if event.type==alien_timer_wave:
                if level==1:
                    x=choice(randomizer1)
                elif level==2:
                    x=choice(randomizer2)
                for i in range(col_nb):
                    if x % 2 == 1:
                        aliens.add(Alien(pos=i))
                    x //= 2
            if event.type == alien_timer_anim:
                ind = 1 - ind
        else:
            #starting or restarting
            if event.type==pg.KEYUP and event.key==pg.K_SPACE:
                player.sprite.__init__()
                boom.empty()
                aliens.empty()
                bullets.empty()
                cross= 0
                score=0
                level=1
                running=True
                col_nb=5
                between=50
                recharge=0.2
                vel_al=0.75
    screen.blit(background, (0, 0))
    if running:
        if score >= 50 and level == 1:
            for a in aliens:
                a.die=True
            level = 2
            col_nb = 7
            between=30
            recharge=0.15
            vel_al=0.6
        rhb_rect=pg.rect.Rect(0, height - 20, (width*player.sprite.health)//100, 20)
        bullets.update()
        player.update()
        aliens.update()
        boom.update()
        aliens.draw(screen)
        if cross>0:
            pg.draw.circle(screen,'#ff0000',(30,30),20)
        if cross>1:
            pg.draw.circle(screen,'#ff0000',(80,30),20)
        if cross>2:
            pg.draw.circle(screen,'#ff0000',(130,30),20)
        pg.draw.rect(screen,'#888888',hb_rect)
        pg.draw.rect(screen,set_color(player.sprite.health),rhb_rect)
        bullets.draw(screen)
        boom.draw(screen)
        score_txt = font.render(f'SCORE: {score}', False, '#ffffff')
        score_txt=pg.transform.rotozoom(score_txt,0,0.5)
        score_rect = score_txt.get_rect(topright=(width, 0))
        level_txt = font.render(f'Level: {level}', False, '#ffffff')
        level_txt=pg.transform.rotozoom(level_txt,0,0.5)
        level_rect = level_txt.get_rect(topright=(width-score_rect.width-10,0))
        screen.blit(score_txt, score_rect)
        screen.blit(level_txt, level_rect)
    else:
        #Setting the welcoming message
        welcom_txt = font.render("SPACE SHOOTER", False, '#ffffff')
        txt_rect = welcom_txt.get_rect(midtop=(width // 2, 50))
        border = pg.rect.Rect(txt_rect.left - 6, txt_rect.top - 6, txt_rect.width + 12, txt_rect.height + 10)
        pg.draw.rect(screen,'#0066cc',border)
        screen.blit(welcom_txt, txt_rect)

        #guide
        welcom_txt=font.render("Press 'space' to take off!!", False, '#ffffff')
        txt_rect=welcom_txt.get_rect(midbottom=(width//2,height))
        border_txt=pg.rect.Rect(txt_rect.left-6,txt_rect.top-6,txt_rect.width+12,txt_rect.height+10)
        pg.draw.rect(screen,'#0066cc',border_txt)
        screen.blit(welcom_txt, txt_rect)

        #score
        if score>0:
            score_txt = font.render(f'SCORE: {score}', False, '#ffffff')
            score_rect = score_txt.get_rect(midbottom=(width // 2, height - 50))
            border_score = pg.rect.Rect(score_rect.left - 6, score_rect.top - 6, score_rect.width + 12, score_rect.height + 10)
            pg.draw.rect(screen, '#0066cc', border_score)
            screen.blit(score_txt, score_rect)

        #logo
        logo = pg.image.load('Graphics/logo.png').convert()
        logo = pg.transform.rotozoom(logo, 0, 0.65)
        logo.set_colorkey(logo.get_at((0, 0)))
        screen.blit(logo,logo.get_rect(center=(width//2,height//2)))

    pg.display.update()
    clock.tick(60)

#requirements: sound effects/win conditions
#extansions:add special attacks/add personal soundtracks/add final boss
#Updates: adjusted difficulty shift& bullets' images/differentiated the projectiles between level 1 & 2(recharge & damage)/adjusted the player's movement limits on edges/changed aliens' images between levels