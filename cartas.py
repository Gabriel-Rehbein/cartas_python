import pygame
import sys
import time
import random

pygame.init()

LARGURA, ALTURA = 1600, 920
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Visualizador Didático de Algoritmos")
clock = pygame.time.Clock()

FUNDO = (9, 13, 24)
PAINEL = (20, 27, 46)
PAINEL_2 = (31, 41, 70)
PAINEL_3 = (42, 55, 92)
PAINEL_ATIVO = (52, 66, 105)

BRANCO = (245, 247, 255)
PRETO = (12, 14, 22)
CINZA = (155, 165, 190)
AZUL = (75, 145, 255)
VERDE = (70, 215, 140)
VERMELHO = (245, 90, 95)
AMARELO = (255, 218, 85)
ROXO = (165, 115, 255)
LARANJA = (255, 160, 75)

FONTE = pygame.font.SysFont("consolas", 14)
FONTE_PEQ = pygame.font.SysFont("consolas", 12)
FONTE_MEDIA = pygame.font.SysFont("consolas", 17, bold=True)
FONTE_GRANDE = pygame.font.SysFont("consolas", 26, bold=True)
FONTE_TITULO = pygame.font.SysFont("consolas", 38, bold=True)

CODIGOS = {
    "Merge Sort": [
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
    ],
    "Quick Sort": [
        "def quick_sort(lista):",
        "    if len(lista) <= 1:",
        "        return lista",
        "    pivo = lista[-1]",
        "    menores = []",
        "    maiores = []",
        "    for item in lista[:-1]:",
        "        if item <= pivo:",
        "            menores.append(item)",
        "        else:",
        "            maiores.append(item)",
        "    return quick_sort(menores) + [pivo] + quick_sort(maiores)",
    ],
    "Counting Sort": [
        "def counting_sort(lista):",
        "    maior = max(lista)",
        "    contador = [0] * (maior + 1)",
        "    for numero in lista:",
        "        contador[numero] += 1",
        "    resultado = []",
        "    for valor in range(len(contador)):",
        "        while contador[valor] > 0:",
        "            resultado.append(valor)",
        "            contador[valor] -= 1",
        "    return resultado",
    ],
    "Radix Sort": [
        "def radix_sort(lista):",
        "    maior = max(lista)",
        "    exp = 1",
        "    while maior // exp > 0:",
        "        lista = counting_por_digito(lista, exp)",
        "        exp *= 10",
        "    return lista",
        "",
        "def counting_por_digito(lista, exp):",
        "    baldes = [[] for _ in range(10)]",
        "    for numero in lista:",
        "        digito = (numero // exp) % 10",
        "        baldes[digito].append(numero)",
        "    resultado = []",
        "    for balde in baldes:",
        "        resultado += balde",
        "    return resultado",
    ],
}

passos = []
historico = []
pilha = []
lista_inicial = []
arvore_merge = []

entradas_recursao = 0
saidas_recursao = 0


class Botao:
    def __init__(self, x, y, largura, altura, texto, cor):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.texto = texto
        self.cor = cor

    def desenhar(self):
        mouse = pygame.mouse.get_pos()
        cor = self.cor

        if self.rect.collidepoint(mouse):
            cor = tuple(min(c + 25, 255) for c in cor)

        pygame.draw.rect(TELA, (4, 7, 15), (self.rect.x + 4, self.rect.y + 5, self.rect.w, self.rect.h), border_radius=14)
        pygame.draw.rect(TELA, cor, self.rect, border_radius=14)
        pygame.draw.rect(TELA, BRANCO, self.rect, 1, border_radius=14)

        texto = FONTE_MEDIA.render(self.texto, True, BRANCO)
        TELA.blit(texto, texto.get_rect(center=self.rect.center))

    def clicado(self, evento):
        return evento.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(evento.pos)


def painel(x, y, w, h, titulo):
    pygame.draw.rect(TELA, (4, 7, 16), (x + 6, y + 8, w, h), border_radius=18)
    pygame.draw.rect(TELA, PAINEL, (x, y, w, h), border_radius=18)
    pygame.draw.rect(TELA, PAINEL_2, (x, y, w, h), 2, border_radius=18)

    titulo_render = FONTE_MEDIA.render(titulo, True, BRANCO)
    TELA.blit(titulo_render, (x + 18, y + 14))


