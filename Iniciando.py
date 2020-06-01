#Importando as bibliotecas necessárias:
import pygame
from Classes import *
from Jogo import *
from Configuracoes import *
 
pygame.init()

g = Game()
g.tela_inicio()
while g.running:
    g.novo_jogo()
    g.game_over()
 
pygame.quit()


    