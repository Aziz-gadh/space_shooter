import pygame as pg
from sys import exit
from random import choice,uniform
pg.init()

#variables declaration
clock = pg.time.Clock()
running = False
font=pg.font.Font("Font/Pixeltype.ttf",72)
height=width=600
score=0
cross=0
level=1
game_music=pg.mixer.Sound("Sounds/game_music.mpeg")
boss_music=pg.mixer.Sound("Sounds/Boss_music.mp3")
game_music.set_volume(0.4)
boss_music.set_volume(0.6)
pl_boss=1
pl_game=1

#Setting the screen
screen = pg.display.set_mode((width,height))
pg.display.set_caption('Space shooter')

#Setting the background
background = pg.image.load("Graphics/background.jpg").convert()
background = pg.transform.scale(background,(600,600))

#Setting the healthbars rect
hb_rect=pg.rect.Rect(0,height-20,width,20)
bhb_rect=pg.rect.Rect(0,0,width,20)

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
        global running,cross,score,level,pl_boss,pl_game
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
                boss_music.stop()
                game_music.stop()
                if pl_boss==0:
                    pl_boss=1
                if pl_game==0:
                    pl_game=1

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
        if level>=2:
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

    #movement method
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
            self.frames=[pg.transform.scale(x,((width-70-col_nb*between)//col_nb,((width-70-col_nb*between)//col_nb)*1.25)) for x in self.frames]
        elif level==2:
            self.frames=[pg.image.load("Graphics/alien3.png").convert(),pg.image.load("Graphics/alien4.png").convert()]
            self.frames=[pg.transform.scale(x,((width-70-col_nb*between)//col_nb,int(((width-70-col_nb*between)//col_nb)*1.25))) for x in self.frames]
        else:
            self.image=pg.image.load(f"Graphics/Boss.png").convert()
            self.image=pg.transform.scale(self.image, (width*4/15,height//3))
            self.image.set_colorkey(self.image.get_at((0, 0)))
        if level<3:
            for x in self.frames:
                x.set_colorkey(x.get_at((0, 0)))
            self.health=75+25*level
            self.image=self.frames[(self.pos+ind)%2]
            self.rect=self.image.get_rect(bottomleft=(self.pos*((width-70-col_nb*between)//col_nb+between)+42,0))
        else:
            self.health=100000
            self.rect = self.image.get_rect(midbottom=(width//2, 0))
        self.dir='R'

    #movement method
    def move(self):
        if level<3 or self.rect.top<20:
            self.rect.y += vel_al
        else:
            if self.rect.right<width and self.dir=='R':
                self.rect.x += vel_al
            elif self.rect.left>0 and self.dir=='L':
                self.rect.x -= vel_al
            elif self.rect.right>=width and self.dir=='R':
                self.dir='L'
                self.rect.x -= vel_al
            elif self.rect.left<=0 and self.dir=='L':
                self.dir='R'
                self.rect.x+= vel_al
    
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
            if level<3:
                boom.add(Boom(pos=self.rect.center,side=(width - 130 - col_nb * between) // col_nb))
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
        if level<3:
            self.image=self.frames[(self.pos+ind)%2]
        self.move()
        self.destroy()
        self.damage()
        self.push()
        self.anim()

#explosion class
class Boom(pg.sprite.Sprite):
    def __init__(self,pos,side):
        super().__init__()
        self.frames = [pg.image.load("Graphics/explosion1.png").convert(), pg.image.load("Graphics/explosion2.png").convert()]
        self.frames = [pg.transform.scale(x, (side,side * 1.25)) for x in self.frames]
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

#The comet's class
class Comet(pg.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.image=pg.image.load("Graphics/comet.png").convert()
        self.image=pg.transform.rotozoom(self.image,180,3)
        self.image.set_colorkey(self.image.get_at((0, 0)))
        self.rect = self.image.get_rect(midtop=(pos,boss.sprite.rect.bottom))

    #movement method
    def move(self):
        self.rect.y += vel_com

    #out of screen
    def destroy(self):
        if self.rect.top==height-20:
            self.kill()

    #collision method
    def damage(self):
        pg.sprite.spritecollide(self,bullets,True)
        for p in pg.sprite.spritecollide(self,player,False):
            p.health-=25
            boom.add(Boom(pos=self.rect.center,side=self.rect.width))
            self.kill()

    def update(self):
        self.move()
        self.destroy()
        self.damage()

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
alien_timer_att=pg.USEREVENT+3
pg.time.set_timer(alien_timer_wave,dt)
pg.time.set_timer(alien_timer_anim,500)
pg.time.set_timer(alien_timer_att,1000)
randomizer1=[x for x in range(0,2**col_nb) if str(bin(x)).count("1")<=4]
randomizer2=[x for x in range(0,2**(col_nb+2)) if str(bin(x)).count("1")<=4]+[x for x in range(0,2**(col_nb+2)) if str(bin(x)).count("1")<=3]

#Setting explosion group
boom=pg.sprite.Group()

#Setting the comets sprite
vel_com=3

#Setting the boss Group
boss=pg.sprite.GroupSingle()

#While loop
while True:
    #Checking big events
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type==pg.KEYDOWN and event.key == pg.K_ESCAPE):
            pg.quit()
            exit()
        if running :
            if event.type==alien_timer_wave:
                if level<3:
                    if level==1:
                        x=choice(randomizer1)
                    elif level==2:
                        x=choice(randomizer2)
                    for i in range(col_nb):
                        if x % 2 == 1:
                            aliens.add(Alien(pos=i))
                        x //= 2
            if level==3:
                if event.type==alien_timer_att:
                    x=uniform(boss.sprite.rect.left, boss.sprite.rect.right)
                    aliens.add(Comet(pos=x))
            if event.type == alien_timer_anim:
                ind = 1 - ind
        else:
            #starting or restarting
            if event.type==pg.KEYUP and event.key==pg.K_RETURN:
                player.sprite.__init__()
                boss.empty()
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
        rhb_rect=pg.rect.Rect(0, height - 20, (width*player.sprite.health)//100, 20)
        bullets.update()
        boss.update()
        player.update()
        aliens.update()
        aliens.draw(screen)
        boss.draw(screen)
        boom.update()
        if level==3:
            pg.draw.rect(screen, '#888888', bhb_rect)
            brhb_rect = pg.rect.Rect(0,0, (width * boss.sprite.health) // 100000, 20)
            pg.draw.rect(screen, set_color(boss.sprite.health//1000), brhb_rect)
        if score >= 50 and level == 1:
            for a in aliens:
                a.die=True
            level = 2
            col_nb = 7
            between=30
            recharge=0.15
            vel_al=0.6
        if score>=120 and level==2:
            for a in aliens:
                a.die=True
            level=3
            col_nb = 1
            recharge=0.3
            vel_al=3
            boss.add(Alien(pos=0))
            game_music.stop()
            boss_music.play(-1)
            pl_boss=0
            pl_game=1
        if score>120 and level==3:
            running=False
            boss_music.stop()
            pl_boss=1
        if level!=3 and pl_game!=0 and running:
            game_music.play(-1)
            pl_game=0
        if cross>0 and level!=3:
            pg.draw.circle(screen,'#ff0000',(30,30),20)
        if cross>1 and level!=3:
            pg.draw.circle(screen,'#ff0000',(80,30),20)
        if cross>2 and level!=3:
            pg.draw.circle(screen,'#ff0000',(130,30),20)
        pg.draw.rect(screen,'#888888',hb_rect)
        pg.draw.rect(screen,set_color(player.sprite.health),rhb_rect)
        bullets.draw(screen)
        boom.draw(screen)
        if level!=3:
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
        welcom_txt=font.render("Press 'enter' to take off!!", False, '#ffffff')
        txt_rect=welcom_txt.get_rect(midbottom=(width//2,height))
        border_txt=pg.rect.Rect(txt_rect.left-6,txt_rect.top-6,txt_rect.width+12,txt_rect.height+10)
        pg.draw.rect(screen,'#0066cc',border_txt)
        screen.blit(welcom_txt, txt_rect)

        #score
        if score>0 :
            if score<=120:
                score_txt = font.render(f'GIT GUD! SCORE: {score}', False, '#ffffff')
            else:
                score_txt = font.render('MISSION ACCOMPLISHED !!', False, '#ffffff')
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
