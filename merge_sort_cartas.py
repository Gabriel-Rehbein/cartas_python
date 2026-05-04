import pygame
import sys
import time
import random

pygame.init()

LARGURA, ALTURA = 1360, 760
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Merge Sort Animado com Cartas - Versão 3")
clock = pygame.time.Clock()

FUNDO = (14, 18, 30)
PAINEL = (27, 34, 54)
PAINEL_CLARO = (42, 52, 80)
BRANCO = (245, 247, 255)
PRETO = (18, 18, 24)
CINZA = (155, 165, 185)
AZUL = (72, 139, 255)
VERDE = (61, 205, 128)
VERMELHO = (235, 82, 82)
AMARELO = (255, 214, 80)
ROXO = (155, 105, 255)
LARANJA = (255, 150, 70)

FONTE = pygame.font.SysFont("consolas", 16)
FONTE_MEDIA = pygame.font.SysFont("consolas", 20, bold=True)
FONTE_GRANDE = pygame.font.SysFont("consolas", 34, bold=True)

CODIGO = [
    "def merge_sort(lista):",
    "    if len(lista) <= 1:",
    "        return lista",
    "    meio = len(lista) // 2",
    "    esquerda = lista[:meio]",
    "    direita = lista[meio:]",
    "    esquerda = merge_sort(esquerda)",
    "    direita = merge_sort(direita)",
    "    return merge(esquerda, direita)",
    "",
    "def merge(esquerda, direita):",
    "    resultado = []",
    "    i = j = 0",
    "    while i < len(esquerda) and j < len(direita):",
    "        if esquerda[i] < direita[j]:",
    "            resultado.append(esquerda[i])",
    "            i += 1",
    "        else:",
    "            resultado.append(direita[j])",
    "            j += 1",
    "    resultado += esquerda[i:]",
    "    resultado += direita[j:]",
    "    return resultado",
]

passos = []
historico = []
lista_inicial_global = []


class Botao:
    def __init__(self, x, y, largura, altura, texto, cor):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.texto = texto
        self.cor = cor

    def desenhar(self):
        mouse = pygame.mouse.get_pos()
        cor = self.cor

        if self.rect.collidepoint(mouse):
            cor = tuple(min(c + 25, 255) for c in self.cor)

        pygame.draw.rect(TELA, cor, self.rect, border_radius=12)
        pygame.draw.rect(TELA, BRANCO, self.rect, 2, border_radius=12)

        texto = FONTE_MEDIA.render(self.texto, True, BRANCO)
        rect = texto.get_rect(center=self.rect.center)
        TELA.blit(texto, rect)

    def clicado(self, evento):
        return evento.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(evento.pos)


def registrar(linha, lista, texto, tipo="passo", comparando=None, ordenadas=None, finalizado=False):
    passos.append({
        "linha": linha,
        "lista": lista[:],
        "texto": texto,
        "tipo": tipo,
        "comparando": comparando or [],
        "ordenadas": ordenadas or [],
        "finalizado": finalizado
    })

    historico.append({
        "tipo": tipo,
        "texto": texto,
        "lista": lista[:]
    })


def merge_sort_visual(lista, nivel=0):
    registrar(0, lista, f"Nível {nivel}: merge_sort recebe {lista}", "recebe")

    registrar(1, lista, f"Nível {nivel}: verifica se a lista tem 0 ou 1 elemento", "verifica")

    if len(lista) <= 1:
        registrar(2, lista, f"Nível {nivel}: retorna {lista}, pois já está ordenada", "retorna")
        return lista

    registrar(3, lista, f"Nível {nivel}: calcula o meio da lista", "meio")
    meio = len(lista) // 2

    esquerda = lista[:meio]
    registrar(4, esquerda, f"Nível {nivel}: divide esquerda {esquerda}", "divide")

    direita = lista[meio:]
    registrar(5, direita, f"Nível {nivel}: divide direita {direita}", "divide")

    registrar(6, esquerda, f"Nível {nivel}: ordena a esquerda {esquerda}", "recursao")
    esquerda = merge_sort_visual(esquerda, nivel + 1)

    registrar(7, direita, f"Nível {nivel}: ordena a direita {direita}", "recursao")
    direita = merge_sort_visual(direita, nivel + 1)

    registrar(8, esquerda + direita, f"Nível {nivel}: junta esquerda {esquerda} com direita {direita}", "junta")
    return merge_visual(esquerda, direita, nivel)


