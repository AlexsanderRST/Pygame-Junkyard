"""As criaturas são peças que o jogador movimentam durante uma partida; \n
Esses objetos são gerenciados pelo script de telas (tela.py); \n
Criado por Alexsander Rosante (20/04/20)"""

import pygame
from scripts.estado import criatura_opcoes, definir_dropar_itens, definir_formacao

info = {'Protagonista': {'textura': 'imagens/Criatura/Protagonista/base.png',
                         'ancoragem': 60,
                         'vida': 15,
                         'ataque': 10,
                         'defesa': 5,
                         'barra de vida x': 40,
                         'barra de vida y': 32,
                         'estado inicial': 'acordado',
                         'pesado': False},
        'Pedra': {'textura': 'imagens/Criatura/Pedra/base.png',
                  'ancoragem': 86,
                  'vida': 10,
                  'ataque': 3,
                  'defesa': 3,
                  'barra de vida x': 40,
                  'barra de vida y': 76,
                  'estado inicial': 'dormindo',
                  'pesado': True},
        'Árvore': {'textura': 'imagens/Criatura/Árvore/base.png',
                   'ancoragem': 158,
                   'vida': 15,
                   'ataque': 3,
                   'defesa': 3,
                   'barra de vida x': 120,
                   'barra de vida y': 204,
                   'estado inicial': 'dormindo',
                   'pesado': True}}


