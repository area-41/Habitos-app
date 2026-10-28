# ==========================================================
# PAINEL DE HÁBITOS · FLET EDITION
# Projeto exemplo — Semana 8 · Programação Web Front-End
#
# OBJETIVO DIDÁTICO DO ARQUIVO
# ----------------------------------------------------------
# Este script foi comentado de forma detalhada para servir
# como material de estudo para quem nunca teve contato com
# Flet.
#
# O Flet permite construir interfaces gráficas usando Python.
# Em vez de escrever HTML, CSS e JavaScript, criamos objetos
# Python como ft.Text, ft.Button, ft.Container, ft.Row e
# ft.Column.
#
# A ideia central é semelhante à de frameworks modernos como
# React e Flutter: a interface é uma árvore de componentes.
# Cada componente pode conter outros componentes, formando a
# tela final.
# ==========================================================

# Importamos a biblioteca Flet e damos a ela o apelido ft.
# Esse apelido é uma convenção comum na documentação do Flet.
import flet as ft
import os
# dataclass é usado para criar classes simples de dados
from dataclasses import dataclass, field

# datetime será usado apenas para exibir a data atual no cabeçalho.
from datetime import datetime


# ----------------------------------------------------------
# PALETA DE CORES
# ----------------------------------------------------------
# Em HTML/CSS, normalmente colocaríamos essas cores em um
# arquivo .css. Aqui, como estamos usando Flet, armazenamos
# as cores em constantes Python.
#
# O uso de constantes facilita a manutenção: se quisermos
# mudar a cor principal do sistema, alteramos em apenas um
# lugar.
# ----------------------------------------------------------
COR_FUNDO        = "#0d1117"  # fundo geral da aplicação
COR_SUPERFICIE   = "#161b22"  # cor dos blocos principais
COR_SUPERFICIE_2 = "#1c2128"  # cor secundária para cartões/ícones
COR_BORDA        = "#3d444d"  # cor das bordas
COR_ACCENT       = "#1f6feb"  # cor principal dos botões
COR_ACCENT_HOVER = "#58a6ff"  # azul mais claro para destaques
COR_SUCESSO      = "#2ea043"  # verde usado para hábito concluído
COR_SUCESSO_BG   = "#1b3a24"  # fundo verde escuro de item concluído
COR_ERRO         = "#f85149"  # vermelho para mensagens de erro
COR_TEXTO        = "#f0f6fc"  # texto principal, com alto contraste
COR_TEXTO_SEC    = "#c9d1d9"  # texto secundário
COR_TEXTO_MUTED  = "#a5b1c2"  # texto de dica/placeholder


# ----------------------------------------------------------
# ÍCONES DISPONÍVEIS
# ----------------------------------------------------------
# O Flet já fornece vários ícones prontos por meio de ft.icons.
# Aqui criamos uma lista com os ícones que o usuário poderá
# escolher ao cadastrar um novo hábito.
# ----------------------------------------------------------
ICONES_DISPONIVEIS = [
    ft.icons.WATER_DROP_OUTLINED,
    ft.icons.FITNESS_CENTER,
    ft.icons.MENU_BOOK_OUTLINED,
    ft.icons.BEDTIME_OUTLINED,
    ft.icons.SELF_IMPROVEMENT,
    ft.icons.DIRECTIONS_RUN,
    ft.icons.CODE,
    ft.icons.RESTAURANT_OUTLINED,
]


# ----------------------------------------------------------
# MODELO DE DADOS
# ----------------------------------------------------------
# Antes de construir a interface, definimos quais dados nossa
# aplicação manipula.
#
# Este projeto tem uma lista de hábitos. Cada hábito possui:
# - nome: texto que aparece no cartão;
# - icone: ícone visual associado ao hábito;
# - concluido: indica se o hábito foi marcado como feito;
# - sequencia: quantidade fictícia de dias seguidos.
# ----------------------------------------------------------
@dataclass
class Habito:
    nome: str
    icone: str
    concluido: bool = False
    sequencia: int = 0


