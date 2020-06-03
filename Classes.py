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
        self.andando= False
        self.pulando= False 
        self.frame_atual= 0 
        self.ultimo_update= 0 
        self.carregando_imagens()
        self.image= self.standing_frame[0] # imagem do jogador parado 
        self.rect= self.image.get_rect()
        self.rect.center= (40, HEIGHT - 100) #p/ ele começar no canto inferior esquerdo da tela
        self.pos= vet(40, HEIGHT - 100) #posição
        self.vel= vet(0, 0)  #velocidade
        self.acc= vet(0, 0)  #aceleração

    def carregando_imagens(self):
        self.standing_frame= [self.game.spritesheet.get_image(260, 1032, 128, 256), self.game.spritesheet.get_image(260, 774, 128, 256)]
        for frame in self.standing_frame:
            frame.set_colorkey(preto) 
        self.walk_frames_r= [self.game.spritesheet.get_image(130, 1290, 128, 256),
                            self.game.spritesheet.get_image(130, 1032, 128, 256) ]
        self.walk_frames_l= []
        for frame in self.walk_frames_r: #rotacionando as imagens para a esquerda
            frame.set_colorkey(preto) 
            self.walk_frames_l.append(pygame.transform.flip(frame, True, False)) #rotaciona horizontalmente, não verticalmente
        self.jump_frame= self.game.spritesheet.get_image(260, 516, 128, 256)
        self.jump_frame.set_colorkey(preto)
        
    def pular_cut(self):
        if self.pulando:
            if self.vel.y < -3:
                self.vel.y = -3

    def pular(self):
        #só pula se tiver em alguma plataforma
        self.rect.x += 2
        colisao= pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 2 #não é visível isso, mas necessário
        if colisao and not self.pulando:
            self.game.jump_sound.play() #só faz esse som quando ele pula p/ outra plataforma
            self.pulando= True
            self.vel.y = -pulo
    
    def update(self):
        self.animate()
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
        if abs(self.vel.x) < 0.1: #abs pois pode ser positiva ou negativa
             self.vel.x = 0 #forçando a ficar zero p/ o personagem parar

        self.pos += self.vel + 0.5*self.acc

        # para o jogador não sair do quadrado da tela
        if self.pos.x > WIDTH + self.rect.width / 2:
            self.pos.x = 0 - self.rect.width / 2
        if self.pos.x < 0 - self.rect.width / 2:
            self.pos.x = WIDTH + self.rect.width / 2
 
        self.rect.midbottom = self.pos

    def animate(self):
        agora= pygame.time.get_ticks()
        if self.vel.x != 0:
            self.andando= True
        else:
            self.andando= False
        #animação para andar 
        if self.andando:
            if agora - self.ultimo_update > 200: #vai depender de quanto o et estiver rápido
                self.ultimo_update = agora
                self.frame_atual= (self.frame_atual + 1) % len(self.walk_frames_l)
                bottom= self.rect.bottom
                if self.vel.x > 0: #ver qual a direção que está andando
                    self.image= self.walk_frames_r[self.frame_atual] 
                else:
                    self.image= self.walk_frames_l[self.frame_atual]
                self.rect= self.image.get_rect()
                self.rect.bottom= bottom
        #mostrar animação
        if not self.pulando and not self.andando:
            if agora - self.ultimo_update > 350: #350 milisegundos
                self.ultimo_update = agora
                self.frame_atual= (self.frame_atual + 1) % len(self.standing_frame)
                bottom= self.rect.bottom
                self.image= self.standing_frame[self.frame_atual]
                self.rect= self.image.get_rect()
                self.rect.bottom= bottom 

class Plataforma(pygame.sprite.Sprite):
    def __init__(self, game, x, y): # coordenadas
        self._layer= layer_plataforma
        self.groups= game.all_sprites, game.platforms #lista de grupos que vamos usar
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game= game
        images= [self.game.spritesheet.get_image(208, 1879, 201, 100)]
        self.image= choice(images)
        self.image.set_colorkey(preto)
        self.rect= self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if randrange(100) < spawn_pct_po:
            Poder(self.game, self)

class Poder(pygame.sprite.Sprite):
    def __init__(self, game, plat):
        self._layer= layer_poder
        self.groups= game.all_sprites, game.poderes #todos os grupos que vamos usar
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game= game
        self.plat= plat
        self.type= choice(['boost'])
        self.image= self.game.spritesheet.get_image(2470, 1170, 128, 128)
        self.image.set_colorkey(preto)
        self.rect= self.image.get_rect()
        self.rect.centerx= self.plat.rect.centerx
        self.rect.bottom= self.plat.rect.top - 5

    def update(self):
        self.rect.bottom= self.plat.rect.top - 5
        if not self.game.platforms.has(self.plat): #o poder so vai existir se tiver alguma plataforma
            self.kill() 

class Nuvem(pygame.sprite.Sprite):
    def __init__(self, game): 
        self._layer= layer_nuvem
        self.groups= game.all_sprites, game.nuvens #lista de grupos que vamos usar
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game= game
        self.image= choice(self.game.nuvem_images)
        self.image.set_colorkey(preto)
        self.rect= self.image.get_rect()
        escala= randrange(50, 101) / 100
        self.image= pygame.transform.scale(self.image, (int(self.rect.width * escala), int(self.rect.height * escala)))
        self.rect.x = randrange(WIDTH - self.rect.width)
        self.rect.y = randrange(-500, -50)
 
    def update(self):
        if self.rect.top > HEIGHT * 2:
            self.kill()

class Inimigo(pygame.sprite.Sprite):
    def __init__(self, game):
        self._layer= layer_inimigo
        self.groups= game.all_sprites, game.inimigos #todos os grupos que vamos usar
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game= game
        self.image_up= self.game.spritesheet.get_image(3510, 130, 128, 128) #pega as imagens da abelha c/ a asa p/ cima
        self.image_up.set_colorkey(preto) 
        self.image_down= self.game.spritesheet.get_image(3380, 1820, 128, 128) #pega as imagens da abelha c/ a asa p/ baixo
        self.image_down.set_colorkey(preto)
        self.image= self.image_up 
        self.rect= self.image.get_rect()
        self.rect.centerx = choice([-100, WIDTH + 100]) #p/ a abelha subir e descer enquanto voa
        self.vx= randrange(1, 4)
        if self.rect.centerx > WIDTH:
            self.vx *= -1
        self.rect.y= randrange(HEIGHT / 2)
        self.vy= 0
        self.dy= 0.5

    def update(self):
        self.rect.x += self.vx
        self.vy += self.dy
        if self.vy > 3 or self.vy < -3:
            self.dy *= -1
        centro= self.rect.center
        if self.dy < 0:
            self.image= self.image_up
        else:
            self.image= self.image_down
        self.rect= self.image.get_rect()
        self.mask= pygame.mask.from_surface(self.image)
        self.rect.center= centro
        self.rect.y += self.vy
        if self.rect.left > WIDTH + 100 or self.rect.right < -100:
            self.kill()