class Criatura(pygame.sprite.Sprite):

    def __init__(self, especie):
        """Inicializa: \n
        - Posição nos blocos: ;
        - Ancoragem: Diferença entre o centro da imagem da criatura e o ponto onde ela está ancorada;
        - Posição na tela e acréscimos: ;
        - Textura e grupo de máscaras: ;
        - Retângulo:
        - ...
        - Pesada: Criaturas que estão presas ao chão ou são pesadas demais para se moverem
        quando sofrem um ataque;
        - Agressiva: Criaturas que atacam ao iniciar a batalha. A negação são aquelas que
        atacam após uma determinada quantidade de dano ou fogem depois de uma certa quantidade de turnos;

        """
        pygame.sprite.Sprite.__init__(self)
        self.tipo = 'Criatura'
        self.especie = especie
        self.jogador = 0
        self.estado = info[especie]['estado inicial']
        self.posicao = (0, 0)  # Defazado
        self.ancoragem = info[especie]['ancoragem']
        self.x, self.y, self.xi, self.yi = 0, 0, 0, 0
        self.velocidade, self.aceleracao = 0, 0
        self.image = pygame.image.load(info[especie]['textura'])
        self.mascaras = pygame.sprite.Group()
        self.rect = self.image.get_rect()
        self.ponto_de_acao = 1
        self.frame = 0
        self.vida = info[especie]['vida']
        self.ataque = info[especie]['ataque']
        self.defesa = info[especie]['defesa']
        self.propriedades = {'pesado': info[especie]['pesado'],
                             'agressiva': False,
                             'racional': True}
        self.inimigo = {}
        self.drops = ['graveto', 'pedra']  # Temporário

        # Aqui mudarei
        if especie == 'Pedra':
            self.mascaras.add(Mascara('olhos', especie, self.rect[2], self.rect[3], self.estado))
            self.mascaras.add(Mascara('palpebras', especie, self.rect[2], self.rect[3], self.estado))
        self.mascaras.add(Mascara('corpo', especie, self.rect[2], self.rect[3], self.estado))
        self.mascaras.add(Mascara('barra de vida', especie, vida=self.vida))

    def update(self, mouse_posicao, mouse_besquerdo, grupo_jogador, grupo_adversario):
        self.interacao(mouse_posicao, mouse_besquerdo, grupo_jogador, grupo_adversario)
        self.image = pygame.image.load(info[self.especie]['textura'])
        self.rect = self.image.get_rect(centerx=self.x, centery=self.y)
        self.mascaras.update(vida=self.vida, ponto_acao=self.ponto_de_acao, estado_criatura=self.estado)
        self.mascaras.draw(self.image)

    def interacao(self, mouse_posicao, mouse_besquerdo, grupo_jogador, grupo_adversario):
        from scripts.estado import criatura_comando

        # Checa se a vida da criatura é zero ou menos e a mata
        if self.vida <= 0:
            if self.estado != 'morrendo':
                self.estado = 'morrendo'
                self.frame = 0
            else:
                self.animar(self.estado)
                if self.frame > 50:  # Esconder criatura
                    if self.jogador > 0:
                        pass
                    else:
                        self.mascaras.empty()
                if self.frame > 90:
                    for criatura in grupo_adversario:
                        grupo_adversario.remove(criatura)
                    definir_formacao('adversário', 'remover membro')
                    criatura_opcoes('festejar', self.jogador*(-1))

        # Nenhum comando dado
        elif not criatura_comando['verdade']:
            if self.rect.collidepoint(mouse_posicao):
                if mouse_besquerdo:
                    criatura_opcoes('selecionar', self.jogador, self.ponto_de_acao)
                else:
                    self.animar('flutuando')
            else:
                self.animar('parado')
        else:  # Comando dado
            if criatura_comando['jogador'] == self.jogador:  # Foi para essa criatura
                if criatura_comando['ação'] == 'selecionar':  # Selecionada
                    self.animar('flutuando')
                    if self.rect.collidepoint(mouse_posicao):  # Mouse sobre
                        if mouse_besquerdo:  # Clicou sobre
                            criatura_opcoes('dormir', self.jogador)
                elif criatura_comando['ação'] == 'atacar':  # Para atacar
                    if not self.estado == 'atacando':
                        self.animar('parado')
                        self.estado = 'atacando'
                    else:
                        pygame.mouse.set_visible(False)
                        self.animar('atacar')
                        if self.frame == 30:
                            for criatura in grupo_adversario:  # Aproveita aqui para coletar algumas infos
                                if self.ataque > criatura.defesa:
                                    criatura.vida -= self.ataque - criatura.defesa
                                self.inimigo['pesado'] = criatura.propriedades['pesado']
                        if self.frame > 90:
                            pygame.mouse.set_visible(True)
                            criatura_opcoes('desselecionar')
                            self.ponto_de_acao -= 1
                            self.estado = ''
                elif criatura_comando['ação'] == 'dormir':  # Para não fazer nada
                    if not self.estado == 'dormindo':
                        self.animar('parado')
                        self.estado = 'dormindo'
                        self.ponto_de_acao -= 1
                        criatura_opcoes('desselecionar')
                elif criatura_comando['ação'] == 'festejar':
                    if not self.estado == 'festejando':
                        self.animar('parado')
                        self.estado = 'festejando'
                    else:
                        pass
            else:  # Não foi para essa criatura
                if criatura_comando['ação'] == 'selecionar':
                    if self.rect.collidepoint(mouse_posicao):
                        if mouse_besquerdo:
                            if self.jogador < 0:
                                criatura_opcoes('atacar', self.jogador*(-1))
                elif criatura_comando['ação'] == 'atacar':
                    if not self.estado == 'sofrendo ataque':
                        self.animar('parado')
                        self.estado = 'sofrendo ataque'
                    else:
                        if not self.propriedades['pesado']:
                            self.animar('sofrer ataque')
                        if self.frame > 120:
                            self.estado = ''

    def animar(self, animacao):
        if animacao == 'parado':
            self.frame = 0
        elif animacao == 'flutuando':
            self.y = self.yi + (-(self.frame - 30)**2)/180
            self.frame += 1
            if self.frame == 60:
                self.frame = 0
        elif animacao == 'atacar':
            if self.frame == 0:
                objetivo, tempo = 240, 30
                self.aceleracao = (2 * (self.yi - objetivo))/tempo**2
            if 0 <= self.frame <= 30:
                self.y = self.yi - (self.aceleracao * self.frame**2)/2
            if self.frame == 30:
                self.yi = self.y
                self.velocidade = (self.aceleracao * self.frame)
                objetivo, tempo = 332, 10
                self.aceleracao = (2 * (self.yi + self.velocidade * tempo - objetivo))/tempo**2
            if 30 <= self.frame <= 40:
                if self.inimigo['pesado']:
                    self.y = self.yi + (self.aceleracao * (self.frame - 30) ** 2) / 2
            if self.frame == 40:
                self.yi = self.y
                self.velocidade = 0
            if 50 <= self.frame <= 90:
                self.y = self.yi + 4.2 * (self.frame - 50)
            if self.frame == 90:
                self.yi = self.y
            self.frame += 1
        elif animacao == 'sofrer ataque':
            pass
        elif animacao == 'morrendo':
            if self.frame == 35:
                self.mascaras.add(Mascara('morte', self.especie, self.rect[2], self.rect[3], self.estado))
            elif self.frame == 40:
                definir_dropar_itens(True, self.jogador, self.drops)
            self.frame += 1
        elif animacao == 'festejar':
            pass


