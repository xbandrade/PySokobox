import pygame


class Floor(pygame.sprite.Sprite):
    """Classe contendo todos os itens fixos ao chão: pisos, marcas e obstáculos"""
    def __init__(self, group1, group2, posx, posy, ts, s):
        super().__init__(group1, group2)
        tLar = 15
        if s == 'F':  # piso
            s = 'floor'
        elif s == 'M':  # marca
            s = 'mark'
        elif s == 'O':  # obstáculos
            if posy == 0 and posx == (tLar - 1) * ts:  # cria o botão de voltar ao menu
                s = 'sair'
            elif posy == 0 and posx == (tLar - 2) * ts:  # cria o botão de resetar o nível
                s = 'reset'
            else:
                s = 'obs'
        self.image = pygame.image.load("sprites/" + s + ".png")
        self.image = pygame.transform.scale(self.image, [ts, ts])
        self.rect = pygame.Rect(posx, posy, ts, ts)