@dataclass
class EstadoApp:
    # default_factory=list cria uma nova lista para cada EstadoApp.
    habitos: list = field(default_factory=list)


# ----------------------------------------------------------
# CLASSE PRINCIPAL DA APLICAÇÃO
# ----------------------------------------------------------
# A classe PainelHabitos concentra a aplicação inteira.
#
# Em um projeto maior, poderíamos separar em vários arquivos:
# - modelos de dados;
# - componentes;
# - serviços;
# - estado;
# - telas.
#
# Para um primeiro contato com Flet, ficou tudo em 
# um único arquivo para facilitar a leitura e a explicação.
# ----------------------------------------------------------
class PainelHabitos:
    def __init__(self, page: ft.Page):
        # page é o objeto principal do Flet.
        # Ele representa a janela/aba onde a aplicação será exibida.
        # Tudo que aparece na interface precisa ser adicionado à page.
        self.page = page

        # Estado inicial da aplicação.
        # Em aplicações interativas, o estado é a memória da interface.
        # Aqui ele guarda a lista de hábitos exibidos na tela.
        self.estado = EstadoApp(habitos=[
            Habito("Beber 2L de água", ft.icons.WATER_DROP_OUTLINED, sequencia=4),
            Habito("Treinar 30 minutos", ft.icons.FITNESS_CENTER, sequencia=2),
            Habito("Ler 10 páginas", ft.icons.MENU_BOOK_OUTLINED, sequencia=7),
            Habito("Dormir antes da meia-noite", ft.icons.BEDTIME_OUTLINED, sequencia=1),
        ])

        # Ícone selecionado no formulário de novo hábito.
        # Começamos selecionando o primeiro ícone da lista.
        self._icone_selecionado = ICONES_DISPONIVEIS[0]

        # --------------------------------------------------
        # Componentes que precisam ser reaproveitados
        # --------------------------------------------------
        # Alguns componentes são criados uma única vez porque
        # seus valores mudam ao longo da execução.
        #
        # Exemplo: texto_progresso começa como "0 de 0 concluídos",
        # mas depois passa a mostrar "2 de 4 concluídos".
        #
        # Em Flet, podemos alterar propriedades de um componente já
        # criado e depois chamar page.update() para redesenhar a tela.
        # --------------------------------------------------
        self.coluna_habitos = ft.Column(spacing=12)

        self.texto_progresso = ft.Text(
            "0 de 0 concluídos",
            size=13,
            color=COR_TEXTO_SEC,
            weight=ft.FontWeight.W_600,
        )

        self.barra_progresso = ft.ProgressBar(
            value=0,                 # valor entre 0 e 1
            color=COR_ACCENT_HOVER,  # cor da parte preenchida
            bgcolor=COR_BORDA,       # cor do fundo da barra
            height=8,
            border_radius=10,
        )

        # Campo de texto usado na tela de cadastro.
        # O TextField equivale, conceitualmente, a um <input> em HTML.
        self.campo_nome_habito = ft.TextField(
            label="Nome do hábito",
            hint_text="Ex: Meditar 10 minutos",
            border_color=COR_BORDA,
            focused_border_color=COR_ACCENT_HOVER,
            color=COR_TEXTO,
            cursor_color=COR_ACCENT_HOVER,
            label_style=ft.TextStyle(color=COR_TEXTO_SEC),
            hint_style=ft.TextStyle(color=COR_TEXTO_MUTED),
            bgcolor=COR_SUPERFICIE,
            border_radius=10,
        )

        # Linha que receberá os ícones disponíveis.
        # wrap=True permite que os ícones quebrem para a próxima linha
        # caso não caibam horizontalmente.
        self.linha_icones = ft.Row(spacing=10, wrap=True)

        # Dicionário que associa cada ícone ao seu Container visual.
        # Isso facilita alterar a aparência do ícone selecionado.
        self._containers_icone = {}

        # Configura a janela/página e monta o seletor de ícones.
        self._configurar_pagina()
        self._montar_seletor_icones()

    # ------------------------------------------------------
    # CONFIGURAÇÃO DA PÁGINA
    # ------------------------------------------------------
    def _configurar_pagina(self):
        # Título exibido na aba do navegador ou na janela do app.
        self.page.title = "Painel de Hábitos"

        # Define o tema escuro do Flet.
        self.page.theme_mode = ft.ThemeMode.DARK

        # Cor de fundo geral da aplicação.
        self.page.bgcolor = COR_FUNDO

        # Remove espaçamentos padrão da página.
        self.page.padding = 0
        self.page.spacing = 0

        # Define uma fonte externa.
        # O Flet baixa e usa essa fonte na renderização da interface.
        self.page.fonts = {
            "Inter": "https://raw.githubusercontent.com/google/fonts/main/ofl/inter/Inter%5Bslnt%2Cwght%5D.ttf"
        }

        # Aplica a fonte e uma cor-base para o tema.
        self.page.theme = ft.Theme(
            font_family="Inter",
            color_scheme_seed=COR_ACCENT,
        )

        # Configura o tamanho inicial da janela.
        # Mesmo rodando no navegador, esses valores ajudam quando
        # executamos o app como janela desktop.
        self.page.window.width = 460
        self.page.window.height = 800
        self.page.window.min_width = 380

    # ------------------------------------------------------
    # TROCA DE TELAS — SEM ROTAS, SEM VIEWS
    # ------------------------------------------------------
    # O Flet possui sistema de rotas, semelhante a navegação entre
    # páginas. Para este projeto simplificado, usamos uma abordagem 
    # mais simples: limpamos a tela atual e adicionamos uma nova 
    # árvore de componentes.
    # ------------------------------------------------------
    def _mostrar(self, *controles):
        # Remove todos os componentes atualmente exibidos na página.
        self.page.clean()

        # Adiciona uma coluna principal contendo os controles recebidos.
        # Essa coluna funciona como a estrutura vertical da tela.
        self.page.add(
            ft.Column(
                expand=True,             # ocupa todo o espaço disponível
                spacing=0,               # sem espaço entre cabeçalho e corpo
                controls=list(controles), # componentes que formam a tela
            )
        )

        # Solicita ao Flet que envie as mudanças para a interface.
        # Sem update(), alterações nos componentes podem não aparecer.
        self.page.update()

    def _mostrar_principal(self):
        # Antes de mostrar a tela principal, recalculamos a lista de
        # hábitos e o progresso. Assim a tela sempre aparece atualizada.
        self._atualizar_lista_habitos()

        # A tela principal é formada por cabeçalho + corpo.
        self._mostrar(
            self._cabecalho_principal(),
            self._corpo_principal(),
        )

    def _mostrar_novo_habito(self):
        # A tela de cadastro também é formada por cabeçalho + corpo.
        self._mostrar(
            self._cabecalho_novo_habito(),
            self._corpo_novo_habito(),
        )

    # ------------------------------------------------------
    # COMPONENTES DE INTERFACE
    # ------------------------------------------------------
    # Cada método abaixo retorna um componente Flet.
    #
    # Essa é uma forma importante de organizar a aplicação: em vez de
    # escrever toda a interface em um único bloco enorme, criamos
    # pequenos componentes reutilizáveis.
    # ------------------------------------------------------
    def _cabecalho_principal(self) -> ft.Container:
        # Container é um componente genérico de agrupamento.
        # Ele pode ter cor de fundo, borda, padding, alinhamento e
        # um conteúdo interno.
        return ft.Container(
            padding=ft.Padding(left=24, right=24, top=28, bottom=20),
            bgcolor=COR_SUPERFICIE,
            border=ft.border(bottom=ft.BorderSide(1, COR_BORDA)),
            content=ft.Column(
                spacing=4,
                controls=[
                    ft.Row(
                        # SPACE_BETWEEN coloca o primeiro bloco à esquerda
                        # e o segundo à direita.
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Column(
                                spacing=2,
                                controls=[
                                    ft.Text(
                                        "Painel de Hábitos",
                                        size=22,
                                        weight=ft.FontWeight.W_800,
                                        color=COR_TEXTO,
                                    ),
                                    ft.Text(
                                        self._data_formatada(),
                                        size=12,
                                        color=COR_TEXTO_SEC,
                                    ),
                                ],
                            ),
                            ft.Container(
                                bgcolor="#1f6feb2e",
                                border=ft.border.all(1, COR_ACCENT_HOVER),
                                border_radius=999,
                                padding=ft.Padding(left=12, right=12, top=6, bottom=6),
                                content=ft.Text(
                                    "🔥 Sequência ativa",
                                    size=11,
                                    color=COR_ACCENT_HOVER,
                                    weight=ft.FontWeight.W_700,
                                ),
                            ),
                        ],
                    ),
                ],
            ),
        )

    def _cabecalho_novo_habito(self) -> ft.Container:
        # Cabeçalho da tela de cadastro.
        # Possui um botão de voltar e o título da tela.
        return ft.Container(
            padding=ft.Padding(left=16, right=24, top=24, bottom=20),
            bgcolor=COR_SUPERFICIE,
            border=ft.border(bottom=ft.BorderSide(1, COR_BORDA)),
            content=ft.Row(
                vertical_alignment=ft.CrossAxisAlignment.center,
                controls=[
                    ft.IconButton(
                        icon=ft.icons.ARROW_BACK_IOS_NEW,
                        icon_color=COR_TEXTO,
                        icon_size=18,
                        # on_click recebe uma função que será executada
                        # quando o usuário clicar no botão.
                        on_click=lambda e: self._mostrar_principal(),
                    ),
                    ft.Text(
                        "Novo Hábito",
                        size=19,
                        weight=ft.FontWeight.W_700,
                        color=COR_TEXTO,
                    ),
                ],
            ),
        )

    def _corpo_principal(self) -> ft.Container:
        # Corpo da tela principal.
        # Ele contém o cartão de progresso, a lista de hábitos e o botão
        # para abrir a tela de cadastro.
        return ft.Container(
            expand=True,
            padding=ft.Padding(left=20, right=20, top=20, bottom=20),
            content=ft.Column(
                expand=True,
                spacing=18,
                controls=[
                    self._cartao_progresso(),
                    ft.Text(
                        "Hábitos de hoje",
                        size=14,
                        weight=ft.FontWeight.W_700,
                        color=COR_TEXTO_SEC,
                    ),
                    ft.Container(
                        expand=True,
                        content=ft.Column(
                            expand=True,
                            # scroll=ft.ScrollMode.AUTO cria rolagem quando
                            # houver muitos hábitos para caber na tela.
                            scroll=ft.ScrollMode.AUTO,
                            controls=[self.coluna_habitos],
                        ),
                    ),
                    ft.Button(
                        content=ft.Text(
                            "+  Adicionar hábito",
                            size=15,
                            weight=ft.FontWeight.W_700,
                            color="#ffffff",
                        ),
                        bgcolor=COR_ACCENT,
                        height=48,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=12),
                        ),
                        # Ao clicar, mostramos a tela de novo hábito.
                        on_click=lambda e: self._mostrar_novo_habito(),
                        width=220,
                    ),
                ],
            ),
        )

    def _cartao_progresso(self) -> ft.Container:
        # Cartão superior com texto e barra de progresso.
        # Note que texto_progresso e barra_progresso foram criados no
        # __init__, pois seus valores mudam conforme o usuário marca
        # hábitos como concluídos.
        return ft.Container(
            padding=20,
            bgcolor=COR_SUPERFICIE,
            border=ft.border.all(1, COR_BORDA),
            border_radius=16,
            content=ft.Column(
                spacing=10,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text(
                                "Progresso de hoje",
                                size=13,
                                color=COR_TEXTO_SEC,
                                weight=ft.FontWeight.W_700,
                            ),
                            self.texto_progresso,
                        ],
                    ),
                    self.barra_progresso,
                ],
            ),
        )

    def _corpo_novo_habito(self) -> ft.Container:
        # Corpo da tela de cadastro.
        # Contém campo de texto, seletor de ícones e botão de salvar.
        return ft.Container(
            expand=True,
            padding=ft.Padding(left=20, right=20, top=20, bottom=20),
            content=ft.Column(
                spacing=22,
                controls=[
                    self.campo_nome_habito,
                    ft.Column(
                        spacing=10,
                        controls=[
                            ft.Text(
                                "Escolha um ícone",
                                size=13,
                                color=COR_TEXTO_SEC,
                                weight=ft.FontWeight.W_700,
                            ),
                            self.linha_icones,
                        ],
                    ),
                    # Este Container expandido empurra o botão para baixo,
                    # ocupando o espaço livre entre o seletor e o botão.
                    ft.Container(expand=True),
                    ft.Button(
                        content=ft.Text(
                            "Salvar hábito",
                            size=15,
                            weight=ft.FontWeight.W_700,
                            color="#ffffff",
                        ),
                        bgcolor=COR_ACCENT,
                        height=48,
                        width=220,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=12),
                        ),
                        # Aqui passamos o método diretamente, sem lambda.
                        # O Flet enviará o evento de clique como argumento.
                        on_click=self._salvar_novo_habito,
                    ),
                ],
            ),
        )

    def _montar_seletor_icones(self):
        # Recria visualmente os botões de ícone.
        # Chamamos este método no início e também após salvar um hábito,
        # para voltar ao primeiro ícone selecionado.
        self._containers_icone.clear()
        self.linha_icones.controls.clear()

        for icone in ICONES_DISPONIVEIS:
            selecionado = icone == self._icone_selecionado

            container = ft.Container(
                width=52,
                height=52,
                border_radius=12,
                bgcolor=COR_ACCENT if selecionado else COR_SUPERFICIE_2,
                border=ft.border.all(1, COR_ACCENT_HOVER if selecionado else COR_BORDA),
                alignment=ft.alignment.center,
                content=ft.Icon(
                    icone,
                    color="#ffffff" if selecionado else COR_TEXTO_SEC,
                    size=24,
                ),
                # Atenção ao padrão lambda e variável de loop:
                # usamos ic=icone para "congelar" o valor atual do ícone.
                # Sem isso, todos os cliques poderiam apontar para o último
                # valor da variável icone no loop.
                on_click=lambda e, ic=icone: self._selecionar_icone(ic),
                animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
            )

            # Guardamos o container em um dicionário para conseguir alterar
            # sua aparência posteriormente, quando o usuário selecionar outro
            # ícone.
            self._containers_icone[icone] = container
            self.linha_icones.controls.append(container)

    def _selecionar_icone(self, icone: str):
        # Atualiza o ícone atualmente selecionado.
        self._icone_selecionado = icone

        # Percorre todos os containers de ícones e aplica estilos diferentes
        # para o selecionado e para os não selecionados.
        for ic, container in self._containers_icone.items():
            selecionado = ic == icone
            container.bgcolor = COR_ACCENT if selecionado else COR_SUPERFICIE_2
            container.border = ft.border.all(1, COR_ACCENT_HOVER if selecionado else COR_BORDA)
            container.content.color = "#ffffff" if selecionado else COR_TEXTO_SEC

        self.page.update()

    # ------------------------------------------------------
    # HANDLERS DE EVENTO
    # ------------------------------------------------------
    # Handler é uma função executada em resposta a um evento do usuário.
    # Exemplos de eventos: clique, digitação, alteração de seleção etc.
    #
    # Em JavaScript, usaríamos addEventListener.
    # Em Flet, passamos funções Python para propriedades como on_click.
    # ------------------------------------------------------
    def _alternar_conclusao(self, habito: Habito):
        # Inverte o valor booleano.
        # Se estava False, vira True. Se estava True, vira False.
        habito.concluido = not habito.concluido

        # Recria a lista visual de hábitos e recalcula progresso.
        self._atualizar_lista_habitos()
        self.page.update()

    def _excluir_habito(self, habito: Habito):
        # Remove o hábito da lista de dados.
        self.estado.habitos.remove(habito)

        # Atualiza a interface para refletir a remoção.
        self._atualizar_lista_habitos()
        self.page.update()

    def _salvar_novo_habito(self, _e):
        # Lê o valor digitado no TextField.
        # O "or \"\"" evita erro caso value seja None.
        # strip() remove espaços no início e no final.
        nome = (self.campo_nome_habito.value or "").strip()

        # Validação simples: não permitir hábito sem nome.
        if not nome:
            self.campo_nome_habito.error_text = "Digite um nome para o hábito"
            self.page.update()
            return

        # Cria um novo objeto Habito usando o nome digitado e o ícone
        # selecionado no formulário.
        novo = Habito(nome=nome, icone=self._icone_selecionado)
        self.estado.habitos.append(novo)

        # Limpa o formulário para o próximo cadastro.
        self.campo_nome_habito.value = ""
        self.campo_nome_habito.error_text = None
        self._icone_selecionado = ICONES_DISPONIVEIS[0]
        self._montar_seletor_icones()

        # Após salvar, voltamos para a tela principal.
        self._mostrar_principal()

    def _atualizar_lista_habitos(self):
        # Remove todos os cartões atualmente exibidos na coluna.
        # Depois, recriamos a lista com base no estado atual.
        self.coluna_habitos.controls.clear()

        if not self.estado.habitos:
            # Caso a lista esteja vazia, exibimos uma mensagem amigável.
            self.coluna_habitos.controls.append(
                ft.Container(
                    padding=30,
                    alignment=ft.alignment.center,
                    content=ft.Text(
                        "Nenhum hábito cadastrado ainda.",
                        color=COR_TEXTO_SEC,
                        size=13,
                        italic=True,
                    ),
                )
            )
        else:
            # Para cada hábito da lista de dados, criamos um cartão visual.
            for habito in self.estado.habitos:
                self.coluna_habitos.controls.append(self._cartao_habito(habito))

        # Recalcula o progresso.
        total = len(self.estado.habitos)
        concluidos = sum(1 for h in self.estado.habitos if h.concluido)

        # Atualiza o texto e o valor da barra.
        self.texto_progresso.value = f"{concluidos} de {total} concluídos"
        self.barra_progresso.value = (concluidos / total) if total > 0 else 0

    def _cartao_habito(self, habito: Habito) -> ft.Container:
        # Cria o cartão visual de um hábito específico.
        # Este método é chamado para cada item da lista de hábitos.
        return ft.Container(
            padding=ft.Padding(left=16, right=16, top=14, bottom=14),
            bgcolor=COR_SUCESSO_BG if habito.concluido else COR_SUPERFICIE,
            border=ft.border.all(1, COR_SUCESSO if habito.concluido else COR_BORDA),
            border_radius=14,
            animate=ft.Animation(180, ft.AnimationCurve.EASE_OUT),
            content=ft.Row(
                vertical_alignment=ft.CrossAxisAlignment.center,
                spacing=12,
                controls=[
                    # Bloco visual do ícone.
                    ft.Container(
                        width=42,
                        height=42,
                        border_radius=10,
                        bgcolor=COR_SUCESSO if habito.concluido else COR_SUPERFICIE_2,
                        alignment=ft.alignment.center,
                        content=ft.Icon(
                            habito.icone,
                            color="#ffffff" if habito.concluido else COR_TEXTO_SEC,
                            size=20,
                        ),
                    ),
                    # Coluna de textos: nome do hábito + sequência.
                    ft.Column(
                        expand=True,
                        spacing=2,
                        controls=[
                            ft.Text(
                                habito.nome,
                                size=14.5,
                                weight=ft.FontWeight.W_700,
                                color=COR_TEXTO,
                                style=ft.TextStyle(
                                    # Se o hábito estiver concluído, aplicamos
                                    # texto riscado, como em uma checklist.
                                    decoration=ft.TextDecoration.LINE_THROUGH
                                    if habito.concluido
                                    else None,
                                ),
                            ),
                            ft.Text(
                                f"🔥 {habito.sequencia} dias seguidos"
                                if habito.sequencia
                                else "Novo hábito",
                                size=11.5,
                                color=COR_TEXTO_SEC,
                                weight=ft.FontWeight.W_500,
                            ),
                        ],
                    ),
                    # Botão de excluir.
                    ft.IconButton(
                        icon=ft.icons.DELETE_OUTLINE,
                        icon_color=COR_TEXTO_SEC,
                        icon_size=18,
                        tooltip="Excluir hábito",
                        on_click=lambda e, h=habito: self._excluir_habito(h),
                    ),
                    # Círculo clicável usado para marcar/desmarcar conclusão.
                    ft.Container(
                        width=30,
                        height=30,
                        border_radius=999,
                        bgcolor=COR_SUCESSO if habito.concluido else "transparent",
                        border=ft.border.all(
                            1.5,
                            COR_SUCESSO if habito.concluido else COR_TEXTO_SEC,
                        ),
                        alignment=ft.alignment.center,
                        on_click=lambda e, h=habito: self._alternar_conclusao(h),
                        animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
                        content=ft.Icon(
                            ft.icons.CHECK,
                            color="#ffffff",
                            size=16,
                        ) if habito.concluido else None,
                    ),
                ],
            ),
        )

    @staticmethod
    def _data_formatada() -> str:
        # Método utilitário para exibir a data atual em português.
        # staticmethod indica que este método não depende de self.
        dias = ["segunda", "terça", "quarta", "quinta", "sexta", "sábado", "domingo"]
        meses = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]
        agora = datetime.now()
        dia_semana = dias[agora.weekday()]
        return f"{dia_semana}, {agora.day} de {meses[agora.month - 1]}".capitalize()


