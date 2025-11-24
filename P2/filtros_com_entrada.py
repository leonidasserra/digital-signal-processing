import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

def filtro_RC(fc, tipo="passa-baixa", ordem=1, A=1.0, f_in=100, fase_in=0):
    wc = 2 * np.pi * fc  # frequência angular de corte

    # # Define numerador e denominador conforme o tipo e a ordem
    # if tipo == "passa-baixa":
    #     if ordem == 1:
    #         num = [1]
    #         den = [1/wc, 1]
    #     elif ordem == 2:
    #         num = [1]
    #         den = [(1/wc)**2, 2*(1/wc), 1]
    # Define numerador e denominador conforme o tipo e a ordem
    if tipo == "passa-baixa":
        if ordem == 1:
            num = [1]
            den = [1, fc]
        elif ordem == 2:
            num = [1]
            den = [(1/wc)**2, 2*(1/wc), 1]
        else:
            raise ValueError("Ordem deve ser 1 ou 2.")
    elif tipo == "passa-alta":
        if ordem == 1:
            num = [1/wc, 1]
            den = [1/wc, 1]
        elif ordem == 2:
            num = [1, 0, 0]
            den = [(1/wc)**2, 2*(1/wc), 1]
        else:
            raise ValueError("Ordem deve ser 1 ou 2.")
    # elif tipo == "passa-alta":
    #     if ordem == 1:
    #         num = [1, 0]
    #         den = [1/wc, 1]
    #     elif ordem == 2:
    #         num = [1, 0, 0]
    #         den = [(1/wc)**2, 2*(1/wc), 1]
    #     else:
    #         raise ValueError("Ordem deve ser 1 ou 2.")
    else:
        raise ValueError("Tipo deve ser 'passa-baixa' ou 'passa-alta'.")

    # Bode
    sistema = signal.TransferFunction(num, den)
    print("FT é:", sistema)
    w, mag, phase = signal.bode(sistema)
    mag_linear = 10**(mag/20)

    # Cálculo do ganho e defasagem na frequência de entrada
    w_in = 2 * np.pi * f_in
    Hjw = np.polyval(num, 1j*w_in) / np.polyval(den, 1j*w_in)
    ganho = np.abs(Hjw)
    defasagem = np.angle(Hjw)

    # Saída no tempo
    A_out = A * ganho
    fase_out = fase_in + defasagem

    # Prints informativos
    print(f"\n=== {tipo.upper()} - {ordem}ª ORDEM ===")
    print(f"Frequência de corte: {fc:.2f} Hz")
    print(f"Sinal de entrada:     {A} * cos(2π*{f_in}t + {fase_in:.2f} rad)")
    print(f"\n→ Função de transferência avaliada em f_in = {f_in} Hz:")
    print(f"   |H(jω)| = {ganho:.3f}")
    print(f"   ∠H(jω)  = {defasagem:.3f} rad  ({np.degrees(defasagem):.1f}°)")
    print(f"\n→ Sinal de saída :")
    print(f"   Amplitude de saída: {A_out:.3f}")
    print(f"   Fase de saída:      {fase_out:.3f} rad  ({np.degrees(fase_out):.1f}°)")
    print(f"   Expressão: {A_out:.3f} * cos(2π*{f_in}t + ({fase_out:.3f}))")

    # --- GRÁFICOS ---
    plt.figure(figsize=(10,8))

    # 1) Magnitude em dB
    plt.subplot(3,1,1)
    plt.semilogx(w/(2*np.pi), mag)
    plt.scatter(f_in, 20*np.log10(ganho), color='r', label='f_in')
    plt.title(f"Bode - Filtro {tipo.title()} RC ({ordem}ª Ordem)")
    plt.ylabel("Magnitude (dB)")
    plt.grid(True, which="both", ls="--")
    plt.legend()

    # 2) Magnitude linear
    plt.subplot(3,1,2)
    plt.semilogx(w/(2*np.pi), mag_linear)
    plt.scatter(f_in, ganho, color='r', label='f_in')
    plt.ylabel("Magnitude (linear)")
    plt.grid(True, which="both", ls="--")
    plt.legend()

    # 3) Fase
    plt.subplot(3,1,3)
    plt.semilogx(w/(2*np.pi), phase)
    plt.scatter(f_in, np.degrees(defasagem), color='r')
    plt.ylabel("Fase (graus)")
    plt.xlabel("Frequência (Hz)")
    plt.grid(True, which="both", ls="--")

    plt.tight_layout()
    plt.show()

    # Gera sinais de entrada e saída no tempo
    t = np.linspace(0, 5/f_in, 1000)
    vin = A * np.cos(2*np.pi*f_in*t + fase_in)
    vout = A_out * np.cos(2*np.pi*f_in*t + fase_out)

    plt.figure(figsize=(10,4))
    plt.plot(t, vin, label="Entrada")
    plt.plot(t, vout, label="Saída (filtrada)")
    plt.title(f"Resposta Temporal - {tipo.title()} {ordem}ª Ordem")
    plt.xlabel("Tempo (s)")
    plt.ylabel("Amplitude (V)")
    plt.legend()
    plt.grid(True)
    plt.show()


# Exemplo de uso
# Exemplo 1: entrada = cos(50t)
# f_in = 50 Hz (frequência linear)

R=1*1e3
C=10*1e-6
tau=10
# fc=1/(2*np.pi*R*C)
fc=1/(2*np.pi*tau)
print("Frequência de corte do Filtro igual a",fc)
# filtro_RC(fc, tipo="passa-baixa", ordem=1, A=1, f_in=100)
filtro_RC(fc, tipo="passa-alta", ordem=1, A=1, f_in=100)


