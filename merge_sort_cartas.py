import pygame
import sys
import time
import random
import math

pygame.init()

LARGURA, ALTURA = 1420, 820
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Merge Sort Animado com Cartas")
clock = pygame.time.Clock()

FUNDO = (11, 15, 28)
PAINEL = (24, 31, 52)
PAINEL_2 = (36, 47, 78)
BRANCO = (246, 248, 255)
PRETO = (15, 17, 25)
CINZA = (160, 170, 190)
AZUL = (72, 140, 255)
VERDE = (65, 210, 135)
VERMELHO = (240, 85, 90)
AMARELO = (255, 215, 85)
ROXO = (160, 110, 255)
LARANJA = (255, 155, 75)

FONTE = pygame.font.SysFont("consolas", 15)
FONTE_MEDIA = pygame.font.SysFont("consolas", 18, bold=True)
FONTE_GRANDE = pygame.font.SysFont("consolas", 32, bold=True)
FONTE_TITULO = pygame.font.SysFont("consolas", 42, bold=True)

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
arvore_nos = []
lista_inicial_global = []
scroll_historico = 0


class Botao:
    def __init__(self, x, y, largura, altura, texto, cor):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.texto = texto
        self.cor = cor

    def desenhar(self):
        mouse = pygame.mouse.get_pos()
        cor = self.cor

        if self.rect.collidepoint(mouse):
            cor = tuple(min(c + 28, 255) for c in self.cor)

        pygame.draw.rect(
            TELA,
            (5, 8, 16),
            (self.rect.x + 4, self.rect.y + 5, self.rect.w, self.rect.h),
            border_radius=14
        )

        pygame.draw.rect(TELA, cor, self.rect, border_radius=14)
        pygame.draw.rect(TELA, BRANCO, self.rect, 2, border_radius=14)

        texto = FONTE_MEDIA.render(self.texto, True, BRANCO)
        rect = texto.get_rect(center=self.rect.center)
        TELA.blit(texto, rect)

    def clicado(self, evento):
        return evento.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(evento.pos)


def painel(x, y, w, h, titulo):
    pygame.draw.rect(TELA, (5, 8, 18), (x + 6, y + 8, w, h), border_radius=16)
    pygame.draw.rect(TELA, PAINEL, (x, y, w, h), border_radius=16)
    pygame.draw.rect(TELA, PAINEL_2, (x, y, w, h), 2, border_radius=16)

    texto = FONTE_MEDIA.render(titulo, True, BRANCO)
    TELA.blit(texto, (x + 15, y + 10))


def quebrar_texto(texto, fonte, largura_max):
    palavras = texto.split()
    linhas = []
    linha_atual = ""

    for palavra in palavras:
        teste = linha_atual + palavra + " "
        largura, _ = fonte.size(teste)

        if largura <= largura_max:
            linha_atual = teste
        else:
            if linha_atual:
                linhas.append(linha_atual.strip())
            linha_atual = palavra + " "

    if linha_atual:
        linhas.append(linha_atual.strip())

    return linhas


def texto_centralizado(texto, fonte, cor, x, y):
    render = fonte.render(texto, True, cor)
    rect = render.get_rect(center=(x, y))
    TELA.blit(render, rect)


def cor_por_tipo(tipo):
    if tipo in ["divide", "recursao"]:
        return AZUL
    if tipo in ["compara", "decisao"]:
        return VERMELHO
    if tipo in ["adiciona", "retorna", "final"]:
        return VERDE
    if tipo in ["junta", "merge"]:
        return ROXO
    if tipo == "restante":
        return LARANJA
    return CINZA


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


def adicionar_no_arvore(lista, nivel, tipo):
    arvore_nos.append({
        "lista": lista[:],
        "nivel": nivel,
        "tipo": tipo
    })


