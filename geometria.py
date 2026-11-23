import numpy as np


class SuavizadorLandmarks:
    """Aplica Media Movel Exponencial (EMA) para estabilizar os 33 landmarks."""

    def __init__(self, alpha: float = 0.55):
        self.alpha = alpha
        self.historico = {}

    def atualizar(self, landmarks, largura: int, altura: int) -> dict:
        pontos_suavizados = {}
        for idx, lm in enumerate(landmarks):
            # Converte coordenadas normalizadas para pixels reais (evita distorcao 16:9)
            coord_atual = np.array([lm.x * largura, lm.y * altura], dtype=np.float32)

            if idx in self.historico and lm.visibility > 0.5:
                coord_filtrada = (
                    self.alpha * coord_atual
                    + (1.0 - self.alpha) * self.historico[idx]["pos"]
                )
            else:
                coord_filtrada = coord_atual

            self.historico[idx] = {
                "pos": coord_filtrada,
                "vis": lm.visibility,
            }
            pontos_suavizados[idx] = self.historico[idx]

        return pontos_suavizados

    def resetar(self):
        self.historico.clear()


def calcular_angulo(pontos: dict, idx_a: int, idx_b: int, idx_c: int, min_vis: float = 0.6):
    """
    Calcula o angulo interno (em graus) no vertice B formado pelos segmentos BA e BC.
    Retorna None se alguma articulacao estiver oclusa.
    """
    if (
        pontos[idx_a]["vis"] < min_vis
        or pontos[idx_b]["vis"] < min_vis
        or pontos[idx_c]["vis"] < min_vis
    ):
        return None

    a = pontos[idx_a]["pos"]
    b = pontos[idx_b]["pos"]
    c = pontos[idx_c]["pos"]

    ba = a - b
    bc = c - b

    norma_ba = np.linalg.norm(ba)
    norma_bc = np.linalg.norm(bc)
    if norma_ba < 1e-6 or norma_bc < 1e-6:
        return None

    cosseno = np.dot(ba, bc) / (norma_ba * norma_bc)
    angulo = np.degrees(np.arccos(np.clip(cosseno, -1.0, 1.0)))
    return float(angulo)


def calcular_inclinacao_vertical(pontos: dict, idx_base: int, idx_topo: int, min_vis: float = 0.6):
    """Calcula o angulo do segmento (base -> topo) em relacao ao eixo vertical."""
    if pontos[idx_base]["vis"] < min_vis or pontos[idx_topo]["vis"] < min_vis:
        return None

    base = pontos[idx_base]["pos"]
    topo = pontos[idx_topo]["pos"]
    vetor = topo - base
    vertical = np.array([0.0, -1.0], dtype=np.float32)  # Eixo Y aponta para cima

    norma = np.linalg.norm(vetor)
    if norma < 1e-6:
        return None

    cosseno = np.dot(vetor, vertical) / norma
    return float(np.degrees(np.arccos(np.clip(cosseno, -1.0, 1.0))))