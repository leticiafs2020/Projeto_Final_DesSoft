#Importando as bibliotecas necessárias:
import pygame
from random import choice, randrange
from os import path
 


g = Game()
g.tela_inicio()
while g.running:
    g.novo_jogo()
    g.game_over()
 
pygame.quit()


    