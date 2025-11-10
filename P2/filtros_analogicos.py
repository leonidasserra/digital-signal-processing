import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

def filtro_passa_baixa(R, C, ordem=1):
    """
    Gera e plota o Bode de um filtro RC passa-baixa de 1ª ou 2ª ordem.
    - Para 1ª ordem: usa R e C únicos.
    - Para 2ª ordem: espera R e C como listas [R1, R2] e [C1, C2].
    """
    if ordem == 1:
        # 1ª ordem: H(s) = 1 / (1 + sRC)
        R1, C1 = R, C
        num = [1]
        den = [R1*C1, 1]
        fc = 1 / (2*np.pi*R1*C1)
        print("\n=== FILTRO PASSA-BAIXA (1ª ORDEM) ===")
        print(f"R = {R1} Ω, C = {C1} F")
        print(f"Frequência de corte: {fc:.2f} Hz")
        print(f"H(s) = 1 / (1 + s*{R1*C1:.2e})")

    elif ordem == 2:
        # 2ª ordem (duas células RC em cascata)
        R1, R2 = R
        C1, C2 = C
        num = [1]
        den = np.polymul([R1*C1, 1], [R2*C2, 1])  # multiplica os dois polinômios (1 + sR1C1)(1 + sR2C2)
        fc1 = 1 / (2*np.pi*R1*C1)
        fc2 = 1 / (2*np.pi*R2*C2)
        print("\n=== FILTRO PASSA-BAIXA (2ª ORDEM) ===")
        print(f"R1 = {R1} Ω, C1 = {C1} F")
        print(f"R2 = {R2} Ω, C2 = {C2} F")
        print(f"Frequências de corte individuais: {fc1:.2f} Hz e {fc2:.2f} Hz")
        print(f"Função de transferência: H(s) = 1 / [(1 + s*{R1*C1:.2e})(1 + s*{R2*C2:.2e})]")

    else:
        raise ValueError("Ordem deve ser 1 ou 2.")

    sistema = signal.TransferFunction(num, den)
    w, mag, phase = signal.bode(sistema)

    plt.figure(figsize=(10,6))
    plt.subplot(2,1,1)
    plt.semilogx(w/(2*np.pi), mag)
    plt.title(f"Filtro Passa-Baixa RC - {ordem}ª Ordem")
    plt.ylabel("Magnitude (dB)")
    plt.grid(True, which="both", ls="--")

    plt.subplot(2,1,2)
    plt.semilogx(w/(2*np.pi), phase)
    plt.ylabel("Fase (graus)")
    plt.xlabel("Frequência (Hz)")
    plt.grid(True, which="both", ls="--")
    plt.show()


def filtro_passa_alta(R, C, ordem=1):
    """
    Gera e plota o Bode de um filtro RC passa-alta de 1ª ou 2ª ordem.
    - Para 1ª ordem: usa R e C únicos.
    - Para 2ª ordem: espera R e C como listas [R1, R2] e [C1, C2].
    """
    if ordem == 1:
        # 1ª ordem: H(s) = sRC / (1 + sRC)
        R1, C1 = R, C
        num = [R1*C1, 0]
        den = [R1*C1, 1]
        fc = 1 / (2*np.pi*R1*C1)
        print("\n=== FILTRO PASSA-ALTA (1ª ORDEM) ===")
        print(f"R = {R1} Ω, C = {C1} F")
        print(f"Frequência de corte: {fc:.2f} Hz")
        print(f"H(s) = (s*{R1*C1:.2e}) / (1 + s*{R1*C1:.2e})")

    elif ordem == 2:
        # 2ª ordem (duas células RC em cascata)
        R1, R2 = R
        C1, C2 = C
        num = np.polymul([R1*C1, 0], [R2*C2, 0])  # (sR1C1)(sR2C2)
        den = np.polymul([R1*C1, 1], [R2*C2, 1])
        fc1 = 1 / (2*np.pi*R1*C1)
        fc2 = 1 / (2*np.pi*R2*C2)
        print("\n=== FILTRO PASSA-ALTA (2ª ORDEM) ===")
        print(f"R1 = {R1} Ω, C1 = {C1} F")
        print(f"R2 = {R2} Ω, C2 = {C2} F")
        print(f"Frequências de corte individuais: {fc1:.2f} Hz e {fc2:.2f} Hz")
        print(f"Função de transferência: H(s) = (s²*{R1*C1*R2*C2:.2e}) / [(1 + s*{R1*C1:.2e})(1 + s*{R2*C2:.2e})]")

    else:
        raise ValueError("Ordem deve ser 1 ou 2.")

    sistema = signal.TransferFunction(num, den)
    w, mag, phase = signal.bode(sistema)

    plt.figure(figsize=(10,6))
    plt.subplot(2,1,1)
    plt.semilogx(w/(2*np.pi), mag)
    plt.title(f"Filtro Passa-Alta RC - {ordem}ª Ordem")
    plt.ylabel("Magnitude (dB)")
    plt.grid(True, which="both", ls="--")

    plt.subplot(2,1,2)
    plt.semilogx(w/(2*np.pi), phase)
    plt.ylabel("Fase (graus)")
    plt.xlabel("Frequência (Hz)")
    plt.grid(True, which="both", ls="--")
    plt.show()


# Exemplo de uso
if __name__ == "__main__":
    # 1ª ordem
    filtro_passa_baixa(1e3, 1e-6, ordem=1)
    filtro_passa_alta(1e3, 1e-6, ordem=1)

    # 2ª ordem (duas células RC)
    R = [1e3, 2e3]
    C = [1e-6, 0.5e-6]
    filtro_passa_baixa(R, C, ordem=2)
    filtro_passa_alta(R, C, ordem=2)
