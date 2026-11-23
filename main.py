import os
import time
import urllib.request
import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import matplotlib.pyplot as plt

from geometria import SuavizadorLandmarks
from alongamentos import GerenciadorAlongamentos

NOME_JANELA = "T5 PDI - Desafio de Alongamento"
MODELO_ARQUIVO = "pose_landmarker_full.task"
MODELO_URL = (
    "https://storage.googleapis.com/mediapipe-models/pose_landmarker/"
    "pose_landmarker_full/float16/1/pose_landmarker_full.task"
)

CONEXOES_CORPO = [
    (11, 12), (11, 13), (13, 15), (12, 14), (14, 16),  # Membros superiores
    (11, 23), (12, 24), (23, 24),                      # Tronco
    (23, 25), (25, 27), (24, 26), (26, 28),            # Membros inferiores
]


def garantir_modelo():
    if not os.path.exists(MODELO_ARQUIVO):
        print(f"Baixando modelo {MODELO_ARQUIVO}...")
        urllib.request.urlretrieve(MODELO_URL, MODELO_ARQUIVO)
        print("Download concluido!")


def abrir_camera(indice: int):
    """Abre a camera no indice informado, usando DirectShow no Windows para webcams USB."""
    cap = cv2.VideoCapture(indice, cv2.CAP_DSHOW) if os.name == "nt" else cv2.VideoCapture(indice)
    if not cap.isOpened():
        cap.release()
        cap = cv2.VideoCapture(indice)

    if cap.isOpened():
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        ret, _ = cap.read()
        if ret:
            return cap
        cap.release()

    return None


def selecionar_camera_inicial():
    """Prioriza webcam externa (indices 1 e 2) e faz fallback para a integrada (0)."""
    for idx in (1, 2, 0):
        cap = abrir_camera(idx)
        if cap is not None:
            print(f"Camera ativa: indice {idx}")
            return cap, idx
    raise RuntimeError("Nenhuma webcam disponivel foi encontrada.")


def alternar_camera(cap_atual, indice_atual: int, max_indices: int = 4):
    """Alterna para a proxima webcam funcional disponivel."""
    cap_atual.release()
    for passo in range(1, max_indices + 1):
        candidato = (indice_atual + passo) % max_indices
        nova_cap = abrir_camera(candidato)
        if nova_cap is not None:
            print(f"Trocou para camera: indice {candidato}")
            return nova_cap, candidato

    # Se nenhuma outra abrir, reabre a atual
    return abrir_camera(indice_atual), indice_atual


