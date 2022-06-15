import pygame


class Box(pygame.sprite.Sprite):
    """Classe das caixas movíveis"""
    def __init__(self, group1, group2, posx, posy, ts, pos_mat):
        super().__init__(group1, group2)
        self.rect = pygame.Rect(posx, posy, ts, ts)
        self.caixa = ''
        if pos_mat == 3 or pos_mat == 4:  # marca com caixa
            self.caixa = 'boxv'  # caixa verde
        else:
            self.caixa = 'box1'  # caixa marrom
        self.image = pygame.image.load('sprites/' + self.caixa + '.png')
        self.image = pygame.transform.scale(self.image, [ts, ts])