# ----------------------------------------------------------
# PONTO DE ENTRADA DA APLICAÇÃO
# ----------------------------------------------------------
# Em Flet, a função main recebe a page. A page é criada pelo
# próprio Flet e entregue para nossa aplicação.
# ----------------------------------------------------------
def main(page: ft.Page):
    # Criamos a aplicação, passando a page para a classe principal.
    app = PainelHabitos(page)

    # A montagem inicial é explícita: mostramos a tela principal.
    # Isso deixa claro para o aluno onde a interface começa.
    app._mostrar_principal()


# ----------------------------------------------------------
# EXECUÇÃO DO SCRIPT
# ----------------------------------------------------------
# Este bloco só é executado quando o arquivo é rodado diretamente,
# por exemplo:
#
#     python habitos_app_comentado.py
#
# ft.run inicia a aplicação Flet.
# view=ft.AppView.WEB_BROWSER abre a aplicação no navegador.
# port=7860 define a porta local usada pelo servidor do Flet.
# Remova os parâmetros "view" e "port" para executar como 
# uma aplicação desktop
# ----------------------------------------------------------
if __name__ == "__main__":
    #ft.run(main, view=ft.AppView.WEB_BROWSER, port=7860)
    # O Render injeta a porta na variável de ambiente PORT (padrão é 10000 se não encontrar)
    port = int(os.environ.get("PORT", 10000))
    
    # Executa como servidor web acessível na nuvem
    ft.app(
        target=main,
        view=None,  # Sem interface nativa/desktop, roda apenas via web server
        port=port,
        host="0.0.0.0"
    )