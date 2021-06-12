"""
Criado por Alexsander Rosante (18/03/20);
Regra-mor: Uma variável que pode ser alterada por uma, e somente uma, função local;
Utilidade: Suas variáveis são consultadas e alteradas pelos demais scripts.
"""

from parametros.gerais import *

# Estados relativos à tela
# 0 -> Menu Principal
# 1 -> Mapa
# 2 -> Tela de batalha
telacontexto = [0, '']

criatura_morrer = [False, [-1, -1]]

# Estados relativos ao bloco
bloco_alvejado = [False, [-1, -1], False]  # [Mouse sobre?, Qual posição?, Está ocupado?]
bloco_selecionado = [False, [-1, -1], False]  # [Selecionado?, Qual posição?, Está ocupado?]

# Estados relativos ao ataque
dano = [False, [-1, -1], 0]  # BETA: [estado, posição do alvo, ataque do atacante]

# Estados relativos aos itens
item_alvejado = False, '', (0, 0)
item_selecionado = False, '', (0, 0)

# Lista dos menus
inventario_lista = ['graveto', 'pedra', 'graveto', 'pedra', 'pedra lascada']

# Estado dos menus
# 0: Não mostrar
# 1: Mostrar
# 2: Manter Fechado
# 3: Manter Aberto
inventario_estado = 2
crafting_estado = 2

# Opções de menu
adicionar_item = False, ''
remover_item = False, '', (0, 0)

# Posições para o mapa
posicao_jogador = [0, 0]
posicao_blocomestre = [tela_largura // 2, tela_altura // 2]
posicao_dx, posicao_dy = 0, 0
posicao_jogador_anterior = posicao_jogador

# Dicionário que converte coordenadas de item em index de lista
inventario_posicao = {(1, 1): 0, (1, 2): 1, (1, 3): 2, (1, 4): 3,
                      (2, 1): 4, (2, 2): 5, (2, 3): 6, (2, 4): 7,
                      (3, 1): 8, (3, 2): 9, (3, 3): 10, (3, 4): 11,
                      (4, 1): 12, (4, 2): 13, (4, 3): 14, (4, 4): 15,
                      (5, 1): 16, (5, 2): 17, (5, 3): 18, (5, 4): 19,
                      (6, 1): 20, (6, 2): 21, (6, 3): 22, (6, 4): 23,
                      (7, 1): 24, (7, 2): 25, (7, 3): 26, (7, 4): 27,
                      (8, 1): 28, (8, 2): 29, (8, 3): 30}

# Formação de batalha
formacao_jogador = ['Protagonista']
formacao_adversario = ['Pedra']

# Baseado no sistema de batalha revisado
criatura_comando = {'verdade': False,
                    'jogador': 0,
                    'ação': '',
                    'ponto de ação': 0}

dropar_itens = {'verdade': False,
                'jogador': 0,
                'lista de drops': []}


encontrou_criatura = [False, '', [0, 0]]  # Verdade?, Qual?, Posição?


def update():
    global posicao_jogador, posicao_blocomestre
    pass


def definir_tela(qual, opcao=''):
    global telacontexto
    telacontexto = [qual, opcao]


def definir_bloco_alvejado(estado, posicao=(-1, -1), ocupacao=False):
    global bloco_alvejado
    bloco_alvejado = [estado, posicao, ocupacao]


def definir_bloco_selecionado(estado, posicao=(-1, -1), ocupacao=False):
    global bloco_selecionado
    bloco_selecionado = [estado, posicao, ocupacao]


def aplicar_dano(estado, posicao_alvo=(-1, -1), ataque=0):
    global dano
    dano = [estado, posicao_alvo, ataque]


def definir_morte_criatura(estado, posicao=(-1, -1)):
    global criatura_morrer
    criatura_morrer = [estado, posicao]


# Criaturas - Tá bizarro, muda isso aqui porra
def criatura_opcoes(opcao='', jogador=0, pontodeacao=0):
    global criatura_comando
    criatura_comando['verdade'] = True
    if opcao == 'selecionar':
        criatura_comando['ação'] = opcao
        criatura_comando['ponto de ação'] = pontodeacao
    elif opcao == 'desselecionar':
        criatura_comando['verdade'] = False
    elif opcao == 'atacar':
        criatura_comando['ação'] = opcao
        criatura_comando['ponto de ação'] = pontodeacao
    elif opcao == 'dormir':
        criatura_comando['ação'] = opcao
        criatura_comando['ponto de ação'] = pontodeacao
    elif opcao == 'festejar':
        criatura_comando['ação'] = opcao
        criatura_comando['ponto de ação'] = pontodeacao
    criatura_comando['ação'] = opcao
    criatura_comando['jogador'] = jogador


# Inventário
def inventario_opcoes(opcao='', item='', posicao=(0, 0)):
    global adicionar_item, remover_item, inventario_lista
    if opcao == 'Adicionar':
        inventario_lista.append(item)
    elif opcao == 'Remover':
        del inventario_lista[inventario_posicao[posicao]]
    else:
        adicionar_item = False, item
        remover_item = False, item, posicao


def mostrar_inventario(n):
    global inventario_estado
    inventario_estado = n


# Crafting
def mostrar_crafting(n):
    global crafting_estado
    crafting_estado = n


def definir_item_alvejado(estado, item='', posicao=(0, 0)):
    global item_alvejado
    item_alvejado = estado, item, posicao


def definir_item_selecionado(estado, item='', posicao=(0, 0)):
    global item_selecionado
    item_selecionado = estado, item, posicao


def definir_posicao_blocomestre(x=0, y=0):
    global posicao_blocomestre
    if x != 0:
        posicao_blocomestre[0] = posicao_blocomestre[0] + x
    elif y != 0:
        posicao_blocomestre[1] = posicao_blocomestre[1] + y
    return 0


def alterar_posicao_jogador(x=0, y=0):
    global posicao_jogador
    if x != 0:
        posicao_jogador[0] += x
    elif y != 0:
        posicao_jogador[1] += y
    return 0


def definir_dropar_itens(verdade, jogador=0, lista_de_itens=()):
    global dropar_itens
    dropar_itens = {'verdade': verdade,
                    'jogador': jogador,
                    'lista de itens': lista_de_itens}


def definir_encontro(verdade, qual='', posicao=(0, 0)):
    global encontrou_criatura
    encontrou_criatura = [verdade, qual, posicao]


def definir_formacao(quem, opcao, nova_formacao=()):
    global formacao_jogador, formacao_adversario
    formacao = {'jogador': formacao_jogador, 'adversário': formacao_adversario}
    if opcao == 'definir':
        formacao[quem] = nova_formacao
    elif opcao == 'remover membro' and len(formacao_jogador) > 0:
        del (formacao[quem])[0]
