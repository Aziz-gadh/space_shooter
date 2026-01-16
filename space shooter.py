import pygame as pg
from sys import exit
pg.init()
#Setting the screen
screen = pg.display.set_mode((600,600))
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
        self.rect=self.image.get_rect(bottom=600)


    #input movement method
    def move(self):
        keys=pg.key.get_pressed()
        if keys[pg.K_LEFT] and self.rect.left>0:
            self.rect.x-=vel_pl
        if keys[pg.K_RIGHT] and self.rect.right<600:
            self.rect.x+=vel_pl
        if keys[pg.K_UP] and self.rect.top>0:
            self.rect.y-=vel_pl
        if keys[pg.K_DOWN] and self.rect.bottom<600:
            self.rect.y+=vel_pl

    def update(self):
        self.move()

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


#variables declaration
clock = pg.time.Clock()
running = False
vel_pl=5
vel_bul=10
font=pg.font.Font("Font/Pixeltype.ttf",72)

#initialize spaceship
player = pg.sprite.GroupSingle()
player.add(Spaceship())
bullets = pg.sprite.Group()
#While loop
while True:
    #Checking keys
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type==pg.KEYDOWN and event.key == pg.K_ESCAPE):
            pg.quit()
            exit()
        if running and event.type==pg.KEYDOWN and event.key == pg.K_SPACE:
            bullets.add(Bullet())
    screen.blit(background, (0, 0))
    if running:
        player.update()
        bullets.update()
        player.draw(screen)
        bullets.draw(screen)
    else:
        #Setting the welcoming message
        welcom_txt=font.render("SPACE SHOOTER", False, '#ffffff')
        txt_rect=welcom_txt.get_rect(midtop=(300,50))
        border=pg.rect.Rect(txt_rect.left-6,txt_rect.top-6,txt_rect.width+12,txt_rect.height+10)
        pg.draw.rect(screen,'#0066cc',border)
        screen.blit(welcom_txt, txt_rect)
    pg.display.update()
    clock.tick(60)
#todo list: enemy spawning and movement/collision detection(2) /score/ health bar/ sound effects/win-lose conditions