def merge_sort_visual(lista, nivel=0):
    adicionar_no_arvore(lista, nivel, "divide")

    registrar(0, lista, f"Nível {nivel}: merge_sort recebe {lista}", "recebe")
    registrar(1, lista, f"Nível {nivel}: verifica se a lista tem 0 ou 1 elemento", "verifica")

    if len(lista) <= 1:
        adicionar_no_arvore(lista, nivel, "folha")
        registrar(2, lista, f"Nível {nivel}: retorna {lista}, pois já está ordenada", "retorna")
        return lista

    registrar(3, lista, f"Nível {nivel}: calcula o meio da lista", "meio")
    meio = len(lista) // 2

    esquerda = lista[:meio]
    registrar(4, esquerda, f"Nível {nivel}: divide a esquerda {esquerda}", "divide")

    direita = lista[meio:]
    registrar(5, direita, f"Nível {nivel}: divide a direita {direita}", "divide")

    registrar(6, esquerda, f"Nível {nivel}: ordena a esquerda {esquerda}", "recursao")
    esquerda = merge_sort_visual(esquerda, nivel + 1)

    registrar(7, direita, f"Nível {nivel}: ordena a direita {direita}", "recursao")
    direita = merge_sort_visual(direita, nivel + 1)

    registrar(8, esquerda + direita, f"Nível {nivel}: junta esquerda {esquerda} com direita {direita}", "junta")
    resultado = merge_visual(esquerda, direita, nivel)

    adicionar_no_arvore(resultado, nivel, "junta")
    return resultado


def merge_visual(esquerda, direita, nivel):
    registrar(10, esquerda + direita, f"Nível {nivel}: inicia a função merge", "merge")

    resultado = []
    registrar(11, esquerda + direita, f"Nível {nivel}: cria a lista resultado vazia", "resultado")

    i = j = 0
    registrar(12, esquerda + direita, f"Nível {nivel}: inicia os índices i = 0 e j = 0", "indices")

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
            registrar(14, resultado + esquerda[i:] + direita[j:], f"{esquerda[i]} é menor que {direita[j]}", "decisao")
            resultado.append(esquerda[i])
            registrar(15, resultado + esquerda[i + 1:] + direita[j:], f"Adiciona {resultado[-1]} ao resultado", "adiciona", ordenadas=resultado)
            i += 1
            registrar(16, resultado + esquerda[i:] + direita[j:], "Avança o índice da esquerda", "indice")
        else:
            registrar(17, resultado + esquerda[i:] + direita[j:], f"{direita[j]} é menor ou igual a {esquerda[i]}", "decisao")
            resultado.append(direita[j])
            registrar(18, resultado + esquerda[i:] + direita[j + 1:], f"Adiciona {resultado[-1]} ao resultado", "adiciona", ordenadas=resultado)
            j += 1
            registrar(19, resultado + esquerda[i:] + direita[j:], "Avança o índice da direita", "indice")

    registrar(20, resultado + esquerda[i:] + direita[j:], "Adiciona o restante da esquerda ao resultado", "restante")
    resultado += esquerda[i:]

    registrar(21, resultado + direita[j:], "Adiciona o restante da direita ao resultado", "restante")
    resultado += direita[j:]

    registrar(22, resultado, f"Retorna a lista ordenada parcial {resultado}", "retorna", ordenadas=resultado)
    return resultado


def gerar_nova_lista():
    return random.sample(range(1, 100), 8)


def gerar_passos(lista):
    global passos, historico, arvore_nos, lista_inicial_global, scroll_historico

    passos = []
    historico = []
    arvore_nos = []
    scroll_historico = 0
    lista_inicial_global = lista[:]

    resultado = merge_sort_visual(lista)
    registrar(
        22,
        resultado,
        f"Lista final ordenada: começou como {lista_inicial_global} e terminou como {resultado}",
        "final",
        ordenadas=resultado,
        finalizado=True
    )


def desenhar_codigo(linha_ativa):
    x, y, w, h = 20, 20, 520, 575
    painel(x, y, w, h, "Código linha por linha")

    yy = y + 45

    for i, linha in enumerate(CODIGO):
        if i == linha_ativa:
            pygame.draw.rect(TELA, AMARELO, (x + 18, yy - 3, w - 35, 23), border_radius=7)
            cor = PRETO
        else:
            cor = BRANCO

        numero = FONTE.render(str(i + 1).rjust(2), True, VERMELHO if i == linha_ativa else CINZA)
        texto = FONTE.render(linha, True, cor)

        TELA.blit(numero, (x + 22, yy))
        TELA.blit(texto, (x + 60, yy))

        yy += 22


