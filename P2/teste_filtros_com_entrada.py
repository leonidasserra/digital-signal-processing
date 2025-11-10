import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

def filtro_RC(fc=None, tipo="passa-baixa", ordem=1, A=1.0, f_in=100, fase_in=0):
    """
    Exemplo de filtro com função de transferência:
        H(s) = (s + 0.1) / (s + 5)
    """

    # --- Define a função de transferência personalizada ---
    num = [1, 0.1]  # s + 0.1
    den = [1, 5]    # s + 5

    sistema = signal.TransferFunction(num, den)
    w, mag, phase = signal.bode(sistema)  # w em rad/s, phase em graus
    mag_linear = 10**(mag/20)

    # --- Avaliação no ponto f_in ---
    w_in = 2 * np.pi * f_in  # rad/s
    Hjw = np.polyval(num, 1j*w_in) / np.polyval(den, 1j*w_in)
    ganho = np.abs(Hjw)
    defasagem = np.angle(Hjw)  # radianos

    # --- Cálculo da saída ---
    A_out = A * ganho
    fase_out = fase_in + defasagem

    # --- Impressão de resultados ---
    print(f"\n=== FILTRO PERSONALIZADO H(s) = (s+0.1)/(s+5) ===")
    print(f"Sinal de entrada:     {A} * cos(2π*{f_in}t + {fase_in:.2f} rad)")
    print(f"\n→ Função de transferência avaliada em:")
    print(f"   ω_in = {w_in:.2f} rad/s  |  f_in = {f_in} Hz")
    print(f"   |H(jω)| = {ganho:.3f}")
    print(f"   ∠H(jω)  = {defasagem:.3f} rad  ({np.degrees(defasagem):.1f}°)")
    print(f"\n→ Sinal de saída :")
    print(f"   Amplitude de saída: {A_out:.3f}")
    print(f"   Fase de saída:      {fase_out:.3f} rad  ({np.degrees(fase_out):.1f}°)")
    print(f"   Expressão: {A_out:.3f} * cos(2π*{f_in}t + {fase_out:.3f})")

    # --- Bode (Hz no eixo X) ---
    plt.figure(figsize=(8,8))

    plt.subplot(3,1,1)
    plt.semilogx(w/(2*np.pi), mag)
    plt.scatter(f_in, 20*np.log10(ganho), color='r', label='f_in')
    plt.title("Bode - Filtro H(s) = (s+0.1)/(s+5)")
    plt.ylabel("Magnitude (dB)")
    plt.grid(True, which="both", ls="--")
    plt.legend()

    plt.subplot(3,1,2)
    plt.semilogx(w/(2*np.pi), mag_linear)
    plt.scatter(f_in, ganho, color='r', label='f_in')
    plt.ylabel("Magnitude (linear)")
    plt.grid(True, which="both", ls="--")
    plt.legend()

    plt.subplot(3,1,3)
    plt.semilogx(w/(2*np.pi), phase)
    plt.scatter(f_in, np.degrees(defasagem), color='r')
    plt.ylabel("Fase (°)")
    plt.xlabel("Frequência (Hz)")
    plt.grid(True, which="both", ls="--")

    plt.tight_layout()
    plt.show()

    # --- Resposta temporal ---
    t = np.linspace(0, 5/f_in, 1000)
    vin = A * np.cos(2*np.pi*f_in*t + fase_in)
    vout = A_out * np.cos(2*np.pi*f_in*t + fase_out)

    plt.figure(figsize=(10,4))
    plt.plot(t, vin, label="Entrada")
    plt.plot(t, vout, label="Saída (filtrada)")
    plt.title("Resposta Temporal - Filtro H(s) = (s+0.1)/(s+5)")
    plt.xlabel("Tempo (s)")
    plt.ylabel("Amplitude (V)")
    plt.legend()
    plt.grid(True)
    plt.show()


# === Teste ===
filtro_RC(A=1, f_in=2)
