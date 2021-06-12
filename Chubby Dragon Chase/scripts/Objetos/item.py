# Criado por Alexsander Rosante (15/04/20)

# Esse script trabalha em conjunto com o de inventátio.

import pygame
from scripts.estado import definir_item_alvejado, mostrar_inventario


class Item(pygame.sprite.Sprite):

    def __init__(self, item, local):
        pygame.sprite.Sprite.__init__(self)

        self.tipo = "Item"
        self.local = local

        self.itens = {'graveto': 'graveto',
                      'machado de pedra': 'machado_pedra',
                      'martelo de pedra': 'martelo_pedra',
                      'pedra': 'pedra',
                      'pedra lascada': 'pedra_lascada'}

        self.item = item
        self.image = pygame.image.load('imagens/itens/' + self.itens[self.item] + '.png')
        self.rect = self.image.get_rect()
        self.posicao = (0, 0)
        self.x, self.y = -100, -100
        self.interativo = True

    def update(self, mouse_posicao, mouse_besquerdo, mouse_bdireito):
        if self.interativo:
            self.interacao(mouse_posicao, mouse_besquerdo)
        else:
            self.image = pygame.image.load('imagens/itens/' + self.itens[self.item] + '_selecionado.png')
        self.rect = self.image.get_rect(centerx=self.x, centery=self.y)

    def interacao(self, mouse_posicao, mouse_besquerdo):
        from scripts.estado import item_selecionado
        if item_selecionado[0] and item_selecionado[2] == self.posicao and self.local == "Inventário":
            self.image = pygame.image.load('imagens/itens/nada.png')
            self.x, self.y = -100, -100
        elif self.local in ['Inventário', 'Crafting', 'Dropado']:
            ajuste = 0
            if self.local == 'Inventário':
                ajuste = 17
            elif self.local == 'Crafting':
                ajuste = 505
            if self.rect.collidepoint(mouse_posicao[0] - ajuste, mouse_posicao[1]):
                if mouse_besquerdo:
                    if self.local == 'Inventário':
                        definir_item_alvejado(True, self.item, self.posicao)
                    elif self.local == 'Dropado':
                        
                        mostrar_inventario(1)
                else:
                    self.image = pygame.image.load('imagens/itens/' + self.itens[self.item] + '_selecionado.png')
            else:
                self.image = pygame.image.load('imagens/itens/' + self.itens[self.item] + '.png')
        else:
            self.image = pygame.image.load('imagens/itens/' + self.itens[self.item] + '.png')