def merge_visual(esquerda, direita, nivel):
    registrar(10, esquerda + direita, f"Nível {nivel}: inicia merge", "merge")

    resultado = []
    registrar(11, esquerda + direita, f"Nível {nivel}: cria resultado vazio", "resultado")

    i = j = 0
    registrar(12, esquerda + direita, f"Nível {nivel}: inicia i = 0 e j = 0", "indices")

    while i < len(esquerda) and j < len(direita):
        registrar(
            13,
            resultado + esquerda[i:] + direita[j:],
            f"Compara {esquerda[i]} com {direita[j]}",
            "compara",
            comparando=[esquerda[i], direita[j]],
            ordenadas=resultado
        )

        if esquerda[i] < direita[j]:
            registrar(14, resultado + esquerda[i:] + direita[j:], f"{esquerda[i]} é menor", "decisao")
            resultado.append(esquerda[i])
            registrar(15, resultado + esquerda[i + 1:] + direita[j:], f"Adiciona {resultado[-1]} ao resultado", "adiciona", ordenadas=resultado)
            i += 1
            registrar(16, resultado + esquerda[i:] + direita[j:], "Avança índice da esquerda", "indice")
        else:
            registrar(17, resultado + esquerda[i:] + direita[j:], f"{direita[j]} é menor ou igual", "decisao")
            resultado.append(direita[j])
            registrar(18, resultado + esquerda[i:] + direita[j + 1:], f"Adiciona {resultado[-1]} ao resultado", "adiciona", ordenadas=resultado)
            j += 1
            registrar(19, resultado + esquerda[i:] + direita[j:], "Avança índice da direita", "indice")

    registrar(20, resultado + esquerda[i:] + direita[j:], "Adiciona restante da esquerda", "restante")
    resultado += esquerda[i:]

    registrar(21, resultado + direita[j:], "Adiciona restante da direita", "restante")
    resultado += direita[j:]

    registrar(22, resultado, f"Retorna {resultado}", "retorna", ordenadas=resultado)
    return resultado


def gerar_nova_lista():
    return random.sample(range(1, 10), 8)


def gerar_passos(lista):
    global passos, historico, lista_inicial_global
    passos = []
    historico = []
    lista_inicial_global = lista[:]

    resultado = merge_sort_visual(lista)
    registrar(22, resultado, f"Lista final ordenada: {resultado}", "final", ordenadas=resultado, finalizado=True)


def painel(x, y, w, h, titulo):
    pygame.draw.rect(TELA, PAINEL, (x, y, w, h), border_radius=16)
    pygame.draw.rect(TELA, PAINEL_CLARO, (x, y, w, h), 2, border_radius=16)

    texto = FONTE_MEDIA.render(titulo, True, BRANCO)
    TELA.blit(texto, (x + 18, y + 14))


def desenhar_codigo(linha_ativa):
    painel(20, 20, 520, 570, "Código")

    y = 65
    for i, linha in enumerate(CODIGO):
        if i == linha_ativa:
            pygame.draw.rect(TELA, AMARELO, (38, y - 3, 485, 23), border_radius=7)
            cor = PRETO
        else:
            cor = BRANCO

        numero = FONTE.render(str(i + 1).rjust(2), True, VERMELHO if i == linha_ativa else CINZA)
        texto = FONTE.render(linha, True, cor)

        TELA.blit(numero, (42, y))
        TELA.blit(texto, (78, y))
        y += 22


def desenhar_carta(x, y, valor, cor, w=58, h=82, destaque=False):
    if destaque:
        y -= 10

    sombra = pygame.Rect(x + 5, y + 6, w, h)
    pygame.draw.rect(TELA, (6, 8, 16), sombra, border_radius=12)

    rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(TELA, cor, rect, border_radius=12)
    pygame.draw.rect(TELA, BRANCO, rect, 2, border_radius=12)

    texto = FONTE_MEDIA.render(str(valor), True, PRETO)
    texto_rect = texto.get_rect(center=rect.center)
    TELA.blit(texto, texto_rect)


