# Criado por Alexsander Rosante

# Funcionamento:
# Passo 1: O tipo de solo de terra (dirt) é definido pelo gerador;
# Passo 2: É difinida a porporção de pixeis de terra:
# 90% de terra e 10% de pedra no usual;
# 50% de terra e 50% de outro em transição;

import random
from Sistema.cores import marrom1, marrom2, marrom3, cinza1


def terra_marrom(bloco_largura, bloco_altura):
    matriz = []
    lista_probabilidade = probabilizador([marrom1, marrom2, marrom3, cinza1], [34, 32, 32, 2])
    for i in range(bloco_altura):
        linha = []
        for j in range(bloco_largura):
            linha.append(random.choice(lista_probabilidade))
        matriz.append(linha)
    return matriz


def probabilizador(lista_de_objetos, lista_de_probabilidade):
    lista = []
    for i in range(len(lista_de_objetos)):
        lista += lista_de_probabilidade[i] * [lista_de_objetos[i]]
    return lista
