from Configuracoes import *
from random import randrange, choice
import pygame

vet= pygame.math.Vector2 # é usado o vetor para o movimento

class Spritesheet:
   #Classe para carregar as Spritesheets
   def __init__(self, filename):
       self.spritesheet = pygame.image.load(filename).convert() #convertendo a imagem do arquivo para o jogo
 
   def get_image(self, x, y, width, height):
       #pegando uma imagem da spritsheet
       imagem = pygame.Surface((width, height))
       imagem.blit(self.spritesheet, (0, 0), (x, y, width, height)) #coordenadas 
       imagem = pygame.transform.scale(imagem, (width // 3, height // 3)) # tamanho do ET 
       return imagem

class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        self._layer= layer_jogador # configurando a camada em que o jogador está 
        self.groups= game.all_sprites # adicionando na função o grupo de sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game= game
        self.andando= False    #sem movimento
        self.pulando= False    #sem movimento
        self.frame_atual= 0    
        self.ultimo_update= 0 
        self.carregando_imagens()  #adicionando a função carregando_imagens
        self.image= self.jogador_parado[0] # imagem do jogador parado 
        self.rect= self.image.get_rect()   # configurando as dimensões da imagem como retângulo
        self.rect.center= (40, HEIGHT - 100) #p/ ele começar no canto inferior esquerdo da tela
        self.pos= vet(40, HEIGHT - 100) #posição
        self.vel= vet(0, 0)  #velocidade
        self.acc= vet(0, 0)  #aceleração
        

    def carregando_imagens(self):
        #Dando as cordenadas das imagens do jogador parado
        self.jogador_parado= [self.game.spritesheet.get_image(260, 1032, 128, 256), self.game.spritesheet.get_image(260, 774, 128, 256)] 
        for frame in self.jogador_parado:
            frame.set_colorkey(preto)   #Definindo o fundo da imagem preto
        #Dando as cordenadas das imagens do jogador andando
        self.jogador_andando_d= [self.game.spritesheet.get_image(130, 1290, 128, 256),
                            self.game.spritesheet.get_image(130, 1032, 128, 256) ]
        self.jogador_andando_e= []
        for frame in self.jogador_andando_d: #rotacionando as imagens para a esquerda
            frame.set_colorkey(preto)   #Definindo o fundo da imagem preto
            self.jogador_andando_e.append(pygame.transform.flip(frame, True, False)) #rotaciona horizontalmente, não verticalmente
        #Dando as cordenadas da imagem do jogador pulando
        self.jogador_pulando= self.game.spritesheet.get_image(260, 516, 128, 256)
        self.jogador_pulando.set_colorkey(preto)  #Definindo o fundo da imagem preto
        
    def pular_cut(self):
        #Arrumando o pulo
        if self.pulando:
            if self.vel.y < -3:
                self.vel.y = -3

    def pular(self):
        #só pula se tiver em alguma plataforma
        self.rect.x += 2
        colisao= pygame.sprite.spritecollide(self, self.game.platforms, False)  #declarando colisão
        self.rect.x -= 2 #não é visível isso, mas necessário
        # Se houver colisão e o E.T não estiver pulando
        if colisao and not self.pulando:
            self.game.jump_sound.play() #só faz esse som quando ele pula p/ outra plataforma
            self.pulando= True
            self.vel.y = -pulo
    
    def update(self):
        self.animate()  # Chamando a função animate para a função update
        self.acc= vet(0, jogador_gravidade)  #A aceleração será igual a gravidade voltada para baixo
        keys= pygame.key.get_pressed()
        #Mudando a direção do jogador
        if keys[pygame.K_LEFT]:   
            self.acc.x= -jogador_aceleracao
        if keys[pygame.K_RIGHT]:
            self.acc.x= jogador_aceleracao

        #Aplicando atrito para o jogador não ir muito rápido:
        self.acc.x += self.vel.x * jogador_atrito
        
        #Equações para o movimento:
        self.vel += self.acc 
        if abs(self.vel.x) < 0.1: #abs pois pode ser positiva ou negativa
             self.vel.x = 0 #forçando a ficar zero p/ o personagem parar

        self.pos += self.vel + 0.5*self.acc

        # para o jogador não sair do quadrado da tela
        if self.pos.x > WIDTH + self.rect.width / 2:
            self.pos.x = 0 - self.rect.width / 2
        if self.pos.x < 0 - self.rect.width / 2:
            self.pos.x = WIDTH + self.rect.width / 2
 
        self.rect.midbottom = self.pos

    def animate(self):   #Função da animação do jogador
        agora= pygame.time.get_ticks()
        if self.vel.x != 0:  #se a velocidade no eixo x for diferente de 0, o jogador anda
            self.andando= True
        else:  #se não tiver velocidade no eixo x, o jogador não anda
            self.andando= False
        #animação para andar 
        if self.andando:
            if agora - self.ultimo_update > 200: #vai depender de quanto o et estiver rápido
                self.ultimo_update = agora       #o ultimo_update se torna o agora a partir do momento em que ele anda
                self.frame_atual= (self.frame_atual + 1) % len(self.jogador_andando_e)  #a posição onde o jogador ficará
                parte_inferior= self.rect.bottom
                if self.vel.x > 0: #ver qual a direção que está andando
                    self.image= self.jogador_andando_d[self.frame_atual] #imagem do E.T quando andando para direita
                else:
                    self.image= self.jogador_andando_e[self.frame_atual] #imagem do E.T quando andando para esquerda
                self.rect= self.image.get_rect()
                self.rect.bottom= parte_inferior
        #mostrar animação
        if not self.pulando and not self.andando:   #se o jogador não estiver pulando nem andando
            if agora - self.ultimo_update > 350: #350 milisegundos
                self.ultimo_update = agora  #o ultimo_update se torna o agora a partir do momento em que ele fica parado
                self.frame_atual= (self.frame_atual + 1) % len(self.jogador_parado)  #a posição onde o jogador ficará
                parte_inferior = self.rect.bottom
                self.image= self.jogador_parado[self.frame_atual]   #imagem do E.T quando parado
                self.rect= self.image.get_rect()
                self.rect.bottom= parte_inferior 

class Plataforma(pygame.sprite.Sprite):
    def __init__(self, game, x, y): # coordenadas
        self._layer= layer_plataforma # em qual camada a plataforma esta 
        self.groups= game.all_sprites, game.platforms #lista de grupos que vamos usar
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game= game
        imagem= self.game.spritesheet.get_image(208, 1879, 201, 100) # adicionando as coordenadas da plataforma 
        self.image= imagem # definindo a imagem da plataforma 
        self.image.set_colorkey(preto) # preenchendo o fundo de preto 
        self.rect= self.image.get_rect() # definindo a imagem como um retângulo
        self.rect.x = x 
        self.rect.y = y
        if randrange(100) < poder_na_plat: # para colocar o poder em cima da plataforma 
            Poder(self.game, self)
        if randrange(50) < moeda_na_plat: # para colocar o poder em cima da plataforma 
            Moeda(self.game, self)
    
class Poder(pygame.sprite.Sprite):
    def __init__(self, game, plat):
        self._layer= layer_poder # em qual camada o poder está
        self.groups= game.all_sprites, game.poderes #todos os grupos que vamos usar
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game= game
        self.plat= plat
        self.type= choice(['boost']) # função do pygame 
        self.image= self.game.spritesheet.get_image(2470, 1300, 128, 128) # coordenadas de onde a imagem do poder
        self.image.set_colorkey(preto) # preenchendo o fundo de preto 
        self.rect= self.image.get_rect() # definindo a imagem como um retângulo
        self.rect.centerx= self.plat.rect.centerx # para o poder ficar no centro da plataforma 
        self.rect.bottom= self.plat.rect.top - 5 # para o poder ficar em cima/flutuando na plataforma 

    def update(self):
        self.rect.bottom= self.plat.rect.top - 5
        if not self.game.platforms.has(self.plat): #o poder so vai existir se tiver alguma plataforma
            self.kill() # se não tiver plataforma, o poder "morre"

class Nuvem(pygame.sprite.Sprite):
    def __init__(self, game): 
        self._layer= layer_nuvem # em qual camada a nuvem vai ficar 
        self.groups= game.all_sprites, game.nuvens #lista de grupos que vamos usar
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game= game
        self.image= choice(self.game.nuvem_images) # sortear a imagem das nuvens pré definidas
        self.image.set_colorkey(preto) # preenche o fundo de preto
        self.rect= self.image.get_rect() # definindo a imagem como um retângulo 
        escala= randrange(50, 101) / 100 # escala do tamanho da figura
        # aplicando a escala na imagem --> transformando 
        self.image= pygame.transform.scale(self.image, (int(self.rect.width * escala), int(self.rect.height * escala)))
        self.rect.x = randrange(WIDTH - self.rect.width) # variar a imagem da nuvem para vários lugares da tela 
        self.rect.y = randrange(-500, -50)
 
    def update(self):
        if self.rect.top > HEIGHT * 2: # se o dobro da altura da janela for menor que o topo do retângulo  
            self.kill() # ela morre 

class Inimigo(pygame.sprite.Sprite):
    def __init__(self, game):
        self._layer= layer_inimigo # em qual camada o inimigo está 
        self.groups= game.all_sprites, game.inimigos #todos os grupos que vamos usar
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game= game
        self.image_up= self.game.spritesheet.get_image(3510, 130, 128, 128) #pega as imagens da abelha com a asa para cima
        self.image_up.set_colorkey(preto) # preenche o fundo da imagem de preto
        self.image_down= self.game.spritesheet.get_image(3380, 1820, 128, 128) #pega as imagens da abelha com a asa para baixo
        self.image_down.set_colorkey(preto) # preenche o fundo da imagem de preto
        self.image= self.image_up # definindo a imagem como a imagem da abelha com a asa para cima
        self.rect= self.image.get_rect() # definindo a imagem como um retângulo 
        self.rect.centerx = choice([-100, WIDTH + 100]) #para a abelha subir e descer enquanto voa
        self.vx= randrange(1, 4) # velocidade da abelha voando somente no eixo x
        if self.rect.centerx > WIDTH: # quando a abelha sair da tela, sua velocidade será negativa, fazendo com que ela suma
            self.vx *= -1
        self.rect.y= randrange(HEIGHT / 2) # abelha só aparece na altura do meio da janela 
        self.vy= 0 # velocidade nula, já que ela não vai voar nessa direção 
        self.dy= 0.5 #Variação de espaço entre um inimigo e outro 

    def update(self):
        self.rect.x += self.vx #Atualizando a velocidade 
        self.vy += self.dy  #Atualizando a variação 
        if self.vy > 3 or self.vy < -3: #Se a velocidade em y for maior que 3 ou menor que -3, ele fica em looping
            self.dy *= -1
        centro= self.rect.center  #Definindo o centro do inimigo
        if self.dy < 0:
            self.image= self.image_up #Se o inimigo subir no eixo Y, é aplicada a imagem dele subindo
        else:
            self.image= self.image_down #Se o inimigo descer no eixo Y, é aplicada a imagem dele descendo
        self.rect= self.image.get_rect()
        self.mask= pygame.mask.from_surface(self.image) #Criando uma mask na imagem do inimigo
        self.rect.center= centro
        self.rect.y += self.vy
        if self.rect.left > WIDTH + 100 or self.rect.right < -100: #Se o inimgo ultrapassar a largura da janela, ele morre
            self.kill()

class Moeda(pygame.sprite.Sprite):
    def __init__(self, game, plat):
        self._layer = layer_poder # em qual camada a moeda está
        self.groups= game.all_sprites, game.moedas #todos os grupos que vamos usar
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game= game
        self.plat= plat 
        self.image= self.game.spritesheet.get_image(2730,0,128,128) # coordenadas de onde a imagem do poder
        self.image.set_colorkey(preto) # preenchendo o fundo de preto 
        self.rect= self.image.get_rect() # definindo a imagem como um retângulo
        self.rect.centerx= self.plat.rect.centerx # para o poder ficar no centro da plataforma 
        self.rect.bottom= self.plat.rect.top - 5 # para o poder ficar em cima/flutuando na plataforma 

    def update(self):
        self.rect.bottom= self.plat.rect.top - 5
        if not self.game.platforms.has(self.plat): #o poder so vai existir se tiver alguma plataforma
            self.kill() # se não tiver plataforma, o poder "morre"