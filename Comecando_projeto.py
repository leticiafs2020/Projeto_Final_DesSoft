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
    
    def update(self):
        self.acc= vet(0, jogador_gravidade)
        keys= pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acc.x= -jogador_aceleracao
        if keys[pygame.K_RIGHT]:
            self.acc.x= jogador_aceleracao
 
        #Aplicando atrito para o jogador não ir muito rápido:
        self.acc.x += self.vel.x * jogador_atrito
        #Equações para o movimento:
        self.vel += self.acc
        self.pos += self.vel + 0.5*self.acc
        #Para o jogador não sair do quadrado da tela:
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
 
        self.rect.midbottom = self.pos


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
        # tela inicial do jogo
        self.screen.fill(fundo)
        self.draw_text(titulo, 48, branco, WIDTH/2, HEIGHT/4)
        self.draw_text("Use o espaço para pular e as setas para andar", 22, branco, WIDTH/2, HEIGHT/2)
        self.draw_text("Aperte qualquer tecla para jogar!", 22, branco, WIDTH/2, HEIGHT*3/4)
        self.draw_text('Sua pontuação máxima é: ' + str(self.highscore), 22, branco, WIDTH/2 , 15)
        pygame.display.flip()

    def draw(self):
        #Desenhos do loop:
        self.screen.fill(fundo)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score), 22, branco, WIDTH/2, 15)
        pygame.display.flip()

    def draw_text(self, text, size, color, x, y):
        font= pygame.font.Font(self.font_name, size)
        text_surface= font.render(text, True, color)
        text_rect= text_surface.get_rect()
        text_rect.midtop= (x, y)
        self.screen.blit(text_surface, text_rect)

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


    