def texto_centralizado(texto, fonte, cor, x, y):
    render = fonte.render(texto, True, cor)
    TELA.blit(render, render.get_rect(center=(x, y)))


def quebrar_texto(texto, fonte, largura_max):
    palavras = texto.split()
    linhas = []
    linha = ""

    for palavra in palavras:
        teste = linha + palavra + " "
        if fonte.size(teste)[0] <= largura_max:
            linha = teste
        else:
            if linha:
                linhas.append(linha.strip())
            linha = palavra + " "

    if linha:
        linhas.append(linha.strip())

    return linhas


def cor_por_tipo(tipo):
    if tipo in ["recursao", "divide", "pivo"]:
        return AZUL
    if tipo in ["compara", "decisao"]:
        return VERMELHO
    if tipo in ["adiciona", "retorna", "final"]:
        return VERDE
    if tipo in ["contador", "balde", "digito"]:
        return LARANJA
    if tipo == "merge":
        return ROXO
    return CINZA


def registrar(algoritmo, linha, lista, texto, tipo="passo", funcao="main", destaque=None, i=None, j=None, k=None):
    passos.append({
        "algoritmo": algoritmo,
        "linha": linha,
        "lista": lista[:],
        "texto": texto,
        "tipo": tipo,
        "funcao": funcao,
        "destaque": destaque or [],
        "pilha": pilha[:],
        "entradas": entradas_recursao,
        "saidas": saidas_recursao,
        "i": i,
        "j": j,
        "k": k,
    })

    historico.append({
        "texto": texto,
        "tipo": tipo
    })

    return len(passos) - 1


def adicionar_arvore(lista, nivel, tipo):
    arvore_merge.append({
        "lista": lista[:],
        "nivel": nivel,
        "tipo": tipo,
        "visivel": max(0, len(passos) - 1)
    })


def desenhar_codigo(passo):
    x, y, w, h = 25, 25, 500, 665
    painel(x, y, w, h, f"Código - {passo['algoritmo']}")

    codigo = CODIGOS[passo["algoritmo"]]
    yy = y + 55

    if passo["algoritmo"] == "Merge Sort" and passo["funcao"] == "merge":
        bloco_inicio = 10
        bloco_fim = len(codigo)
    else:
        bloco_inicio = 0
        bloco_fim = len(codigo)

    bloco_y = yy + bloco_inicio * 23 - 5
    bloco_h = max(28, (bloco_fim - bloco_inicio) * 23 + 8)

    pygame.draw.rect(TELA, PAINEL_ATIVO, (x + 14, bloco_y, w - 28, bloco_h), border_radius=12)

    for i, linha in enumerate(codigo):
        linha_rect = pygame.Rect(x + 18, yy - 3, w - 36, 23)

        if i == passo["linha"]:
            pygame.draw.rect(TELA, AMARELO, linha_rect, border_radius=8)
            cor_texto = PRETO
            cor_num = PRETO
        else:
            cor_texto = BRANCO
            cor_num = CINZA

        if i == 0 or linha.startswith("def "):
            pygame.draw.rect(TELA, (75, 145, 255), (x + 18, yy - 3, 5, 23), border_radius=3)

        if passo["funcao"] in linha:
            pygame.draw.rect(TELA, ROXO, (x + 18, yy - 3, 5, 23), border_radius=3)

        numero = FONTE.render(str(i + 1).rjust(2), True, cor_num)
        texto = FONTE.render(linha, True, cor_texto)

        TELA.blit(numero, (x + 28, yy))
        TELA.blit(texto, (x + 68, yy))

        yy += 23

    desenhar_funcao_ativa(passo, x + 18, y + h - 62, w - 36, 40)


def desenhar_funcao_ativa(passo, x, y, w, h):
    pygame.draw.rect(TELA, PAINEL_3, (x, y, w, h), border_radius=12)
    pygame.draw.rect(TELA, cor_por_tipo(passo["tipo"]), (x, y, 8, h), border_radius=5)

    texto = FONTE_MEDIA.render(f"Função ativa: {passo['funcao']}", True, BRANCO)
    TELA.blit(texto, (x + 18, y + 10))


def desenhar_carta(x, y, valor, cor, w=50, h=68, destaque=False):
    if destaque:
        y -= 7

    pygame.draw.rect(TELA, (4, 6, 14), (x + 5, y + 6, w, h), border_radius=13)
    rect = pygame.Rect(x, y, w, h)

    pygame.draw.rect(TELA, cor, rect, border_radius=13)
    pygame.draw.rect(TELA, BRANCO, rect, 2, border_radius=13)

    texto = FONTE_MEDIA.render(str(valor), True, PRETO)
    TELA.blit(texto, texto.get_rect(center=rect.center))