def desenhar_carta(x, y, valor, cor, w=58, h=82, destaque=False):
    if destaque:
        y -= 8

    pygame.draw.rect(TELA, (5, 7, 15), (x + 5, y + 7, w, h), border_radius=13)

    rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(TELA, cor, rect, border_radius=13)
    pygame.draw.rect(TELA, BRANCO, rect, 2, border_radius=13)

    brilho = pygame.Rect(x + 6, y + 6, w - 12, 11)
    pygame.draw.rect(TELA, (255, 255, 255), brilho, border_radius=8)

    texto = FONTE_MEDIA.render(str(valor), True, PRETO)
    texto_rect = texto.get_rect(center=rect.center)
    TELA.blit(texto, texto_rect)


def desenhar_linha_cartas(lista, x, y, titulo, cor=BRANCO):
    if titulo:
        texto = FONTE.render(titulo, True, CINZA)
        TELA.blit(texto, (x, y - 22))

    for i, valor in enumerate(lista):
        desenhar_carta(x + i * 48, y, valor, cor, 42, 58)


def desenhar_animacao_atual(passo):
    x, y, w, h = 560, 20, 840, 275
    painel(x, y, w, h, "Animação atual")

    lista = passo["lista"]
    comparando = passo["comparando"]
    ordenadas = passo["ordenadas"]
    finalizado = passo["finalizado"]

    pulso = math.sin(time.time() * 5) * 5

    x_cartas = x + 45
    y_cartas = y + 105

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

        deslocamento = pulso if destaque else 0
        desenhar_carta(x_cartas + i * 82, y_cartas - deslocamento, valor, cor, 66, 94, destaque)

    cor_tipo = cor_por_tipo(passo["tipo"])
    caixa = pygame.Rect(x + 25, y + 225, w - 50, 38)

    pygame.draw.rect(TELA, cor_tipo, caixa, border_radius=10)

    linhas = quebrar_texto("Último passo executado: " + passo["texto"], FONTE, w - 80)

    yy = y + 235
    for linha in linhas[:2]:
        texto = FONTE.render(linha, True, BRANCO)
        TELA.blit(texto, (x + 40, yy))
        yy += 18


def desenhar_comparacao_inicial_final(passo):
    x, y, w, h = 560, 310, 410, 160
    painel(x, y, w, h, "Começo x estado atual")

    desenhar_linha_cartas(lista_inicial_global, x + 30, y + 70, "Início:", BRANCO)

    cor_resultado = VERDE if passo["finalizado"] else AZUL
    desenhar_linha_cartas(passo["lista"], x + 30, y + 135, "Atual:", cor_resultado)


def desenhar_historico(indice):
    global scroll_historico

    x, y, w, h = 990, 310, 410, 160
    painel(x, y, w, h, "Histórico com scroll")

    itens = historico[:indice + 1]

    linhas_render = []

    for item in itens:
        linhas = quebrar_texto(item["texto"], FONTE, w - 65)
        for linha in linhas:
            linhas_render.append({
                "texto": linha,
                "tipo": item["tipo"]
            })

    altura_total = len(linhas_render) * 22
    area_visivel = h - 45
    max_scroll = max(0, altura_total - area_visivel)

    scroll_historico = max(0, min(scroll_historico, max_scroll))

    yy = y + 42 - scroll_historico

    clip_original = TELA.get_clip()
    TELA.set_clip(pygame.Rect(x, y + 38, w, h - 45))

    for i, item in enumerate(linhas_render):
        cor = cor_por_tipo(item["tipo"])
        eh_ultimo = i == len(linhas_render) - 1

        if y + 38 <= yy <= y + h - 10:
            if eh_ultimo:
                pygame.draw.rect(TELA, cor, (x + 12, yy - 4, w - 24, 22), border_radius=7)
                texto_cor = BRANCO
            else:
                texto_cor = CINZA

            pygame.draw.circle(TELA, cor if not eh_ultimo else BRANCO, (x + 24, yy + 8), 5)

            render = FONTE.render(item["texto"], True, texto_cor)
            TELA.blit(render, (x + 40, yy))

        yy += 22

    TELA.set_clip(clip_original)


