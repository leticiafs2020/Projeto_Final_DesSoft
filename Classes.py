import Configuracoes
import Iniciando
import Jogo
from random import randrange, choice
from os import path
import pygame

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