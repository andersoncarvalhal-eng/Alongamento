```{=html}
<h1 align="center">
```
🧍 T5 --- Desafio de Alongamento
```{=html}
</h1>
```
```{=html}
<p align="center">
```
`<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">`{=html}
`<img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white" alt="OpenCV">`{=html}
`<img src="https://img.shields.io/badge/MediaPipe-0097A7?style=for-the-badge&logo=google&logoColor=white" alt="MediaPipe">`{=html}
`<img src="https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white" alt="NumPy">`{=html}
`<img src="https://img.shields.io/badge/Matplotlib-11557C?style=for-the-badge&logo=python&logoColor=white" alt="Matplotlib">`{=html}
```{=html}
</p>
```
```{=html}
<p align="center">
```
Uma aplicação de visão computacional desenvolvida em Python para
reconhecer e avaliar exercícios de alongamento por meio de uma webcam. O
sistema utiliza o MediaPipe Pose para detectar pontos articulares,
calcula ângulos do corpo e fornece feedback visual em tempo real durante
a execução dos movimentos.
```{=html}
</p>
```
## 🚀 Funcionalidades

-   **📷 Captura de Vídeo em Tempo Real:** utilização da webcam para
    obter imagens do usuário durante a execução dos exercícios.
-   **🧍 Detecção da Pose Corporal:** identificação dos principais
    pontos articulares do corpo humano por meio do MediaPipe Pose
    Landmarker.
-   **🦴 Visualização do Esqueleto:** desenho das conexões e dos pontos
    corporais detectados diretamente sobre a imagem da câmera.
-   **📐 Cálculo de Ângulos Articulares:** cálculo dos ângulos dos
    ombros, cotovelos e joelhos, além da inclinação lateral do tronco.
-   **〰️ Suavização dos Landmarks:** aplicação de Média Móvel
    Exponencial (EMA) para reduzir oscilações nas coordenadas dos pontos
    detectados.
-   **💬 Feedback Visual:** apresentação de instruções e mensagens que
    orientam o usuário a ajustar a postura.
-   **⏱️ Controle do Tempo de Sustentação:** acompanhamento do tempo em
    que a postura permanece dentro dos critérios definidos, com meta de
    5 segundos por exercício.
-   **📊 Métricas de Desempenho:** exibição de FPS e latência durante o
    processamento dos frames.
-   **📈 Relatório Gráfico:** geração de um gráfico com a amplitude
    máxima registrada para cada exercício ao final da avaliação.

## 🏋️ Exercícios Avaliados

A aplicação acompanha quatro exercícios, utilizando critérios angulares
definidos no código:

  -----------------------------------------------------------------------
  Exercício                           Critério de validação
  ----------------------------------- -----------------------------------
  Elevação de braços                  Os dois ombros devem atingir pelo
                                      menos 150° e os dois cotovelos pelo
                                      menos 145°.

  Inclinação lateral do tronco        Inclinação entre 18° e 45°, com
                                      pelo menos um braço atingindo 145°.

  Alongamento de quadríceps           Um joelho deve apresentar ângulo de
                                      até 65° e o outro deve permanecer
                                      com pelo menos 155°.

  Afundo                              Joelho dianteiro entre 80° e 115° e
                                      joelho traseiro com pelo menos
                                      150°.
  -----------------------------------------------------------------------

Cada postura precisa ser mantida por **5 segundos** para ser
contabilizada como concluída.

> **Observação:** os limites angulares são parâmetros definidos para
> este projeto acadêmico. O sistema não substitui avaliação
> profissional, orientação médica ou análise clínica de movimento.

## 🛠️ Tecnologias Utilizadas

O projeto foi desenvolvido em Python, utilizando bibliotecas de visão
computacional, processamento numérico e visualização de dados:

-   **Python:** linguagem principal utilizada no desenvolvimento da
    aplicação.
-   **OpenCV:** captura de vídeo da webcam, manipulação dos frames,
    desenho do esqueleto e exibição da interface.
-   **MediaPipe Pose Landmarker:** detecção e rastreamento dos pontos
    corporais (*landmarks*) em tempo real.
-   **NumPy:** operações vetoriais, tratamento das coordenadas e
    cálculos matemáticos dos ângulos.
-   **Matplotlib:** criação e salvamento do gráfico com os resultados da
    avaliação.

## 📂 Estrutura do Projeto

``` text
T5/
├── main.py
├── alongamentos.py
├── geometria.py
├── relatorio_alongamento.png
├── .gitignore
└── README.md
```

**Descrição dos arquivos:**

-   **`main.py`:** arquivo principal. Inicializa o MediaPipe, verifica a
    disponibilidade do modelo, acessa a webcam, executa o processamento
    em tempo real e apresenta o resumo da avaliação.
-   **`alongamentos.py`:** contém a lógica dos quatro exercícios, os
    critérios de validação, o controle do tempo de sustentação e o
    registro das amplitudes.
-   **`geometria.py`:** implementa a suavização dos landmarks e as
    funções matemáticas para calcular ângulos articulares e inclinação
    em relação ao eixo vertical.
