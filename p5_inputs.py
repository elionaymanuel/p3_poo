import random
import os
import pygame

# Cores usadas para desenhar o jogo.
PRETO = (0, 0, 0)
VERDE = (0, 255, 0)
BRANCO = (255, 255, 255)

# Configurações da janela e dos objetos.
LARGURA_JANELA = 400
ALTURA_JANELA = 500
VELOCIDADE_JOGADOR = 6
INTERVALO_BLOCOS = 30
TAMANHO_BLOCO = 20


class Jogador:
    """Representa o jogador controlado pelo teclado."""

    def __init__(self):
        self.retangulo = pygame.Rect(300, 100, 50, 50)
        self.cor = VERDE
        self.velocidade = VELOCIDADE_JOGADOR
        self.teclas_pressionadas = set()

    def atualizar_tecla(self, tecla, pressionada):
        """Registra quais teclas de movimento estão pressionadas."""
        teclas_movimento = (
            pygame.K_LEFT, pygame.K_a,
            pygame.K_RIGHT, pygame.K_d,
            pygame.K_UP, pygame.K_w,
            pygame.K_DOWN, pygame.K_s,
        )

        if tecla not in teclas_movimento:
            return

        if pressionada:
            self.teclas_pressionadas.add(tecla)
        else:
            self.teclas_pressionadas.discard(tecla)

    def mover(self):
        """Move o jogador e mantém o retângulo dentro da janela."""
        esquerda = pygame.K_LEFT in self.teclas_pressionadas or pygame.K_a in self.teclas_pressionadas
        direita = pygame.K_RIGHT in self.teclas_pressionadas or pygame.K_d in self.teclas_pressionadas
        cima = pygame.K_UP in self.teclas_pressionadas or pygame.K_w in self.teclas_pressionadas
        baixo = pygame.K_DOWN in self.teclas_pressionadas or pygame.K_s in self.teclas_pressionadas

        if esquerda:
            self.retangulo.x -= self.velocidade
        if direita:
            self.retangulo.x += self.velocidade
        if cima:
            self.retangulo.y -= self.velocidade
        if baixo:
            self.retangulo.y += self.velocidade

        self.retangulo.clamp_ip(
            pygame.Rect(0, 0, LARGURA_JANELA, ALTURA_JANELA)
        )

    def desenhar(self, janela):
        pygame.draw.rect(janela, self.cor, self.retangulo)


class Bloco:
    """Representa um bloco branco que cai pela janela."""

    def __init__(self, x, y, velocidade):
        self.retangulo = pygame.Rect(x, y, TAMANHO_BLOCO, TAMANHO_BLOCO)
        self.cor = BRANCO
        self.velocidade = velocidade

    def mover(self):
        self.retangulo.y += self.velocidade

    def desenhar(self, janela):
        pygame.draw.rect(janela, self.cor, self.retangulo)


class Jogo:
    """Controla a janela, os eventos e o ciclo principal do jogo."""

    def __init__(self):
        pygame.init()
        self.janela = pygame.display.set_mode(
            (LARGURA_JANELA, ALTURA_JANELA)
        )
        pygame.display.set_caption('Teclado e Mouse')
        self.relogio = pygame.time.Clock()
        self.jogador = Jogador()
        self.blocos = []
        self.contador = 0
        self.deve_continuar = True

    def processar_eventos(self):
        """Lê os eventos de janela, teclado e mouse."""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.deve_continuar = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.deve_continuar = False
                self.jogador.atualizar_tecla(evento.key, True)
            elif evento.type == pygame.KEYUP:
                self.jogador.atualizar_tecla(evento.key, False)
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = evento.pos
                self.blocos.append(Bloco(x, y, 1))

    def criar_bloco_automatico(self):
        """Cria um bloco no topo a cada intervalo definido."""
        self.contador += 1
        if self.contador >= INTERVALO_BLOCOS:
            self.contador = 0
            x = random.randint(0, LARGURA_JANELA - TAMANHO_BLOCO)
            y = -TAMANHO_BLOCO
            velocidade = random.randint(1, VELOCIDADE_JOGADOR + 3)
            self.blocos.append(Bloco(x, y, velocidade))

    def atualizar_e_desenhar(self):
        """Atualiza posições e desenha os objetos do quadro atual."""
        self.janela.fill(PRETO)
        self.jogador.mover()
        self.jogador.desenhar(self.janela)

        for bloco in self.blocos[:]:
            bloco.mover()

            colidiu_com_jogador = self.jogador.retangulo.colliderect(
                bloco.retangulo
            )
            saiu_da_janela = bloco.retangulo.top > ALTURA_JANELA

            if colidiu_com_jogador or saiu_da_janela:
                self.blocos.remove(bloco)
            else:
                bloco.desenhar(self.janela)

        pygame.display.update()

    def executar(self):
        """Executa o jogo até a janela ser fechada ou Esc ser pressionado."""
        while self.deve_continuar:
            self.processar_eventos()
            self.criar_bloco_automatico()
            self.atualizar_e_desenhar()
            self.relogio.tick(40)

        #pygame.quit()
        os._exit(0)


if __name__ == '__main__':
    # Este bloco evita iniciar o jogo quando o arquivo é importado por outro.
    Jogo().executar()
