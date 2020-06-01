import Classes
import Iniciando
import Configuracoes
from random import randrange, choice
from os import path
import pygame

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
        
        #imagem para o fundo 
        self.nuvem_images= []
        for i in range(1, 4): # sorteia diferentes formatos de nuvem 
            self.nuvem_images.append(pygame.image.load(path.join(imagem_dir, 'nuvem{}.png'.format(i))).convert())

        #carregando sons para o jogo
        self.som_dir = path.join(self.dir, 'som')
        self.jump_sound= pygame.mixer.Sound(path.join(self.som_dir, 'pulando.ogg')) 
        self.boost_sound= pygame.mixer.Sound(path.join(self.som_dir, 'powerup.wav')) 

    def novo_jogo(self):
        # para começar um novo jogo
        self.score= 0
        self.all_sprites= pygame.sprite.LayeredUpdates()  #especifica um n° 
        self.platforms= pygame.sprite.Group()
        self.poderes= pygame.sprite.Group()
        self.moobs= pygame.sprite.Group()
        self.nuvens= pygame.sprite.Group()
        self.player= Player(self)
        for plat in l_plataformas:
            Plataforma(self, *plat) #explora a lista de plataformas
        self.moob_timer= 0.1
        pygame.mixer.music.load(path.join(self.som_dir, 'no jogo.wav'))
        for i in range(7): # p/ colocar nuvens na tela inicial 
            n= Nuvem(self)
            n.rect.y += 500
        self.run()

    def tela_inicio(self):  
        # tela inicial do jogo
        pygame.mixer.music.load(path.join(self.som_dir, 'durante o jogo.wav'))
        pygame.mixer.music.play(loops= -1)
        self.screen.fill(fundo)
        self.draw_text(titulo, 48, azul, WIDTH/2, HEIGHT/4)
        self.draw_text("Use o espaço para pular e as setas para andar", 22, azul, WIDTH/2, HEIGHT/2)
        self.draw_text("Aperte qualquer tecla para jogar!", 22, azul, WIDTH/2, HEIGHT*3/4)
        self.draw_text('Sua pontuação máxima é: ' + str(self.highscore), 22, azul, WIDTH/2 , 15)
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
        #spawn a moob
        agora= pygame.time.get_ticks()
        if agora - self.moob_timer > 5000 + choice([-1000, -500, 0, 500, 1000]):  #p/ ficar uma hora maior e outra menor--> variando 
            self.moob_timer = agora
            Moob(self)
        # colisão do contorno da abelha com o contorno do et
        moob_colisao= pygame.sprite.spritecollide(self.player, self.moobs, False, pygame.sprite.collide_mask)
        if moob_colisao:
            self.playing= False
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
            if randrange(100) < 15:
                Nuvem(self)
            self.player.pos.y += max(abs(self.player.vel.y), 2)
            for nuvem in self.nuvens:
                nuvem.rect.y += max(abs(self.player.vel.y / 2 ), 2)
            for moob in self.moobs:
                moob.rect.y += max(abs(self.player.vel.y), 2)
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
            width= randrange(50, 100)
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
        self.draw_text("Game Over", 48, vermelho, WIDTH/2, HEIGHT/4)
        self.draw_text("Pontuação: " + str(self.score), 22, azul, WIDTH/2, HEIGHT/2)
        self.draw_text("Aperte qualquer tecla para jogar denovo!", 22, azul, WIDTH/2, HEIGHT*3/4)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text('Nova pontuação máxima: ', 22, azul, WIDTH/2, HEIGHT/2 + 40)
            with open(path.join(self.dir, pontuacao_maxima), 'w') as f:
                f.write(str(self.score))
        else:
            self.draw_text('Sua pontuação máxima é: ' + str(self.highscore), 22, azul, WIDTH/2, HEIGHT/2 + 40)
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