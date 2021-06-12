"""Uma interface em que o jogador administra os itens, chamada de inventário.
Criado por Alexsander Rosante (14/04/20)"""

import pygame
from scripts.estado import mostrar_inventario, inventario_opcoes, definir_item_selecionado, definir_item_alvejado
from scripts.Objetos.item import Item
from scripts.objetos import Menu
from parametros.gerais import tela_largura, tela_altura


class Inventario(pygame.sprite.Sprite):

    def __init__(self, lista):
        pygame.sprite.Sprite.__init__(self)
        self.tipo = 'Inventário'
        self.image = pygame.image.load('imagens/menus/inventario_aberto.png')
        self.lotes = pygame.sprite.Group()
        self.itens = pygame.sprite.Group()
        self.posicionar_itens(lista)
        self.x, self.y = 195, 380
        self.rect = self.image.get_rect(centerx=self.x, centery=self.y)

        # Inicializa a lixeira
        lixeira = Lote('Lixeira', 48, 696)
        self.lotes.add(lixeira)

    def update(self, mouse_posicao, mouse_besquerdo, mouse_bdireito):
        self.interacao(mouse_posicao, mouse_besquerdo, mouse_bdireito)
        self.lotes.update(mouse_posicao, mouse_besquerdo)
        self.image = pygame.image.load('imagens/menus/inventario_aberto.png')
        self.itens.update(mouse_posicao, mouse_besquerdo, mouse_bdireito)
        self.lotes.draw(self.image)
        self.itens.draw(self.image)

    def interacao(self, mouse_posicao, mouse_besquerdo, mouse_bdireito):
        from scripts.estado import item_selecionado
        if not self.rect.collidepoint(mouse_posicao) and not item_selecionado[0]:
            if mouse_bdireito:
                mostrar_inventario(0)

    def posicionar_itens(self, lista):
        self.itens.empty()
        if 0 < len(lista) < 32:
            for i in range(len(lista)):
                item = Item(lista[i], "Inventário")
                if i == 0:
                    item.posicao = (1, 1)
                    item.x, item.y = 48, 52
                if i == 1:
                    item.posicao = (1, 2)
                    item.x, item.y = 136, 52
                if i == 2:
                    item.posicao = (1, 3)
                    item.x, item.y = 224, 52
                if i == 3:
                    item.posicao = (1, 4)
                    item.x, item.y = 312, 52
                if i == 4:
                    item.posicao = (2, 1)
                    item.x, item.y = 48, 144
                if i == 5:
                    item.posicao = (2, 2)
                    item.x, item.y = 136, 144
                if i == 6:
                    item.posicao = (2, 3)
                    item.x, item.y = 224, 144
                if i == 7:
                    item.posicao = (2, 4)
                    item.x, item.y = 312, 144
                if i == 8:
                    item.posicao = (3, 1)
                    item.x, item.y = 48, 236
                if i == 9:
                    item.posicao = (3, 2)
                    item.x, item.y = 136, 236
                if i == 10:
                    item.posicao = (3, 3)
                    item.x, item.y = 224, 236
                if i == 11:
                    item.posicao = (3, 4)
                    item.x, item.y = 312, 236
                if i == 12:
                    item.posicao = (4, 1)
                    item.x, item.y = 48, 328
                if i == 13:
                    item.posicao = (4, 2)
                    item.x, item.y = 136, 328
                if i == 14:
                    item.posicao = (4, 3)
                    item.x, item.y = 224, 328
                if i == 15:
                    item.posicao = (4, 4)
                    item.x, item.y = 312, 328
                if i == 16:
                    item.posicao = (5, 1)
                    item.x, item.y = 48, 420
                if i == 17:
                    item.posicao = (5, 2)
                    item.x, item.y = 136, 420
                if i == 18:
                    item.posicao = (5, 3)
                    item.x, item.y = 224, 420
                if i == 19:
                    item.posicao = (5, 4)
                    item.x, item.y = 312, 420
                if i == 20:
                    item.posicao = (6, 1)
                    item.x, item.y = 48, 512
                if i == 21:
                    item.posicao = (6, 2)
                    item.x, item.y = 136, 512
                if i == 22:
                    item.posicao = (6, 3)
                    item.x, item.y = 224, 512
                if i == 23:
                    item.posicao = (6, 4)
                    item.x, item.y = 312, 512
                if i == 24:
                    item.posicao = (7, 1)
                    item.x, item.y = 48, 604
                if i == 25:
                    item.posicao = (7, 2)
                    item.x, item.y = 136, 604
                if i == 26:
                    item.posicao = (7, 3)
                    item.x, item.y = 224, 604
                if i == 27:
                    item.posicao = (7, 4)
                    item.x, item.y = 312, 604
                if i == 28:
                    item.posicao = (8, 1)
                    item.x, item.y = 136, 696
                if i == 29:
                    item.posicao = (8, 2)
                    item.x, item.y = 224, 696
                if i == 30:
                    item.posicao = (8, 3)
                    item.x, item.y = 312, 696
                self.itens.add(item)


class Lote(pygame.sprite.Sprite):

    def __init__(self, tipo, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.tipo = tipo
        self.posicao = 0, 0
        if self.tipo == 'Lixeira':
            self.image = pygame.image.load('imagens/menus/lixeira.png')
        else:
            self.image = pygame.image.load('imagens/menus/transparente.png')
        self.rect = self.image.get_rect(centerx=x, centery=y)

    def update(self, mouse_posicao, mouse_besquerdo):
        from scripts.estado import item_selecionado
        if self.rect.collidepoint(mouse_posicao[0] - 17, mouse_posicao[1]) and item_selecionado[0]:
            if mouse_besquerdo:
                if self.tipo == 'Lixeira':
                    inventario_opcoes('Remover', item_selecionado[1], item_selecionado[2])
                    mostrar_inventario(1)
                    definir_item_selecionado(False)
                    pygame.mouse.set_visible(True)
            else:
                if self.tipo == 'Lixeira':
                    self.image = pygame.image.load('imagens/menus/lixeira_selecionada.png')
        else:
            if self.tipo == 'Lixeira':
                self.image = pygame.image.load('imagens/menus/lixeira.png')


def gerenciar_inventario(grupo, mouse_posicao, inventario):
    from scripts.estado import item_alvejado, item_selecionado, inventario_estado
    """Função que gere o inventário:
    - Seleciona ou desseleciona um item;
    - Abre ou fecha o inventário"""
    if item_alvejado[0]:  # O jogador clicou no item
        item = Item(item_alvejado[1], "Livre")
        item.interativo = False
        grupo.add(item)
        definir_item_selecionado(True, item_alvejado[1], item_alvejado[2])
        definir_item_alvejado(False)
    if item_selecionado[0]:  # O item foi selecionado
        for i in grupo:
            if i.tipo == "Item":
                pygame.mouse.set_visible(False)
                i.x, i.y = mouse_posicao
    else:  # O item foi dessecelecionado
        if inventario_estado == 1:
            for i in grupo:
                if i.tipo == "Item":
                    grupo.remove(i)
    if inventario_estado == 1:  # Abriu o inventário
        for i in grupo:
            if i.tipo == 'Inventário':
                grupo.remove(i)
        grupo.add(Inventario(inventario))
        mostrar_inventario(3)
    elif inventario_estado == 0:  # Fechou o inventário
        for i in grupo:
            if i.tipo == 'Inventário':
                grupo.remove(i)
        menu = Menu("Inventário")
        menu.x, menu.y = menu.largura // 2, tela_altura - menu.altura // 2 - 10
        grupo.add(menu)
        mostrar_inventario(2)