def desenhar_linha_cartas(lista, x, y, titulo, cor=BRANCO):
    texto = FONTE.render(titulo, True, CINZA)
    TELA.blit(texto, (x, y - 24))

    for i, valor in enumerate(lista):
        desenhar_carta(x + i * 48, y, valor, cor, 42, 58)


def desenhar_animacao_atual(passo):
    painel(560, 20, 780, 280, "Animação atual")

    lista = passo["lista"]
    comparando = passo["comparando"]
    ordenadas = passo["ordenadas"]
    finalizado = passo["finalizado"]

    x = 600
    y = 150

    for i, valor in enumerate(lista):
        cor = BRANCO
        destaque = False

        if valor in comparando:
            cor = VERMELHO
            destaque = True

        if valor in ordenadas:
            cor = VERDE

        if finalizado:
            cor = VERDE
            destaque = True

        desenhar_carta(x + i * 78, y, valor, cor, 64, 92, destaque)


def desenhar_comparacao_inicial_final(passo):
    painel(560, 320, 780, 140, "Comparação geral")

    desenhar_linha_cartas(lista_inicial_global, 590, 375, "Como começou:", BRANCO)

    resultado_atual = passo["lista"]
    cor_resultado = VERDE if passo["finalizado"] else AZUL
    desenhar_linha_cartas(resultado_atual, 940, 375, "Estado atual / final:", cor_resultado)


def desenhar_historico(indice):
    painel(560, 480, 780, 170, "Histórico dos passos anteriores")

    inicio = max(0, indice - 5)
    ultimos = historico[inicio:indice + 1]

    y = 525
    for item in ultimos:
        tipo = item["tipo"]

        if tipo in ["divide", "recursao"]:
            cor = AZUL
        elif tipo in ["compara", "decisao"]:
            cor = VERMELHO
        elif tipo in ["adiciona", "retorna", "final"]:
            cor = VERDE
        elif tipo in ["junta", "merge"]:
            cor = ROXO
        else:
            cor = CINZA

        pygame.draw.circle(TELA, cor, (585, y + 8), 6)

        texto = item["texto"]
        if len(texto) > 85:
            texto = texto[:85] + "..."

        render = FONTE.render(texto, True, BRANCO)
        TELA.blit(render, (605, y))
        y += 24


def desenhar_mensagem(texto):
    pygame.draw.rect(TELA, PAINEL_CLARO, (20, 605, 520, 80), border_radius=14)

    titulo = FONTE_MEDIA.render("Explicação", True, BRANCO)
    TELA.blit(titulo, (40, 620))

    if len(texto) > 62:
        texto = texto[:62] + "..."

    render = FONTE.render(texto, True, BRANCO)
    TELA.blit(render, (40, 655))


def barra_progresso(indice):
    x, y, w, h = 20, 700, 520, 24

    pygame.draw.rect(TELA, PAINEL_CLARO, (x, y, w, h), border_radius=12)

    progresso = (indice + 1) / len(passos)
    pygame.draw.rect(TELA, VERDE, (x, y, int(w * progresso), h), border_radius=12)

    texto = FONTE.render(f"{int(progresso * 100)}%", True, BRANCO)
    TELA.blit(texto, (x + 235, y + 3))


def desenhar_panorama_final():
    painel(560, 20, 780, 630, "Panorama final do Merge Sort")

    titulo1 = FONTE_MEDIA.render("Lista inicial", True, BRANCO)
    TELA.blit(titulo1, (600, 80))
    desenhar_linha_cartas(lista_inicial_global, 600, 125, "", BRANCO)

    resultado = passos[-1]["lista"]

    titulo2 = FONTE_MEDIA.render("Lista final ordenada", True, BRANCO)
    TELA.blit(titulo2, (600, 230))
    desenhar_linha_cartas(resultado, 600, 275, "", VERDE)

    titulo3 = FONTE_MEDIA.render("Resumo do processo", True, BRANCO)
    TELA.blit(titulo3, (600, 385))

    resumos = [
        "1. A lista foi dividida em partes menores.",
        "2. Cada parte foi quebrada até sobrar 1 carta.",
        "3. Depois, as cartas foram comparadas duas a duas.",
        "4. As menores cartas foram voltando primeiro.",
        "5. No final, todas as partes foram juntadas em ordem."
    ]

    y = 430
    for texto in resumos:
        render = FONTE.render(texto, True, BRANCO)
        TELA.blit(render, (620, y))
        y += 32