def desenhar_seta(x, y, texto, cor):
    pygame.draw.polygon(TELA, cor, [(x, y), (x - 8, y + 14), (x + 8, y + 14)])
    render = FONTE_MEDIA.render(texto, True, cor)
    TELA.blit(render, render.get_rect(center=(x, y + 30)))


def desenhar_lista_cartas(lista, x, y, destaque=None, i=None, j=None, k=None):
    destaque = destaque or []

    max_por_linha = 10
    espaco = 56

    for idx, valor in enumerate(lista):
        linha = idx // max_por_linha
        coluna = idx % max_por_linha

        cx = x + coluna * espaco
        cy = y + linha * 94

        ativo = idx in destaque or valor in destaque
        cor = VERDE if ativo else BRANCO

        desenhar_carta(cx, cy, valor, cor, 46, 64, ativo)

        if i == idx:
            desenhar_seta(cx + 23, cy - 32, "i", AZUL)

        if j == idx:
            desenhar_seta(cx + 23, cy + 70, "j", VERMELHO)

        if k == idx:
            desenhar_seta(cx + 23, cy + 100, "k", LARANJA)


def desenhar_animacao(passo):
    x, y, w, h = 550, 25, 620, 300
    painel(x, y, w, h, "Visualização do algoritmo")

    subtitulo = FONTE.render("Cartas representam a lista no estado atual", True, CINZA)
    TELA.blit(subtitulo, (x + 22, y + 48))

    desenhar_lista_cartas(
        passo["lista"],
        x + 35,
        y + 105,
        passo["destaque"],
        passo["i"],
        passo["j"],
        passo["k"]
    )

    faixa = pygame.Rect(x + 22, y + h - 56, w - 44, 36)
    pygame.draw.rect(TELA, cor_por_tipo(passo["tipo"]), faixa, border_radius=12)

    linhas = quebrar_texto(passo["texto"], FONTE, w - 70)
    yy = y + h - 47

    for linha in linhas[:2]:
        render = FONTE.render(linha, True, BRANCO)
        TELA.blit(render, (x + 40, yy))
        yy += 16


