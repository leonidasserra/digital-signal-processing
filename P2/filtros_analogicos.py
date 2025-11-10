import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

def filtro_passa_baixa(fc, ordem=1):
    """
    Gera e plota o Bode de um filtro passa-baixa de 1ª ou 2ª ordem,
    a partir da frequência de corte fc (em Hz).
    """
    RC = 1 / (2 * np.pi * fc)

    if ordem == 1:
        # 1ª ordem: H(s) = 1 / (1 + sRC)
        num = [1]
        den = [RC, 1]
        print("\n=== FILTRO PASSA-BAIXA (1ª ORDEM) ===")
        print(f"Frequência de corte: {fc:.2f} Hz")
        print(f"H(s) = 1 / (1 + s*{RC:.2e})")

    elif ordem == 2:
        # 2ª ordem: H(s) = 1 / (1 + sRC)^2
        num = [1]
        den = [RC**2, 2*RC, 1]
        print("\n=== FILTRO PASSA-BAIXA (2ª ORDEM) ===")
        print(f"Frequência de corte: {fc:.2f} Hz")
        print(f"H(s) = 1 / (1 + s*{RC:.2e})²")

    else:
        raise ValueError("Ordem deve ser 1 ou 2.")

    sistema = signal.TransferFunction(num, den)
    w, mag, phase = signal.bode(sistema)

    plt.figure(figsize=(10,6))
    plt.subplot(2,1,1)
    plt.semilogx(w/(2*np.pi), mag)
    plt.title(f"Filtro Passa-Baixa - {ordem}ª Ordem")
    plt.ylabel("Magnitude (dB)")
    plt.grid(True, which="both", ls="--")

    plt.subplot(2,1,2)
    plt.semilogx(w/(2*np.pi), phase)
    plt.ylabel("Fase (graus)")
    plt.xlabel("Frequência (Hz)")
    plt.grid(True, which="both", ls="--")
    plt.show()


def filtro_passa_alta(fc, ordem=1):
    """
    Gera e plota o Bode de um filtro passa-alta de 1ª ou 2ª ordem,
    a partir da frequência de corte fc (em Hz).
    """
    RC = 1 / (2 * np.pi * fc)

    if ordem == 1:
        # 1ª ordem: H(s) = sRC / (1 + sRC)
        num = [RC, 0]
        den = [RC, 1]
        print("\n=== FILTRO PASSA-ALTA (1ª ORDEM) ===")
        print(f"Frequência de corte: {fc:.2f} Hz")
        print(f"H(s) = (s*{RC:.2e}) / (1 + s*{RC:.2e})")

    elif ordem == 2:
        # 2ª ordem: H(s) = (sRC)^2 / (1 + sRC)^2
        num = [RC**2, 0, 0]
        den = [RC**2, 2*RC, 1]
        print("\n=== FILTRO PASSA-ALTA (2ª ORDEM) ===")
        print(f"Frequência de corte: {fc:.2f} Hz")
        print(f"H(s) = (s²*{RC**2:.2e}) / (1 + s*{RC:.2e})²")

    else:
        raise ValueError("Ordem deve ser 1 ou 2.")

    sistema = signal.TransferFunction(num, den)
    w, mag, phase = signal.bode(sistema)

    plt.figure(figsize=(10,6))
    plt.subplot(2,1,1)
    plt.semilogx(w/(2*np.pi), mag)
    plt.title(f"Filtro Passa-Alta - {ordem}ª Ordem")
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
    filtro_passa_baixa(1000, ordem=1)
    filtro_passa_baixa(1000, ordem=2)
    filtro_passa_alta(1000, ordem=1)
    filtro_passa_alta(1000, ordem=2)
