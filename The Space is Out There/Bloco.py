# Criado por Alexsander Rosante

from Pixel import *
import random
from Textura.textura_blocos import terra_marrom

# Notas:
# . A posição do mouse na função update entra para suprir a demanda da função comando. Como a única que interage com
# o módulo Main é a update, fica que ele deve passar por esta;
# . O mesmo vale para o botão esquerdo do mouse;


class Bloco(object):

    # Parâmetros iniciais
    image = pygame.Surface((1, 1))
    rect = image.get_rect()

    def __init__(self):

        # Superfície genérica
        self.superficie = pygame.Surface((1, 1))
        self.lista_superficie = []

        # Características
        self.quantidade_de_pixeis = 16
        self.largura, self.altura = tamanho_do_pixel * self.quantidade_de_pixeis, \
                                    tamanho_do_pixel * self.quantidade_de_pixeis
        self.cor = branco

        # Posição
        self.x, self.y = tela_centro
        self.altura_minima = fundo_altura - self.altura / 2
        self.centro = (self.largura//2, self.altura//2)

        # Estado
        self.gravidade = False
        self.quebrando = False

        # Propriedades principais
        self.lista = []
        self.image = pygame.Surface((self.largura, self.altura))
        self.rect = self.image.get_rect(centerx=self.x, centery=self.y)

        # Propriedades secundárias
        self.image.fill(cor_do_fundo)

        # Criando o bloco (de terra)
        textura_do_bloco = terra_marrom(self.quantidade_de_pixeis, self.quantidade_de_pixeis)
        for i in range(self.quantidade_de_pixeis):
            for j in range(self.quantidade_de_pixeis):
                pixel = Pixel()
                pixel.cor = textura_do_bloco[i][j]
                pixel.superficie = self.image
                pixel.x = tamanho_do_pixel * j + tamanho_do_pixel / 2
                pixel.y = tamanho_do_pixel * i + tamanho_do_pixel / 2
                self.lista.append(pixel)

        # Atualizando os blocos pela primeira vez
        for pixel in self.lista:
            pixel.update()

    def update(self, posicao_mouse, mouse_besquerdo):
        if len(self.lista) > 0:
            quebrando = self.interacao(posicao_mouse, mouse_besquerdo)
            if quebrando:
                self.image.fill(cor_do_fundo)
                for pixel in self.lista: # For
                    pixel.update()
            if self.gravidade:
                self.gravidade_()
            self.rect = self.image.get_rect(centerx=self.x, centery=self.y)
            self.superficie.blit(self.image, self.rect)

    def interacao(self, posicao_mouse, mouse_besquerdo):
        if mouse_besquerdo:
            if self.rect.collidepoint(posicao_mouse):
                if len(self.lista) < self.quantidade_de_pixeis ** 2 / 2:  # Equação, reduzir
                    for i in range(len(self.lista)):
                        pixel = self.lista[i]
                        pixel.gravidade = True
                        pixel.superficie = self.superficie
                        pixel.x = self.x - self.largura / 2 + pixel.x
                        pixel.y = self.y - self.altura / 2 + pixel.y
                        self.lista_superficie.append(pixel)
                    self.lista = []
                else:
                    try:
                        pixel = self.lista.pop(random.randint(0, len(self.lista)))
                    except:
                        pixel = self.lista.pop(0)
                    pixel.gravidade = True  # Repete (Otimizar depois)
                    pixel.superficie = self.superficie  # Repete (Otimizar depois)
                    pixel.x = self.x - self.largura / 2 + pixel.x  # Repete (Otimizar depois)
                    pixel.y = self.y - self.altura / 2 + pixel.y  # Repete (Otimizar depois)
                    self.lista_superficie.append(pixel)  # Repete (Otimizar depois)
                    return True

    def gravidade_(self):
        if self.y <= self.altura_minima:
            self.y += aceleracao_gravidade
