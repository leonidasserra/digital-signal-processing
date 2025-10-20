import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

def analisar_resposta_frequencia(num, den, N=512, plotar=True):
    """
    Analisa a resposta em frequência de um sistema discreto.
    
    Parâmetros:
    -----------
    num : array_like
        Coeficientes do numerador da função de transferência (potências decrescentes de z^-1)
    den : array_like
        Coeficientes do denominador da função de transferência (potências decrescentes de z^-1)
    N : int, opcional
        Número de pontos para o cálculo da resposta em frequência (default = 512)
    plotar : bool, opcional
        Se True, plota a resposta em magnitude e fase
    
    Retorna:
    --------
    w : ndarray
        Frequências normalizadas (rad/amostra)
    H : ndarray
        Resposta em frequência complexa
    mag : ndarray
        Magnitude (linear)
    fase : ndarray
        Fase (em graus)
    """

    # Cálculo da resposta em frequência
    w, H = signal.freqz(num, den, worN=N)

    # Magnitude linear e fase
    mag = np.abs(H)
    fase = np.angle(H, deg=True)

    if plotar:
        plt.figure(figsize=(10, 6))

        # Gráfico da magnitude (ESCALA LINEAR FIXA)
        plt.subplot(2, 1, 1)
        plt.plot(w, mag, color='b', linewidth=1.5)
        plt.title('Resposta em Frequência do Sistema')
        plt.ylabel('Magnitude (linear)')
        plt.xlabel('Frequência Normalizada (rad/amostra)')
        plt.grid(True)

        # Gráfico da fase
        plt.subplot(2, 1, 2)
        plt.plot(w, fase, color='r', linewidth=1.5)
        plt.ylabel('Fase (graus)')
        plt.xlabel('Frequência Normalizada (rad/amostra)')
        plt.grid(True)

        plt.tight_layout()
        plt.show()

    return w, H, mag, fase


# Exemplo de uso
if __name__ == "__main__":
    # Função de transferência de exemplo: H(z) = (1 - 0.9z^-1) / (1 - 0.5z^-1)
    num = [1]
    den = [1, -0.8]

    analisar_resposta_frequencia(num, den)
