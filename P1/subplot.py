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
# COMPARAÇÃO ENTRE PROCESSAMENTO ANALÓGICO E DIGITAL
# ============================================================

# Diferenças principais:
# - Analógico: sinal contínuo, processado por componentes eletrônicos.
# - Digital: sinal discretizado via A/D, processado por DSPs ou microcontroladores.

# Vantagens Analógico:
# - Resposta imediata, baixa latência, circuitos simples.
# Desvantagens:
# - Sensível a ruído, difícil reproduzir resultados, dependente de tolerâncias de componentes.

# Vantagens Digital:
# - Alta precisão e reprodutibilidade, algoritmos complexos, robustez a ruídos,
#   fácil armazenamento e reconfiguração via software.
# Desvantagens:
# - Necessita conversão A/D e D/A, maior consumo de energia, limitações de amostragem.

# Resumo comparativo:
# | Característica       | Analógico    | Digital       |
# |----------------------|-------------|---------------|
# | Sinal                | Contínuo    | Discreto      |
# | Sensibilidade a ruído| Alta        | Baixa         |
# | Precisão             | Limitada    | Alta          |
# | Flexibilidade        | Baixa       | Alta          |
# | Custo inicial        | Baixo       | Alto          |
# | Tempo de resposta    | Imediato    | Pode ter latência |

# ============================================================
# VANTAGENS DE SISTEMAS LTI (LINEAR E INVARIANTE NO TEMPO)
# ============================================================

# - Linearidade e invariância no tempo: resposta proporcional à entrada e constante no tempo.
# - Facilita análise matemática (Laplace, Fourier, Z), previsão de comportamento e estabilidade.
# - Entrada senoidal gera saída senoidal (mesma frequência, diferente amplitude/fase).
# - Resposta reproduzível, simplifica projeto de filtros e controladores.

# ============================================================
# CIRCUITO RC SÉRIE
# ============================================================

# (a) Equação diferencial:
# R*C * dvc(t)/dt + vc(t) = vi(t)

# (c) Equação de diferenças (T = 1):
# vc[k] = (1 / (1 + R*C)) * vi[k] + (R*C / (1 + R*C)) * vc[k-1]

# (d) Função de transferência discreta (T = 1):
# H(z) = Vc(z) / Vi(z) = (1 / (1 + R*C)) / (1 - (R*C / (1 + R*C)) * z^(-1))
