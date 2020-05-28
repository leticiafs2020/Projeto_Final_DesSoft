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
pontuacao_maxima= "pontuacao_maxima.txt"
sprite_sheet = "spritesheet_complete.png"

# plataformas iniciais 
l_plataformas= [(0, HEIGHT-40, WIDTH, 40), (175, 100, 50, 20),
(WIDTH / 2 - 50, HEIGHT * 3 /4, 100, 20),
(350, 200, 100, 20), (125, HEIGHT - 350, 100, 20)] 

#propriedades do jogo
boost_poder= 60
spawn_pct_po= 7 #tempo p/ responder 

vet= pygame.math.Vector2 # é usado o vetor para o movimento 

class Spritesheet:
   #Classe para carregar as Spritesheets
   def __init__(self, filename):
       self.spritesheet = pygame.image.load(filename).convert()
 
   def get_image(self, x, y, width, height):
       #pegando uma imagem da spritsheet
       imagem = pygame.Surface((width, height))
       imagem.blit(self.spritesheet, (0, 0), (x, y, width, height))
       imagem = pygame.transform.scale(imagem, (width // 3, height // 3))
       return imagem

class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        self.groups= game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game= game
        self.walking= False
        self.jumping= False 
        self.current_frame= 0 
        self.last_update= 0 
        self.load_images()
        self.image= self.standing_frame[0]
        self.rect= self.image.get_rect()
        self.rect.center= (40, HEIGHT - 100) #p/ ele começar no canto inferior esquerdo da tela
        self.pos= vet(40, HEIGHT - 100) #posição
        self.vel= vet(0, 0)  #velocidade
        self.acc= vet(0, 0)  #aceleração

    def load_images(self):
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
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    def pular(self):
        #só pula se tiver em alguma plataforma
        self.rect.x += 2
        colisao= pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 2 #não é visível isso, mas necessário
        if colisao and not self.jumping:
            self.game.jump_sound.play() #só faz esse som quando ele pula p/ outra plataforma
            self.jumping= True
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
            self.walking= True
        else:
            self.walking= False
        #animação para andar 
        if self.walking:
            if agora - self.last_update > 200: #vai depender de quanto o et estiver rápido
                self.last_update = agora
                self.current_frame= (self.current_frame + 1) % len(self.walk_frames_l)
                bottom= self.rect.bottom
                if self.vel.x > 0: #ver qual a direção que está andando
                    self.image= self.walk_frames_r[self.current_frame] 
                else:
                    self.image= self.walk_frames_l[self.current_frame]
                self.rect= self.image.get_rect()
                self.rect.bottom= bottom
        #mostrar animação
        if not self.jumping and not self.walking:
            if agora - self.last_update > 350: #350 milisegundos
                self.last_update = agora
                self.current_frame= (self.current_frame + 1) % len(self.standing_frame)
                bottom= self.rect.bottom
                self.image= self.standing_frame[self.current_frame]
                self.rect= self.image.get_rect()
                self.rect.bottom= bottom 
                
class Plataforma(pygame.sprite.Sprite):
    def __init__(self, game, x, y): # coordenadas
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
        self.load_data()

    def load_data(self):
        self.dir = path.dirname(__file__)
        imagem_dir = path.join(self.dir, 'imagem')
        with open(path.join(self.dir, pontuacao_maxima), 'w')as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0    
        self.spritesheet=Spritesheet(path.join(imagem_dir,sprite_sheet))     
        #carregando sons para o jogo
        self.som_dir = path.join(self.dir, 'som')
        self.jump_sound= pygame.mixer.Sound(path.join(self.som_dir, 'pulando.ogg')) 
        self.boost_sound= pygame.mixer.Sound(path.join(self.som_dir, 'perdeu.wav')) 

    def novo_jogo(self):
        # para começar um novo jogo
        self.score= 0
        self.all_sprites= pygame.sprite.Group()
        self.platforms= pygame.sprite.Group()
        self.poderes= pygame.sprite.Group()
        self.player= Player(self)
        for plat in l_plataformas:
            Plataforma(self, *plat) #explora a lista de plataformas
        pygame.mixer.music.load(path.join(self.som_dir, 'durante o jogo.wav'))

        self.run()

    def tela_inicio(self):  
        # tela inicial do jogo
        pygame.mixer.music.load(path.join(self.som_dir, 'durante o jogo.wav'))
        pygame.mixer.music.play(loops= -1)
        self.screen.fill(fundo)
        self.draw_text(titulo, 48, branco, WIDTH/2, HEIGHT/4)
        self.draw_text("Use o espaço para pular e as setas para andar", 22, branco, WIDTH/2, HEIGHT/2)
        self.draw_text("Aperte qualquer tecla para jogar!", 22, branco, WIDTH/2, HEIGHT*3/4)
        self.draw_text('Sua pontuação máxima é: ' + str(self.highscore), 22, branco, WIDTH/2 , 15)
        pygame.display.flip()
        self.espera_para_comecar()
        pygame.mixer.music.fadeout(500)

    def draw(self):
        #Desenhos do loop:
        self.screen.fill(fundo)
        self.all_sprites.draw(self.screen)
        self.screen.blit(self.player.image, self.player.rect) #p/ o jogador ficar na frente da plataforma 
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
        pygame.mixer.music.play(loops= -1) #p/ a musica não tocar só uma vez
        self.playing= True
        while self.playing:
            self.clock.tick(FPS)
            self.eventos()
            self.update()
            self.draw()
        pygame.mixer.music.fadeout(500) #p/ parar a musica
    
    def update(self):
        # atualização do loop
        self.all_sprites.update()
        #Checa se o jogador bateu na plataforma, só se estiver caindo:
        if self.player.vel.y > 0:
            colisao= pygame.sprite.spritecollide(self.player, self.platforms, False)
            if colisao:
                menor= colisao[0]
                for colisoes in colisao:
                    if colisoes.rect.bottom > menor.rect.bottom:
                        menor= colisoes
                #p/ ele não ficar flutuando nas extremidades das plataformas  
                if self.player.pos.x < menor.rect.right and self.player.pos.x > menor.rect.left:
                    if self.player.pos.y < menor.rect.centery:
                        self.player.pos.y = menor.rect.top
                        self.player.vel.y = 0
                        self.player.jumping= False 

        #Se o jogador alcanca 1/4 do topo da tela:
        if self.player.rect.top <= HEIGHT / 4:
            self.player.pos.y += abs(self.player.vel.y)
            for plat in self.platforms:
                plat.rect.y += abs(self.player.vel.y)
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    self.score += 10

        #se o jogador pega um poder
        poder_colisao= pygame.sprite.spritecollide(self.player, self.poderes, True)
        for poder in poder_colisao:
            if poder.type == 'boost':
                self.boost_sound.play()
                self.player.vel.y = -boost_poder
                self.player.jumping= False #p/ o pulo_cut não parar o boost

        #Game over:
        if self.player.rect.bottom > HEIGHT: 
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.platforms) == 0:
            self.playing= False

        #Cria novas plataformas sem ultrapassar uma quantidade de 5 plataformas
        while len(self.platforms) < 6:
            width= random.randrange(50, 100)
            Plataforma(self, randrange(0, WIDTH-width), randrange(-75, -30))

    def eventos(self):
        # eventos do loop
        for event in pygame.event.get():
            # checa se a janela do jogo foi fechada
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing= False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.pular()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.player.pular_cut() #arrumando o tamanho do salto

    def game_over(self):  
        # continuação ou termino do jogo
        if not self.running:
            return
        pygame.mixer.music.load(path.join(self.som_dir, 'perdeu.wav'))
        pygame.mixer.music.play()
        self.screen.fill(fundo)
        self.draw_text("Game Over", 48, branco, WIDTH/2, HEIGHT/4)
        self.draw_text("Pontuação: " + str(self.score), 22, branco, WIDTH/2, HEIGHT/2)
        self.draw_text("Aperte qualquer tecla para jogar denovo!", 22, branco, WIDTH/2, HEIGHT*3/4)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text('Nova pontuação máxima: ', 22, branco, WIDTH/2, HEIGHT/2 + 40)
            with open(path.join(self.dir, pontuacao_maxima), 'w') as f:
                f.write(str(self.score))
        else:
            self.draw_text('Sua pontuação máxima é: ' + str(self.highscore), 22, branco, WIDTH/2, HEIGHT/2 + 40)
        pygame.display.flip()
        self.espera_para_comecar()
        pygame.mixer.music.fadeout(500)
   
    def espera_para_comecar(self):
        waiting= True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting= False
                    self.running= False 
                if event.type == pygame.KEYUP:
                    waiting= False 

g = Game()
g.tela_inicio()
while g.running:
    g.novo_jogo()
    g.game_over()
 
pygame.quit()


    