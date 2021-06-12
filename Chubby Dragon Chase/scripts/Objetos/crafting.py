"""Criado por Alexsander Rosante (18/04/2020)"""

import pygame
from parametros.gerais import tela_largura, tela_altura
from scripts.estado import definir_item_selecionado, mostrar_inventario, inventario_opcoes, mostrar_crafting
from scripts.Objetos.item import Item
from scripts.objetos import Menu


class Crafting(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.tipo = "Crafting"

        # Inicializa os grupos
        self.interacao_interna = pygame.sprite.Group()
        self.itens_entrada = pygame.sprite.Group()
        self.item_saida = pygame.sprite.GroupSingle()

        # Inicializa imagem, posição e rect
        self.image = pygame.image.load('imagens/menus/crafting_aberto.png')
        self.x, self.y = tela_largura//2, 380
        self.rect = self.image.get_rect(centerx=self.x, centery=self.y)

        # Posiciona os quadrados interativos
        self.posicionar_interativo_interno('Saída', 180, 144)
        self.posicionar_interativo_interno('Entrada', 100, 328, (1, 1))
        self.posicionar_interativo_interno('Entrada', 260, 328, (1, 2))

        # Estados
        self.interagiu = False

    def update(self, mouse_posicao, mouse_besquerdo, mouse_bdireito):
        if not self.interacao_externa(mouse_posicao, mouse_bdireito):
            self.image = pygame.image.load('imagens/menus/crafting_aberto.png')
            self.interacao_interna.update(mouse_posicao, mouse_besquerdo, self.itens_entrada, self.item_saida)
            self.itens_entrada.update(mouse_posicao, mouse_besquerdo, mouse_bdireito)
            self.item_saida.update(mouse_posicao, mouse_besquerdo, mouse_bdireito)
            self.interacao_interna.draw(self.image)
            self.itens_entrada.draw(self.image)
            self.item_saida.draw(self.image)

    def interacao_externa(self, mouse_posicao, mouse_bdireito):
        if not self.rect.collidepoint(mouse_posicao) and mouse_bdireito:
            if len(self.itens_entrada) > 0:
                return False
            else:
                mostrar_crafting(0)
                return True
        return False

    def posicionar_interativo_interno(self, tipo, x, y, posicao=(0, 0)):
        interativo = QuadradoInterativo(tipo)
        interativo.x, interativo.y, interativo.posicao = x, y, posicao
        self.interacao_interna.add(interativo)


class QuadradoInterativo(pygame.sprite.Sprite):

    def __init__(self, tipo):
        pygame.sprite.Sprite.__init__(self)
        self.tipo = tipo
        self.posicao = 0, 0
        self.image = pygame.image.load('imagens/menus/transparente.png')
        self.x, self.y = 0, 0
        self.rect = self.image.get_rect()
        self.ocupado = False

    def update(self, mouse_posicao, mouse_besquerdo, grupo_itens_entrada, grupo_item_saida):
        from scripts.estado import item_selecionado
        combinacoes = {'pedragraveto': 'martelo de pedra',
                       'gravetopedra': 'martelo de pedra',
                       'gravetopedra lascada': 'machado de pedra',
                       'pedra lascadagraveto': 'machado de pedra'}
        posicao_para_coordenada = {(0, 0): (180, 144),
                                   (1, 1): (100, 328),
                                   (1, 2): (260, 328)}
        self.rect = self.image.get_rect(centerx=self.x, centery=self.y)
        if len(grupo_itens_entrada) == 0:
            self.ocupado = False
        if self.tipo == 'Entrada':
            # Mouse sobre e clique sobre um slot
            if self.rect.collidepoint((mouse_posicao[0] - 505, mouse_posicao[1])) and mouse_besquerdo:
                if item_selecionado[0]:  # Item selecionado
                    if self.ocupado:  # Slot ocupado -> Não faz nada
                        pass
                    else:  # Slot vazio -> Adiciona item nele
                        inventario_opcoes('Remover', item_selecionado[1], item_selecionado[2])
                        item = Item(item_selecionado[1], 'Crafting')
                        item.posicao = self.posicao
                        item.x, item.y = posicao_para_coordenada[self.posicao]
                        grupo_itens_entrada.add(item)
                        definir_item_selecionado(False)
                        mostrar_inventario(1)
                        pygame.mouse.set_visible(True)
                        self.ocupado = True
                else:  # Item não selecionado -> O devolve para o inventário
                    for i in grupo_itens_entrada:
                        if i.posicao == self.posicao:
                            inventario_opcoes('Adicionar', i.item)
                            grupo_itens_entrada.remove(i)
                            mostrar_inventario(1)
                            self.ocupado = False
        elif self.tipo == 'Saída':
            if len(grupo_itens_entrada) > 0:
                grupo_item_saida.empty()
                saida = ''
                for i in grupo_itens_entrada:
                    saida += i.item
                if saida in combinacoes:
                    item = Item(combinacoes[saida], 'Crafting')
                    item.posicao = self.posicao
                    item.x, item.y = posicao_para_coordenada[self.posicao]
                    grupo_item_saida.add(item)
                else:
                    grupo_item_saida.empty()
            if len(grupo_item_saida) > 0:
                if self.rect.collidepoint((mouse_posicao[0] - 505, mouse_posicao[1])) and mouse_besquerdo:
                    for i in grupo_item_saida:
                        inventario_opcoes('Adicionar', i.item)
                        grupo_itens_entrada.empty()
                        grupo_item_saida.empty()
                        mostrar_inventario(1)


def gerenciar_crafting(grupo):
    """Abre ou fecha o sistema de crafting"""
    from scripts.estado import crafting_estado
    # Abriu ou fechou o crafting
    if crafting_estado == 1:
        for i in grupo:
            if i.tipo == 'Crafting':
                grupo.remove(i)
        grupo.add(Crafting())
        mostrar_crafting(3)
        mostrar_inventario(1)
    elif crafting_estado == 0:
        for i in grupo:
            if i.tipo == 'Crafting':
                grupo.remove(i)
        menu = Menu("Crafting")
        menu.x, menu.y = tela_largura // 2, tela_altura - menu.altura // 2 - 10
        grupo.add(menu)
        mostrar_crafting(2)
