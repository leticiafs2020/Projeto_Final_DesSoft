#Definindo as cores
branco= (255, 255, 255)
preto= (0, 0, 0)
vermelho= (255, 0, 0)
azul= (0, 100, 100)
azul_claro= (0, 210, 210)
fundo= azul_claro

#Propriedades do jogador(player)
jogador_aceleracao= 0.5
jogador_atrito= -0.12
jogador_gravidade= 0.8
pulo= 22

#Configurações do jogo
WIDTH= 480
HEIGHT= 600
FPS= 60
titulo= 'E.T de volta para casa'
nome_fonte= 'arial'
pontuacao_maxima= "pontuacao_maxima.txt"
sprite_sheet = "spritesheet_complete.png"

#Plataformas iniciais 
l_plataformas= [(0, HEIGHT-60), (175, 100),
(WIDTH / 2 - 50, HEIGHT * 3 /4),
(350, 200), (125, HEIGHT - 350)] 

#Propriedades do jogo
boost_poder= 60
poder_na_plat= 7 #tempo p/ responder
frequencia_inimigo= 5000 #ms = 5 segundos 
moeda_na_plat = 7

#Camada em que cada componente está 
layer_jogador= 2
layer_plataforma= 1
layer_poder= 1
layer_inimigo= 2
layer_nuvem= 0 

