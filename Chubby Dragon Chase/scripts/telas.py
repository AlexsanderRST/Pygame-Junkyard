"""Responsável por gerir as telas
Criado por Alexsander Rosante (12/03/2020)"""

import pygame
from scripts.objetos import Menu, Marcador
from scripts.gerador_de_cenario import gerar_cenario
from scripts.estado import *
from parametros.gerais import *
from scripts.ia import IA
from scripts.Objetos.crafting import gerenciar_crafting
from scripts.Objetos.criatura import Criatura, gerenciar_criaturas
from scripts.Objetos.inventario import gerenciar_inventario
from scripts.Objetos.item import Item
from scripts.Objetos.submapa import Submapa
import random


class Batalha(object):

    def __init__(self, tela, inventario):

        # Inicializa informações de batalha
        self.turno = 1  # 1 -> Jogador, -1 -> Adversário
        self.inventario = inventario

        # Assume a tela do jogo como própria
        self.tela = tela

        # Grupos da tela, devem ser desenhados na ordem que segue
        self.cenario = pygame.sprite.Group()
        self.blocos = pygame.sprite.Group()
        self.criatura_adversario = pygame.sprite.GroupSingle()
        self.criatura_jogador = pygame.sprite.GroupSingle()
        self.drops = pygame.sprite.Group()  # teste
        self.interface = pygame.sprite.Group()

        # Inicia a tela da batalha, com ressalvas
        self.naodesenharem = []
        self.organizar_cenario()
        self.posicionar_criaturas()

        # Inicia a IA
        self.ia = IA()

        self.grupos = [self.cenario, self.blocos, self.drops, self.criatura_adversario, self.criatura_jogador,
                       self.interface]

        self.mouse_posicao_anterior = (-1, -1)
        self.frame = 0

    def update(self, mouse_posicao, mouse_besquerdo, mouse_bdireito):
        self.checar_vitoria()
        self.intermediar_interacoes(mouse_bdireito)
        if self.turno == -1:
            self.ia.jogar(self.criatura_adversario)
        gerenciar_criaturas(mouse_bdireito)
        self.cenario.update()
        self.criatura_adversario.update(mouse_posicao, mouse_besquerdo, self.criatura_jogador, self.criatura_adversario)
        self.criatura_jogador.update(mouse_posicao, mouse_besquerdo, self.criatura_jogador, self.criatura_adversario)
        self.drops.update(mouse_posicao, mouse_besquerdo, mouse_bdireito)
        gerenciar_inventario(self.interface, mouse_posicao, self.inventario)
        self.interface.update(mouse_posicao, mouse_besquerdo, mouse_bdireito)
        for i in self.grupos:
            i.draw(self.tela)
        self.checar_fim_do_turno()

    def organizar_cenario(self):
        """Carrega o tipo de cenário (Exemplo: floresta, rio); \n
        Posiciona em sequência os seguintes elementos: \n
        - Fundo do cenário; \n
        - Blocos; \n
        - Elementos de interface (Exemplo: inventário)."""
        # Gera o mapa
        self.cenario.add(gerar_cenario('floresta', self.naodesenharem))  # BETA
        # Posiciona os elementos de interface
        menu = Menu("Inventário")
        menu.x, menu.y = menu.largura//2, tela_altura - menu.altura//2 - 10
        self.interface.add(menu)

    def posicionar_criaturas(self):
        """Cria e posiciona as criaturas sobre os blocos; \n
        As listas administradas por esta função estão no __init__ (Exemplo de lista: [0, 0, 'pedra']); \n
        Essa função é chamada pelo __init__;"""
        from scripts.estado import formacao_jogador, formacao_adversario
        if formacao_adversario != 0:  # Deve ser garantido
            for i in range(2):
                if i == 0:  # Jogador
                    criatura = Criatura(formacao_jogador[0])
                    criatura.jogador = 1
                    criatura.y = tela_altura - 240 - criatura.ancoragem
                else:  # Adversário
                    criatura = Criatura(formacao_adversario[0])
                    criatura.jogador = -1
                    criatura.y = 240 - criatura.ancoragem
                criatura.x = tela_largura // 2
                criatura.xi, criatura.yi = criatura.x, criatura.y
                criatura.posicao = [i, 0]
                if i == 0:
                    self.criatura_jogador.add(criatura)
                else:
                    self.criatura_adversario.add(criatura)

    def intermediar_interacoes(self, _):
        from scripts.estado import dropar_itens
        if dropar_itens['verdade']:
            n = random.randint(0, 3)
            if n > 0:
                for i in range(n):
                    item = Item(random.choice(dropar_itens['lista de itens']), 'Dropado')
                    item.x = random.randint(583, 783)
                    if dropar_itens['jogador'] < 0:
                        item.y = random.randint(54, 254)
                    else:
                        item.y = random.randint(368, 568)
                    self.drops.add(item)
            definir_dropar_itens(False)

    def checar_fim_do_turno(self):
        if self.turno == 1:
            for criatura in self.criatura_jogador:
                if criatura.ponto_de_acao == 0:
                    self.turno = -1
                    for criatura_adversaria in self.criatura_adversario:
                        criatura_adversaria.ponto_de_acao = 1
        else:
            for criatura_adversaria in self.criatura_adversario:
                if criatura_adversaria.ponto_de_acao == 0:
                    self.turno = 1
                    for criatura in self.criatura_jogador:
                        criatura.ponto_de_acao = 1

    def checar_vitoria(self):
        from scripts.estado import formacao_adversario
        if len(formacao_adversario) == 0:
            self.turno = 1