def desenhar_pilha(passo):
    x, y, w, h = 1195, 25, 380, 300
    painel(x, y, w, h, "Pilha de chamadas")

    yy = y + 58

    if not passo["pilha"]:
        texto_centralizado("Sem chamadas ativas", FONTE, CINZA, x + w // 2, y + 145)

    for item in reversed(passo["pilha"][-6:]):
        pygame.draw.rect(TELA, PAINEL_3, (x + 24, yy, w - 48, 32), border_radius=10)
        pygame.draw.rect(TELA, AZUL, (x + 24, yy, 6, 32), border_radius=5)

        linhas = quebrar_texto(item, FONTE_PEQ, w - 70)
        render = FONTE_PEQ.render(linhas[0], True, BRANCO)
        TELA.blit(render, (x + 38, yy + 9))

        yy += 39

    pygame.draw.line(TELA, PAINEL_3, (x + 25, y + h - 68), (x + w - 25, y + h - 68), 2)

    entrou = FONTE.render(f"Entrou na recursão: {passo['entradas']}x", True, VERDE)
    saiu = FONTE.render(f"Saiu da recursão: {passo['saidas']}x", True, VERMELHO)

    TELA.blit(entrou, (x + 28, y + h - 54))
    TELA.blit(saiu, (x + 28, y + h - 31))


def desenhar_memoria(passo):
    x, y, w, h = 550, 345, 620, 120
    painel(x, y, w, h, "Escopo e variáveis")

    cor_tipo = cor_por_tipo(passo["tipo"])

    pygame.draw.rect(TELA, cor_tipo, (x + 25, y + 55, 165, 36), border_radius=12)
    texto = FONTE_MEDIA.render(passo["funcao"], True, BRANCO)
    TELA.blit(texto, texto.get_rect(center=(x + 108, y + 73)))

    info = [
        f"Tipo de passo: {passo['tipo']}",
        f"Linha executada: {passo['linha'] + 1}",
        "O bloco destacado no código mostra o escopo ativo.",
    ]

    yy = y + 50
    for item in info:
        render = FONTE.render(item, True, BRANCO)
        TELA.blit(render, (x + 215, yy))
        yy += 21


def desenhar_arvore_merge(indice, algoritmo):
    x, y, w, h = 1195, 345, 380, 320
    painel(x, y, w, h, "Árvore do Merge Sort")

    if algoritmo != "Merge Sort":
        texto_centralizado("Disponível no Merge Sort", FONTE, CINZA, x + w // 2, y + h // 2)
        return

    visiveis = [no for no in arvore_merge if no["visivel"] <= indice]

    if not visiveis:
        texto_centralizado("A árvore aparecerá durante as divisões", FONTE_PEQ, CINZA, x + w // 2, y + h // 2)
        return

    por_nivel = {}

    for no in visiveis:
        por_nivel.setdefault(no["nivel"], []).append(no)

    y_base = y + 55
    altura_nivel = 42

    for nivel, nos in por_nivel.items():
        qtd = len(nos)
        espaco = (w - 50) / max(qtd, 1)

        for i, no in enumerate(nos):
            cx = x + 25 + i * espaco + espaco / 2
            cy = y_base + nivel * altura_nivel

            if cy > y + h - 28:
                continue

            cor = AZUL if no["tipo"] == "divide" else VERDE if no["tipo"] == "junta" else AMARELO

            rect = pygame.Rect(cx - 48, cy - 13, 96, 26)
            pygame.draw.rect(TELA, cor, rect, border_radius=8)
            pygame.draw.rect(TELA, BRANCO, rect, 1, border_radius=8)

            texto_lista = str(no["lista"])
            if len(texto_lista) > 13:
                texto_lista = texto_lista[:12] + "..."

            render = FONTE_PEQ.render(texto_lista, True, PRETO)
            TELA.blit(render, render.get_rect(center=rect.center))


def desenhar_historico(indice):
    x, y, w, h = 25, 705, 1550, 105
    painel(x, y, w, h, "Passo didático atual")

    passo = passos[indice]

    cor = cor_por_tipo(passo["tipo"])
    pygame.draw.rect(TELA, cor, (x + 22, y + 50, 10, 38), border_radius=5)

    linhas = quebrar_texto(passo["texto"], FONTE_MEDIA, w - 80)
    yy = y + 50

    for linha in linhas[:2]:
        render = FONTE_MEDIA.render(linha, True, BRANCO)
        TELA.blit(render, (x + 45, yy))
        yy += 26


def desenhar_linha_resumo(lista, x, y, titulo, cor):
    render = FONTE.render(titulo, True, CINZA)
    TELA.blit(render, (x, y - 24))

    for i, valor in enumerate(lista[:13]):
        desenhar_carta(x + i * 52, y, valor, cor, 42, 58)


def desenhar_panorama_final(passo):
    x, y, w, h = 550, 25, 1025, 640
    painel(x, y, w, h, f"Panorama final - {passo['algoritmo']}")

    texto_centralizado("RESULTADO FINAL", FONTE_GRANDE, VERDE, x + w // 2, y + 60)

    desenhar_linha_resumo(lista_inicial, x + 80, y + 135, "Lista inicial:", BRANCO)
    desenhar_linha_resumo(passo["lista"], x + 80, y + 245, "Lista ordenada:", VERDE)

    pygame.draw.line(TELA, PAINEL_3, (x + 60, y + 335), (x + w - 60, y + 335), 2)

    textos = [
        "O algoritmo terminou a execução.",
        "A lista foi processada passo a passo.",
        "Você pode voltar para revisar qualquer momento.",
        "A função ativa e o bloco do código mostram onde o algoritmo está.",
        "No Merge Sort, a árvore mostra a divisão e a junção das listas."
    ]

    yy = y + 365
    for item in textos:
        render = FONTE_MEDIA.render("• " + item, True, BRANCO)
        TELA.blit(render, (x + 80, yy))
        yy += 30


def barra_progresso(indice):
    x, y, w, h = 25, 830, 500, 24

    pygame.draw.rect(TELA, PAINEL_2, (x, y, w, h), border_radius=14)

    progresso = (indice + 1) / max(1, len(passos))
    pygame.draw.rect(TELA, VERDE, (x, y, int(w * progresso), h), border_radius=14)

    texto = FONTE.render(f"Progresso {int(progresso * 100)}%", True, BRANCO)
    TELA.blit(texto, texto.get_rect(center=(x + w // 2, y + h // 2)))


def merge_visual(esquerda, direita, nivel):
    registrar("Merge Sort", 10, esquerda + direita, f"Camada {nivel}: entrou na função merge.", "merge", "merge")

    resultado = []
    registrar("Merge Sort", 11, esquerda + direita, "Cria a lista resultado vazia.", "merge", "merge")

    i = j = 0
    registrar("Merge Sort", 12, esquerda + direita, "Inicializa os ponteiros i = 0 e j = 0.", "merge", "merge")

    while i < len(esquerda) and j < len(direita):
        tela = resultado + esquerda[i:] + direita[j:]

        registrar(
            "Merge Sort",
            13,
            tela,
            f"Compara {esquerda[i]} com {direita[j]}.",
            "compara",
            "merge",
            destaque=[esquerda[i], direita[j]]
        )

        if esquerda[i] < direita[j]:
            registrar("Merge Sort", 14, tela, f"{esquerda[i]} é menor que {direita[j]}.", "decisao", "merge")
            resultado.append(esquerda[i])
            registrar("Merge Sort", 15, resultado + esquerda[i + 1:] + direita[j:], f"Adiciona {resultado[-1]} ao resultado.", "adiciona", "merge", destaque=[resultado[-1]])
            i += 1
            registrar("Merge Sort", 16, resultado + esquerda[i:] + direita[j:], "Avança o ponteiro i.", "compara", "merge")
        else:
            registrar("Merge Sort", 17, tela, f"{direita[j]} é menor ou igual a {esquerda[i]}.", "decisao", "merge")
            resultado.append(direita[j])
            registrar("Merge Sort", 18, resultado + esquerda[i:] + direita[j + 1:], f"Adiciona {resultado[-1]} ao resultado.", "adiciona", "merge", destaque=[resultado[-1]])
            j += 1
            registrar("Merge Sort", 19, resultado + esquerda[i:] + direita[j:], "Avança o ponteiro j.", "compara", "merge")

    resultado += esquerda[i:]
    registrar("Merge Sort", 20, resultado + direita[j:], "Adiciona o restante da esquerda.", "adiciona", "merge")

    resultado += direita[j:]
    registrar("Merge Sort", 21, resultado, "Adiciona o restante da direita.", "adiciona", "merge")

    registrar("Merge Sort", 22, resultado, f"Retorna {resultado}.", "retorna", "merge")
    adicionar_arvore(resultado, nivel, "junta")

    return resultado


def merge_sort_visual(lista, nivel=0):
    global entradas_recursao, saidas_recursao

    entradas_recursao += 1
    pilha.append(f"merge_sort({lista})")

    registrar("Merge Sort", 0, lista, f"Camada {nivel}: entrou em merge_sort com {lista}.", "recursao", "merge_sort")
    adicionar_arvore(lista, nivel, "divide")

    registrar("Merge Sort", 1, lista, "Verifica se a lista tem 0 ou 1 elemento.", "decisao", "merge_sort")

    if len(lista) <= 1:
        registrar("Merge Sort", 2, lista, f"Retorna {lista}, pois já está ordenada.", "retorna", "merge_sort")
        adicionar_arvore(lista, nivel, "folha")
        saidas_recursao += 1
        pilha.pop()
        return lista

    meio = len(lista) // 2
    registrar("Merge Sort", 3, lista, f"Calcula o meio da lista: {meio}.", "divide", "merge_sort")

    esquerda = lista[:meio]
    registrar("Merge Sort", 4, esquerda, f"Cria uma cópia da esquerda: {esquerda}.", "divide", "merge_sort")

    direita = lista[meio:]
    registrar("Merge Sort", 5, direita, f"Cria uma cópia da direita: {direita}.", "divide", "merge_sort")

    registrar("Merge Sort", 6, esquerda, "Chama recursão para ordenar a esquerda.", "recursao", "merge_sort")
    esquerda = merge_sort_visual(esquerda, nivel + 1)

    registrar("Merge Sort", 7, direita, "Chama recursão para ordenar a direita.", "recursao", "merge_sort")
    direita = merge_sort_visual(direita, nivel + 1)

    registrar("Merge Sort", 8, esquerda + direita, "Junta esquerda e direita usando merge.", "merge", "merge_sort")
    resultado = merge_visual(esquerda, direita, nivel)

    saidas_recursao += 1
    pilha.pop()
    return resultado


def quick_sort_visual(lista, nivel=0):
    global entradas_recursao, saidas_recursao

    entradas_recursao += 1
    pilha.append(f"quick_sort({lista})")
    registrar("Quick Sort", 0, lista, f"Camada {nivel}: entrou em quick_sort com {lista}.", "recursao", "quick_sort")

    registrar("Quick Sort", 1, lista, "Verifica se a lista tem 0 ou 1 elemento.", "decisao", "quick_sort")

    if len(lista) <= 1:
        registrar("Quick Sort", 2, lista, f"Retorna {lista}, pois já está ordenada.", "retorna", "quick_sort")
        saidas_recursao += 1
        pilha.pop()
        return lista

    pivo = lista[-1]
    registrar("Quick Sort", 3, lista, f"Escolhe o pivô: {pivo}.", "pivo", "quick_sort", destaque=[pivo])

    menores = []
    registrar("Quick Sort", 4, lista, "Cria a lista menores.", "divide", "quick_sort")

    maiores = []
    registrar("Quick Sort", 5, lista, "Cria a lista maiores.", "divide", "quick_sort")

    for idx, item in enumerate(lista[:-1]):
        registrar("Quick Sort", 6, lista, f"Analisa o item {item}.", "compara", "quick_sort", destaque=[idx], i=idx)

        if item <= pivo:
            registrar("Quick Sort", 7, lista, f"{item} vai para menores.", "decisao", "quick_sort")
            menores.append(item)
            registrar("Quick Sort", 8, menores, f"Menores agora é {menores}.", "adiciona", "quick_sort")
        else:
            registrar("Quick Sort", 9, lista, f"{item} vai para maiores.", "decisao", "quick_sort")
            maiores.append(item)
            registrar("Quick Sort", 10, maiores, f"Maiores agora é {maiores}.", "adiciona", "quick_sort")

    registrar("Quick Sort", 11, menores + [pivo] + maiores, "Ordena menores e maiores recursivamente.", "recursao", "quick_sort")
    resultado = quick_sort_visual(menores, nivel + 1) + [pivo] + quick_sort_visual(maiores, nivel + 1)

    registrar("Quick Sort", 11, resultado, f"Junta menores + pivô + maiores: {resultado}.", "retorna", "quick_sort")

    saidas_recursao += 1
    pilha.pop()
    return resultado


def counting_sort_visual(lista):
    registrar("Counting Sort", 0, lista, f"Recebe a lista {lista}.", "passo", "counting_sort")

    maior = max(lista)
    registrar("Counting Sort", 1, lista, f"Encontra o maior valor: {maior}.", "contador", "counting_sort", destaque=[maior])

    contador = [0] * (maior + 1)
    registrar("Counting Sort", 2, contador, f"Cria o contador com {maior + 1} posições.", "contador", "counting_sort")

    for numero in lista:
        registrar("Counting Sort", 3, lista, f"Lê o número {numero}.", "compara", "counting_sort", destaque=[numero])
        contador[numero] += 1
        registrar("Counting Sort", 4, contador, f"Incrementa contador[{numero}].", "contador", "counting_sort", k=numero)

    resultado = []
    registrar("Counting Sort", 5, resultado, "Cria a lista resultado vazia.", "adiciona", "counting_sort")

    for valor in range(len(contador)):
        registrar("Counting Sort", 6, contador, f"Verifica contador[{valor}].", "compara", "counting_sort", k=valor)

        while contador[valor] > 0:
            registrar("Counting Sort", 7, contador, f"contador[{valor}] ainda é maior que zero.", "decisao", "counting_sort", k=valor)
            resultado.append(valor)
            registrar("Counting Sort", 8, resultado, f"Adiciona {valor} ao resultado.", "adiciona", "counting_sort", destaque=[valor])
            contador[valor] -= 1
            registrar("Counting Sort", 9, contador, f"Reduz contador[{valor}].", "contador", "counting_sort", k=valor)

    registrar("Counting Sort", 10, resultado, f"Retorna {resultado}.", "final", "counting_sort")
    return resultado


def counting_por_digito_visual(lista, exp):
    registrar("Radix Sort", 8, lista, f"Cria 10 baldes para a casa {exp}.", "balde", "radix_sort")

    baldes = [[] for _ in range(10)]

    for idx, numero in enumerate(lista):
        digito = (numero // exp) % 10
        registrar("Radix Sort", 9, lista, f"O dígito de {numero} na casa {exp} é {digito}.", "digito", "radix_sort", destaque=[idx], i=idx)

        baldes[digito].append(numero)
        parcial = [item for balde in baldes for item in balde]
        registrar("Radix Sort", 10, parcial, f"Coloca {numero} no balde {digito}.", "balde", "radix_sort")

    resultado = []
    registrar("Radix Sort", 11, resultado, "Cria resultado vazio para juntar os baldes.", "adiciona", "radix_sort")

    for indice, balde in enumerate(baldes):
        registrar("Radix Sort", 12, resultado + balde, f"Lê o balde {indice}: {balde}.", "balde", "radix_sort")
        resultado += balde

    registrar("Radix Sort", 13, resultado, f"Retorna a lista após essa casa decimal: {resultado}.", "retorna", "radix_sort")
    return resultado


def radix_sort_visual(lista):
    registrar("Radix Sort", 0, lista, f"Recebe a lista {lista}.", "passo", "radix_sort")

    maior = max(lista)
    registrar("Radix Sort", 1, lista, f"Encontra o maior número: {maior}.", "digito", "radix_sort", destaque=[maior])

    exp = 1
    registrar("Radix Sort", 2, lista, "Começa pela casa das unidades.", "digito", "radix_sort")

    while maior // exp > 0:
        registrar("Radix Sort", 3, lista, f"Ordena usando a casa decimal {exp}.", "decisao", "radix_sort")

        lista = counting_por_digito_visual(lista, exp)

        registrar("Radix Sort", 4, lista, f"Lista após processar a casa {exp}: {lista}.", "balde", "radix_sort")

        exp *= 10
        registrar("Radix Sort", 5, lista, f"Avança para a próxima casa decimal: {exp}.", "digito", "radix_sort")

    registrar("Radix Sort", 6, lista, f"Retorna {lista}.", "final", "radix_sort")
    return lista


def gerar_passos(lista, algoritmo):
    global passos, historico, pilha, lista_inicial, arvore_merge
    global entradas_recursao, saidas_recursao

    passos = []
    historico = []
    pilha = []
    arvore_merge = []
    lista_inicial = lista[:]
    entradas_recursao = 0
    saidas_recursao = 0

    if algoritmo == "Merge Sort":
        resultado = merge_sort_visual(lista)
    elif algoritmo == "Quick Sort":
        resultado = quick_sort_visual(lista)
    elif algoritmo == "Counting Sort":
        resultado = counting_sort_visual(lista)
    else:
        resultado = radix_sort_visual(lista)

    registrar(
        algoritmo,
        len(CODIGOS[algoritmo]) - 1,
        resultado,
        f"Final: começou como {lista_inicial} e terminou como {resultado}.",
        "final",
        "main"
    )


def converter_texto_para_lista(texto):
    texto = texto.replace(",", " ")
    partes = texto.split()
    lista = []

    for parte in partes:
        if parte.lstrip("-").isdigit():
            numero = int(parte)
            if numero >= 0:
                lista.append(numero)

    return lista


def gerar_nova_lista():
    return random.sample(range(1, 99), 8)


def tela_inicio():
    algoritmos = ["Merge Sort", "Quick Sort", "Counting Sort", "Radix Sort"]
    algoritmo_atual = 0

    lista = gerar_nova_lista()
    texto_digitado = ""
    erro = ""
    input_ativo = False

    input_rect = pygame.Rect(500, 355, 600, 56)

    iniciar = Botao(650, 615, 300, 56, "Iniciar", AZUL)
    nova = Botao(650, 685, 300, 56, "Nova lista", ROXO)
    esquerda = Botao(505, 505, 80, 54, "<", PAINEL_3)
    direita = Botao(1015, 505, 80, 54, ">", PAINEL_3)

    while True:
        TELA.fill(FUNDO)

        texto_centralizado("Visualizador Didático de Ordenação", FONTE_TITULO, BRANCO, LARGURA // 2, 115)
        texto_centralizado("Escolha o algoritmo e acompanhe a execução passo a passo", FONTE_MEDIA, CINZA, LARGURA // 2, 165)

        pygame.draw.rect(TELA, PAINEL, (470, 235, 660, 88), border_radius=22)
        texto_centralizado(f"Lista atual: {lista}", FONTE_MEDIA, AMARELO, LARGURA // 2, 279)

        pygame.draw.rect(TELA, AMARELO if input_ativo else PAINEL_2, input_rect, border_radius=16)
        pygame.draw.rect(TELA, BRANCO, input_rect, 2, border_radius=16)

        texto_input = texto_digitado if texto_digitado else "Digite: 7 4 9 2 8 1 5 3"
        cor = PRETO if input_ativo else CINZA
        render = FONTE_MEDIA.render(texto_input[:55], True, cor)
        TELA.blit(render, (input_rect.x + 18, input_rect.y + 17))

        algoritmo = algoritmos[algoritmo_atual]

        pygame.draw.rect(TELA, PAINEL, (595, 497, 410, 68), border_radius=22)
        texto_centralizado(algoritmo, FONTE_GRANDE, VERDE, LARGURA // 2, 531)

        if erro:
            texto_centralizado(erro, FONTE, VERMELHO, LARGURA // 2, 445)

        iniciar.desenhar()
        nova.desenhar()
        esquerda.desenhar()
        direita.desenhar()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                input_ativo = input_rect.collidepoint(evento.pos)

            if evento.type == pygame.KEYDOWN and input_ativo:
                if evento.key == pygame.K_BACKSPACE:
                    texto_digitado = texto_digitado[:-1]
                elif evento.key == pygame.K_RETURN:
                    nova_lista = converter_texto_para_lista(texto_digitado)
                    if len(nova_lista) >= 2:
                        return nova_lista, algoritmo
                    erro = "Digite pelo menos 2 números positivos."
                else:
                    if len(texto_digitado) < 80:
                        texto_digitado += evento.unicode

            if esquerda.clicado(evento):
                algoritmo_atual = (algoritmo_atual - 1) % len(algoritmos)

            if direita.clicado(evento):
                algoritmo_atual = (algoritmo_atual + 1) % len(algoritmos)

            if nova.clicado(evento):
                lista = gerar_nova_lista()
                texto_digitado = ""
                erro = ""

            if iniciar.clicado(evento):
                nova_lista = converter_texto_para_lista(texto_digitado)

                if texto_digitado and len(nova_lista) >= 2:
                    return nova_lista, algoritmo

                return lista, algoritmo

        pygame.display.update()
        clock.tick(60)


def main():
    lista, algoritmo = tela_inicio()
    gerar_passos(lista, algoritmo)

    indice = 0
    rodando = False
    velocidade = 1.0
    ultimo = time.time()

    play = Botao(550, 865, 95, 38, "Play", VERDE)
    pause = Botao(655, 865, 95, 38, "Pause", VERMELHO)
    voltar = Botao(760, 865, 105, 38, "Voltar", LARANJA)
    proximo = Botao(875, 865, 115, 38, "Próximo", AZUL)
    reset = Botao(1000, 865, 105, 38, "Reset", ROXO)
    menu = Botao(1115, 865, 105, 38, "Menu", PAINEL_3)
    menos = Botao(1230, 865, 45, 38, "-", PAINEL_3)
    mais = Botao(1285, 865, 45, 38, "+", PAINEL_3)

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

            if voltar.clicado(evento):
                rodando = False
                if indice > 0:
                    indice -= 1

            if proximo.clicado(evento):
                rodando = False
                if indice < len(passos) - 1:
                    indice += 1

            if reset.clicado(evento):
                indice = 0
                rodando = False

            if menu.clicado(evento):
                lista, algoritmo = tela_inicio()
                gerar_passos(lista, algoritmo)
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

        desenhar_codigo(passo)

        if passo["tipo"] == "final":
            desenhar_panorama_final(passo)
        else:
            desenhar_animacao(passo)
            desenhar_pilha(passo)
            desenhar_memoria(passo)
            desenhar_arvore_merge(indice, passo["algoritmo"])

        desenhar_historico(indice)
        barra_progresso(indice)

        play.desenhar()
        pause.desenhar()
        voltar.desenhar()
        proximo.desenhar()
        reset.desenhar()
        menu.desenhar()
        menos.desenhar()
        mais.desenhar()

        status = "Executando" if rodando else "Pausado"
        info = FONTE.render(
            f"Status: {status} | Algoritmo: {passo['algoritmo']} | Passo {indice + 1}/{len(passos)} | Velocidade: {velocidade:.1f}s",
            True,
            BRANCO
        )
        TELA.blit(info, (550, 838))

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()