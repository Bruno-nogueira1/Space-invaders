import math
import random
import pygame
from pygame import font
from pygame import display
from pygame import event
from pygame import image
from pygame import mixer
from pygame.constants import K_SPACE, KEYDOWN, KEYUP, NUMEVENTS, QUIT, K_a, K_d

pygame.init()

tela = display.set_mode((800,600))
icon = image.load('espadas.png')
background = image.load('fundo.jpg')
display.set_caption('Space invaders')
display.set_icon(icon)

naveimg = image.load('nave.png')
naveposx = 336
naveposxvelo = 0
naveposy = 504

alienimg = []
alienposx = []
alienposxvelo = []
alienposy = []

numinimigos = 15

for c in range(numinimigos):
    alienimg.append(image.load('alien.png'))
    alienposx.append(random.randint(0,736))
    alienposxvelo.append(0.4)
    alienposy.append(random.randint(0,192))

balaimg = image.load('bala.png')
balaposx = 0
balaposy = 504
recarregar = False

pontuacao = 0
fonte = font.Font('freesansbold.ttf',25)

def mostrarplacar():
    placar = fonte.render('Placar: '+ str(pontuacao),True,(0,255,0))
    tela.blit(placar,(10,10))

def atirar(x,y):
    global recarregar
    tela.blit(balaimg,(x+35, y+10))

def inimigo(alienposx,alienposy,c):
    tela.blit(alienimg[c],(alienposx[c],alienposy[c]))
    

def jogador(x,y):
    tela.blit(naveimg,(x,y))
 
def colidir(alienposx,alienposy,balaposx,balaposy):
    dist = math.sqrt(math.pow(alienposx-balaposx,2) + math.pow(alienposy-balaposy,2))
    if dist < 32:
        return True
    else:
        return False
    
    
rodando = True

while rodando:
    tela.blit(background,(0,0))
    for evento in event.get():
        if evento.type == QUIT:
            rodando = False
        #BINDS DO TECLADO
        if evento.type == KEYDOWN:
            if evento.key == K_d:
                naveposxvelo = 0.5
            if evento.key == K_a:
                naveposxvelo = -0.5
            if evento.key == K_SPACE:
                if not recarregar:
                    balaposx = naveposx
                    tiro = mixer.Sound('tiro.wav')
                    mixer.Sound.set_volume(tiro,0.1)
                    mixer.Sound.play(tiro)
                recarregar = True
        if evento.type == KEYUP:
            if evento.key == K_d or evento.key == K_a:
                naveposxvelo = 0
    #BORDAS
    if naveposx >= 704:
        naveposx = 704
    if naveposx <= 0:
        naveposx = 0
    if recarregar:
        atirar(balaposx,balaposy)
        balaposy -= 0.8
        if balaposy <= 0:
            balaposy = 504
            recarregar = False
    naveposx += naveposxvelo
    jogador(naveposx,naveposy)
    for c in range(numinimigos):
        if alienposy[c] >= 450:
            for c in range(numinimigos):
                alienposy[c] = 2000
            gameover = font.Font('freesansbold.ttf',64)
            gameovertexto = gameover.render('GAME OVER',True,(255,0,0))
            tela.blit(gameovertexto,(200,250))
            break
        if alienposx[c] <= 0:
            alienposxvelo[c] = 0.3
            alienposy[c] += 42
        if alienposx[c] >= 736:
            alienposxvelo[c] = -0.3
            alienposy[c] += 42
            primeiravolta = True
        alienposx[c] += alienposxvelo[c]
        inimigo(alienposx,alienposy,c)
        colisao = colidir(alienposx[c],alienposy[c],balaposx,balaposy)
        if colisao:
            explosao = mixer.Sound('explosao.wav')
            mixer.Sound.play(explosao)
            mixer.Sound.set_volume(explosao,0.1)
            balaposy = 504
            recarregar = False
            pontuacao += 50
            alienposy[c] = random.randint(0,256)
            alienposx[c] = random.randint(0,736)
    mostrarplacar()
    display.update()