def desenhar_arvore(indice):
    x, y, w, h = 560, 485, 840, 210
    painel(x, y, w, h, "Árvore visual de divisão e junção")

    if not arvore_nos:
        return

    max_mostrar = min(
        len(arvore_nos),
        max(1, int((indice + 1) / max(1, len(passos)) * len(arvore_nos)))
    )

    por_nivel = {}

    for no in arvore_nos[:max_mostrar]:
        nivel = no["nivel"]
        por_nivel.setdefault(nivel, []).append(no)

    y_base = y + 55
    altura_nivel = 38

    for nivel, nos in por_nivel.items():
        qtd = len(nos)
        espaco = (w - 70) / max(qtd, 1)

        for i, no in enumerate(nos):
            cx = x + 35 + i * espaco + espaco / 2
            cy = y_base + nivel * altura_nivel

            cor = AZUL if no["tipo"] == "divide" else VERDE if no["tipo"] == "junta" else AMARELO
            texto = str(no["lista"])

            rect = pygame.Rect(cx - 55, cy - 14, 110, 28)
            pygame.draw.rect(TELA, cor, rect, border_radius=8)
            pygame.draw.rect(TELA, BRANCO, rect, 1, border_radius=8)

            linhas = quebrar_texto(texto, FONTE, 100)
            render = FONTE.render(linhas[0], True, PRETO)
            TELA.blit(render, render.get_rect(center=rect.center))


def desenhar_mensagem(passo):
    x, y, w, h = 20, 610, 520, 90

    pygame.draw.rect(TELA, PAINEL_2, (x, y, w, h), border_radius=15)
    pygame.draw.rect(TELA, cor_por_tipo(passo["tipo"]), (x, y, 8, h), border_radius=6)

    titulo = FONTE_MEDIA.render("Último passo em evidência", True, BRANCO)
    TELA.blit(titulo, (x + 25, y + 12))

    linhas = quebrar_texto(passo["texto"], FONTE, w - 40)

    yy = y + 42
    for linha in linhas:
        render = FONTE.render(linha, True, BRANCO)
        TELA.blit(render, (x + 25, yy))
        yy += 19


def barra_progresso(indice):
    x, y, w, h = 20, 715, 520, 24

    pygame.draw.rect(TELA, PAINEL_2, (x, y, w, h), border_radius=12)

    progresso = (indice + 1) / len(passos)
    pygame.draw.rect(TELA, VERDE, (x, y, int(w * progresso), h), border_radius=12)

    texto = FONTE.render(f"Progresso {int(progresso * 100)}%", True, BRANCO)
    TELA.blit(texto, (x + 190, y + 3))


