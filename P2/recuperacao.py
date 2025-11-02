import numpy as np
import matplotlib.pyplot as plt
from amostragem import amostragem

def recuperacao_sinal(x_n, T, dt=0.001):
    """
    Conversão Digital → Analógica: x[n] → x(t)
    
    Implementa a fórmula de recuperação ideal:
    x_r(t) = Σ x[n] * h_r(t - nT)
    onde h_r(t) = sin(πt/T) / (πt/T)  [função sinc]
    
    Parâmetros:
    - x_n: sinal discreto (amostrado) - pode ser vetor esparso com zeros
    - T: período de amostragem
    - dt: resolução temporal para reconstrução (padrão: 0.001s)
    
    Retorna:
    - x_recuperado: sinal contínuo recuperado x(t)
    - t: vetor de tempo correspondente
    """
    
    # Extrair apenas as amostras não-zero (valores de x[n])
    indices_amostras = []
    valores_amostras = []
    
    for i in range(len(x_n)):
        if x_n[i] != 0:
            indices_amostras.append(i)
            valores_amostras.append(x_n[i])
    
    # Converter índices para tempo: t = n*T
    t_amostras = np.array(indices_amostras) * dt
    x_n_valores = np.array(valores_amostras)
    
    # Criar vetor de tempo contínuo para reconstrução
    t = np.arange(len(x_n)) * dt
    
    # Inicializar sinal recuperado
    x_recuperado = np.zeros(len(t))
    
    # Aplicar a fórmula de recuperação: x_r(t) = Σ x[n] * sinc((t-nT)/T)
    for n, (t_n, x_n_val) in enumerate(zip(t_amostras, x_n_valores)):
        # Calcular h_r(t - nT) = sin(π(t-nT)/T) / (π(t-nT)/T)
        arg = np.pi * (t - t_n) / T
        
        # Calcular sinc, tratando o caso t = nT (sinc(0) = 1)
        sinc_values = np.zeros_like(arg)
        mask = arg != 0
        sinc_values[mask] = np.sin(arg[mask]) / arg[mask]
        sinc_values[~mask] = 1.0  # h_r(0) = 1
        
        # Acumular contribuição de cada amostra
        x_recuperado += x_n_val * sinc_values
    
    return x_recuperado, t


# ========== DEMONSTRAÇÃO COMPLETA: x(t) → x[n] → x(t) ==========

# 1. Criar sinal analógico original x(t)
duracao = 1  # 1 segundo
dt = 0.001  # resolução de 1ms
t_original = np.arange(0, duracao, dt)
frequencia_sinal = 5  # Hz
x_t_original = np.sin(2 * np.pi * frequencia_sinal * t_original)

print("=" * 60)
print("CONVERSÃO ANALÓGICA → DIGITAL → ANALÓGICA")
print("=" * 60)

# Testar com diferentes frequências de amostragem
fig, axes = plt.subplots(3, 1, figsize=(14, 10))

for idx, fs in enumerate([15, 20, 50]):
    print(f"\n--- Teste com fs = {fs} Hz ---")
    
    # PASSO 1: Amostragem x(t) → x[n]
    T = 1/fs  # Período de amostragem
    x_n = amostragem(x_t_original, fs)
    n_amostras = sum(1 for v in x_n if v != 0)
    print(f"✓ Amostragem concluída: {n_amostras} amostras")
    
    # PASSO 2: Recuperação x[n] → x(t)
    x_t_recuperado, t_recuperado = recuperacao_sinal(x_n, T, dt)
    print(f"✓ Recuperação concluída")
    
    # Plotar
    ax = axes[idx]
    ax.plot(t_original, x_t_original, 'b-', label='x(t) Original', 
            alpha=0.7, linewidth=2)
    ax.plot(t_recuperado, x_t_recuperado, 'g--', 
            label='x(t) Recuperado', linewidth=2, alpha=0.8)
    
    markerline, stemlines, baseline = ax.stem(t_original, x_n, 
                                               linefmt='r-', 
                                               markerfmt='ro', 
                                               basefmt='k-', 
                                               label=f'x[n] (fs={fs} Hz)')
    markerline.set_alpha(0.5)
    stemlines.set_alpha(0.5)
    
    ax.set_xlabel('Tempo (s)')
    ax.set_ylabel('Amplitude')
    ax.set_title(f'Recuperação do Sinal com fs={fs} Hz, T={T:.3f}s')
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print("\n" + "=" * 60)
print("Conversão completa!")
print("=" * 60)