class MenuPrincipal(object):

    def __init__(self, tela):
        self.tela = tela
        self.fundo = pygame.sprite.Group()
        self.menus = pygame.sprite.Group()
        self.fundo.add(gerar_cenario('floresta'))
        self.posicionar_menus()

    def update(self, mouse_posicao, mouse_besquerdo, mouse_bdireito):
        # Atualiza os grupos
        self.fundo.update()
        self.menus.update(mouse_posicao, mouse_besquerdo, mouse_bdireito)
        # Desenha os grupos na tela
        self.fundo.draw(self.tela)
        self.menus.draw(self.tela)

    def posicionar_menus(self):
        menu = Menu('Novo jogo')
        menu.x, menu.y = tela_largura//2, tela_altura//2
        self.menus.add(menu)
        menu = Menu('Versão')
        menu.x, menu.y = menu.largura//2, menu.altura//2
        self.menus.add(menu)


class Mapa(object):

    movimento = {'frame': 45, 'distância': 100, 'mover para cima': [0, 1], 'mover para baixo': [0, -1],
                 'mover para esquerda': [1, 0], 'mover para direita': [-1, 0]}
    mover = movimento['distância'] / movimento['frame']

    def __init__(self, tela, inventario):
        self.tela, self.inventario = tela, inventario

        # Inicializa alguns parâmetros de referência
        self.mapa_tamanho = 20

        # Inicializa as camadas, sendo que o número determina a sequência que ela aparecerá
        self.submapas = pygame.sprite.Group()
        self.marcadores = pygame.sprite.Group()
        self.interface = pygame.sprite.Group()

        # Inicializa a tela em geral
        if self.mapa_tamanho > 1:
            for j in range(-self.mapa_tamanho//2, self.mapa_tamanho//2 + 1):
                for i in range(-self.mapa_tamanho // 2, self.mapa_tamanho // 2 + 1):
                    submapa = Submapa('Floresta')
                    submapa.posicao = [i, j]
                    submapa.x = i * submapa.largura
                    submapa.y = j * submapa.altura
                    if submapa.posicao == [0, 0]:
                        submapa.explorar()
                    self.submapas.add(submapa)
        menu = Menu("Inventário")
        menu.x, menu.y = menu.largura//2, tela_altura - menu.altura//2 - 10
        self.interface.add(menu)
        menu = Menu("Crafting")
        menu.x, menu.y = tela_largura//2, tela_altura - menu.altura//2 - 10
        self.interface.add(menu)
        self.marcadores.add(Marcador('Protagonista'))

        # Estados
        self.interacao_permitida = True
        self.frame = 0
        self.animacao = False, ''

    def update(self, mouse_posicao, mouse_besquerdo, mouse_bdireito, lista_inventario, entrada_teclado):
        """Em sequência:\n
        - Compara se a lista de inventário mudou. Se sim, pede para a próxima função reinicializar o inventário;
        - Gerencia os elementos da interface;
        - Gerencia as interações;
        - Atualiza os grupos;
        - Desenha os grupos na tela."""
        from scripts.estado import posicao_jogador
        if lista_inventario != self.inventario:
            self.inventario = lista_inventario
            mostrar_inventario(1)
        gerenciar_inventario(self.interface, mouse_posicao, self.inventario)
        gerenciar_crafting(self.interface)
        self.interacao(mouse_bdireito, entrada_teclado)
        self.submapas.update(posicao_jogador)  # Custará muito poder de processamento em relação ao tamanho do mapa
        self.marcadores.update(posicao_jogador)
        self.interface.update(mouse_posicao, mouse_besquerdo, mouse_bdireito)
        self.submapas.draw(self.tela)  # Custará muito poder de processamento em relação ao tamanho do mapa
        self.marcadores.draw(self.tela)
        self.interface.draw(self.tela)

    def interacao(self, mouse_bdireito, entrada_teclado):
        from scripts.estado import item_selecionado
        if self.interacao_permitida:
            if entrada_teclado[pygame.K_w]:
                self.interacao_permitida = False
                alterar_posicao_jogador(0, -1)
                self.animacao = True, 'mover para cima'
            elif entrada_teclado[pygame.K_s]:
                self.interacao_permitida = False
                alterar_posicao_jogador(0, 1)
                self.animacao = True, 'mover para baixo'
            elif entrada_teclado[pygame.K_a]:
                self.interacao_permitida = False
                alterar_posicao_jogador(-1, 0)
                self.animacao = True, 'mover para esquerda'
            elif entrada_teclado[pygame.K_d]:
                self.interacao_permitida = False
                alterar_posicao_jogador(1, 0)
                self.animacao = True, 'mover para direita'
            elif mouse_bdireito:
                if item_selecionado[0]:
                    for i in self.interface:
                        if i.tipo == "Item":
                            self.interface.remove(i)
                    definir_item_selecionado(False)
                    mostrar_inventario(1)
                    pygame.mouse.set_visible(True)
        elif self.animacao[0]:
            self.animar(self.animacao[1])

    def animar(self, animacao):
        if animacao in self.movimento:
            definir_posicao_blocomestre(x=self.movimento[animacao][0]*self.mover,
                                        y=self.movimento[animacao][1]*self.mover)
            if self.frame == self.movimento['frame']:
                from scripts.encontro import checar_encontro
                lista = checar_encontro()
                if len(lista) > 0:
                    definir_tela(2, 'iniciar')
                self.animacao = False, ''
                self.frame = 0
                self.interacao_permitida = True
        self.frame += 1
