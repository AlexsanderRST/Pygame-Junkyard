# Criado por Alexsander Rosante (03/04/2020)

# Como o funcionamento do jogo acontece pelas interações, esse script fará uma simulação de interação

from scripts.estado import criatura_opcoes


class IA(object):

    def __init__(self):
        pass

    def jogar(self, listadecriaturas):
        from scripts.estado import formacao_adversario
        oponente = formacao_adversario[0]
        if oponente == 'Pedra':
            criatura_opcoes('dormir', -1, 1)
