from Classes import *
from Configuracoes import *
from random import randrange, choice
from os import path
import pygame

class Game:
    def __init__(self):
        #iniciando a janela do jogo
        pygame.mixer.init()
        self.screen= pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(titulo)
        self.clock= pygame.time.Clock()
        self.running= True
        self.font_name= pygame.font.match_font(nome_fonte)
        self.load_data()
        self.vida = 3
        self.moedinha = 0

    def load_data(self):
        #Importando imagens e sons para o jogo
        #Abrindo diretório do arquivo 
        self.dir = path.dirname(__file__)
        imagem_dir = path.join(self.dir, 'imagem')
        with open(path.join(self.dir, pontuacao_maxima), 'w')as f:  #W = Criar um arquivo e escrever por cima dele
            try:                               #Salva a pontuação máxima e a guarda no arquivo
                self.highscore = int(f.read())
            except:                            #Se a pontuação for menor que a máxima, ele não salva essa pontuação
                self.highscore = 0    
        self.spritesheet=Spritesheet(path.join(imagem_dir,sprite_sheet))  #Acessar diretórios de arquivos   
        
        #imagem para o fundo 
        self.nuvem_images= []
        for i in range(1, 4): # sorteia diferentes formatos de nuvem 
            #Adiciona imagens de nuvens randomicamente entre as três existentes para isso dentro da pasta "imagens"
            self.nuvem_images.append(pygame.image.load(path.join(imagem_dir, 'nuvem{}.png'.format(i))).convert()) 

        #carregando sons para o jogo
        self.som_dir = path.join(self.dir, 'som')
        self.jump_sound= pygame.mixer.Sound(path.join(self.som_dir, 'pulando.ogg')) 
        self.boost_sound= pygame.mixer.Sound(path.join(self.som_dir, 'powerup.wav')) 

    def novo_jogo(self):
        #para começar um novo jogo
        self.score= 0      #A pontuação é começa em zero quando inicia o jogo
        self.vida = 3
        self.moedinha = 0
        self.all_sprites= pygame.sprite.LayeredUpdates()  #Divide as classes em camadas
        #Criando grupos de componentes do jogo
        self.platforms= pygame.sprite.Group()
        self.poderes= pygame.sprite.Group()
        self.inimigos= pygame.sprite.Group()
        self.nuvens= pygame.sprite.Group()
        self.moedas = pygame.sprite.Group()
        self.player= Player(self)
        for plat in l_plataformas:
            Plataforma(self, *plat) #explora a lista de plataformas na classe Plataforma    #a=Plataforma(self, *plat)
            #self.platforms.add(a)
            #print(a)
        #Intervalo e tempo entre a aparição de inimigos
        self.inimigo_timer= 0.1
        #Música durante o jogo
        pygame.mixer.music.load(path.join(self.som_dir, 'no jogo.wav'))
        for i in range(7): # p/ colocar nuvens na tela inicial 
            n= Nuvem(self)
            n.rect.y += 500
        self.run()

    def tela_inicio(self):  
        # tela inicial do jogo
        pygame.mixer.music.load(path.join(self.som_dir, 'durante o jogo.wav'))
        #Pôr a música para tocar mais de uma vez
        pygame.mixer.music.play(loops= -1)
        #Aplica a cor de fundo da tela inicial
        self.screen.fill(fundo)
        #Escrevendo título e informações na tela inicial
        self.draw_text(titulo, 48, azul, WIDTH/2, HEIGHT/4)
        self.draw_text("Use o espaço para pular e as setas para andar", 22, azul, WIDTH/2, HEIGHT/2)
        self.draw_text("Aperte qualquer tecla para jogar!", 22, azul, WIDTH/2, HEIGHT*3/4)
        self.draw_text('Sua pontuação máxima é: ' + str(self.highscore), 22, azul, WIDTH/2 , 15)
        pygame.display.flip()
        #Aplica a função em que o jogo só começa se o jogador apertar uma tecla
        self.espera_para_comecar()
        #Quando aperta uma tecla, a música para de tocar, após cinco segundos e diminui gradativamente
        pygame.mixer.music.fadeout(500)

    def draw(self):
        #Desenhos do loop:
        self.screen.fill(fundo)
        self.all_sprites.draw(self.screen)
        self.screen.blit(self.player.image, self.player.rect) #p/ o jogador ficar na frente da plataforma 
        #Escreve a pontuação que vai sendo adquirida ao longo do jogo 
        self.draw_text(str(self.score), 22, branco, WIDTH/2, 15)
        pygame.display.flip()


    def draw_text(self, text, size, color, x, y):
        #Especificações do texto a ser escrito
        font= pygame.font.Font(self.font_name, size)
        text_surface= font.render(text, True, color)
        text_rect= text_surface.get_rect()
        text_rect.midtop= (x, y)
        self.screen.blit(text_surface, text_rect)
        text_surface2 = font.render(chr(9829) * self.vida, True, (255, 0, 0))
        text_rect2 = text_surface2.get_rect()
        text_rect2.bottomleft = (10, 20)
        self.screen.blit(text_surface2, text_rect2)

    def run(self):
        #Loop do jogo:
        pygame.mixer.music.play(loops= -1) #p/ a musica não tocar só uma vez
        self.playing= True
        #Estado do jogo durante a partida
        while self.playing:
            self.clock.tick(FPS)
            self.eventos()
            self.update()
            self.draw()
        pygame.mixer.music.fadeout(500) #p/ parar a musica gradativamente após cinco segundos
 
    def update(self):
        # atualização do loop
        self.all_sprites.update()
        #criando um inimigo
        agora= pygame.time.get_ticks()
        if agora - self.inimigo_timer > frequencia_inimigo + choice([-1000, -500, 0, 500, 1000]):  #p/ ficar uma hora maior e outra menor--> variando 
            self.inimigo_timer = agora
            Inimigo(self)
        # colisão do contorno da abelha com o contorno do et
        inimigo_colisao= pygame.sprite.spritecollide(self.player, self.inimigos, False, pygame.sprite.collide_mask)
        if inimigo_colisao:
            self.vida -= 1 
            for i in inimigo_colisao:
                i.kill()
            if self.vida <= 0:
                self.playing= False
        #Checa se o jogador bateu na plataforma, só se estiver caindo:
        if self.player.vel.y > 0:
            colisao = pygame.sprite.spritecollide(self.player, self.platforms, False)
            if colisao:
                menor= colisao[0]
                #Quando há colisões entre o pé do E.T e a plataforma, o E.T ficará em cima da plataforma
                for colisoes in colisao:
                    if colisoes.rect.bottom > menor.rect.bottom:
                        menor= colisoes
                #Para o E.T não ficar flutuando nas extremidades das plataformas  
                if self.player.pos.x < menor.rect.right and self.player.pos.x > menor.rect.left:
                    if self.player.pos.y < menor.rect.centery:
                        self.player.pos.y = menor.rect.top
                        self.player.vel.y = 0
                        self.player.pulando= False 

        #Se o jogador alcanca 1/4 do topo da tela:
        #Efeito de que o jogador está subindo e os componentes estão ficando para baixo/trás, criando novos componentes logo acima
        if self.player.rect.top <= HEIGHT / 4:
            if randrange(100) < 15:
                Nuvem(self)
            self.player.pos.y += max(abs(self.player.vel.y), 2)
            for nuvem in self.nuvens:
                nuvem.rect.y += max(abs(self.player.vel.y / 2 ), 2)
            for inimigo in self.inimigos:
                inimigo.rect.y += max(abs(self.player.vel.y), 2)
            for plat in self.platforms:
                plat.rect.y += abs(self.player.vel.y)
                #Se a plataforma sai da tela do jogo ela é apagada/morre
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    self.score += 10

        #Se o jogador pega um poder
        poder_colisao= pygame.sprite.spritecollide(self.player, self.poderes, True)
        for poder in poder_colisao:
            if poder.type == 'boost':
                #Som de quando se pega o boost
                self.boost_sound.play()
                self.player.vel.y = -boost_poder
                self.player.pulando= False #Para a função pulo_cut não limitar o salto do boost
        
        #Se o jogador pega uma moeda
        moeda_colisao= pygame.sprite.spritecollide(self.player, self.moedas, True)
        if moeda_colisao:
            self.score += 50
            self.moedinha +=1
            for moeda in moeda_colisao:
                moeda.kill()
            if self.moedinha == 15:
                self.vida += 1
        #Game over:
        if self.player.rect.bottom > HEIGHT: 
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        #Quando o player morre, as plataformas também "morrem"
        if len(self.platforms) == 0:
            self.playing= False

        #Criando novas plataformas sem ultrapassar uma quantidade de 5 plataformas dadas pela lista já definida
        while len(self.platforms) < 6:
            width= randrange(50, 100)
            Plataforma(self, randrange(0, WIDTH-width), randrange(-75, -30))

    def eventos(self):
        # eventos do loop
        for event in pygame.event.get():
            # checa se a janela do jogo foi fechada e nisso não há jogo
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing= False
                self.running = False   # Jogo não roda
            #Se apenas a tecla "espaço" está pressionada, o player consegue saltar
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.pular()
            #Se a tecla "espaço" estiver pressionada levemente ou não estiver pressionada, o salto é menor ou não há salto
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.player.pular_cut() #Limitando o tamanho do salto

    def game_over(self):  
        #Continuação ou término do jogo
        if not self.running:
            return
        #Música de quando aparece a tela de Game Over
        pygame.mixer.music.load(path.join(self.som_dir, 'perdeu.wav'))
        pygame.mixer.music.play()
        #Preenchendo o fundo da tela de Game Over
        self.screen.fill(fundo)
        #Escrevendo na tela de Game Over
        self.draw_text("Game Over", 48, vermelho, WIDTH/2, HEIGHT/4)
        self.draw_text("Pontuação: " + str(self.score), 22, azul, WIDTH/2, HEIGHT/2)
        self.draw_text("Aperte qualquer tecla para jogar denovo!", 22, azul, WIDTH/2, HEIGHT*3/4)
        #Se a pontuação é maior que a máxima atingida anteriormente, será considerada a nova pontuação máxima
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text('Nova pontuação máxima: ', 22, azul, WIDTH/2, HEIGHT/2 + 40)
            #Reescreve a nova pontuação no arquivo, por cima da que existia antes
            with open(path.join(self.dir, pontuacao_maxima), 'w') as f:
                f.write(str(self.score))
        #Quando a pontuação máxima não é superada, aparece a pontuação máxima 
        else:
            self.draw_text('Sua pontuação máxima é: ' + str(self.highscore), 22, azul, WIDTH/2, HEIGHT/2 + 40)
        pygame.display.flip()
        #Quando está na tela de Game Over e espera do jogador apertar uma tecla para começar uma nova partida, guardando a pontuação máxima existente
        self.espera_para_comecar()
        pygame.mixer.music.fadeout(500)
   
    def espera_para_comecar(self):  #Espera o jogador pressionar alguma tecla para dar início à partida
        waiting= True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                #Se você fecha a janela, o jogo para
                if event.type == pygame.QUIT:
                    waiting= False
                    self.running= False 
                if event.type == pygame.KEYUP:
                    waiting= False 

