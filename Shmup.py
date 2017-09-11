## Pygame template
import pygame
import random
import os

img_folder=os.path.join(os.path.dirname(__file__),"image")
sound_folder=os.path.join(os.path.dirname(__file__),"Sound")
WIDTH=480
HEIGHT=600
FPS=30
POWERUP_TIME = 5000
score =0
##Define RGB Colors
White=(255,255,255)
Black=(0,0,0)
Red=(255,0,0)
Blue=(0,0,255)
Green=(0,255,0)
Yellow=(255,255,0)

##initialize pygame and create window
pygame.init()
##For Sound
pygame.mixer.init()
 
screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("$$ SPACE SHOOTER $$ ")
clock=pygame.time.Clock()

font_name=pygame.font.match_font('arial')
def draw_text(surf,text,size,x,y):
    font = pygame.font.Font(font_name,size)
    text_surface =font.render(text,True,White)
    text_rect=text_surface.get_rect()
    text_rect.midtop=(x,y)
    surf.blit(text_surface,text_rect)

def newmob():
    m=Mob()
    all_sprites.add(m)
    mobs.add(m)

def draw_shield_bar(surf,x,y,pct):
    if pct <0:
        pct=0
    BAR_LENGTH = 100
    BAR_HEIGHT =10
    fill=(pct/100)* BAR_LENGTH
    outline_rect=pygame.Rect(x,y,BAR_LENGTH, BAR_HEIGHT)
    fill_rect=pygame.Rect(x,y,fill, BAR_HEIGHT)
    pygame.draw.rect(surf,Green,fill_rect)
    pygame.draw.rect(surf,White, outline_rect,2)
    
def draw_lives(surf,x,y,lives,img):
    for i in range(lives):
        img_rect=img.get_rect()
        img_rect.x=x+30*i
        img_rect.y=y
        surf.blit(img,img_rect)
    
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(player_img,(50,38))
        self.image.set_colorkey(Black)
        self.rect=self.image.get_rect()
        self.radius=20
        self.rect.centerx=WIDTH/2
        self.rect.bottom=HEIGHT-10
        self.speedx=0
        self.shield=100
        self.shoot_delay=250
        self.last_shot=pygame.time.get_ticks()
        self.lives = 3
        self.hidden =False
        self.hide_tmr=pygame.time.get_ticks()
        self.power=1
        self.power_timer= pygame.time.get_ticks()
        
    def update(self):
