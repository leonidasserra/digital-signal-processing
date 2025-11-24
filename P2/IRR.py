import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, cont2discrete, freqz, lfilter

def projetar_filtro_iir(N=None, fs=10000, fp=1000, fs_reject=1500, 
                        passband_ripple_db=1, stopband_atten_db=15,
                        plotar=True, testar=True):
    """
    Projeta e testa filtro IIR Butterworth usando invariância ao impulso
    
    N : int ou None
        Ordem do filtro. Se None, calcula automaticamente (padrão: None)
        Se fornecido, usa o valor especificado
    
    fs : float
        Frequência de amostragem em Hz (padrão: 10000 Hz)
    
    fp : float
        Frequência de corte (passagem) em Hz (padrão: 1000 Hz)
    
    fs_reject : float
        Frequência de rejeição em Hz (padrão: 1500 Hz)
    
    passband_ripple_db : float
        Ripple máximo na faixa de passagem em dB (padrão: 1 dB)
    
    stopband_atten_db : float
        Atenuação mínima na faixa de rejeição em dB (padrão: 15 dB)
    
    plotar : bool
        Se True, gera gráficos (padrão: True)
    
    testar : bool
        Se True, executa testes com diferentes frequências (padrão: True)
    
    RETORNA:
        dict com 'b_z', 'a_z' (coeficientes), 'specs' e 'resultados_testes'
    """
    
    # Calcular período de amostragem
    Ts = 1 / fs
    
    # Converter frequências de Hz para rad/amostra (frequências digitais)
    wp_digital = 2 * np.pi * fp / fs
    ws_digital = 2 * np.pi * fs_reject / fs
    
    # CÁLCULO DE N E Ωc (MÉTODO DO SLIDE 17)
    # Com Td = 1: Ωp = ωp e Ωs = ωs numericamente
    Omega_p = wp_digital  # rad/s (com Td=1)
    Omega_s = ws_digital  # rad/s (com Td=1)
    
    # Tolerâncias lineares (conversão de dB para linear)
    delta_p = 10**(-passband_ripple_db/20)      # Ex: 0,89125 para -1dB
    delta_s = 10**(-stopband_atten_db/20)       # Ex: 0,17783 para -15dB
    
    # Calcular ordem N (resolvendo sistema de equações Butterworth)
    # Fórmula: (Ωs/Ωp)^(2N) = [(1/δs)² - 1] / [(1/δp)² - 1]
    numerador = (1/delta_s)**2 - 1
    denominador = (1/delta_p)**2 - 1
    razao_freq = Omega_s / Omega_p
    
    N_calculado = np.log10(numerador/denominador) / (2 * np.log10(razao_freq))
    N_automatico = int(np.ceil(N_calculado))  # Arredondar para cima
    
    # Decidir qual N usar
    if N is None:
        N_usado = N_automatico
        print(f"🔢 N calculado automaticamente: {N_calculado:.4f} → N={N_usado}")
    else:
        N_usado = N
        if N != N_automatico:
            print(f"⚠️  N fornecido: {N} (calculado seria {N_automatico})")
        else:
            print(f"✓ N fornecido coincide com o calculado: {N}")
    
    # Calcular Ωc (ou Ωn) com N escolhido
    # Fórmula: 1 + (Ωp/Ωc)^(2N) = (1/δp)²
    # Resolvendo: Ωc = Ωp / [(1/δp)² - 1]^(1/2N)
    Omega_c = Omega_p / (((1/delta_p)**2 - 1)**(1/(2*N_usado)))
    
    print(f"✓ Ωc calculado: {Omega_c:.5f} rad/s (com Td=1)")
    
    # Mostrar especificações
    print("\n" + "="*70)
    print("ESPECIFICAÇÕES DO FILTRO (Invariância ao Impulso)")
    print("="*70)
    print(f"Ordem: N={N_usado} | Amostragem: fs={fs}Hz (Ts={Ts}s)")
    print(f"Método: Td=1 normalizado → ω=Ω | Ωc={Omega_c:.5f}rad/s")
    print(f"Passagem: {fp}Hz (ωp={wp_digital/np.pi:.3f}π) | Ripple≤{passband_ripple_db}dB (δp={delta_p:.5f})")
    print(f"Rejeição: {fs_reject}Hz (ωs={ws_digital/np.pi:.3f}π) | Atten≥{stopband_atten_db}dB (δs={delta_s:.5f})")
    print("="*70)
    
    # PASSO 1: Criar filtro analógico Butterworth H(s)
    b_s, a_s = butter(N_usado, Omega_c, btype='low', analog=True)
    
    # PASSO 2: Converter para digital H(z) usando invariância ao impulso
    # Usamos Td = 1 (normalizado) conforme slide do professor
    Td = 1  # Período normalizado
    sysd = cont2discrete((b_s, a_s), Td, method='impulse')
    b_z = sysd[0].flatten()
    a_z = sysd[1].flatten()
    
    print(f"\n✓ Filtro criado | Método: Invariância ao Impulso | Td=1")
    print(f"Coefs b ({len(b_z)}): {b_z}")
    print(f"Coefs a ({len(a_z)}): {a_z}")
    
    # PASSO 3: Calcular resposta em frequência
    w, h = freqz(b_z, a_z, worN=4096)
    h_db = 20 * np.log10(np.abs(h) + 1e-10)
    h_mag = np.abs(h)
    
    # Separar regiões de passagem e rejeição
    idx_passband = np.where(w <= wp_digital)[0]
    idx_stopband = np.where(w >= ws_digital)[0]
    
    # Verificar ganhos máximos e mínimos
    if len(idx_passband) > 0:
        passband_max = np.max(h_db[idx_passband])
        passband_min = np.min(h_db[idx_passband])
    else:
        passband_max = passband_min = 0
    
    if len(idx_stopband) > 0:
        stopband_max = np.max(h_db[idx_stopband])
    else:
        stopband_max = -100
    
    # Checar se atende as especificações
    passband_ok = (passband_min >= -passband_ripple_db) and (passband_max <= 0.1)
    stopband_ok = stopband_max <= -stopband_atten_db + 0.1  # margem de 0.1dB
    
    print("\n" + "="*70)
    print("VALIDAÇÃO")
    print("="*70)
    print(f"Passagem (0 a {wp_digital/np.pi:.3f}π): max={passband_max:.2f}dB, min={passband_min:.2f}dB")
    print(f"  Spec: 0 a -{passband_ripple_db}dB | {'✓ ATENDE' if passband_ok else '✗ NÃO ATENDE'}")
    print(f"Rejeição ({ws_digital/np.pi:.3f}π a π): max={stopband_max:.2f}dB")
    print(f"  Spec: ≤-{stopband_atten_db}dB | {'✓ ATENDE' if stopband_ok else '✗ NÃO ATENDE'}")
    print("="*70)
    
    # Plotar resposta em frequência
    if plotar:
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
        
        specs_text = f"N={N_usado}, fs={fs}Hz, fp={fp}Hz, fs_rej={fs_reject}Hz, Ripple≤{passband_ripple_db}dB, Atten≥{stopband_atten_db}dB"
        
        # Gráfico 1: Magnitude em dB
        ax1.plot(w, h_db, 'b-', linewidth=2.5, label='Resposta do filtro')
        ax1.axvline(wp_digital, color='g', linestyle='--', linewidth=2, 
                   label=f'fp={fp}Hz ({wp_digital/np.pi:.2f}π)')
        ax1.axvline(ws_digital, color='orange', linestyle='--', linewidth=2, 
                   label=f'fs={fs_reject}Hz ({ws_digital/np.pi:.2f}π)')
        ax1.axhline(0, color='green', linestyle=':', alpha=0.7, linewidth=1.5)
        ax1.axhline(-passband_ripple_db, color='green', linestyle=':', alpha=0.7, 
                   linewidth=1.5, label=f'Passagem: 0 a -{passband_ripple_db}dB')
        ax1.axhline(-stopband_atten_db, color='red', linestyle=':', alpha=0.7, 
                   linewidth=1.5, label=f'Rejeição: ≤-{stopband_atten_db}dB')
        
        ax1.set_xlabel('Frequência (rad/amostra)', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Magnitude (dB)', fontsize=12, fontweight='bold')
        ax1.set_title(f'Magnitude Logarítmica - {specs_text}', fontsize=13, fontweight='bold')
        ax1.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
        ax1.legend(fontsize=10, loc='upper right')
        ax1.set_xlim([0, np.pi])
        ax1.set_ylim([-100, 5])
        
        # Gráfico 2: Magnitude linear
        threshold_pass = 10**(-passband_ripple_db/20)
        threshold_stop = 10**(-stopband_atten_db/20)
        
        ax2.plot(w, h_mag, 'b-', linewidth=2.5, label='Resposta do filtro')
        ax2.axvline(wp_digital, color='g', linestyle='--', linewidth=2, 
                   label=f'fp={fp}Hz')
        ax2.axvline(ws_digital, color='orange', linestyle='--', linewidth=2, 
                   label=f'fs={fs_reject}Hz')
        ax2.axhline(1.0, color='green', linestyle=':', alpha=0.7, linewidth=1.5)
        ax2.axhline(threshold_pass, color='green', linestyle=':', alpha=0.7, 
                   linewidth=1.5, label=f'Limite passagem: {threshold_pass:.5f}')
        ax2.axhline(threshold_stop, color='red', linestyle=':', alpha=0.7, 
                   linewidth=1.5, label=f'Limite rejeição: {threshold_stop:.5f}')
        
        ax2.set_xlabel('Frequência (rad/amostra)', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Amplitude', fontsize=12, fontweight='bold')
        ax2.set_title(f'Magnitude Linear - {specs_text}', fontsize=13, fontweight='bold')
        ax2.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
        ax2.legend(fontsize=10, loc='upper right')
        ax2.set_xlim([0, np.pi])
        ax2.set_ylim([0, 1.2])
        
        plt.tight_layout()
        plt.show()
    
    # Testar o filtro com várias frequências
    resultados_testes = []
    
    if testar:
        print("\n" + "="*70)
        print("TESTES")
        print("="*70)
        
        # Lista de frequências para testar
        frequencias_teste = [
            fp * 0.1,          # 10% da corte
            fp * 0.5,          # 50% da corte
            fp * 0.8,          # 80% da corte
            fp,                # Exatamente na corte
            fp * 1.2,          # 20% acima
            fs_reject,         # Na rejeição
            fs_reject * 1.5,   # 50% acima da rejeição
            fs_reject * 2,     # 2x a rejeição
            fs * 0.4,          # 40% de Nyquist
        ]
        
        for freq in frequencias_teste:
            # Criar sinal senoidal de teste
            duracao = 0.02  # 20ms
            t = np.arange(0, duracao, Ts)
            x = np.sin(2 * np.pi * freq * t)
            
            # Aplicar o filtro
            y = lfilter(b_z, a_z, x)
            
            # Calcular atenuação após regime transitório
            n_stable = len(y) // 2
            x_rms = np.sqrt(np.mean(x[n_stable:]**2))
            y_rms = np.sqrt(np.mean(y[n_stable:]**2))
            
            if x_rms > 1e-10:
                atenuacao_db = 20 * np.log10(y_rms / x_rms)
            else:
                atenuacao_db = -np.inf
            
            # Classificar resultado
            if freq <= fp:
                esperado = "PASSA"
                ok = atenuacao_db >= -passband_ripple_db - 3
            elif freq >= fs_reject:
                esperado = "REJEITA"
                ok = atenuacao_db <= -stopband_atten_db + 3
            else:
                esperado = "TRANSIÇÃO"
                ok = True
            
            status = "✓" if ok else "✗"
            
            print(f"{status} {freq:7.1f} Hz | Atenuação: {atenuacao_db:7.2f} dB | {esperado:10s}")
            
            resultados_testes.append({
                'freq': freq,
                't': t,
                'x': x,
                'y': y,
                'atten_db': atenuacao_db,
                'esperado': esperado,
                'ok': ok
            })
        
        print("="*70)
        
        # Plotar alguns casos
        if plotar and len(resultados_testes) >= 4:
            indices_plot = [1, 3, 5, 7]
            fig, axes = plt.subplots(2, 2, figsize=(16, 10))
            axes = axes.flatten()
            
            for idx, caso_idx in enumerate(indices_plot):
                if caso_idx < len(resultados_testes):
                    res = resultados_testes[caso_idx]
                    ax = axes[idx]
                    
                    ax.plot(res['t'], res['x'], 'b-', alpha=0.6, 
                           label=f"Entrada {res['freq']:.0f} Hz", linewidth=2)
                    ax.plot(res['t'], res['y'], 'r-', alpha=0.9, 
                           label=f"Saída ({res['atten_db']:.1f} dB)", linewidth=2.5)
                    
                    status_text = '✓ OK' if res['ok'] else '✗ FALHOU'
                    ax.set_title(f"{res['freq']:.0f} Hz ({res['esperado']}) - {status_text}", 
                               fontsize=12, fontweight='bold')
                    ax.set_xlabel('Tempo (s)', fontsize=10)
                    ax.set_ylabel('Amplitude', fontsize=10)
                    ax.legend(loc='upper right', fontsize=9)
                    ax.grid(True, alpha=0.3)
                    ax.set_xlim([0, 0.01])
            
            plt.suptitle(f'Testes do Filtro - {specs_text}', 
                        fontsize=14, fontweight='bold', y=0.995)
            plt.tight_layout()
            plt.show()
    
    # Retornar resultados
    return {
        'b_z': b_z,
        'a_z': a_z,
        'specs': {
            'N': N_usado,
            'N_calculado': N_calculado,
            'Omega_c': Omega_c,
            'fs': fs,
            'fp': fp,
            'fs_reject': fs_reject,
            'passband_ripple_db': passband_ripple_db,
            'stopband_atten_db': stopband_atten_db,
            'delta_p': delta_p,
            'delta_s': delta_s,
            'passband_ok': passband_ok,
            'stopband_ok': stopband_ok
        },
        'resultados_testes': resultados_testes
    }


# Executar com os parâmetros do slide 15/32
if __name__ == "__main__":
    
    # Opção 1: Calcular N automaticamente
    # resultado = projetar_filtro_iir(
    #     N=None,                 # Calcula automaticamente
    #     fs=10000,
    #     fp=1000,
    #     fs_reject=1500,
    #     passband_ripple_db=1,
    #     stopband_atten_db=15,
    #     plotar=True,
    #     testar=True
    # )
    
    # Opção 2: Forçar N=6 como no slide
    resultado = projetar_filtro_iir(
        N=6,                    # Forçar N=6 (como no slide)
        fs=10000,
        fp=1000,
        fs_reject=1500,
        passband_ripple_db=1,
        stopband_atten_db=15,
        plotar=True,
        testar=True
    )
    