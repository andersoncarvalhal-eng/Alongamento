import time
from geometria import calcular_angulo, calcular_inclinacao_vertical

# Indices oficiais do MediaPipe Pose (33 landmarks)
OMBRO_ESQ, OMBRO_DIR = 11, 12
COTOVELO_ESQ, COTOVELO_DIR = 13, 14
PUNHO_ESQ, PUNHO_DIR = 15, 16
QUADRIL_ESQ, QUADRIL_DIR = 23, 24
JOELHO_ESQ, JOELHO_DIR = 25, 26
TORNOZELO_ESQ, TORNOZELO_DIR = 27, 28


class GerenciadorAlongamentos:
    def __init__(self, tempo_alvo: float = 5.0):
        self.tempo_alvo = tempo_alvo
        self.indice_atual = 0
        self.inicio_sustentacao = None
        self.tempo_acumulado = 0.0
        self.historico_amplitudes = {i: [] for i in range(4)}
        self.historico_amplitudes_validas = {i: [] for i in range(4)}

        self.exercicios = [
            {
                "nome": "1. Elevacao de Bracos (Ombros)",
                "grupo": "Membros Superiores",
                "instrucao": "Estenda os dois bracos acima da cabeca",
                "alvo_texto": "Ombro >= 150 deg",
                "avaliar": self._avaliar_elevacao_bracos,
            },
            {
                "nome": "2. Inclinacao Lateral de Tronco",
                "grupo": "Membros Superiores / Tronco",
                "instrucao": "Eleve um braco e incline o tronco lateralmente",
                "alvo_texto": "Tronco >= 18 deg | Braco >= 145 deg",
                "avaliar": self._avaliar_inclinacao_lateral,
            },
            {
                "nome": "3. Alongamento de Quadriceps",
                "grupo": "Membros Inferiores",
                "instrucao": "Em pe, flexione um joelho levando o pe atras",
                "alvo_texto": "Joelho <= 65 deg | Apoio >= 155 deg",
                "avaliar": self._avaliar_quadriceps,
            },
            {
                "nome": "4. Afundo (Flexores do Quadril)",
                "grupo": "Membros Inferiores",
                "instrucao": "De um passo a frente e flexione o joelho dianteiro",
                "alvo_texto": "Joelho frente: 80-115 deg | Tras >= 150 deg",
                "avaliar": self._avaliar_afundo,
            },
        ]

        self.resultados = [
            {
                "nome": ex["nome"],
                "concluido": False,
                "amplitude_max": 0.0,
                "tempo_total": 0.0,
            }
            for ex in self.exercicios
        ]

    def _avaliar_elevacao_bracos(self, pts: dict):
        ombro_e = calcular_angulo(pts, QUADRIL_ESQ, OMBRO_ESQ, COTOVELO_ESQ)
        ombro_d = calcular_angulo(pts, QUADRIL_DIR, OMBRO_DIR, COTOVELO_DIR)
        cotov_e = calcular_angulo(pts, OMBRO_ESQ, COTOVELO_ESQ, PUNHO_ESQ)
        cotov_d = calcular_angulo(pts, OMBRO_DIR, COTOVELO_DIR, PUNHO_DIR)

        if None in (ombro_e, ombro_d, cotov_e, cotov_d):
            return False, 0.0, [], "Posicione tronco e bracos na camera"

        amplitude = min(ombro_e, ombro_d)
        valido = (ombro_e >= 150.0 and ombro_d >= 150.0) and (cotov_e >= 145.0 and cotov_d >= 145.0)
        articulacoes = [
            (OMBRO_ESQ, f"{int(ombro_e)} deg"),
            (OMBRO_DIR, f"{int(ombro_d)} deg"),
        ]
        feedback = "Mantenha a extensao!" if valido else "Eleve mais os bracos e estique os cotovelos"
        return valido, amplitude, articulacoes, feedback

    def _avaliar_inclinacao_lateral(self, pts: dict):
        inc_e = calcular_inclinacao_vertical(pts, QUADRIL_ESQ, OMBRO_ESQ)
        inc_d = calcular_inclinacao_vertical(pts, QUADRIL_DIR, OMBRO_DIR)
        ombro_e = calcular_angulo(pts, QUADRIL_ESQ, OMBRO_ESQ, COTOVELO_ESQ)
        ombro_d = calcular_angulo(pts, QUADRIL_DIR, OMBRO_DIR, COTOVELO_DIR)

        if None in (inc_e, inc_d, ombro_e, ombro_d):
            return False, 0.0, [], "Enquadre quadril, ombros e bracos"

        inclinacao = max(inc_e, inc_d)
        braco_max = max(ombro_e, ombro_d)
        valido = (18.0 <= inclinacao <= 45.0) and (braco_max >= 145.0)
        articulacoes = [
            (OMBRO_ESQ, f"Tronco: {int(inclinacao)} deg"),
            (OMBRO_DIR, f"Braco: {int(braco_max)} deg"),
        ]
        feedback = "Otima inclinacao!" if valido else "Incline mais o tronco com o braco elevado"
        return valido, inclinacao, articulacoes, feedback

    def _avaliar_quadriceps(self, pts: dict):
        joelho_e = calcular_angulo(pts, QUADRIL_ESQ, JOELHO_ESQ, TORNOZELO_ESQ)
        joelho_d = calcular_angulo(pts, QUADRIL_DIR, JOELHO_DIR, TORNOZELO_DIR)

        if joelho_e is None or joelho_d is None:
            return False, 0.0, [], "Afaste-se para mostrar o corpo inteiro"

        # Um joelho flexionado (<= 65) e o outro estendido de apoio (>= 155)
        esq_flex = joelho_e <= 65.0 and joelho_d >= 155.0
        dir_flex = joelho_d <= 65.0 and joelho_e >= 155.0
        valido = esq_flex or dir_flex

        # Amplitude de flexao (quanto menor o angulo do joelho, maior o alongamento)
        menor_angulo = min(joelho_e, joelho_d)
        amplitude_alongamento = max(0.0, 180.0 - menor_angulo)

        articulacoes = [
            (JOELHO_ESQ, f"{int(joelho_e)} deg"),
            (JOELHO_DIR, f"{int(joelho_d)} deg"),
        ]
        feedback = "Equilibrio perfeito!" if valido else "Puxe o calcanhar em direcao ao quadril"
        return valido, amplitude_alongamento, articulacoes, feedback

    def _avaliar_afundo(self, pts: dict):
        joelho_e = calcular_angulo(pts, QUADRIL_ESQ, JOELHO_ESQ, TORNOZELO_ESQ)
        joelho_d = calcular_angulo(pts, QUADRIL_DIR, JOELHO_DIR, TORNOZELO_DIR)

        if joelho_e is None or joelho_d is None:
            return False, 0.0, [], "Mostre as duas pernas de perfil/diagonal"

        caso_1 = (80.0 <= joelho_e <= 115.0) and (joelho_d >= 150.0)
        caso_2 = (80.0 <= joelho_d <= 115.0) and (joelho_e >= 150.0)
        valido = caso_1 or caso_2

        # Amplitude real de flexao do joelho da frente
        amplitude = max(0.0, 180.0 - min(joelho_e, joelho_d))
        articulacoes = [
            (JOELHO_ESQ, f"{int(joelho_e)} deg"),
            (JOELHO_DIR, f"{int(joelho_d)} deg"),
        ]
        feedback = "Postura de afundo valida!" if valido else "Flexione o joelho da frente (90 deg) e estique o de tras"
        return valido, amplitude, articulacoes, feedback

    def atualizar(self, pts: dict):
        if self.indice_atual >= len(self.exercicios):
            return {
                "finalizado": True,
                "exercicio": self.exercicios[-1],
                "valido": True,
                "progresso": 1.0,
                "tempo_restante": 0.0,
                "amplitude": 0.0,
                "articulacoes": [],
                "feedback": "Treino concluido! Pressione Q para ver o grafico.",
            }

        ex = self.exercicios[self.indice_atual]
        valido, amplitude, articulacoes, feedback = ex["avaliar"](pts)

        if amplitude > 0:
            self.historico_amplitudes[self.indice_atual].append(amplitude)
            if valido:
                self.historico_amplitudes_validas[self.indice_atual].append(amplitude)
            if amplitude > self.resultados[self.indice_atual]["amplitude_max"]:
                self.resultados[self.indice_atual]["amplitude_max"] = amplitude

        agora = time.perf_counter()
        if valido:
            if self.inicio_sustentacao is None:
                self.inicio_sustentacao = agora
            self.tempo_acumulado = agora - self.inicio_sustentacao
        else:
            # Decaimento suave em vez de zerar abruptamente por 1 frame de ruido
            if self.inicio_sustentacao is not None:
                self.tempo_acumulado = max(0.0, self.tempo_acumulado - 0.08)
                self.inicio_sustentacao = (
                    agora - self.tempo_acumulado if self.tempo_acumulado > 0 else None
                )

        progresso = min(1.0, self.tempo_acumulado / self.tempo_alvo)
        self.resultados[self.indice_atual]["tempo_total"] = max(
            self.resultados[self.indice_atual]["tempo_total"], self.tempo_acumulado
        )

        if self.tempo_acumulado >= self.tempo_alvo:
            self.resultados[self.indice_atual]["concluido"] = True
            self.indice_atual += 1
            self.inicio_sustentacao = None
            self.tempo_acumulado = 0.0

        return {
            "finalizado": self.indice_atual >= len(self.exercicios),
            "exercicio": ex,
            "valido": valido,
            "progresso": progresso,
            "tempo_restante": max(0.0, self.tempo_alvo - self.tempo_acumulado),
            "amplitude": amplitude,
            "articulacoes": articulacoes,
            "feedback": feedback,
        }

    def pular_exercicio(self):
        if self.indice_atual < len(self.exercicios):
            self.indice_atual += 1
            self.inicio_sustentacao = None
            self.tempo_acumulado = 0.0

    def resetar(self):
        self.__init__(tempo_alvo=self.tempo_alvo)