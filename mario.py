import pgzrun
import random
import math
from pygame import Rect

WIDTH=800
HEIGHT=600

MENU="menu"
GAME="game"
estado=MENU
musica=True

class Boton:
    def __init__(self,t,x,y,w,h,accion):
        self.rect=Rect(x,y,w,h)
        self.t=t
        self.accion=accion
    def draw(self):
        screen.draw.filled_rect(self.rect,(60,120,220))
        screen.draw.text(self.t,center=self.rect.center,fontsize=28,color="white")
    def click(self,pos):
        if self.rect.collidepoint(pos):
            self.accion()

player=Rect(80,450,30,45)
vx=4
vy=0
g=0.8
jump=-14
ground=550
on_ground=True
score=0
lives=3
platforms=[]
coins=[]
enemies=[]
camera=0

def reset():
    global vy,on_ground,score,camera
    player.topleft=(80,ground-45)
    vy=0
    on_ground=True
    score=0
    camera=0
    platforms[:]=[]
    coins[:]=[]
    enemies[:]=[]
    x=250
    for i in range(10):
        h=random.randint(60,150)
        platforms.append(Rect(x,ground-h,80,h))
        coins.append(Rect(x+25,ground-h-30,20,20))
        enemies.append(Rect(x+180,ground-30,30,30))
        x+=220

def start():
    global estado
    estado=GAME
    reset()

def toggle():
    global musica
    musica = not musica
    if musica:
        music.play("background")      
        music.set_volume(0.5)     
    else:
        music.stop()             
    botones[1].t = f"Musica: {'ON' if musica else 'OFF'}"

def salir():
    raise SystemExit

botones=[
Boton("Iniciar",300,180,200,50,start),
Boton("Musica: ON",300,260,200,50,toggle),
Boton("Salir",300,340,200,50,salir)
]

def draw():
    screen.fill((135,206,235))
    if estado==MENU:
        screen.draw.text("BROSS MARIO",center=(400,90),fontsize=48,color="White")
        for b in botones:b.draw()
    else:
        screen.draw.filled_rect(Rect(0,ground,WIDTH,50),"brown")
        for p in platforms:
            screen.draw.filled_rect(Rect(p.x-camera,p.y,p.w,p.h),"green")
        for c in coins:
            screen.draw.filled_circle((c.centerx-camera,c.centery),10,"gold")
        for e in enemies:
            screen.draw.filled_rect(Rect(e.x-camera,e.y,e.w,e.h),"black")
            screen.draw.filled_rect(Rect(player.x-camera,player.y,player.w,player.h),"red")
            screen.draw.text(f"PUNTUACION:  {score}",(10,10),fontsize=28,color="red")
            screen.draw.text(f"VIDAS:  {lives}",(10,40),fontsize=28,color="red")

def update():
    global vy, on_ground, camera, score, lives
    if estado != GAME:
        return
    if keyboard.left:
        player.x -= vx
    if keyboard.right:
        player.x += vx
    if keyboard.space and on_ground:
        vy = jump
        on_ground = False
    vy += g
    player.y += vy
    if player.bottom >= ground:
        player.bottom = ground
        vy = 0
        on_ground = True
    for p in platforms:
        if player.colliderect(p):
            if vy > 0 and player.bottom - vy <= p.top:
                player.bottom = p.top
                vy = 0
                on_ground = True
            elif vy < 0 and player.top - vy >= p.bottom:
                player.top = p.bottom
                vy = 0
            elif player.centerx < p.centerx:
                player.right = p.left
            else:
                player.left = p.right
    for c in coins[:]:
        if player.colliderect(c):
            coins.remove(c)
            score += 10
    for e in enemies:
        e.x += math.sin(random.random()) * 0.5
        if player.colliderect(e):
            lives -= 1
            player.topleft = (80, ground - 45)
            if lives <= 0:
                start()
    camera = max(0, player.centerx - 250)

def on_mouse_down(pos):
    if estado==MENU:
        for b in botones:b.click(pos)

pgzrun.go()