##Unhide if hidden
##Timeout for powerup
        if self.power >=2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()

        if self.hidden and pygame.time.get_ticks() - self.hide_tmr > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10

        self.speedx=0
        keystate=pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx= -5
        if keystate[pygame.K_RIGHT]:
            self.speedx= 5
        if keystate[pygame.K_SPACE]:
            self.shoot()
        self.rect.x+=self.speedx

        if self.rect.right>WIDTH:
            self.rect.right=WIDTH
        if self.rect.left<0:
            self.rect.left=0
    def powerup(self):
        self.power+=1
        self.power_time=pygame.time.get_ticks()
        
    def shoot(self):
        now=pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot=now
            if self.power==1:
                bullet=Bullet(self.rect.centerx,self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            if self.power>=2:
                bullet1=Bullet(self.rect.left,self.rect.centery)
                bullet2=Bullet(self.rect.right,self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()
                

    def hide(self):
        ## hide the player temporarily
        self.hidden=True
        self.hide_tmr=pygame.time.get_ticks()
        self.rect.center=(WIDTH/2,HEIGHT+200)
              
            
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=random.choice(meteor_images)
        self.image.set_colorkey(Black)
        self.rect=self.image.get_rect()
        self.radius=int(self.rect.width*0.85/2)      
        self.rect.x=random.randrange(WIDTH - self.rect.width)
        self.rect.y=random.randrange(-100,-40)
        self.speedy=random.randrange(1,8)
        self.speedx=random.randrange(-3 ,3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()
        
    def update(self):
        self.rect.y +=self.speedy
        self.rect.x+=self.speedx
        if self.rect.top > HEIGHT +10 or self.rect.left < -25 or self.rect.right>WIDTH + 20:
            self.rect.x=random.randrange(WIDTH-self.rect.width)
            self.rect.y=random.randrange(-100,-40)
            self.speddy=random.randrange(1,8)

    
        
class Bullet(pygame.sprite.Sprite):
     def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=bullet_img
        self.image.set_colorkey(Black)
        self.rect=self.image.get_rect()
        self.rect.bottom=y
        self.rect.centerx=x
        self.speedy=-10

     def update(self):
        self.rect.y +=self.speedy
        ##Kill if it moves off the top of the screen
        if self.rect.bottom <0:
            self.kill()
class Pow(pygame.sprite.Sprite):
     def __init__(self,center):
         pygame.sprite.Sprite.__init__(self)
         self.type=random.choice(['shield','gun'])
         self.image=powerup_images[self.type]
         self.image.set_colorkey(Black)
         self.rect=self.image.get_rect()
         self.rect.center = center
         self.speedy= 5
         
     def update(self):
        self.rect.y +=self.speedy
        ##Kill if it moves off the top of the screen
        if self.rect.top >HEIGHT:
            self.kill()
         
         
    
class Explosion(pygame.sprite.Sprite):
    def __init__(self,center,size):
         pygame.sprite.Sprite.__init__(self)
         self.size =size
         self.image= explosion_img[self.size][0]
         self.rect=self.image.get_rect()
         self.rect.center=center
         self.frame=0
         self.last_update=pygame.time.get_ticks()
         self.frame_rate=75

    def update(self):
        now=pygame.time.get_ticks()
        if now-self.last_update >self.frame_rate:
            self.last_update=now
            self.frame +=1
            if self.frame ==len(explosion_img[self.size]):
                self.kill()
            else:
                center=self.rect.center
                self.image=explosion_img[self.size][self.frame]
                self.rect.center=center
   
def  show_go_screen():
    screen.blit(backgrond_img,background_rect)
    draw_text(screen,"Space Shooter",64,WIDTH/2,HEIGHT/4)
    draw_text(screen,str(score),25,WIDTH/2,10)
    draw_text(screen,"Arrow keys move,space to fire",22,WIDTH/2,HEIGHT/2)
    draw_text(screen,"Press a key to begin",18,WIDTH/2,HEIGHT *3/4)
    pygame.display.flip()
    waiting=True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                pygame.quit()
            if  event.type ==pygame.KEYUP:
                waiting=False
                
       

## Load all game graphics
background=pygame.image.load(os.path.join(img_folder,"blue.png")).convert()
backgrond_img=pygame.transform.scale(background,(480,600))
background_rect=background.get_rect()
player_img=pygame.image.load(os.path.join(img_folder,"playerShip1_orange.png")).convert()
player_img_mini=pygame.transform.scale(player_img, (25, 19))
player_img_mini.set_colorkey(Black)
#meteor_img=pygame.image.load(os.path.join(img_folder,"meteorBrown_big2.png")).convert()
meteor_images = []
meteor_list = [
    'meteorBrown_big1.png',
    'meteorBrown_big2.png', 
    'meteorBrown_med1.png', 
    'meteorBrown_med3.png',
    'meteorBrown_small1.png',
    'meteorBrown_small2.png',
    'meteorBrown_tiny1.png'
]

for image in meteor_list:
    meteor_images.append(pygame.image.load(os.path.join(img_folder+'/SpaceShooterRedux/PNG/Meteors/', image)).convert())
  
bullet_img=pygame.image.load(os.path.join(img_folder,"laserBlue16.png")).convert()

explosion_img={}
explosion_img['lg']=[]
explosion_img['sm']=[]
explosion_img['player']=[]


for i in range(9):
    filename='regularExplosion0{}.png'.format(i)
    img=pygame.image.load(os.path.join(img_folder,filename)).convert()
    img.set_colorkey(Black)
    img_lg=pygame.transform.scale(img,(75,75))
    explosion_img['lg'].append(img_lg)
    img_sm=pygame.transform.scale(img,(32,32))
    explosion_img['sm'].append(img_sm)
    filename='sonicExplosion0{}.png'.format(i)
    img=pygame.image.load(os.path.join(img_folder,filename)).convert()
    img.set_colorkey(Black)
    explosion_img['player'].append(img)
    
powerup_images={}
powerup_images['shield']=pygame.image.load(os.path.join(img_folder,'shield_gold.png')).convert()
powerup_images['gun']=pygame.image.load(os.path.join(img_folder,'bolt_gold.png')).convert()

## Load Music
shoot_sound=pygame.mixer.Sound(os.path.join(sound_folder,'Laser_Shoot6.wav'))
shield_sound=pygame.mixer.Sound(os.path.join(sound_folder,'Pickup_Coin.wav'))
power_sound=pygame.mixer.Sound(os.path.join(sound_folder,'Powerup.wav'))
explsn_sound=pygame.mixer.Sound(os.path.join(sound_folder,'Explosion7.wav'))
player_die_sound=pygame.mixer.Sound(os.path.join(sound_folder,'Explosion2.wav'))
pygame.mixer.music.load(os.path.join(sound_folder,'tgfcoder-FrozenJam-SeamlessLoop.ogg'))


pygame.mixer.music.play(loops=-1)
##Game Loop
game_over =True
running =True

while running:
    if game_over:
        show_go_screen()
        game_over=False
        pygame.mixer.music.set_volume(4)
        all_sprites=pygame.sprite.Group()
        powerups=pygame.sprite.Group()
        mobs=pygame.sprite.Group()
        bullets=pygame.sprite.Group()
        player=Player()
        all_sprites.add(player)
        for i in range(8):
            newmob()
        score =0
        
    ##Keep loop running at the right speed
    clock.tick(FPS)
    ##Process input(events)
    for event in pygame.event.get():
        # Check for closing the window
        if event.type==pygame.QUIT:
            running =False
        ## Press ESC to exit game
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    ##Updates
    all_sprites.update()        
##Check to see if a bullet hit a mob
    hits=pygame.sprite.groupcollide(mobs,bullets,True,True)
    for hit in hits:
        score += 50-hit.radius
        explsn_sound.play()
        expl=Explosion(hit.rect.center,'lg')
        all_sprites.add(expl)
        if random.random()>0.9:
            pow =Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        newmob()
        
## check to see if a mob hit the player
    hits=pygame.sprite.spritecollide(player,mobs,True,pygame.sprite.collide_circle)
    for hit in hits:
        player.shield-=hit.radius*2
        expl=Explosion(hit.rect.center,'sm')
        all_sprites.add(expl)
        newmob()
        if player.shield <=0 :
            player_die_sound.play()
            death_explosion=Explosion(player.rect.center,'player')
            all_sprites.add(death_explosion)
            player.hide()
            player.lives -=1
            player.shield=100
##check to see if the player hit a powerup
    hits=pygame.sprite.spritecollide(player,powerups,True)
    for hit in hits:
        if hit.type=='shield':
            player.shield +=random.randrange(10,30)
            shield_sound.play()
            if player.shield>=100:
                player.shield =100
        if hit.type =='gun':
            player.powerup()
            power_sound.play() 
                  

##if the player has died and the explosion has finished playing        
    if player.lives == 0 and not death_explosion.alive():
        game_over=True
    ##Draw/Render
    screen.fill(Black)
    screen.blit(backgrond_img,background_rect)
    all_sprites.draw(screen)
    draw_text(screen,str(score),18,WIDTH/2,10)
    draw_shield_bar(screen,5,5,player.shield)
    draw_lives(screen,WIDTH-100,5,player.lives,player_img_mini)
##After drwaing everything flip the display
    pygame.display.flip()
    
pygame.quit()
