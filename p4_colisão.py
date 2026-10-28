import pygame
import os

# Cores usadas para desenhar o fundo, os blocos e a bola.
PRETO = (0, 0, 0)
AMARELO = (255, 255, 0)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
BRANCO = (255, 255, 255)

# Tamanho da área em que as figuras se movimentam.
LARGURA_JANELA = 500
ALTURA_JANELA = 400


class Figura:
    # Classe base com os dados e comportamentos comuns das figuras.
    def __init__(self, retangulo, cor, velocidade):
        self.retangulo = retangulo
        self.cor = cor
        self.velocidade = velocidade

    def mover(self):
        # Inverte a velocidade ao alcançar as bordas da janela.
        if self.retangulo.top < 0 or self.retangulo.bottom > ALTURA_JANELA:
            self.velocidade[1] = -self.velocidade[1]

        if self.retangulo.left < 0 or self.retangulo.right > LARGURA_JANELA:
            self.velocidade[0] = -self.velocidade[0]

        # Atualiza a posição usando a velocidade horizontal e vertical.
        self.retangulo.x += self.velocidade[0]
        self.retangulo.y += self.velocidade[1]


class Bloco(Figura):
    def desenhar(self, janela):
        # Desenha o bloco como um retângulo.
        pygame.draw.rect(janela, self.cor, self.retangulo)


class Bola(Figura):
    def verificar_colisao(self, bloco):
        # Quando toca um bloco, a bola passa a ter a cor dele.
        if self.retangulo.colliderect(bloco.retangulo):
            self.cor = bloco.cor

    def desenhar(self, janela):
        # Desenha a bola como uma elipse.
        pygame.draw.ellipse(janela, self.cor, self.retangulo)


class Jogo:
    def __init__(self):
        # Inicializa o Pygame e configura a janela e o relógio do jogo.
        pygame.init()
        self.relogio = pygame.time.Clock()
        self.janela = pygame.display.set_mode(
            (LARGURA_JANELA, ALTURA_JANELA)
        )
        pygame.display.set_caption('Colisão')

        # Cria os blocos com suas posições, cores e velocidades.
        self.blocos = [
            Bloco(pygame.Rect(375, 80, 40, 40), VERMELHO, [0, 2]),
            Bloco(pygame.Rect(175, 200, 40, 40), VERDE, [0, -3]),
            Bloco(pygame.Rect(275, 150, 40, 40), AMARELO, [0, -1]),
            Bloco(pygame.Rect(75, 150, 40, 40), AZUL, [0, 4]),
        ]
        # Cria a bola branca, que se movimenta na diagonal.
        self.bola = Bola(pygame.Rect(270, 330, 30, 30), BRANCO, [3, 3])

    def executar(self):
        deve_continuar = True

        # Repete o jogo até que a janela seja fechada.
        while deve_continuar:
            # Verifica se o usuário pediu para fechar a janela.
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    deve_continuar = False

            # Apaga o quadro anterior e desenha os objetos em suas novas posições.
            self.janela.fill(PRETO)

            for bloco in self.blocos:
                bloco.mover()
                bloco.desenhar(self.janela)
                self.bola.verificar_colisao(bloco)

            self.bola.mover()
            self.bola.desenhar(self.janela)

            # Atualiza a tela e limita a execução a 40 quadros por segundo.
            pygame.display.update()
            self.relogio.tick(40)

       #pygame.quit()
        # Encerra o processo imediatamente ao sair do loop.
        os._exit(0)


if __name__ == '__main__':
    # Cria o jogo e inicia sua execução.
    Jogo().executar()
