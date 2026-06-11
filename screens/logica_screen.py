import pygame
import os
import random

from ui_components import LegoButton, draw_lego_brick


class LogicaScreen:
    def __init__(self, surf, largura, altura, cores, estado):
        self.surf = surf
        self.W = largura
        self.H = altura
        self.cores = cores
        self.estado = estado
        self.tick = 0

        self.FONT_BIG = pygame.font.SysFont("Impact", 56, bold=True)
        self.FONT_MED = pygame.font.SysFont("Impact", 42, bold=True)
        self.FONT_SM = pygame.font.SysFont("Impact", 28)

        self.bg = self.cores["cinza_esc"]

        # assets
        base = os.path.join(os.path.dirname(__file__), "..")
        self.ASSETS_DIR = os.path.normpath(os.path.join(base, "assets"))
        self.ANIMALS_DIR = os.path.join(self.ASSETS_DIR, "animais")
        self.OPCOES_DIR = os.path.join(self.ASSETS_DIR, "opcoes")

        # feedback images
        self.IMG_ACERTO = None
        self.IMG_ERRO = None
        for fn in ("Acertou.png", "Errou.png"):
            p = os.path.join(self.OPCOES_DIR, fn)
            if os.path.exists(p):
                try:
                    img = pygame.image.load(p).convert_alpha()
                    img = pygame.transform.smoothscale(img, (500, 300))
                    if fn == "Acertou.png":
                        self.IMG_ACERTO = img
                    else:
                        self.IMG_ERRO = img
                except Exception:
                    pass

        # exemplos de problemas lógicos (nome, patas serves as data placeholder)
        self.ITEMS = [
            {"nome": "gato", "patas": 4},
            {"nome": "cachorro", "patas": 4},
            {"nome": "elefante", "patas": 4},
            {"nome": "pato", "patas": 2},
        ]

        # botão voltar
        self.btn_voltar = LegoButton(40, self.H - 70, 200, 46,
                                     "◀ VOLTAR AO MAPA", self.cores["cinza_med"],
                                     pygame.font.SysFont("Impact", 20), studs=1)

        # estado do quiz
        self.reset_quiz()

    def reset_quiz(self):
        seq = self.ITEMS.copy()
        random.shuffle(seq)
        self.seq = seq
        self.index = 0
        self.pontos = 0
        self.state = "pergunta1"  # pergunta1, pergunta2, pergunta3, feedback
        self.feedback = None
        self.feedback_t0 = 0
        self.buttons = []
        self.prepare_question()

    def prepare_question(self):
        self.buttons = []
        if self.index >= len(self.seq):
            return
        item = self.seq[self.index]
        etapa = self.state
        
        # Cores LEGO para alternância
        cores_btns = [self.cores["vermelho"], self.cores["azul"], self.cores["amarelo"]]
        
        if etapa == "pergunta1":
            correto = len(item["nome"])
            opts = self._num_options(correto)
            for i, val in enumerate(opts):
                bx = 160 + i * 300
                cor = cores_btns[i % len(cores_btns)]
                self.buttons.append(LegoButton(bx, 480, 240, 90, str(val), cor,
                                             pygame.font.SysFont("Impact", 42, bold=True), studs=1))
        elif etapa == "pergunta2":
            correto = item["nome"][0]
            opts = self._letter_options(correto)
            for i, val in enumerate(opts):
                bx = 160 + i * 240
                cor = cores_btns[i % len(cores_btns)]
                self.buttons.append(LegoButton(bx, 480, 240, 90, val.upper(), cor,
                                             pygame.font.SysFont("Impact", 42, bold=True), studs=1))
        elif etapa == "pergunta3":
            correto = item["patas"]
            opts = self._num_options(correto)
            for i, val in enumerate(opts):
                bx = 160 + i * 300
                cor = cores_btns[i % len(cores_btns)]
                self.buttons.append(LegoButton(bx, 480, 240, 90, str(val), cor,
                                             pygame.font.SysFont("Impact", 42, bold=True), studs=1))

    def _num_options(self, correto):
        opts = {correto}
        while len(opts) < 3:
            delta = random.choice([-3, -2, -1, 1, 2, 3, 4])
            alt = max(0, correto + delta)
            opts.add(alt)
        l = list(opts)
        random.shuffle(l)
        return l

    def _letter_options(self, correta):
        letras = list("abcdefghijklmnopqrstuvwxyz")
        if correta.lower() in letras:
            letras.remove(correta.lower())
        escolhas = random.sample(letras, 3)
        escolhas.append(correta.lower())
        random.shuffle(escolhas)
        return escolhas

    def handle_events(self, eventos):
        for ev in eventos:
            if self.btn_voltar.handle_event(ev):
                self.estado["tela_atual"] = "mapa"
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                self.estado["tela_atual"] = "mapa"
            if self.state != "feedback":
                for b in self.buttons:
                    if b.handle_event(ev):
                        resp = b.texto  # LegoButton usa 'texto' não 'text'
                        item = self.seq[self.index]
                        if self.state == "pergunta1":
                            ok = (int(resp) == len(item["nome"]))
                        elif self.state == "pergunta2":
                            ok = (str(resp).upper() == item["nome"][0].upper())
                        else:
                            ok = (int(resp) == item["patas"])

                        if ok:
                            self.pontos += 1
                            self.feedback = "acerto"
                        else:
                            self.feedback = "erro"
                        self.state = "feedback"
                        self.feedback_t0 = pygame.time.get_ticks()
                        break

    def update(self):
        self.tick += 1
        if self.state == "feedback":
            t = pygame.time.get_ticks() - self.feedback_t0
            if t > 900:
                # avançar
                sample = self.buttons[0].texto if self.buttons else None  # LegoButton usa 'texto'
                if isinstance(sample, str) and sample.isalpha() and len(sample) == 1:
                    prev = 2
                else:
                    try:
                        if int(self.buttons[0].texto) == len(self.seq[self.index]["nome"]):  # LegoButton usa 'texto'
                            prev = 1
                        else:
                            prev = 3
                    except Exception:
                        prev = 1

                if prev == 1:
                    self.state = "pergunta2"
                    self.prepare_question()
                elif prev == 2:
                    self.state = "pergunta3"
                    self.prepare_question()
                else:
                    self.index += 1
                    if self.index >= len(self.seq):
                        # fim -> voltar ao mapa
                        self.estado["tela_atual"] = "mapa"
                    else:
                        self.state = "pergunta1"
                        self.prepare_question()
                self.feedback = None

    def draw(self):
        self.surf.fill(self.bg)
        
        # Título com sombra
        title = self.FONT_BIG.render("🐾 QUIZ DE ANIMAIS", True, (255, 255, 255))
        title_sombra = self.FONT_BIG.render("🐾 QUIZ DE ANIMAIS", True, (0, 0, 0))
        self.surf.blit(title_sombra, (42, 26))
        self.surf.blit(title, (40, 24))
        
        # Pontuação
        score_txt = self.FONT_SM.render(f"Pontos: {self.pontos}", True, (255, 255, 255))
        score_sombra = self.FONT_SM.render(f"Pontos: {self.pontos}", True, (0, 0, 0))
        self.surf.blit(score_sombra, (42, 92))
        self.surf.blit(score_txt, (40, 90))

        if self.index < len(self.seq):
            item = self.seq[self.index]
            # Painel com imagem do animal
            box = pygame.Rect(80, 140, 440, 300)
            pygame.draw.rect(self.surf, (220, 220, 220), box, border_radius=12)
            pygame.draw.rect(self.surf, (100, 100, 100), box, 2, border_radius=12)
            
            img_path = os.path.join(self.ANIMALS_DIR, f"{item['nome']}.png")
            if os.path.exists(img_path):
                try:
                    img = pygame.image.load(img_path).convert_alpha()
                    iw = box.width - 20
                    ih = box.height - 20
                    img = pygame.transform.smoothscale(img, (iw, ih))
                    self.surf.blit(img, (box.x + 10, box.y + 10))
                except Exception:
                    txt = self.FONT_MED.render(item["nome"].capitalize(), True, (30, 30, 30))
                    self.surf.blit(txt, (box.centerx - txt.get_width() // 2, box.centery - txt.get_height() // 2))
            else:
                txt = self.FONT_BIG.render(item["nome"].capitalize(), True, (30, 30, 30))
                self.surf.blit(txt, (box.centerx - txt.get_width() // 2, box.centery - txt.get_height() // 2))

            # Pergunta com sombra
            if self.state == "pergunta1":
                qtxt = self.FONT_MED.render("Quantas letras tem o nome?", True, (255, 255, 255))
                qtxt_sombra = self.FONT_MED.render("Quantas letras tem o nome?", True, (0, 0, 0))
                self.surf.blit(qtxt_sombra, (602, 202))
                self.surf.blit(qtxt, (600, 200))
            elif self.state == "pergunta2":
                qtxt = self.FONT_MED.render("Qual é a primeira letra?", True, (255, 255, 255))
                qtxt_sombra = self.FONT_MED.render("Qual é a primeira letra?", True, (0, 0, 0))
                self.surf.blit(qtxt_sombra, (602, 202))
                self.surf.blit(qtxt, (600, 200))
            elif self.state == "pergunta3":
                qtxt = self.FONT_MED.render("Quantas patas ele possui?", True, (255, 255, 255))
                qtxt_sombra = self.FONT_MED.render("Quantas patas ele possui?", True, (0, 0, 0))
                self.surf.blit(qtxt_sombra, (602, 202))
                self.surf.blit(qtxt, (600, 200))

        # feedback
        if self.state == "feedback":
            t = pygame.time.get_ticks() - self.feedback_t0
            if self.feedback == "acerto" and self.IMG_ACERTO:
                self.surf.blit(self.IMG_ACERTO, (300, 180))
            elif self.feedback == "erro" and self.IMG_ERRO:
                self.surf.blit(self.IMG_ERRO, (300, 180))
            else:
                msg = "✓ ACERTO!" if self.feedback == "acerto" else "✗ ERRO"
                c = (52, 211, 153) if self.feedback == "acerto" else (239, 68, 68)
                ttxt = self.FONT_BIG.render(msg, True, c)
                ttxt_sombra = self.FONT_BIG.render(msg, True, (0, 0, 0))
                self.surf.blit(ttxt_sombra, (self.W // 2 - ttxt.get_width() // 2 + 2, self.H // 2 - ttxt.get_height() // 2 + 2))
                self.surf.blit(ttxt, (self.W // 2 - ttxt.get_width() // 2, self.H // 2 - ttxt.get_height() // 2))

        # desenhar botões
        if self.state != "feedback":
            for b in self.buttons:
                b.draw(self.surf)

        # botão voltar
        self.btn_voltar.draw(self.surf)
