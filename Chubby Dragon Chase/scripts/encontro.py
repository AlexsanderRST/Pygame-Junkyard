"""
Criado por Alexsander Rosante (30/04/20);
Não é um estado, pois depende de mais de uma função local;
"""

import random

verdade = False, []  # Verdade?, Lista de inimigos

# A soma das possibilidades deve ser 100
possibilidade = {'Floresta': (('Pedra', 50),
                              ('Árvore', 50))}


def checar_encontro(cenario='Floresta'):
    """
    Supondo que o cenário entrado foi floresta
    """
    lista = []
    lista_auxiliar = []
    for i in possibilidade[cenario]:
        lista_auxiliar += i[1] * [i[0]]
    random.shuffle(lista_auxiliar)
    lista.append(lista_auxiliar[0])
    return lista