def desenhar_esqueleto(frame, pts: dict, estado: dict):
    cor_linha = (0, 230, 118) if estado["valido"] else (0, 195, 255)

    for idx_a, idx_b in CONEXOES_CORPO:
        if pts[idx_a]["vis"] > 0.55 and pts[idx_b]["vis"] > 0.55:
            p1 = tuple(pts[idx_a]["pos"].astype(int))
            p2 = tuple(pts[idx_b]["pos"].astype(int))
            cv2.line(frame, p1, p2, cor_linha, 3, cv2.LINE_AA)

    for idx in range(11, 29):
        if pts[idx]["vis"] > 0.55:
            centro = tuple(pts[idx]["pos"].astype(int))
            cv2.circle(frame, centro, 5, (255, 255, 255), -1, cv2.LINE_AA)
            cv2.circle(frame, centro, 6, cor_linha, 2, cv2.LINE_AA)

    for idx_art, texto in estado["articulacoes"]:
        if pts[idx_art]["vis"] > 0.55:
            x, y = pts[idx_art]["pos"].astype(int)
            cv2.putText(
                frame,
                texto,
                (x + 10, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2,
                cv2.LINE_AA,
            )


def desenhar_painel(frame, gerenciador: GerenciadorAlongamentos, estado: dict, fps: float, latencia_ms: float, indice_cam: int):
    h, w, _ = frame.shape
    largura_painel = 360

    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (largura_painel, h), (22, 24, 30), -1)
    cv2.addWeighted(overlay, 0.82, frame, 0.18, 0, frame)

    # Cabecalho
    cv2.putText(frame, "DESAFIO DE ALONGAMENTO", (16, 34), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 230, 118), 2)
    cv2.putText(
        frame,
        f"FPS: {fps:.1f} | Lat: {latencia_ms:.1f}ms | Cam: {indice_cam}",
        (16, 62),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.48,
        (200, 200, 200),
        1,
    )
    cv2.line(frame, (16, 75), (largura_painel - 16, 75), (70, 75, 85), 1)

    # Exercicio atual
    ex = estado["exercicio"]
    cv2.putText(frame, "EXERCICIO ATUAL:", (16, 102), cv2.FONT_HERSHEY_SIMPLEX, 0.48, (140, 190, 255), 1)
    cv2.putText(frame, ex["nome"], (16, 126), cv2.FONT_HERSHEY_SIMPLEX, 0.54, (255, 255, 255), 2)
    cv2.putText(frame, f"Grupo: {ex['grupo']}", (16, 148), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (180, 180, 180), 1)
    cv2.putText(frame, f"Meta: {ex['alvo_texto']}", (16, 168), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 215, 255), 1)

    # Barra de progresso do tempo de sustentacao
    cv2.putText(
        frame,
        f"Sustentacao: {int(estado['progresso'] * 100)}% ({estado['tempo_restante']:.1f}s)",
        (16, 202),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (255, 255, 255),
        1,
    )
    cv2.rectangle(frame, (16, 212), (largura_painel - 16, 234), (60, 65, 75), -1)
    largura_barra = int((largura_painel - 32) * estado["progresso"])
    cor_barra = (0, 230, 118) if estado["valido"] else (0, 165, 255)
    if largura_barra > 0:
        cv2.rectangle(frame, (16, 212), (16 + largura_barra, 234), cor_barra, -1)

    # Feedback dinamico
    cv2.putText(frame, estado["feedback"], (16, 262), cv2.FONT_HERSHEY_SIMPLEX, 0.45, cor_barra, 1)
    cv2.line(frame, (16, 278), (largura_painel - 16, 278), (70, 75, 85), 1)

    # Lista de acompanhamento da sessao
    cv2.putText(frame, "PAINEL DE ACOMPANHAMENTO:", (16, 304), cv2.FONT_HERSHEY_SIMPLEX, 0.48, (140, 190, 255), 1)
    y_cursor = 332
    for res in gerenciador.resultados:
        status = "[OK]" if res["concluido"] else "[  ]"
        cor_item = (0, 230, 118) if res["concluido"] else (210, 210, 210)
        cv2.putText(frame, f"{status} {res['nome']}", (16, y_cursor), cv2.FONT_HERSHEY_SIMPLEX, 0.45, cor_item, 1)
        cv2.putText(
            frame,
            f"   Amplitude max: {res['amplitude_max']:.1f} deg",
            (16, y_cursor + 18),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.42,
            (160, 165, 175),
            1,
        )
        y_cursor += 44

    # Atalhos
    cv2.putText(
        frame,
        "[C] Cam  [N] Pular  [R] Reset  [Q] Sair",
        (16, h - 18),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.42,
        (160, 160, 160),
        1,
    )


def imprimir_resumo_avaliacao(gerenciador: GerenciadorAlongamentos, hist_fps: list, hist_latencia: list):
    print("\n" + "=" * 56)
    print("RESUMO DE AVALIACAO - T5 PDI (DESAFIO DE ALONGAMENTO)")
    print("=" * 56)
    if hist_fps:
        print(f"FPS medio:       {np.mean(hist_fps):.2f} fps (min: {np.min(hist_fps):.1f} | max: {np.max(hist_fps):.1f})")
    if hist_latencia:
        print(f"Latencia media:  {np.mean(hist_latencia):.2f} ms")

    concluidos = sum(1 for r in gerenciador.resultados if r["concluido"])
    print(f"Exercicios:      {concluidos}/{len(gerenciador.resultados)} concluidos")
    print("-" * 56)
    print("ESTABILIDADE POR EXERCICIO (Desvio Padrao Angular):")
    for idx, res in enumerate(gerenciador.resultados):
        amostras_validas = gerenciador.historico_amplitudes_validas.get(idx, [])
        amostras = amostras_validas if len(amostras_validas) > 1 else gerenciador.historico_amplitudes.get(idx, [])
        desvio = float(np.std(amostras)) if len(amostras) > 1 else 0.0
        origem = "pose valida" if len(amostras_validas) > 1 else "geral"
        print(f"  {res['nome']}: max={res['amplitude_max']:.1f} deg | std={desvio:.2f} deg ({origem})")
    print("=" * 56 + "\n")


