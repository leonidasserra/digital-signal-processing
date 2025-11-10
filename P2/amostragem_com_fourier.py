import numpy as np
import matplotlib.pyplot as plt

def amostragem_completa(x_t, t, fs, plotar=True):

    
    T = 1/fs  # Período de amostragem
    dt = t[1] - t[0]  # Resolução temporal
    
    # ===== AMOSTRAGEM =====
    passo = int(T/dt)
    trem = np.zeros(len(x_t))
    for i in range(len(trem)):
        if i % passo == 0:
            trem[i] = 1
    
    x_n = x_t * trem  # Sinal amostrado (com zeros)
    
    # Extrair valores compactos
    indices_amostras = []
    x_n_compacto = []
    for i in range(len(x_n)):
        if x_n[i] != 0:
            indices_amostras.append(i)
            x_n_compacto.append(x_n[i])
    
    # ===== TRANSFORMADA DE FOURIER =====
    
    # Fourier de x(t) - sinal contínuo
    N_t = len(x_t)
    X_f = np.fft.fft(x_t)
    X_f_mag = np.abs(X_f) / N_t
    freqs_t = np.fft.fftfreq(N_t, dt)
    
    # Fourier de x[n] - sinal amostrado
    X_n_f = np.fft.fft(x_n)
    X_n_f_mag = np.abs(X_n_f) / N_t
    freqs_n = np.fft.fftfreq(N_t, dt)
    
    # Informações
    info = {
        'T': T,
        'fs': fs,
        'n_amostras': len(x_n_compacto),
        'X_f': X_f,
        'X_n_f': X_n_f,
        'freqs': freqs_t
    }
    
    # ===== PLOTAGEM =====
    if plotar:
        fig = plt.figure(figsize=(16, 10))
        
        # ===== DOMÍNIO DO TEMPO =====
        
        # Subplot 1: x(t) - Sinal Contínuo
        plt.subplot(2, 2, 1)
        plt.plot(t, x_t, 'b-', linewidth=2, label='x(t)')
        plt.xlabel('Tempo (s)')
        plt.ylabel('Amplitude')
        plt.title('Sinal Contínuo x(t)')
        plt.grid(True, alpha=0.3)
        plt.legend()
        
        # Subplot 2: x[n] - Sinal Amostrado
        plt.subplot(2, 2, 2)
        plt.plot(t, x_t, 'b-', alpha=0.3, linewidth=1, label='x(t) original')
        markerline, stemlines, baseline = plt.stem(t, x_n, 
                                                     linefmt='r-', 
                                                     markerfmt='ro', 
                                                     basefmt='k-',
                                                     label=f'x[n] (fs={fs} Hz)')
        markerline.set_alpha(0.7)
        stemlines.set_alpha(0.7)
        plt.xlabel('Tempo (s)')
        plt.ylabel('Amplitude')
        plt.title(f'Sinal Amostrado x[n] (T={T:.4f}s, {len(x_n_compacto)} amostras)')
        plt.grid(True, alpha=0.3)
        plt.legend()
        
        # ===== DOMÍNIO DA FREQUÊNCIA =====
        
        # Subplot 3: Fourier de x(t)
        plt.subplot(2, 2, 3)
        # Plotar apenas frequências positivas até fs/2
        mask_pos = (freqs_t >= 0) & (freqs_t <= fs)
        plt.plot(freqs_t[mask_pos], X_f_mag[mask_pos], 'b-', linewidth=2)
        plt.xlabel('Frequência (Hz)')
        plt.ylabel('Magnitude')
        plt.title('Transformada de Fourier de x(t)')
        plt.grid(True, alpha=0.3)
        plt.xlim([0, fs])
        
        # Subplot 4: Fourier de x[n] - MOSTRANDO REPETIÇÕES
        plt.subplot(2, 2, 4)
        # Plotar até 2*fs para mostrar as repetições (aliasing)
        mask_rep = (freqs_n >= 0) & (freqs_n <= 2*fs)
        plt.plot(freqs_n[mask_rep], X_n_f_mag[mask_rep], 'r-', linewidth=2)
        
        # Marcar fs
        plt.axvline(x=fs, color='orange', linestyle='--', linewidth=2, 
                    label=f'fs = {fs} Hz')
        
        # Destacar as repetições
        plt.text(fs*0.15, max(X_n_f_mag[mask_rep])*0.9, 
                'Espectro\nOriginal', fontsize=10, ha='center',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        if 2*fs <= max(freqs_n):
            plt.text(fs*1.15, max(X_n_f_mag[mask_rep])*0.9, 
                    'Repetição\n(Aliasing)', fontsize=10, ha='center',
                    bbox=dict(boxstyle='round', facecolor='salmon', alpha=0.5))
        
        plt.xlabel('Frequência (Hz)')
        plt.ylabel('Magnitude')
        plt.title('Transformada de Fourier de x[n]\n(Note as repetições a cada fs)')
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.xlim([0, 2*fs])
        
        plt.tight_layout()
        plt.show()
    
    return x_n, np.array(x_n_compacto), np.array(indices_amostras), info


# ========== EXEMPLO DE USO ==========

# Criar sinal contínuo x(t)
duracao = 1  # 1 segundo
dt = 0.001  # resolução de 1ms
t = np.arange(0, duracao, dt)

# Sinal com múltiplas frequências
f1 = 5  # Hz
f2 = 8  # Hz
x_t = np.sin(2 * np.pi * f1 * t) + 0.5 * np.sin(2 * np.pi * f2 * t)

print("\n" + "="*70)
print("TESTE 1: fs = 30 Hz")
print("="*70)
fs1 = 10
x_n1, x_n_comp1, indices1, info1 = amostragem_completa(x_t, t, fs1)