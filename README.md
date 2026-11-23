<h1 align="center">
  🧍 T5 --- Desafio de Alongamento
</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white" alt="OpenCV">
  <img src="https://img.shields.io/badge/MediaPipe-0097A7?style=for-the-badge&logo=google&logoColor=white" alt="MediaPipe">
  <img src="https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white" alt="NumPy">
  <img src="https://img.shields.io/badge/Matplotlib-11557C?style=for-the-badge&logo=python&logoColor=white" alt="Matplotlib">
</p>

<p align="center">
  Uma aplicação de visão computacional desenvolvida em Python para reconhecer e avaliar exercícios de alongamento por meio de uma webcam. O sistema utiliza o MediaPipe Pose para detectar pontos articulares, calcula ângulos do corpo e fornece feedback visual em tempo real durante a execução dos movimentos.
</p>

## 🚀 Funcionalidades

- **📷 Captura de Vídeo em Tempo Real:** Utilização da webcam para obter imagens do usuário durante a execução dos exercícios.
- **🧍 Detecção da Pose Corporal:** Identificação dos principais pontos articulares do corpo humano por meio do MediaPipe Pose Landmarker.
- **🦴 Visualização do Esqueleto:** Desenho das conexões e dos pontos corporais detectados diretamente sobre a imagem da câmera.
- **📐 Cálculo de Ângulos Articulares:** Cálculo dos ângulos dos ombros, cotovelos e joelhos, além da inclinação lateral do tronco.
- **〰️ Suavização dos Landmarks:** Aplicação de Média Móvel Exponencial (EMA) para reduzir oscilações nas coordenadas dos pontos detectados.
- **💬 Feedback Visual:** Apresentação de instruções e mensagens que orientam o usuário a ajustar a postura.
- **⏱️ Controle do Tempo de Sustentação:** Acompanhamento do tempo em que a postura permanece dentro dos critérios definidos, com meta de 5 segundos por exercício.
- **📊 Métricas de Desempenho:** Exibição de FPS e latência durante o processamento dos frames.
- **📈 Relatório Gráfico:** Geração de um gráfico com a amplitude máxima registrada para cada exercício ao final da avaliação.

## 🏋️ Exercícios Avaliados

A aplicação acompanha quatro exercícios, utilizando critérios angulares definidos no código:

| Exercício | Critério de validação |
| :--- | :--- |
| **Elevação de braços** | Os dois ombros devem atingir pelo menos 150° e os dois cotovelos pelo menos 145°. |
| **Inclinação lateral do tronco** | Inclinação entre 18° e 45°, com pelo menos um braço atingindo 145°. |
| **Alongamento de quadríceps** | Um joelho deve apresentar ângulo de até 65° e o outro deve permanecer com pelo menos 155°. |
| **Afundo** | Joelho dianteiro entre 80° e 115° e joelho traseiro com pelo menos 150°. |

Cada postura precisa ser mantida por **5 segundos** para ser contabilizada como concluída.

> **Observação:** Os limites angulares são parâmetros definidos para este projeto acadêmico. O sistema não substitui avaliação profissional, orientação médica ou análise clínica de movimento.

## 🛠️ Tecnologias Utilizadas

Este projeto foi desenvolvido em Python, utilizando bibliotecas de visão computacional, processamento numérico e visualização de dados:

* **Python:** Linguagem principal utilizada no desenvolvimento da aplicação.
* **OpenCV:** Captura de vídeo da webcam, manipulação dos frames, desenho do esqueleto e exibição da interface.
* **MediaPipe Pose Landmarker:** Detecção e rastreamento dos pontos corporais (*landmarks*) em tempo real.
* **NumPy:** Operações vetoriais, tratamento das coordenadas e cálculos matemáticos dos ângulos.
* **Matplotlib:** Criação e salvamento do gráfico com os resultados da avaliação.

## 📂 Estrutura do Projeto

```text
T5/
├── main.py
├── alongamentos.py
├── geometria.py
├── relatorio_alongamento.png
├── .gitignore
└── README.md