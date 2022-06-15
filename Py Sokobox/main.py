import pygame
import numpy as np
from classes.floor import Floor
from classes.player import Player
from classes.box import Box

# Variáveis globais
gameLevel = ''
reset = '-1'
gameLoop = True
tamS = 64  # tamanho de cada sprite
tLargura = 15  # quantidade de pisos horizontal
tAltura = 10  # quantidade de pisos vertical
tamX = tamS * tLargura
tamY = tamS * tAltura
movimentos = 0

# Matriz
rangeMatX = range(tamX // tamS)
rangeMatY = range(tamY // tamS)
mat = []

#  Inicializa o pygame e a janela do jogo
pygame.init()
resDisplay = (tamX, tamY)
display1 = pygame.display.set_mode(resDisplay)
pygame.display.set_caption("Sokobox")
displayIcon = pygame.image.load('sprites/box.png')
pygame.display.set_icon(displayIcon)

# Cria os grupos
objectGroup = pygame.sprite.Group()
playerGroup = pygame.sprite.Group()
groundGroup = pygame.sprite.Group()
obstacleGroup = pygame.sprite.Group()
boxGroup = pygame.sprite.Group()


def draw_groups():
    """Desenha os grupos e atualiza a tela"""
    objectGroup.draw(display1)
    playerGroup.draw(display1)
    boxGroup.draw(display1)
    pygame.display.update()


def play_game(level):
    """Inicia o jogo no nivel recebido como argumento"""
    global gameLoop, movimentos, mat, gameLevel
    erro = False
    # level = '6'  # força um IOError ~teste~
    gameLevel = level
    movimentos = 0
    for d in objectGroup:
        d.kill()
    # mat = np.loadtxt("levels/lvl" + level + ".dat", dtype='i', delimiter=' ')
    try:
        mat = np.loadtxt("levels/lvl" + level + ".dat", dtype='i', delimiter=' ')
    except OSError:  # OSError inclui vários tipos de erro, incluindo também o IOError
        print("Erro ao tentar abrir o arquivo!")
        gameLoop = False
        erro = True
        return erro
    gameLoop = True
    return erro


# lvl.dat -> 0 - chão, 1 - player, 2 - caixa, 3 - marca, 4 - marca com caixa, 5 - marca com player, 6 - obstáculo
def draw_objects():
    """Desenha na tela todos os objetos obtidos do arquivo de 'levels'"""
    for y in range(0, tamY // tamS):
        for x in range(0, tamX // tamS):
            Floor(objectGroup, groundGroup, posx=x * tamS, posy=y * tamS, ts=tamS, s='F')  # chão
    for x in range(0, tLargura):
        for y in range(0, tAltura):
            if mat[y][x] == 2:  # caixa
                Box(objectGroup, boxGroup, posx=x * tamS, posy=y * tamS, ts=tamS, pos_mat=mat[y][x])
            elif mat[y][x] == 3 or mat[y][x] == 5:  # marca
                Floor(objectGroup, groundGroup, posx=x * tamS, posy=y * tamS, ts=tamS, s='M')
            elif mat[y][x] == 4:  # marca com caixa
                Box(objectGroup, boxGroup, posx=x * tamS, posy=y * tamS, ts=tamS, pos_mat=mat[y][x])
                Floor(objectGroup, groundGroup, posx=x * tamS, posy=y * tamS, ts=tamS, s='M')
            elif mat[y][x] == 6:  # obstáculo
                Floor(objectGroup, obstacleGroup, posx=x * tamS, posy=y * tamS, ts=tamS, s='O')


def draw_button(but_posx, but_posy, but_tamx, but_tamy, text, pos_textx, pos_texty, mouse):
    """Cria um botão usando as coordenadas, tamanhos e texto recebidos e muda a cor do botão ao passar o mouse"""
    dark = (121, 65, 35)
    light = (255, 120, 12)
    if but_posx <= mouse[0] <= but_posx + but_tamx and but_posy <= mouse[1] <= but_posy + but_tamy:
        cor = light
    else:
        cor = dark
    pygame.draw.rect(display1, cor, [but_posx, but_posy, but_tamx, but_tamy])
    display1.blit(text, (pos_textx, pos_texty))


def add_highscore():
    """Se 'movimentos' for menor que o maior elemento dos Highscores daquele level, adiciona 'movimentos' à lista"""
    f = open("highscores/lvl" + gameLevel + ".dat", 'r')  # abre arquivos com os highscores
    hs = f.read().splitlines()
    hs = [int(i) for i in hs]  # list comprehension -> converter a lista de strings lidas do arquivo em int
    if movimentos < (max(hs)):  # adiciona aos highscores se teve menos movimentos que o maior da lista
        if len(hs) == 10:  # limite de 10 highscores por level
            hs.remove(max(hs))
        hs.append(movimentos)
        hs.sort()  # organiza a lista em ordem crescente
        hs = [str(i) for i in hs]  # converter a nova lista de int para str
        with open("highscores/lvl" + gameLevel + ".dat", 'w') as f:
            for k in hs:
                f.write("%s\n" % k)
    f.close()


def highscores():
    """Cria a tela de melhores pontuações usando os arquivos .dat em 'highscores'"""
    global gameLoop
    f = [0, 0, 0, 0, 0, 0]  # arquivos
    hs = [0, 0, 0, 0, 0, 0]  # lista de highscores
    for k in range(1, 6):
        f[k] = open("highscores/lvl" + str(k) + ".dat", 'r')  # abre arquivos com os highscores
    for j in range(1, 6):
        hs[j] = f[j].read().splitlines()
        hs[j] = [int(i) for i in hs[j]]  # list comprehension -> converter as strings lidas do arquivo em int
        hs[j].sort()  # organiza a lista em ordem crescente
    color = (0, 204, 202)
    color2 = (255, 255, 255)
    font1 = pygame.font.SysFont('Comic Sans', tamY // 6)
    font2 = pygame.font.SysFont('Comic Sans', tamY // 20)
    font3 = pygame.font.SysFont('Comic Sans', tamY // 28)
    font4 = pygame.font.SysFont('Comic Sans', tamY // 35)
    text1 = font1.render('Highscores', True, color)
    bg = pygame.image.load("sprites/bbg.png")
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                gameLoop = False
                return
        display1.blit(bg, (0, 0))
        display1.blit(text1, (tamX // 5, 20))
        for i in range(5):
            s = 'Level ' + str(i + 1)
            text2 = font2.render(s, True, color2)
            display1.blit(text2, (int(tamX * (0.05 + i * 0.2)), 160))
        for p in range(5):
            for q in range(len(hs[p + 1])):
                s = str(hs[p + 1][q]) + ' mov.'
                text2 = font3.render(s, True, color2)
                display1.blit(text2, (int(tamX * (0.05 + p * 0.2)), int(200 + q * 40)))
        mouse = pygame.mouse.get_pos()
        draw_button(tamX - 100, tamY - 50, 60, 30, font4.render('Voltar', True, color2), tamX - 95, tamY - 45, mouse)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if tamX - 100 <= mouse[0] <= tamX - 100 + 60 and tamY - 50 <= mouse[1] <= tamY - 50 + 30:
                    for k in range(1, 6):
                        f[k].close()  # fecha os arquivos ao sair da tela de highscores
                    return

        pygame.display.update()


def game():
    global gameLoop, movimentos, gameLevel, reset
    moves2 = movimentos
    victory = pygame.image.load("sprites/vict.png")
    surface = pygame.display.get_surface()
    color = (192, 192, 192)
    w, h = surface.get_width(), surface.get_height()
    font1 = pygame.font.SysFont('Comic Sans', tamY // 10)
    font2 = pygame.font.SysFont('Comic Sans', tamY // 20)
    iniX, iniY = 0, 0
    found = False
    for x in rangeMatX:  # posição inicial do player
        for y in rangeMatY:
            if mat[y][x] == 1 or mat[y][x] == 5:
                iniX = x
                iniY = y
                found = True
                break
        if found:
            break
    auxX = iniX  # auxiliares -> guardam a posição anterior do jogador
    auxY = iniY
    # inicia o jogador na posição mat[y][x] == 1 ou 5
    P1 = Player(objectGroup, playerGroup, posx=iniX * tamS, posy=iniY * tamS, ts=tamS, yalt=tAltura, xlar=tLargura)
    draw_objects()
    while gameLoop:
        cont = 0  # contador para a condição de vitória
        mouse = pygame.mouse.get_pos()
        clock.tick(60)  # taxa de atualização -> 60 quadros por segundo
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # X -> terminar o jogo
                gameLoop = False
                P1.kill()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if tamX - tamS < mouse[0] <= tamX and 0 <= mouse[1] <= tamS:  # botão para voltar ao menu
                    gameLoop = False
                    P1.kill()
                    return
                elif tamX - 2 * tamS <= mouse[0] <= tamX - tamS and 0 <= mouse[1] <= tamS:  # botão para resetar o nivel
                    P1.kill()
                    play_game(gameLevel)
                    gameLoop = False
                    reset = gameLevel
                    print(f'gameLevel = {gameLevel}')
                    return
        # update
        colPlayerBox = pygame.sprite.groupcollide(playerGroup, boxGroup, False, True)  # colisão player x caixa
        colPlayerObs = pygame.sprite.groupcollide(playerGroup, obstacleGroup, False, False)  # colisão player x obst.

        # se o personagem se moveu
        if P1.rect.left // tamS != auxX or P1.rect.top // tamS != auxY:
            if colPlayerBox:
                getPos = P1.posPlayer  # obtém a direção em que o player está virado
                if getPos == 'playerU':
                    if P1.rect.top == 0:  # caixa x parede
                        P1.rect.top = tamS
                        Box(objectGroup, boxGroup, posx=P1.rect.left, posy=0, ts=tamS,
                            pos_mat=mat[0][P1.rect.left // tamS])
                    # caixa x caixa / caixa x obstáculo
                    elif mat[P1.rect.top // tamS - 1][P1.rect.left // tamS] == 2 \
                            or mat[P1.rect.top // tamS - 1][P1.rect.left // tamS] == 4 \
                            or mat[P1.rect.top // tamS - 1][P1.rect.left // tamS] == 6:
                        Box(objectGroup, boxGroup, posx=P1.rect.left, posy=P1.rect.top, ts=tamS,
                            pos_mat=mat[P1.rect.top // tamS][P1.rect.left // tamS])
                        P1.rect.top = P1.rect.top + tamS
                    else:  # player consegue empurrar a caixa
                        movimentos += 1
                        Box(objectGroup, boxGroup, posx=P1.rect.left, posy=P1.rect.top - tamS, ts=tamS,
                            pos_mat=mat[(P1.rect.top - tamS) // tamS][P1.rect.left // tamS])
                        if mat[(P1.rect.top - tamS) // tamS][P1.rect.left // tamS] == 3:
                            # se tiver marca no chão -> caixa verde
                            mat[(P1.rect.top - tamS) // tamS][P1.rect.left // tamS] = 4
                        else:
                            mat[(P1.rect.top - tamS) // tamS][P1.rect.left // tamS] = 2
                elif getPos == 'playerD':
                    if P1.rect.bottom == tamY:
                        P1.rect.bottom = tamY - tamS
                        Box(objectGroup, boxGroup, posx=P1.rect.left, posy=tamY - tamS, ts=tamS,
                            pos_mat=mat[(tamY - tamS) // tamS][P1.rect.left // tamS])
                    elif mat[P1.rect.top // tamS + 1][P1.rect.left // tamS] == 2 \
                            or mat[P1.rect.top // tamS + 1][P1.rect.left // tamS] == 4 \
                            or mat[P1.rect.top // tamS + 1][P1.rect.left // tamS] == 6:
                        Box(objectGroup, boxGroup, posx=P1.rect.left, posy=P1.rect.top, ts=tamS,
                            pos_mat=mat[P1.rect.top // tamS][P1.rect.left // tamS])
                        P1.rect.top = P1.rect.top - tamS
                    else:
                        movimentos += 1
                        Box(objectGroup, boxGroup, posx=P1.rect.left, posy=P1.rect.top + tamS, ts=tamS,
                            pos_mat=mat[(P1.rect.top + tamS) // tamS][P1.rect.left // tamS])
                        if mat[(P1.rect.top + tamS) // tamS][P1.rect.left // tamS] == 3:
                            mat[(P1.rect.top + tamS) // tamS][P1.rect.left // tamS] = 4
                        else:
                            mat[(P1.rect.top + tamS) // tamS][P1.rect.left // tamS] = 2
                elif getPos == 'playerL':
                    if P1.rect.left == 0:
                        P1.rect.left = tamS
                        Box(objectGroup, boxGroup, posx=0, posy=P1.rect.top, ts=tamS,
                            pos_mat=mat[P1.rect.top // tamS][0])
                    elif mat[P1.rect.top // tamS][P1.rect.left // tamS - 1] == 2 \
                            or mat[P1.rect.top // tamS][P1.rect.left // tamS - 1] == 4 \
                            or mat[P1.rect.top // tamS][P1.rect.left // tamS - 1] == 6:
                        Box(objectGroup, boxGroup, posx=P1.rect.left, posy=P1.rect.top, ts=tamS,
                            pos_mat=mat[P1.rect.top // tamS][P1.rect.left // tamS])
                        P1.rect.left = P1.rect.left + tamS
                    else:
                        movimentos += 1
                        Box(objectGroup, boxGroup, posx=P1.rect.left - tamS, posy=P1.rect.top, ts=tamS,
                            pos_mat=mat[P1.rect.top // tamS][(P1.rect.left - tamS) // tamS])
                        if mat[P1.rect.top // tamS][(P1.rect.left - tamS) // tamS] == 3:
                            mat[P1.rect.top // tamS][(P1.rect.left - tamS) // tamS] = 4
                        else:
                            mat[P1.rect.top // tamS][(P1.rect.left - tamS) // tamS] = 2
                elif getPos == 'playerR':
                    if P1.rect.right == tamX:
                        P1.rect.right = tamX - tamS
                        Box(objectGroup, boxGroup, posx=tamX - tamS, posy=P1.rect.top, ts=tamS,
                            pos_mat=mat[P1.rect.top // tamS][(tamX - tamS) // tamS])
                    elif mat[P1.rect.top // tamS][P1.rect.left // tamS + 1] == 2 \
                            or mat[P1.rect.top // tamS][P1.rect.left // tamS + 1] == 4 \
                            or mat[P1.rect.top // tamS][P1.rect.left // tamS + 1] == 6:
                        Box(objectGroup, boxGroup, posx=P1.rect.left, posy=P1.rect.top, ts=tamS,
                            pos_mat=mat[P1.rect.top // tamS][P1.rect.left // tamS])
                        P1.rect.left = P1.rect.left - tamS
                    else:
                        movimentos += 1
                        Box(objectGroup, boxGroup, posx=P1.rect.left + tamS, posy=P1.rect.top, ts=tamS,
                            pos_mat=mat[P1.rect.top // tamS][(P1.rect.left + tamS) // tamS])
                        if mat[P1.rect.top // tamS][(P1.rect.left + tamS) // tamS] == 3:
                            mat[P1.rect.top // tamS][(P1.rect.left + tamS) // tamS] = 4
                        else:
                            mat[P1.rect.top // tamS][(P1.rect.left + tamS) // tamS] = 2

            elif colPlayerObs:  # player x obstáculo
                getPos = P1.posPlayer
                if getPos == 'playerU':
                    P1.rect.top = P1.rect.top + tamS
                elif getPos == 'playerD':
                    P1.rect.top = P1.rect.top - tamS
                elif getPos == 'playerL':
                    P1.rect.left = P1.rect.left + tamS
                elif getPos == 'playerR':
                    P1.rect.left = P1.rect.left - tamS

            else:
                movimentos += 1

            # posição anterior do player
            if mat[auxY][auxX] == 5:  # player em cima da marca -> marca
                mat[auxY][auxX] = 3
            else:
                mat[auxY][auxX] = 0

            # posição atual do player
            if mat[P1.rect.top // tamS][P1.rect.left // tamS] == 3 or \
                    mat[P1.rect.top // tamS][P1.rect.left // tamS] == 4:
                mat[P1.rect.top // tamS][P1.rect.left // tamS] = 5
            else:
                mat[P1.rect.top // tamS][P1.rect.left // tamS] = 1

            # posição anterior -> posição atual
            auxX = P1.rect.left // tamS
            auxY = P1.rect.top // tamS
        draw_groups()

        # CONDIÇÃO DE VITÓRIA
        for x in rangeMatX:
            for y in rangeMatY:
                if mat[y][x] != 0 and mat[y][x] != 1 and mat[y][x] != 4 and mat[y][x] != 6:
                    cont += 1  # se encontrar item que não seja piso, player, marca com caixa e obstáculos -> cont++

        if cont == 0:  # se todas as caixas estão em cima de uma marca
            print(f' movimentos = {movimentos}')
            # verifica se o número de movimentos é uma das melhores pontuações e adiciona à lista caso seja
            add_highscore()
            gameLoop = False
            # imagens e textos da tela de vitória
            victory = pygame.transform.scale(victory, [int(0.85 * w), int(0.4 * h)])
            txt = font1.render('Pressione qualquer tecla...', True, color)
            txt2 = font2.render(f'Movimentos: {movimentos}', True, color)
            display1.blit(victory, ((w - int(0.85 * w)) // 2, int(0.08 * h)))
            display1.blit(txt, (int(tamX * 0.22), int(tamY * 0.5)))
            display1.blit(txt2, (int(tamX * 0.42), int(tamY * 0.6)))
            pygame.display.update()
            pressed = False
            while not pressed:
                for event in pygame.event.get():  # aguarda uma tecla ser pressionada
                    if event.type == pygame.KEYDOWN:
                        pressed = True
                        break
        if moves2 is not movimentos and cont != 0:
            moves2 = movimentos
            print(f'movimentos -> {movimentos}')
        objectGroup.update()


def menu():
    global gameLoop, reset
    bg = pygame.image.load("sprites/bgm.png")
    bgtxt = pygame.image.load("sprites/skb.png")
    color = (255, 255, 255)
    # Obtém a superfície da tela criada
    surface = pygame.display.get_surface()
    x, y = surface.get_width(), surface.get_height()
    font1 = pygame.font.SysFont('Comic Sans', tamY // 36)
    # TAMANHOS
    # botao 1
    but1X = int(tamX * 0.05)
    # botao 2
    but2X = int(tamX * 0.25)
    # botao 3
    but3X = int(tamX * 0.45)
    # botao 4
    but4X = int(tamX * 0.65)
    # botao 5
    but5X = int(tamX * 0.85)
    # highscore
    but6X = int(tamX * 0.35)
    # sair
    but7X = int(tamX * 0.55)

    butY = int(0.58 * tamY)
    # highscores/sair
    butHY = int(0.72 * tamY)

    # altura e largura dos botões
    butW = int(tamX * 0.13)
    butH = int(tamY * 0.05)

    # textos dos botões
    text1 = font1.render('Level 1', True, color)
    text2 = font1.render('Level 2', True, color)
    text3 = font1.render('Level 3', True, color)
    text4 = font1.render('Level 4', True, color)
    text5 = font1.render('Level 5', True, color)
    text6 = font1.render('Highscores', True, color)
    text7 = font1.render('Sair', True, color)

    while True:
        mouse = pygame.mouse.get_pos()
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:  # Click no 'X' da janela
                gameLoop = False
                return
            # AÇÕES DOS BOTÕES DO MENU
            # level 1
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if but1X <= mouse[0] <= but1X + butW and butY <= mouse[1] <= butY + butH:
                    # se encontrar um IOError não entra em game() e continua no menu inicial
                    if not play_game('1'):
                        game()
            # level 2
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if but2X <= mouse[0] <= but2X + butW and butY <= mouse[1] <= butY + butH:
                    if not play_game('2'):
                        game()
            # level 3
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if but3X <= mouse[0] <= but3X + butW and butY <= mouse[1] <= butY + butH:
                    if not play_game('3'):
                        game()
            # level 4
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if but4X <= mouse[0] <= but4X + butW and butY <= mouse[1] <= butY + butH:
                    if not play_game('4'):
                        game()
            # level 5
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if but5X <= mouse[0] <= but5X + butW and butY <= mouse[1] <= butY + butH:
                    if not play_game('5'):
                        game()
            # Highscores
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if but6X <= mouse[0] <= but6X + butW and butHY <= mouse[1] <= butHY + butH:
                    highscores()
            # Sair
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if but7X <= mouse[0] <= but7X + butW and butHY <= mouse[1] <= butHY + butH:
                    gameLoop = False
                    return

        # Desenha as imagens do menu
        bgtxt = pygame.transform.scale(bgtxt, [int(0.85 * x), int(0.4 * y)])
        display1.blit(bg, (0, 0))
        display1.blit(bgtxt, ((x - int(0.85 * x)) // 2, int(0.08 * y)))

        # Desenha os botões
        # 1
        draw_button(but1X, butY, butW, butH, text1, but1X + 32, butY + 5, mouse)
        # 2
        draw_button(but2X, butY, butW, butH, text2, but2X + 32, butY + 5, mouse)
        # 3
        draw_button(but3X, butY, butW, butH, text3, but3X + 32, butY + 5, mouse)
        # 4
        draw_button(but4X, butY, butW, butH, text4, but4X + 32, butY + 5, mouse)
        # 5
        draw_button(but5X, butY, butW, butH, text5, but5X + 32, butY + 5, mouse)
        # Highscores
        draw_button(but6X, butHY, butW, butH, text6, but6X + 15, butHY + 5, mouse)
        # Sair
        draw_button(but7X, butHY, butW, butH, text7, but7X + 43, butHY + 5, mouse)
        if int(reset) > 0:
            reset = '-1'
            gameLoop = True
            game()
        # atualiza a tela
        pygame.display.update()


def main():
    menu()


clock = pygame.time.Clock()  # inicia o timer do pygame para exibição de quadros por segundo
main()