class Mascara(pygame.sprite.Sprite):

    def __init__(self, tipo,
                 criatura_tipo, criatura_largura=0, criatura_altura=0, criatura_estado='',
                 vida=None):
        pygame.sprite.Sprite.__init__(self)
        self.tipo = tipo
        self.frame = 0
        self.criatura = criatura_tipo
        self.criatura_largura, self.criatura_altura = criatura_largura, criatura_altura
        self.subestado = criatura_estado
        self.image = pygame.Surface((100, 100))
        self.x, self.y = self.criatura_largura//2, self.criatura_altura//2
        self.xi, self.yi = self.x, self.y
        if tipo == 'barra de vida':
            self.imagens = {100: pygame.image.load('imagens/Batalha/Criatura/Mascara/barradevida/100.png'),
                            90: pygame.image.load('imagens/Batalha/Criatura/Mascara/barradevida/90.png'),
                            80: pygame.image.load('imagens/Batalha/Criatura/Mascara/barradevida/80.png'),
                            70: pygame.image.load('imagens/Batalha/Criatura/Mascara/barradevida/70.png'),
                            60: pygame.image.load('imagens/Batalha/Criatura/Mascara/barradevida/60.png'),
                            50: pygame.image.load('imagens/Batalha/Criatura/Mascara/barradevida/50.png'),
                            40: pygame.image.load('imagens/Batalha/Criatura/Mascara/barradevida/40.png'),
                            30: pygame.image.load('imagens/Batalha/Criatura/Mascara/barradevida/30.png'),
                            20: pygame.image.load('imagens/Batalha/Criatura/Mascara/barradevida/20.png'),
                            10: pygame.image.load('imagens/Batalha/Criatura/Mascara/barradevida/10.png')}
            self.vida = vida
            self.x, self.y = info[self.criatura]['barra de vida x'], info[self.criatura]['barra de vida y']
        elif tipo in ['corpo', 'olhos', 'morte']:
            self.image = pygame.image.load('imagens/Criatura/' + self.criatura + '/' + tipo + '.png')
        elif tipo == 'palpebras':
            self.image = pygame.image.load('imagens/Criatura/' + self.criatura + '/palpebras.png')
            self.y -= 7
        self.rect = self.image.get_rect()

    def update(self, vida=None, ponto_acao=None, estado_criatura=''):
        self.mudar_de_estado(estado_criatura)
        if self.tipo == 'barra de vida':
            self.barra_vida(vida)
        if self.criatura == 'Pedra' or 'Protagonista' and self.tipo in ['corpo', 'palpebras', 'olhos']:
            self.animar(self.subestado)

        self.rect = self.image.get_rect(centerx=self.x, centery=self.y)

    def barra_vida(self, vida):
        if vida > 0:
            self.image = self.imagens[round(vida/self.vida, 1) * 100]

    def animar(self, animacao):
        # Animação do personagem acordado
        if animacao == 'acordado':
            if self.criatura == 'Protagonista' and self.tipo == 'corpo':
                if self.frame > 120:
                    self.yi = self.y
                    self.frame = 0
                    return 0
                if 0 <= self.frame <= 30:
                    self.y = self.yi - 2/30*self.frame
                if self.frame == 30:
                    self.yi = self.y
                if 30 <= self.frame <= 120:
                    self.y = self.yi + 2/90 * (self.frame - 30)
                self.frame += 1
        # Animação do personagem dormindo
        elif animacao == 'dormindo':
            if self.criatura == 'Pedra' and self.tipo in ['corpo', 'palpebras', 'olhos']:
                if self.frame > 120:
                    self.yi = self.y
                    self.frame = 0
                    return 0
                if 0 <= self.frame <= 30:
                    self.y = self.yi - 4/30*self.frame
                if self.frame == 30:
                    self.yi = self.y
                if 30 <= self.frame <= 120:
                    self.y = self.yi + 4/90 * (self.frame - 30)
                self.frame += 1
        # Animação do personagem acordando
        elif animacao == 'acordar':
            if self.criatura == 'Pedra' and self.tipo in ['corpo', 'palpebras', 'olhos']:
                if self.frame > 60:
                    self.subestado = 'acordado'
                    self.yi = self.y
                    self.frame = 0
                    return 0
                if self.tipo in ['corpo', 'olhos']:
                    if 30 <= self.frame <= 45:
                        self.y = self.yi - 36/15*(self.frame - 30)
                    if self.frame == 45:
                        self.yi = self.y
                    if 45 <= self.frame <= 60:
                        self.y = self.yi + 38/15*(self.frame - 45)
                else:
                    if self.frame == 30:
                        self.y += 7
                self.frame += 1
        # Animação do personagem morrendo
        elif animacao == 'morrendo':
            if self.criatura == 'Pedra' and self.tipo in ['corpo', 'palpebras', 'olhos']:
                if self.frame == 0 and self.tipo == 'palpebras':
                    self.yi -= 5.05
                if 0 <= self.frame <= 25:
                    self.y = self.yi - 36/25*self.frame
                self.frame += 1

    def mudar_de_estado(self, estado_atual):
        """Compara o estado atual da criatura e o estado das máscaras (subestado)"""
        if estado_atual == 'sofrendo ataque' and self.subestado == 'dormindo':
            if self.frame == 30:
                self.y = self.criatura_altura // 2
                self.subestado = 'acordar'
                return 0
            self.frame += 1
        elif estado_atual == 'morrendo' and self.subestado != 'morrendo':
            self.subestado = 'morrendo'


def gerenciar_criaturas(mouse_bdireito):
    from scripts.estado import criatura_comando
    # Criatura selecionada
    if criatura_comando['verdade']:
        # Clicou com o direito, desselecionou a criatura
        if mouse_bdireito:
            criatura_opcoes('desselecionar')