def desenhar_panorama_final():
    x, y, w, h = 560, 20, 840, 675
    painel(x, y, w, h, "Panorama final do Merge Sort")

    texto_centralizado("RESULTADO FINAL", FONTE_GRANDE, VERDE, x + w // 2, y + 55)

    resultado = passos[-1]["lista"]

    desenhar_linha_cartas(lista_inicial_global, x + 80, y + 135, "Lista inicial:", BRANCO)
    desenhar_linha_cartas(resultado, x + 80, y + 245, "Lista ordenada:", VERDE)

    pygame.draw.line(TELA, CINZA, (x + 60, y + 335), (x + w - 60, y + 335), 2)

    resumos = [
        "1. A lista original foi dividida em partes menores.",
        "2. Cada parte foi quebrada até sobrar apenas uma carta.",
        "3. Depois, o algoritmo começou a comparar as cartas.",
        "4. A menor carta sempre voltou primeiro para o resultado.",
        "5. No final, todas as partes foram juntadas em ordem crescente."
    ]

    yy = y + 380
    for texto in resumos:
        linhas = quebrar_texto(texto, FONTE_MEDIA, w - 120)
        for linha in linhas:
            render = FONTE_MEDIA.render(linha, True, BRANCO)
            TELA.blit(render, (x + 70, yy))
            yy += 30

    pygame.draw.rect(TELA, VERDE, (x + 60, y + 610, w - 120, 45), border_radius=14)

    final = f"Começou como {lista_inicial_global}  →  terminou como {resultado}"
    linhas = quebrar_texto(final, FONTE_MEDIA, w - 160)

    yy = y + 620
    for linha in linhas:
        render = FONTE_MEDIA.render(linha, True, PRETO)
        TELA.blit(render, render.get_rect(center=(x + w // 2, yy)))
        yy += 20


def converter_texto_para_lista(texto):
    texto = texto.replace(",", " ")
    partes = texto.split()

    lista = []

    for parte in partes:
        if parte.lstrip("-").isdigit():
            lista.append(int(parte))

    return lista


def tela_inicio():
    iniciar = Botao(560, 500, 300, 58, "Iniciar Visualização", AZUL)
    nova = Botao(560, 575, 300, 58, "Nova Lista", ROXO)
    usar_digitada = Botao(560, 650, 300, 58, "Usar Lista Digitada", VERDE)

    lista = gerar_nova_lista()
    texto_digitado = ""
    mensagem_erro = ""

    input_rect = pygame.Rect(410, 385, 600, 55)
    input_ativo = False

    while True:
        TELA.fill(FUNDO)

        texto_centralizado("Merge Sort com Cartas", FONTE_TITULO, BRANCO, LARGURA // 2, 120)
        texto_centralizado("Digite uma lista ou use uma lista aleatória", FONTE_MEDIA, CINZA, LARGURA // 2, 175)

        pygame.draw.rect(TELA, PAINEL, (405, 230, 610, 85), border_radius=18)
        texto_centralizado(f"Lista atual: {lista}", FONTE_MEDIA, AMARELO, LARGURA // 2, 272)

        cor_input = AMARELO if input_ativo else PAINEL_2
        pygame.draw.rect(TELA, cor_input, input_rect, border_radius=14)
        pygame.draw.rect(TELA, BRANCO, input_rect, 2, border_radius=14)

        placeholder = "Digite os números: 7 4 9 2 8 1 5 3"
        texto_input = texto_digitado if texto_digitado else placeholder
        cor_texto = BRANCO if texto_digitado else CINZA

        linhas_input = quebrar_texto(texto_input, FONTE_MEDIA, input_rect.w - 30)
        render = FONTE_MEDIA.render(linhas_input[0], True, cor_texto)
        TELA.blit(render, (input_rect.x + 15, input_rect.y + 17))

        if mensagem_erro:
            erro = FONTE.render(mensagem_erro, True, VERMELHO)
            TELA.blit(erro, erro.get_rect(center=(LARGURA // 2, 462)))

        iniciar.desenhar()
        nova.desenhar()
        usar_digitada.desenhar()

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
                    nova_lista_digitada = converter_texto_para_lista(texto_digitado)

                    if len(nova_lista_digitada) >= 2:
                        lista = nova_lista_digitada
                        return lista
                    else:
                        mensagem_erro = "Digite pelo menos 2 números válidos."
                else:
                    if len(texto_digitado) < 80:
                        texto_digitado += evento.unicode

            if iniciar.clicado(evento):
                return lista

            if nova.clicado(evento):
                lista = gerar_nova_lista()
                texto_digitado = ""
                mensagem_erro = ""

            if usar_digitada.clicado(evento):
                nova_lista_digitada = converter_texto_para_lista(texto_digitado)

                if len(nova_lista_digitada) >= 2:
                    lista = nova_lista_digitada
                    return lista
                else:
                    mensagem_erro = "Digite pelo menos 2 números válidos."

        pygame.display.update()
        clock.tick(60)


def main():
    global scroll_historico

    lista = tela_inicio()
    gerar_passos(lista)

    indice = 0
    rodando = False
    velocidade = 1.0
    ultimo = time.time()

    play = Botao(560, 755, 105, 45, "Play", VERDE)
    pause = Botao(675, 755, 105, 45, "Pause", VERMELHO)
    next_btn = Botao(790, 755, 130, 45, "Próximo", AZUL)
    reset = Botao(930, 755, 130, 45, "Reiniciar", ROXO)
    nova_lista = Botao(1070, 755, 130, 45, "Nova Lista", LARANJA)
    menos = Botao(1210, 755, 45, 45, "-", PAINEL_2)
    mais = Botao(1265, 755, 45, 45, "+", PAINEL_2)

    while True:
        agora = time.time()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 4:
                    scroll_historico -= 25
                elif evento.button == 5:
                    scroll_historico += 25

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
                scroll_historico = 0

            if nova_lista.clicado(evento):
                lista = gerar_nova_lista()
                gerar_passos(lista)
                indice = 0
                rodando = False
                scroll_historico = 0

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
            desenhar_arvore(indice)

        desenhar_mensagem(passo)
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