# Subplots
fig, axs = plt.subplots(2, 1, figsize=(6, 4), sharex=True)
t=np.arange()
axs[0].stem(t, x_impulso, linefmt='red', markerfmt='ro', basefmt='k')
axs[0].set_title('Impulso original')
axs[0].grid(True)

axs[1].stem(t, x_atrasado, linefmt='blue', markerfmt='bo', basefmt='k')
axs[1].set_title(f'Impulso atrasado de {k} unidades')
axs[1].grid(True)

plt.xlabel('Tempo (n)')
plt.tight_layout()
plt.show()

# ======================================================

"""
stem_plot_guide.py

Guia de gráficos de sinais discretos usando matplotlib.stem
Inclui exemplos de:
 - stem simples
 - múltiplos sinais no mesmo plot
 - múltiplos subplots
 - customização de cores, marcadores e linhas
 - eixos, títulos e grids

Como usar:
 - rodar diretamente: `python stem_plot_guide.py`
 - importar funções: `from stem_plot_guide import example_stem_basic`

Requisitos:
 - matplotlib
 - numpy
"""

import numpy as np
import matplotlib.pyplot as plt

def example_stem_basic():
    """Exemplo básico de stem"""
    n = np.arange(0, 20)
    x = np.sin(n)

    plt.stem(n, x, linefmt='r-', markerfmt='ro', basefmt='k')
    plt.title('Exemplo stem básico')
    plt.xlabel('n')
    plt.ylabel('x[n]')
    plt.grid(True)
    plt.show()


def example_stem_multiple():
    """Dois sinais discretos no mesmo stem"""
    n = np.arange(0, 20)
    x = np.sin(n)
    y = 0.5 * np.cos(n)

    plt.stem(n, x, linefmt='r-', markerfmt='ro', basefmt='k', label='sin(n)')
    plt.stem(n, y, linefmt='b-', markerfmt='bo', basefmt='k', label='0.5*cos(n)')
    plt.title('Stem múltiplos sinais')
    plt.xlabel('n')
    plt.ylabel('Amplitude')
    plt.grid(True)
    plt.legend()
    plt.show()


def example_stem_subplots():
    """Múltiplos subplots para sinais discretos"""
    n = np.arange(0, 20)
    x = np.sin(n)
    y = 0.5 * np.cos(n)

    fig, axs = plt.subplots(2, 1, figsize=(6, 5), sharex=True)

    axs[0].stem(n, x, linefmt='r-', markerfmt='ro', basefmt='k')
    axs[0].set_title('Seno discreto')
    axs[0].grid(True)

    axs[1].stem(n, y, linefmt='b-', markerfmt='bo', basefmt='k')
    axs[1].set_title('Cosseno discreto')
    axs[1].grid(True)

    plt.xlabel('n')
    plt.tight_layout()
    plt.show()



















# ============================================================
# COMPARAÇÃO ENTRE PROCESSAMENTO ANALÓGICO E DIGITAL DE SINAIS
# ============================================================

# 1. DIFERENÇAS FUNDAMENTAIS
# --------------------------
# - Processamento Analógico:
#     O sinal é tratado de forma contínua, mantendo todas as variações
#     originais no tempo e na amplitude. O processamento ocorre por meio
#     de componentes eletrônicos analógicos, como resistores, capacitores,
#     indutores e amplificadores operacionais.
#
# - Processamento Digital:
#     O sinal contínuo é amostrado e convertido em uma sequência discreta
#     de números (amostras) por meio de conversores A/D. O processamento
#     é realizado por sistemas digitais, como microcontroladores,
#     DSPs (Digital Signal Processors) ou computadores.

# 2. VANTAGENS DO PROCESSAMENTO ANALÓGICO
# ---------------------------------------
# - Resposta em tempo real imediata (sem discretização).
# - Menor atraso (latência) no tratamento do sinal.
# - Circuitos simples podem ser suficientes para tarefas básicas.
#
# DESVANTAGENS DO ANALÓGICO:
# - Sensível a ruídos e interferências.
# - Dificuldade em realizar ajustes e reproduzir resultados idênticos.
# - Variações de temperatura e tolerância dos componentes afetam o desempenho.
# - Pouca flexibilidade para alterar parâmetros sem modificar o hardware.

# 3. VANTAGENS DO PROCESSAMENTO DIGITAL
# -------------------------------------
# - Alta precisão e reprodutibilidade: resultados idênticos a cada execução.
# - Facilidade para implementar algoritmos complexos (ex: filtros adaptativos).
# - Menor influência de ruídos e variações externas (robustez).
# - Facilidade de armazenamento, transmissão e modificação dos dados.
# - Reconfiguração por software (sem necessidade de alterar hardware).
#
# DESVANTAGENS DO DIGITAL:
# - Necessita conversão A/D e D/A, o que introduz atrasos e perdas.
# - Consome mais energia e requer maior complexidade computacional.
# - Limitações impostas pela taxa de amostragem e quantização (erro de truncamento).

# 4. RESUMO COMPARATIVO
# ---------------------
# | Característica       | Analógico                  | Digital                      |
# |----------------------|----------------------------|------------------------------|
# | Natureza do sinal    | Contínua                   | Discreta                     |
# | Sensibilidade a ruído| Alta                       | Baixa                        |
# | Precisão             | Limitada pelos componentes | Alta (dependente de bits)    |
# | Flexibilidade        | Baixa                      | Alta (software reprogramável)|
# | Custo inicial        | Baixo                      | Alto (conversores, processador)|
# | Tempo de resposta    | Imediato                   | Pode ter latência            |

# ============================================================
# Em resumo:
# O processamento analógico é mais direto e rápido, mas menos preciso
# e mais sensível a interferências. O digital, por outro lado, oferece
# flexibilidade, precisão e imunidade a ruídos, sendo preferido em
# aplicações modernas, apesar do custo e complexidade maiores.
# ============================================================


# ============================================================
# VANTAGENS DE DEFINIR UM SISTEMA COMO LTI (LINEAR E INVARIANTE NO TEMPO)
# ============================================================

# - Um sistema LTI obedece à linearidade (superposição) e à invariância no tempo.
#   Isso significa que sua resposta é proporcional à entrada e não muda com o tempo.

# - PRINCIPAIS VANTAGENS:
#   • Simplicidade matemática: pode ser analisado por transformadas de Laplace,
#     Fourier ou Z, reduzindo equações diferenciais a expressões algébricas.
#
#   • Previsibilidade: o comportamento do sistema pode ser totalmente descrito
#     pela função de transferência H(s) ou pela resposta ao impulso h(t),
#     permitindo traçar sua estabilidade, ganho e resposta em frequência.
#
#   • Análise em frequência facilitada: uma entrada senoidal gera uma saída
#     senoidal da mesma frequência (com alteração apenas de amplitude e fase).
#
#   • Reprodutibilidade e estabilidade: o sistema responde da mesma forma
#     para a mesma entrada, independentemente do instante de aplicação.
#
#   • Implementação prática: muitos filtros, amplificadores e controladores
#     são LTI ou podem ser aproximados como tal, simplificando projeto e simulação.

# - Em resumo:
#   Sistemas LTI são amplamente usados porque permitem análise previsível,
#   simplificada e precisa, servindo de base para o estudo e o projeto
#   de sistemas de controle e processamento de sinais.
# ============================================================
