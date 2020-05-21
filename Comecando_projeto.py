#Importando as bibliotecas necessárias:
import pygame
import random
from os import path
 
# definindo as cores
branco= (255, 255, 255)
preto= (0, 0, 0)
vermelho= (255, 0, 0)
verde= (0, 255, 0)
azul= (0, 0, 255)
amarelo= (255, 255, 0)
azul_claro= (0, 155, 155)
fundo= azul_claro

# propriedades do jogador(player)
jogador_aceleracao= 0.5
jogador_atrito= -0.12
jogador_gravidade= 0.8
pulo= 20

# configurações do jogo
WIDTH= 480
HEIGHT= 600
FPS= 60
titulo= 'E.t de volta para casa'
nome_fonte= 'arial'
pontuacao_maxima= "highscore.txt"

vet= pygame.math.Vector2 # é usado o vetor para o movimento 

class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game= game
        self.image= pygame.Surface((30,40))
        self.image.fill(amarelo)
        self.rect= self.image.get_rect()
        self.rect.center= (WIDTH / 2, HEIGHT / 2)
        self.pos= vet(WIDTH / 2, HEIGHT / 2) #posição
        self.vel= vet(0, 0)  #velocidade
        self.acc= vet(0, 0)  #aceleração
    
    def pular(self):
        #só pula se tiver em alguma plataforma
        self.rect.x += 1
        colisao= pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1 #não é visível isso, mas necessário
        if colisao:
            self.vel.y = -pulo

class Plataforma(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h): # coordenadas e altura
        pygame.sprite.Sprite.__init__(self)
        self.image= pygame.Surface((w, h))
        self.image.fill(verde)
        self.rect= self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Game:
    def __init__(self):
        #iniciando a janela do jogo
        pygame.init()
        pygame.mixer.init()
        self.screen= pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(titulo)
        self.clock= pygame.time.Clock()
        self.running= True
        self.font_name= pygame.font.match_font(nome_fonte)

    def novo_jogo(self):
        # para começar um novo jogo
        self.all_sprites= pygame.sprite.Group()
        self.run()

    def tela_inicio(self): 

    def draw(self):
        #Desenhos do loop:
        self.screen.fill(fundo)
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def run(self):
        #Loop do jogo:
        self.playing= True
        while self.playing:
            self.clock.tick(FPS)
            self.eventos()
            self.update()
            self.draw()
    
    def update(self):
        # atualização do loop
        self.all_sprites.update()

    def eventos(self):
        # eventos do loop
        for event in pygame.event.get():
            # checa se a janela do jogo foi fechada
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing= False
                self.running = False

    def game_over(self):

g = Game()
g.tela_inicio()
while g.running:
    g.novo_jogo()
    g.game_over()
 
pygame.quit()


    