def gerar_relatorio_grafico(gerenciador: GerenciadorAlongamentos):
    nomes = [r["nome"].split(".")[1].strip() for r in gerenciador.resultados]
    amplitudes_max = [r["amplitude_max"] for r in gerenciador.resultados]

    plt.figure(figsize=(9, 4.8))
    barras = plt.bar(nomes, amplitudes_max, color=["#0f766e", "#0284c7", "#ea580c", "#475569"])
    plt.title("Amplitude Articular Maxima Atingida por Alongamento")
    plt.ylabel("Amplitude (graus)")
    plt.ylim(0, max(max(amplitudes_max) + 25, 180))
    plt.grid(axis="y", linestyle="--", alpha=0.4)

    for barra in barras:
        altura = barra.get_height()
        plt.text(
            barra.get_x() + barra.get_width() / 2.0,
            altura + 2,
            f"{altura:.1f}°",
            ha="center",
            va="bottom",
            fontweight="bold",
        )

    plt.tight_layout()
    caminho_saida = os.path.abspath("relatorio_alongamento.png")
    plt.savefig(caminho_saida, dpi=150)
    print(f"Grafico salvo em: {caminho_saida}")
    plt.show()


def main():
    garantir_modelo()

    base_options = python.BaseOptions(model_asset_path=MODELO_ARQUIVO)
    options = vision.PoseLandmarkerOptions(
        base_options=base_options,
        running_mode=vision.RunningMode.VIDEO,
        num_poses=1,
        min_pose_detection_confidence=0.6,
        min_pose_presence_confidence=0.6,
        min_tracking_confidence=0.6,
    )

    cap, indice_cam = selecionar_camera_inicial()

    suavizador = SuavizadorLandmarks(alpha=0.55)
    gerenciador = GerenciadorAlongamentos(tempo_alvo=5.0)

    ultimo_timestamp = 0
    tempo_frame_anterior = time.perf_counter()
    historico_fps = []
    historico_latencia = []

    with vision.PoseLandmarker.create_from_options(options) as detector:
        while cap is not None and cap.isOpened():
            t_inicio = time.perf_counter()
            ret, frame = cap.read()
            if not ret:
                break

            # Espelha horizontalmente para interacao natural
            frame = cv2.flip(frame, 1)
            h, w, _ = frame.shape

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

            timestamp_ms = int(time.perf_counter() * 1000)
            if timestamp_ms <= ultimo_timestamp:
                timestamp_ms = ultimo_timestamp + 1
            ultimo_timestamp = timestamp_ms

            resultado = detector.detect_for_video(mp_image, timestamp_ms)

            if resultado.pose_landmarks:
                pts = suavizador.atualizar(resultado.pose_landmarks[0], w, h)
                estado = gerenciador.atualizar(pts)
                desenhar_esqueleto(frame, pts, estado)
            else:
                estado = {
                    "finalizado": False,
                    "exercicio": gerenciador.exercicios[min(gerenciador.indice_atual, 3)],
                    "valido": False,
                    "progresso": 0.0,
                    "tempo_restante": gerenciador.tempo_alvo,
                    "amplitude": 0.0,
                    "articulacoes": [],
                    "feedback": "Nenhuma pessoa detectada na camera",
                }

            t_fim = time.perf_counter()
            latencia_ms = (t_fim - t_inicio) * 1000.0
            fps = 1.0 / max(1e-6, (t_fim - tempo_frame_anterior))
            tempo_frame_anterior = t_fim

            historico_fps.append(fps)
            historico_latencia.append(latencia_ms)

            desenhar_painel(frame, gerenciador, estado, fps, latencia_ms, indice_cam)
            cv2.imshow(NOME_JANELA, frame)

            tecla = cv2.waitKey(1) & 0xFF
            if tecla == ord("q") or cv2.getWindowProperty(NOME_JANELA, cv2.WND_PROP_VISIBLE) < 1:
                break
            elif tecla == ord("c"):
                cap, indice_cam = alternar_camera(cap, indice_cam)
                suavizador.resetar()
            elif tecla == ord("n"):
                gerenciador.pular_exercicio()
            elif tecla == ord("r"):
                gerenciador.resetar()
                suavizador.resetar()
                historico_fps.clear()
                historico_latencia.clear()

    if cap is not None:
        cap.release()
    cv2.destroyAllWindows()
    imprimir_resumo_avaliacao(gerenciador, historico_fps, historico_latencia)
    gerar_relatorio_grafico(gerenciador)


if __name__ == "__main__":
    main()