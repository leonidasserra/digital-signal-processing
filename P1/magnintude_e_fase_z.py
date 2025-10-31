import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

def analisar_resposta_frequencia(num, den, N=512, plotar=True):
    """
    Analisa a resposta em frequência de um sistema discreto.
    
    Parâmetros:
    -----------
    num : array_like
        Coeficientes do numerador da função de transferência (potências decrescentes de z)
    den : array_like
        Coeficientes do denominador da função de transferência (potências decrescentes de z)
    N : int
        Número de pontos de frequência (padrão: 512)
    plotar : bool
        Se True, plota os gráficos de -2π a 2π
    
    Retorna:
    --------
    w : ndarray
        Vetor de frequências normalizadas (0 a π)
    H : ndarray
        Resposta em frequência complexa
    mag : ndarray
        Magnitude (linear)
    mag_dB : ndarray
        Magnitude em dB
    fase : ndarray
        Fase em radianos
    fase_graus : ndarray
        Fase em graus
    """
    
    # Calcula a resposta em frequência para [0, π]
    w, H = signal.freqz(num, den, worN=N, whole=False)
    
    # Calcula magnitude e fase
    mag = np.abs(H)
    mag_dB = 20 * np.log10(mag + 1e-10)
    fase = np.angle(H)  # Em radianos
    fase_graus = np.angle(H, deg=True)
    
    # Imprime expressões simbólicas
    print("=" * 60)
    print("FUNÇÃO DE TRANSFERÊNCIA H(z)")
    print("=" * 60)
    print(f"\nNumerador (potências decrescentes de z):")
    print(f"  {num}")
    print(f"\nDenominador (potências decrescentes de z):")
    print(f"  {den}")
    
    # Forma simbólica
    print("\nForma expandida:")
    num_str = " + ".join([f"{c:.4g}*z^(-{i})" if i > 0 else f"{c:.4g}" 
                          for i, c in enumerate(num) if c != 0])
    den_str = " + ".join([f"{c:.4g}*z^(-{i})" if i > 0 else f"{c:.4g}" 
                          for i, c in enumerate(den) if c != 0])
    print(f"H(z) = ({num_str}) / ({den_str})")
    
    print("\n" + "=" * 60)
    print("RESPOSTA EM FREQUÊNCIA H(e^jω)")
    print("=" * 60)
    print("\n|H(e^jω)| = Magnitude")
    print(f"  Em ω=0 (DC): {mag[0]:.6f} ({mag_dB[0]:.2f} dB)")
    print(f"  Em ω=π/2: {mag[N//2]:.6f} ({mag_dB[N//2]:.2f} dB)")
    print(f"  Em ω=π (Nyquist): {mag[-1]:.6f} ({mag_dB[-1]:.2f} dB)")
    print(f"  Máximo: {np.max(mag):.6f} ({np.max(mag_dB):.2f} dB)")
    print(f"  Mínimo: {np.min(mag):.6f} ({np.min(mag_dB):.2f} dB)")
    
    print("\n∠H(e^jω) = Fase")
    print(f"  Em ω=0: {fase_graus[0]:.2f}° ({fase[0]:.4f} rad)")
    print(f"  Em ω=π/2: {fase_graus[N//2]:.2f}° ({fase[N//2]:.4f} rad)")
    print(f"  Em ω=π: {fase_graus[-1]:.2f}° ({fase[-1]:.4f} rad)")
    
    # Expressões matemáticas
    print("\n" + "=" * 60)
    print("EXPRESSÕES MATEMÁTICAS")
    print("=" * 60)
    print("\nMagnitude:")
    print("  |H(e^jω)| = |H(z)|_{z=e^jω}")
    print("  Propriedade: |H(e^jω)| é PAR e PERIÓDICA com período 2π")
    print("\nFase:")
    print("  ∠H(e^jω) = arg(H(e^jω))")
    print("  Propriedade: ∠H(e^jω) é ÍMPAR e PERIÓDICA com período 2π")
    
    if plotar:
        # SEMPRE plota de -2π a 2π mostrando periodicidade
        w_ext = np.linspace(-2*np.pi, 2*np.pi, N*4)
        
        # Para magnitude (par): |H(e^-jω)| = |H(e^jω)|
        # Para fase (ímpar): ∠H(e^-jω) = -∠H(e^jω)
        mag_ext = np.zeros_like(w_ext)
        fase_ext = np.zeros_like(w_ext)
        
        for i, omega in enumerate(w_ext):
            omega_mod = omega % (2*np.pi)
            if omega_mod <= np.pi:
                idx = np.searchsorted(w, omega_mod)
                if idx >= len(mag): idx = len(mag) - 1
                mag_ext[i] = mag[idx]
                fase_ext[i] = fase[idx] if omega >= 0 else -fase[idx]
            else:
                omega_sym = 2*np.pi - omega_mod
                idx = np.searchsorted(w, omega_sym)
                if idx >= len(mag): idx = len(mag) - 1
                mag_ext[i] = mag[idx]
                fase_ext[i] = -fase[idx] if omega >= 0 else fase[idx]
        
        fase_graus_ext = fase_ext * 180/np.pi
        mag_dB_ext = 20 * np.log10(mag_ext + 1e-10)
        
        # =============================================================
        # PLOT 1: Magnitude linear + fase (juntos)
        # =============================================================
        fig1, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

        # --- Magnitude linear ---
        ax1.plot(w_ext, mag_ext, 'b-', linewidth=2, label='|H(e^jω)|')
        ax1.axvspan(0, np.pi, alpha=0.15, color='cyan', label='[0, π]')
        ax1.axvline(x=0, color='r', linestyle='--', alpha=0.4)
        ax1.axvline(x=np.pi, color='r', linestyle='--', alpha=0.4)
        ax1.set_ylabel('Magnitude (linear)', fontsize=11)
        ax1.set_title('Espectro de Magnitude (Linear) e Fase [-2π, 2π]', fontsize=13, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.set_xlim([-2*np.pi, 2*np.pi])
        ax1.set_xticks([-2*np.pi, -np.pi, 0, np.pi, 2*np.pi])
        ax1.set_xticklabels(['-2π', '-π', '0', 'π', '2π'])
        ax1.legend()

        # --- Fase ---
        ax2.plot(w_ext, fase_graus_ext, 'r-', linewidth=2, label='∠H(e^jω)')
        ax2.axvspan(0, np.pi, alpha=0.15, color='pink', label='[0, π]')
        ax2.axvline(x=0, color='r', linestyle='--', alpha=0.4)
        ax2.axvline(x=np.pi, color='r', linestyle='--', alpha=0.4)
        ax2.axhline(y=0, color='k', linestyle='--', alpha=0.3)
        ax2.set_xlabel('Frequência (rad/amostra)', fontsize=11)
        ax2.set_ylabel('Fase (graus)', fontsize=11)
        ax2.grid(True, alpha=0.3)
        ax2.set_xlim([-2*np.pi, 2*np.pi])
        ax2.set_xticks([-2*np.pi, -np.pi, 0, np.pi, 2*np.pi])
        ax2.set_xticklabels(['-2π', '-π', '0', 'π', '2π'])
        ax2.legend()

        plt.tight_layout()
        plt.show()
        
        # =============================================================
        # PLOT 2: Magnitude em dB separado
        # =============================================================
        fig2, ax3 = plt.subplots(figsize=(12, 6))
        ax3.plot(w_ext, mag_dB_ext, 'g-', linewidth=2, label='|H(e^jω)| (dB)')
        ax3.axvspan(0, np.pi, alpha=0.15, color='lime', label='[0, π]')
        ax3.axhline(y=-3, color='r', linestyle='--', alpha=0.4, label='-3 dB')
        ax3.axvline(x=0, color='r', linestyle='--', alpha=0.4)
        ax3.axvline(x=np.pi, color='r', linestyle='--', alpha=0.4)
        ax3.set_xlabel('Frequência (rad/amostra)', fontsize=11)
        ax3.set_ylabel('Magnitude (dB)', fontsize=11)
        ax3.set_title('Espectro de Magnitude |H(e^jω)| em dB [-2π, 2π]', fontsize=13, fontweight='bold')
        ax3.grid(True, alpha=0.3)
        ax3.set_xlim([-2*np.pi, 2*np.pi])
        ax3.set_xticks([-2*np.pi, -np.pi, 0, np.pi, 2*np.pi])
        ax3.set_xticklabels(['-2π', '-π', '0', 'π', '2π'])
        ax3.legend()
        plt.tight_layout()
        plt.show()

    return w, H, mag, mag_dB, fase, fase_graus


def plotar_polos_zeros(num, den):
    """
    Plota o diagrama de polos e zeros no plano Z.
    """
    # Calcula zeros e polos
    zeros = np.roots(num) if len(num) > 1 else np.array([])
    polos = np.roots(den) if len(den) > 1 else np.array([])
    
    # Cria figura
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Círculo unitário
    theta = np.linspace(0, 2*np.pi, 100)
    ax.plot(np.cos(theta), np.sin(theta), 'k--', linewidth=1.5, label='Círculo unitário')
    
    # Plota zeros
    if len(zeros) > 0:
        ax.plot(np.real(zeros), np.imag(zeros), 'go', markersize=12, 
                markerfacecolor='none', markeredgewidth=2, label='Zeros')
        for i, z in enumerate(zeros):
            ax.text(np.real(z), np.imag(z)+0.1, f'z{i}={z:.3f}', 
                   ha='center', fontsize=9)
    
    # Plota polos
    if len(polos) > 0:
        ax.plot(np.real(polos), np.imag(polos), 'rx', markersize=12, 
                markeredgewidth=2, label='Polos')
        for i, p in enumerate(polos):
            ax.text(np.real(p), np.imag(p)-0.15, f'p{i}={p:.3f}', 
                   ha='center', fontsize=9)
    
    ax.axhline(y=0, color='k', linewidth=0.5)
    ax.axvline(x=0, color='k', linewidth=0.5)
    ax.grid(True, alpha=0.3)
    ax.set_xlabel('Parte Real', fontsize=11)
    ax.set_ylabel('Parte Imaginária', fontsize=11)
    ax.set_title('Diagrama de Polos e Zeros', fontsize=13, fontweight='bold')
    ax.legend(fontsize=10)
    ax.axis('equal')
    
    # Define limites do plot
    max_val = max(1.5, 
                  np.max(np.abs(zeros)) + 0.5 if len(zeros) > 0 else 1.5,
                  np.max(np.abs(polos)) + 0.5 if len(polos) > 0 else 1.5)
    ax.set_xlim([-max_val, max_val])
    ax.set_ylim([-max_val, max_val])
    
    plt.tight_layout()
    plt.show()


def verificar_calculos(num, den):
    """
    Verifica os cálculos em pontos específicos para debug.
    """
    print("\n" + "=" * 60)
    print("VERIFICAÇÃO DE CÁLCULOS")
    print("=" * 60)
    
    # Testa em ω = 0, π/2, π
    omegas = [0, np.pi/2, np.pi]
    
    for omega in omegas:
        z = np.exp(1j * omega)
        
        # Calcula H(z) manualmente
        H_num = sum([c * z**(-k) for k, c in enumerate(num)])
        H_den = sum([c * z**(-k) for k, c in enumerate(den)])
        H = H_num / H_den
        
        mag = np.abs(H)
        fase_rad = np.angle(H)
        fase_grau = np.angle(H, deg=True)
        
        print(f"\nω = {omega:.4f} rad ({omega/np.pi:.2f}π):")
        print(f"  z = e^(j{omega:.4f}) = {z:.4f}")
        print(f"  H(e^jω) = {H:.6f}")
        print(f"  |H(e^jω)| = {mag:.6f}")
        print(f"  ∠H(e^jω) = {fase_rad:.4f} rad = {fase_grau:.2f}°")


def usar_funcao_nativa_scipy(num, den, N=512):
    """
    Usa signal.freqz do scipy - a função CORRETA para sistemas discretos.
    Este é o método nativo e mais confiável para transformada Z.
    """
    print("\n" + "="*70)
    print("USANDO scipy.signal.freqz (MÉTODO NATIVO PARA SISTEMAS DISCRETOS)")
    print("="*70)
    
    # signal.freqz é a função correta para sistemas discretos (transformada Z)
    w, H = signal.freqz(num, den, worN=N, whole=False)
    
    # Calcula magnitude e fase
    mag = np.abs(H)
    mag_dB = 20 * np.log10(mag + 1e-10)
    fase_rad = np.angle(H)
    fase_graus = np.angle(H, deg=True)
    
    print(f"\nPontos calculados: {len(w)}")
    print(f"Faixa de frequência: 0 a π rad/amostra")
    print(f"\nValores em pontos chave:")
    print(f"  ω=0:    |H|={mag[0]:.6f} ({mag_dB[0]:.2f} dB), ∠H={fase_graus[0]:.2f}°")
    print(f"  ω=π/2:  |H|={mag[N//2]:.6f} ({mag_dB[N//2]:.2f} dB), ∠H={fase_graus[N//2]:.2f}°")
    print(f"  ω=π:    |H|={mag[-1]:.6f} ({mag_dB[-1]:.2f} dB), ∠H={fase_graus[-1]:.2f}°")
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    # Magnitude em dB
    ax1.plot(w, mag_dB, 'b-', linewidth=2)
    ax1.axhline(y=0, color='k', linestyle='--', alpha=0.3)
    ax1.axhline(y=-3, color='r', linestyle='--', alpha=0.3, label='-3dB')
    ax1.set_xlabel('Frequência (rad/amostra)', fontsize=11)
    ax1.set_ylabel('Magnitude (dB)', fontsize=11)
    ax1.set_title('Espectro de Magnitude |H(e^jω)| - scipy.signal.freqz', fontsize=13, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim([0, np.pi])
    ax1.set_xticks([0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi])
    ax1.set_xticklabels(['0', 'π/4', 'π/2', '3π/4', 'π'])
    ax1.legend()
    
    # Fase em graus
    ax2.plot(w, fase_graus, 'r-', linewidth=2)
    ax2.axhline(y=0, color='k', linestyle='--', alpha=0.3)
    ax2.set_xlabel('Frequência (rad/amostra)', fontsize=11)
    ax2.set_ylabel('Fase (graus)', fontsize=11)
    ax2.set_title('Espectro de Fase ∠H(e^jω) - scipy.signal.freqz', fontsize=13, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim([0, np.pi])
    ax2.set_xticks([0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi])
    ax2.set_xticklabels(['0', 'π/4', 'π/2', '3π/4', 'π'])
    
    plt.tight_layout()
    plt.show()
    
    return w, H, mag, mag_dB, fase_rad, fase_graus


# ============================================================================
# EXEMPLOS DE USO
# ============================================================================

print("\n" + "="*70)
print("EXEMPLO 1: H(z) = z/(z-0.8) = 1/(1-0.8z^-1)")
print("="*70)
num1 = [1]
den1 = [1, -0.8]
verificar_calculos(num1, den1)
w1, H1, mag1, mag_dB1, fase1, fase_graus1 = analisar_resposta_frequencia(num1, den1)
plotar_polos_zeros(num1, den1)

# print("\n" + "="*70)
# print("EXEMPLO 2: Filtro Passa-Baixas H(z) = (0.5 + 0.5z^-1)/(1 - 0.8z^-1)")
# print("="*70)
# num2 = [0.5, 0.5]
# den2 = [1, -0.8]
# verificar_calculos(num2, den2)
# w2, H2, mag2, mag_dB2, fase2, fase_graus2 = analisar_resposta_frequencia(num2, den2)
# plotar_polos_zeros(num2, den2)

# print("\n" + "="*70)
# print("COMPARAÇÃO: Usando função nativa do scipy.signal")
# print("="*70)
# num_teste = [1]
# den_teste = [1, -0.8]
# usar_funcao_nativa_scipy(num_teste, den_teste)

# ============================================================================
# PARA USAR COM SUA PRÓPRIA FUNÇÃO DE TRANSFERÊNCIA:
# ============================================================================
# 
# MÉTODO 1 - Usando as funções personalizadas deste código:
# num = [b0, b1, b2, ...]  # Coeficientes de z^0, z^-1, z^-2, ...
# den = [a0, a1, a2, ...]  # Coeficientes de z^0, z^-1, z^-2, ...
#
# verificar_calculos(num, den)  # Para debug
# w, H, mag, mag_dB, fase, fase_graus = analisar_resposta_frequencia(num, den)
# plotar_polos_zeros(num, den)
#
# MÉTODO 2 - Usando função nativa do scipy (mais simples):
# usar_funcao_nativa_scipy(num, den)
#
# MÉTODO 3 - Usando apenas signal.freqz (o mais básico):
# w, H = signal.freqz(num, den, worN=512)
# mag = np.abs(H)
# fase = np.angle(H)
# ============================================================================