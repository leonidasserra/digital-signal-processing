import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

def filtro_passa_baixa(R, C, ordem=1):
    """
    Gera e plota o Bode de um filtro RC passa-baixa de 1ª ou 2ª ordem.
    - Ordem 1: H(s) = 1 / (1 + sRC)
    - Ordem 2: H(s) = 1 / (1 + sRC)^2
    """
    if ordem == 1:
        num = [1]
        den = [R*C, 1]
        fc = 1 / (2*np.pi*R*C)
        print("\n=== FILTRO PASSA-BAIXA (1ª ORDEM) ===")
        print(f"R = {R} Ω, C = {C} F")
        print(f"Frequência de corte: {fc:.2f} Hz")
        print(f"H(s) = 1 / (1 + s*{R*C:.2e})")

    elif ordem == 2:
        # Segunda ordem com R1=R2=R e C1=C2=C → uma única frequência de corte
        num = [1]
        den = [R**2 * C**2, 2*R*C, 1]
        fc = 1 / (2*np.pi*R*C)
        print("\n=== FILTRO PASSA-BAIXA (2ª ORDEM) ===")
        print(f"R1 = R2 = {R} Ω, C1 = C2 = {C} F")
        print(f"Frequência de corte única: {fc:.2f} Hz")
        print(f"H(s) = 1 / (1 + s*{R*C:.2e})²")

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
    - Ordem 1: H(s) = sRC / (1 + sRC)
    - Ordem 2: H(s) = (sRC)^2 / (1 + sRC)^2
    """
    if ordem == 1:
        num = [R*C, 0]
        den = [R*C, 1]
        fc = 1 / (2*np.pi*R*C)
        print("\n=== FILTRO PASSA-ALTA (1ª ORDEM) ===")
        print(f"R = {R} Ω, C = {C} F")
        print(f"Frequência de corte: {fc:.2f} Hz")
        print(f"H(s) = (s*{R*C:.2e}) / (1 + s*{R*C:.2e})")

    elif ordem == 2:
        num = [R**2 * C**2, 0, 0]  # (sRC)^2
        den = [R**2 * C**2, 2*R*C, 1]
        fc = 1 / (2*np.pi*R*C)
        print("\n=== FILTRO PASSA-ALTA (2ª ORDEM) ===")
        print(f"R1 = R2 = {R} Ω, C1 = C2 = {C} F")
        print(f"Frequência de corte única: {fc:.2f} Hz")
        print(f"H(s) = (s²*{R**2*C**2:.2e}) / (1 + s*{R*C:.2e})²")

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
    filtro_passa_baixa(1e3, 1e-6, ordem=1)
    filtro_passa_baixa(1e3, 1e-6, ordem=2)
    filtro_passa_alta(1e3, 1e-6, ordem=1)
    filtro_passa_alta(1e3, 1e-6, ordem=2)
