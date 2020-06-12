# Projeto_Final_DesSoft

@authors: Amanda Colucci, Letícia Sanchez e Natália Carreras

**Título:** "E.T de volta para casa"

**Link do vídeo da demonstração do jogo postada no Youtube:** [https://youtu.be/G7TSI5cWqWI]

O Projeto Final se baseia no desenvolvimento de um jogo de computador em Python 3 utilizando os recursos da biblioteca PyGame. Nosso projeto consiste em um jogo singleplayer em que o player salta entre as plataformas tentando não ser atingido pelos inimigos nem cair. 

## Enredo do jogo:

  Com o intuito de voltar para casa, Pink o E.T salta de plataforma em plataforma enfrentando vários desafios, encontrando seus inimigos, os Abelhões, porém com seu poder de Super Salto consegue deixá-los para trás. Mas não deixe Pink encostar nos Abelhões, eles podem tirar uma de suas três vidas. Não se preocupe, caso você perca uma delas, pode consegui-la novamente pegando dez moedas. Aventure-se com Pink nessa incrível jornada :)
  
## Regras do jogo:
  
- Caso você não faça Pink alcançar a plataforma e ele cair, você perderá todas as suas vidas e o jogo acabará.
- Pegando o Super Salto, Pink é lançado em elevadas. 
- Você começa o jogo com três vidas.
- A cada moeda que você pega durante o jogo, você ganha 50 pontos no score. 
- A cada 10 moedas que você pega durante um jogo, você ganha uma vida.

## Como jogar:
  
- Para iniciar o jogo, basta pressionar a barra de espaço. 
- Para fazer com que Pink salte, pressione a barra de espaço.
- Para fazer com que Pink ande, pressione as teclas com as setas para a esquerda ou para a direita.
- Para fazer com que Pink dê um salto maior, pressione a barra de espaço por mais tempo.

## Baixando dependências:

### Pygame:
  
#### Instalação
  
##### Windows e Linux:
  
  Abra o seu terminal (Linux) ou Anaconda Prompt (Windows) e digite:

  pip install pygame

##### Mac OSX:
  
  A instalação no Mac é um pouco mais complicada, infelizmente. Se você não tiver o Homebrew instalado, instale-o seguindo as instruções disponíveis neste link (se você não sabe se tem o Homebrew instalado, provavelmente não tem): [https://brew.sh/]
   
  Abra o terminal e digite:

  brew install sdl2 sdl2_gfx sdl2_image sdl2_mixer sdl2_net sdl2_ttf

  brew install Caskroom/cask/xquartz

  git clone -b 1.9.6 --single-branch https://github.com/pygame/pygame.git cd pygame

  python setup.py -config -auto -sdl2

  python setup.py install

  cd ..

  rm -rf pygame

  Para mais detalhes e outras opções de instalação no Mac, consulte a documentação: [https://www.pygame.org/wiki/MacCompile]

## Músicas:

Todos os áudios utilizados na elaboração do projeto foram retirados do site: [https://opengameart.org/]

## Spritesheets/Imagens:

Todas as imagens utilizadas na elaboração do projeto foram retiradas do site: [https://www.kenney.nl/assets/platformer-pack-redux]

## Referências:

- Kids Can Code [http://kidscancode.org].
- Handout do professor.
- Material disponível no curso de Design de Software.
- Kenny [https://www.kenney.nl/].
- Open Game Art [https://opengameart.org/].
- Pygame [https://www.pygame.org/].
