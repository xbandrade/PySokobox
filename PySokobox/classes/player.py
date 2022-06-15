import pygame
import time


class Player(pygame.sprite.Sprite):
    """Classe que contém o personagem"""
    def __init__(self, group1, group2, posx, posy, ts, yalt, xlar):
        super().__init__(group1, group2)
        self.rect = pygame.Rect(posx, posy, ts, ts)
        self.Tw = xlar * ts  # largura total da janela
        self.Th = yalt * ts  # altura total da janela
        self.tS = ts
        self.posPlayer = 'playerD'  # lado em que o jogador começa o jogo
        self.image = pygame.image.load('sprites/' + self.posPlayer + '.png')  # carrega a sprite do jogador

    def update(self):
        """Atualiza a posição e a sprite do personagem"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.posPlayer = 'playerR'
            self.rect.x += self.tS
            if self.rect.right >= self.Tw:  # não atravessar a borda do mapa e sair da tela
                self.rect.right = self.Tw
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.posPlayer = 'playerL'
            self.rect.x -= self.tS
            if self.rect.left <= 0:
                self.rect.left = 0
        elif keys[pygame.K_w] or keys[pygame.K_UP]:
            self.posPlayer = 'playerU'
            self.rect.y -= self.tS
            if self.rect.top < 0:
                self.rect.top = 0
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.posPlayer = 'playerD'
            self.rect.y += self.tS
            if self.rect.bottom > self.Th:
                self.rect.bottom = self.Th
        self.image = pygame.image.load('sprites/' + self.posPlayer + '.png')
        self.image = pygame.transform.scale(self.image, [self.tS, self.tS])
        pygame.display.update()
        time.sleep(0.17)  # adiciona um delay ao movimento do player