-   **`relatorio_alongamento.png`:** gráfico gerado pela aplicação ao
    final da execução. O arquivo é atualizado quando uma nova avaliação
    é encerrada.
-   **`pose_landmarker_full.task`:** modelo utilizado pelo MediaPipe.
    Não precisa estar versionado no repositório, pois o programa realiza
    o download automaticamente quando o arquivo não é encontrado.

## ⚙️ Como Executar Localmente

Para executar o projeto, é necessário ter Python instalado, uma webcam
disponível e conexão com a internet na primeira execução, caso o modelo
do MediaPipe ainda não esteja presente na pasta.

### 1. Clonar o repositório

``` bash
git clone https://github.com/SEU-USUARIO/NOME-DO-REPOSITORIO.git
```

Acesse a pasta do projeto:

``` bash
cd NOME-DO-REPOSITORIO
```

### 2. Criar um ambiente virtual (recomendado)

**Windows:**

``` bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux ou macOS:**

``` bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar as dependências

``` bash
python -m pip install --upgrade pip
python -m pip install opencv-python mediapipe numpy matplotlib
```

### 4. Executar a aplicação

``` bash
python main.py
```

Na primeira execução, se o arquivo `pose_landmarker_full.task` não
estiver na pasta do projeto, o programa tentará baixá-lo
automaticamente.

## 🎮 Controles da Aplicação

Durante a execução, os comandos abaixo podem ser utilizados na janela da
webcam:

  Tecla   Ação
  ------- -------------------------------------------------------------
  `C`     Alterna entre as câmeras disponíveis.
  `N`     Pula o exercício atual.
  `R`     Reinicia a avaliação e os indicadores da sessão.
  `Q`     Encerra a aplicação e apresenta o resumo e o gráfico final.

A aplicação tenta abrir inicialmente as câmeras nos índices 1 e 2 e,
como alternativa, utiliza o índice 0. A disponibilidade depende das
câmeras conectadas ao computador.

## 🔬 Etapas do Processamento

O funcionamento do sistema é dividido nas seguintes etapas:

1.  **Aquisição da imagem:** o OpenCV captura os frames da webcam.
2.  **Pré-processamento:** a imagem é espelhada horizontalmente e
    convertida do padrão BGR para RGB.
3.  **Detecção corporal:** o MediaPipe Pose Landmarker identifica os
    pontos articulares da pessoa.
4.  **Suavização dos pontos:** as coordenadas dos landmarks são
    convertidas para pixels e estabilizadas por meio de uma Média Móvel
    Exponencial (EMA).
5.  **Processamento geométrico:** são calculados os ângulos entre
    segmentos corporais e a inclinação do tronco em relação à vertical.
6.  **Validação dos exercícios:** os valores calculados são comparados
    com os limites definidos para cada alongamento. Pontos com
    visibilidade insuficiente são desconsiderados.
7.  **Feedback em tempo real:** o sistema atualiza o esqueleto, os
    ângulos, as instruções e o progresso do tempo de sustentação.
8.  **Geração dos resultados:** ao encerrar a aplicação, são exibidas
    métricas de desempenho e gerado o gráfico das amplitudes máximas
    registradas.

## 📊 Resultados e Métricas

Ao finalizar a avaliação, o programa apresenta no terminal:

-   FPS médio, mínimo e máximo.
-   Latência média de processamento por frame.
-   Quantidade de exercícios concluídos.
-   Amplitude máxima registrada em cada exercício.
-   Desvio padrão das amplitudes angulares registradas.

Além do resumo textual, é salvo o arquivo `relatorio_alongamento.png`,
com um gráfico de barras das amplitudes máximas calculadas para os
quatro exercícios.

## 🔮 Roadmap (Próximos Passos)

-   **📁 Histórico de Avaliações:** salvar os resultados de diferentes
    sessões para permitir comparações.
-   **📄 Exportação de Relatórios:** disponibilizar os resultados em
    formatos como CSV ou PDF.
-   **🎯 Calibração Individual:** permitir ajustar os limites angulares
    de acordo com o enquadramento e as características de cada usuário.
-   **🖥️ Interface Aprimorada:** desenvolver uma interface com recursos
    adicionais para acompanhar o histórico e os resultados das
    avaliações.

## ⚠️ Limitações

-   A aplicação avalia uma pessoa por vez.
-   A qualidade da detecção depende da iluminação, do enquadramento e da
    visibilidade das articulações.
-   Oclusões ou partes do corpo fora da imagem podem impedir o cálculo
    de alguns ângulos.
-   A perspectiva da câmera pode influenciar os ângulos estimados.
-   Os critérios angulares são parâmetros definidos na implementação e
    não representam diagnóstico ou avaliação clínica.


------------------------------------------------------------------------

```{=html}
<p align="center">
```
Desenvolvido para a disciplina de `<strong>`{=html}Processamento Digital
de Imagens (PDI)`</strong>`{=html} --- Projeto T5.
```{=html}
</p>
```
