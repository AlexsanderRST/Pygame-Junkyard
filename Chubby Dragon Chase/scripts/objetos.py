# Criado por Alexsander Rosante (12/03/20)

import pygame
from parametros.gerais import *
from scripts.estado import definir_tela, mostrar_inventario, mostrar_crafting
from parametros import cores
from parametros.textos import infobar


# Menu interativo
class Menu(pygame.sprite.Sprite):

    def __init__(self, tipo):
        pygame.sprite.Sprite.__init__(self)
        self.tipo = tipo
        if self.tipo == 'Novo jogo' or self.tipo == 'Carregar jogo':
            self.largura, self.altura = 240, 80
            self.image = pygame.image.load('imagens/menus/barra_1.png')
        elif self.tipo == 'Versão':
            self.largura, self.altura = 120, 40
            self.image = pygame.image.load('imagens/menus/versao.png')
        elif self.tipo == 'Informação':
            self.largura, self.altura = 80, 80
            self.image = pygame.image.load('imagens/menus/informacao.png')
        elif self.tipo == 'Inventário' or 'Crafting':
            self.largura, self.altura = 80, 160
            if self.tipo == 'Inventário':
                self.image = pygame.image.load('imagens/menus/inventario.png')
            else:
                self.image = pygame.image.load('imagens/menus/crafting.png')
        else:
            self.largura, self.altura = 100, 100
            self.image = pygame.Surface((self.largura, self.altura))
            self.image.fill(cores.preto)

        # Inicializa posição e retângulo
        self.x, self.y = 0, 0
        self.rect = self.image.get_rect()

        # Inicializa alguns estados
        self.interativo = True
        self.clicado = False
        self.clique_anterior = False

    def update(self, mouse_posicao, mouse_besquerdo, mouse_bdireito):
        if self.interativo:
            self.interacao(mouse_posicao, mouse_besquerdo)
        self.rect = self.image.get_rect(centerx=self.x, centery=self.y)

    def interacao(self, mouse_posicao, mouse_besquerdo):
        if self.rect.collidepoint(mouse_posicao):
            # Clicou no menu
            if mouse_besquerdo:
                if self.tipo == 'Novo jogo':
                    self.image = pygame.image.load('imagens/menus/' + idioma + '/novojogo_clicado.png')
                    definir_tela(1, 'iniciar')
                elif self.tipo == 'Informação':
                    if not self.clicado:
                        self.image = pygame.image.load('imagens/menus/informacao_clicado.png')
                        self.clicado = True
                    else:
                        self.image = pygame.image.load('imagens/menus/informacao.png')
                        self.clicado = False
                elif self.tipo == 'Inventário':
                    mostrar_inventario(1)
                elif self.tipo == 'Crafting':
                    mostrar_crafting(1)
            # Cursor sobre menu
            else:
                if self.tipo == 'Novo jogo':
                    self.image = pygame.image.load('imagens/menus/' + idioma + '/novojogo_selecionado.png')
                elif self.tipo == 'Inventário':
                    self.image = pygame.image.load('imagens/menus/inventario_selecionado.png')
        # Nada do anterior
        else:
            if self.tipo == 'Novo jogo':
                self.image = pygame.image.load('imagens/menus/' + idioma + '/novojogo.png')
            elif self.tipo == 'Inventário':
                self.image = pygame.image.load('imagens/menus/inventario.png')


# O objeto abaixo indica o local onde o jogador se encontra na tela mapa;
# Ele não é interativo;
# É animado;
class Marcador(pygame.sprite.Sprite):

    def __init__(self, especie):
        pygame.sprite.Sprite.__init__(self)
        self.tipo = 'Marcador'
        self.image = pygame.image.load('imagens/Marcador/' + especie + '/base.png')
        if especie == 'Protagonista':
            self.especie = especie
            self.frame = 0
            self.posicao = (0, 0)
            self.rect = self.image.get_rect(centerx=tela_largura // 2, centery=tela_altura // 2 - 32)

    def update(self, posicao_jogador):
        if self.especie == 'Protagonista' and self.posicao != posicao_jogador:
            self.posicao = posicao_jogador


# Aparece quando o jogador posiciona o mouse sobre um item ou criatura sobre um determinado tempo;
# Uma barra de informação aparece mostrando o nome, vida, etc;
class Infobar(pygame.sprite.Sprite):

    def __init__(self, tipo, mouse_posicao):
        pygame.sprite.Sprite.__init__(self)
        self.tipo = 'Infobar'
        margem = 5
        tamanho = [0, 0]
        fonte = pygame.font.Font('Fonte/bahnschrift.ttf', 22)
        texto = fonte.render(infobar[idioma][tipo], True, cores.branco)
        tamanho[0] += fonte.size(infobar[idioma][tipo])[0] + margem*2
        tamanho[1] += fonte.size(infobar[idioma][tipo])[1] + margem*2
        self.image = pygame.Surface((tamanho[0], tamanho[1]))
        self.image.blit(texto, texto.get_rect(left=margem, top=margem))
        pygame.draw.rect(self.image, cores.roxo, (0, 0, tamanho[0], tamanho[1]), 1)
        self.rect = self.image.get_rect(left=mouse_posicao[0], top=mouse_posicao[1])


class Cursores(pygame.sprite.Sprite):

    def __init__(self, especie):
        pygame.sprite.Sprite.__init__(self)
        self.tipo = 'Cursor'
        self.especie = especie
        self.image = pygame.image.load('imagens/Cursores/' + self.especie + '.png')
        self.rect = self.image.get_rect()
        self.x, self.y = 0, 0

    def update(self, mouse_posicao):
        pass