def tela_inicio():
    iniciar = Botao(530, 400, 300, 55, "Iniciar Visualização", AZUL)
    nova = Botao(530, 470, 300, 55, "Nova Lista", ROXO)

    lista = gerar_nova_lista()

    while True:
        TELA.fill(FUNDO)

        titulo = FONTE_GRANDE.render("Merge Sort Animado com Cartas", True, BRANCO)
        subtitulo = FONTE_MEDIA.render("Código linha por linha + animação + histórico visual", True, CINZA)

        TELA.blit(titulo, titulo.get_rect(center=(LARGURA // 2, 190)))
        TELA.blit(subtitulo, subtitulo.get_rect(center=(LARGURA // 2, 245)))

        texto_lista = FONTE_MEDIA.render(f"Lista atual: {lista}", True, AMARELO)
        TELA.blit(texto_lista, texto_lista.get_rect(center=(LARGURA // 2, 330)))

        iniciar.desenhar()
        nova.desenhar()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if iniciar.clicado(evento):
                return lista

            if nova.clicado(evento):
                lista = gerar_nova_lista()

        pygame.display.update()
        clock.tick(60)


def main():
    lista = tela_inicio()
    gerar_passos(lista)

    indice = 0
    rodando = False
    velocidade = 1.0
    ultimo = time.time()

    play = Botao(560, 675, 105, 45, "Play", VERDE)
    pause = Botao(675, 675, 105, 45, "Pause", VERMELHO)
    next_btn = Botao(790, 675, 130, 45, "Próximo", AZUL)
    reset = Botao(930, 675, 130, 45, "Reiniciar", ROXO)
    nova_lista = Botao(1070, 675, 130, 45, "Nova Lista", LARANJA)
    menos = Botao(1210, 675, 45, 45, "-", PAINEL_CLARO)
    mais = Botao(1265, 675, 45, 45, "+", PAINEL_CLARO)

    while True:
        agora = time.time()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if play.clicado(evento):
                rodando = True

            if pause.clicado(evento):
                rodando = False

            if next_btn.clicado(evento):
                rodando = False
                if indice < len(passos) - 1:
                    indice += 1

            if reset.clicado(evento):
                indice = 0
                rodando = False

            if nova_lista.clicado(evento):
                lista = gerar_nova_lista()
                gerar_passos(lista)
                indice = 0
                rodando = False

            if menos.clicado(evento):
                velocidade = min(3.0, velocidade + 0.2)

            if mais.clicado(evento):
                velocidade = max(0.2, velocidade - 0.2)

        if rodando and agora - ultimo >= velocidade:
            if indice < len(passos) - 1:
                indice += 1
            else:
                rodando = False

            ultimo = agora

        passo = passos[indice]

        TELA.fill(FUNDO)

        desenhar_codigo(passo["linha"])

        if passo["finalizado"]:
            desenhar_panorama_final()
        else:
            desenhar_animacao_atual(passo)
            desenhar_comparacao_inicial_final(passo)
            desenhar_historico(indice)

        desenhar_mensagem(passo["texto"])
        barra_progresso(indice)

        play.desenhar()
        pause.desenhar()
        next_btn.desenhar()
        reset.desenhar()
        nova_lista.desenhar()
        menos.desenhar()
        mais.desenhar()

        status = "Executando" if rodando else "Pausado"
        info = FONTE.render(
            f"Status: {status} | Passo {indice + 1}/{len(passos)} | Velocidade: {velocidade:.1f}s",
            True,
            BRANCO
        )
        TELA.blit(info, (560, 735))

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()