import numpy as np
import matplotlib.pyplot as plt

def amostragem(x, fs):
    """
    Amostra um sinal 'contínuo' x com frequência fs
    Assume que x está discretizado a 0.001s por amostra
    
    Retorna: (x_esparso, valores_compactos, indices_compactos)
    """
    # Convertendo passo para inteiro
    passo = int(1000 / fs)
    
    # Criando trem de impulsos
    trem = np.zeros(len(x))
    for i in range(len(trem)):
        if i % passo == 0:
            trem[i] = 1
    
    # Versão esparsa (com zeros)
    x_amostrado_esparso = [0] * len(x)
    for i in range(len(x)):
        x_amostrado_esparso[i] = x[i] * trem[i]
    
    # Versão compacta (sem zeros)
    valores_compactos = []
    indices_compactos = []
    for i in range(len(x_amostrado_esparso)):
        if x_amostrado_esparso[i] != 0:
            valores_compactos.append(x_amostrado_esparso[i])
            indices_compactos.append(i)
    
    return x_amostrado_esparso, valores_compactos, indices_compactos


# Exemplo de uso
# Criando um sinal senoidal "contínuo"
duracao = 1  # 1 segundo
t = np.arange(0, duracao, 0.001)  # vetor de tempo com 0.001s de resolução
frequencia_sinal = 5  # Hz
x = np.sin(2 * np.pi * frequencia_sinal * t)

# Amostrando com fs = 20 Hz
fs = 20
x_esparso, valores, indices = amostragem(x, fs)

# Criando as visualizações
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

# Plot 1: Versão esparsa
ax1.plot(t, x, 'b-', label='Sinal Original', alpha=0.7)
ax1.stem(t, x_esparso, linefmt='r-', markerfmt='ro', basefmt='k-', label='Amostrado (esparso)')
ax1.set_xlabel('Tempo (s)')
ax1.set_ylabel('Amplitude')
ax1.set_title(f'Amostragem com Representação Esparsa (fs = {fs} Hz)')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Plot 2: Versão compacta
t_amostrado = np.array(indices) * 0.001
ax2.plot(t, x, 'b-', label='Sinal Original', alpha=0.7)
ax2.stem(t_amostrado, valores, linefmt='g-', markerfmt='go', basefmt='k-', label='Amostrado (compacto)')
ax2.set_xlabel('Tempo (s)')
ax2.set_ylabel('Amplitude')
ax2.set_title(f'Amostragem com Representação Compacta (fs = {fs} Hz)')
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print(f"Sinal original: {len(x)} pontos")
print(f"Versão esparsa: {len(x_esparso)} pontos (maioria zeros)")
print(f"Versão compacta: {len(valores)} pontos (apenas amostras)")