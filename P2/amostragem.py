import numpy as np
import matplotlib.pyplot as plt

def amostragem(x,fs):
    #assumindo  que a frequencia de amostragem de x continuo é 0.001s:
    passo = int((1/fs)/0.001)
    trem=np.zeros(len(x))
    for i in range(len(trem)):
        if i%passo==0:
            trem[i]=1

    x_amostrado=[0]*len(x)
    for i in range(len(x)):        
        x_amostrado[i] = x[i] * trem[i]
    print(x_amostrado)


    # valores_compactos = []
    # indices_compactos = []
    # for i in range(len(x_amostrado)):
    #     if x_amostrado[i] != 0:
    #         valores_compactos.append(x_amostrado[i])
    #         indices_compactos.append(i)
    return x_amostrado

duracao = 1  # 1 segundo
t = np.arange(0, duracao, 0.001)  # vetor de tempo com 0.001s de resolução
frequencia_sinal = 5  # Hz
x = np.sin(2 * np.pi * frequencia_sinal * t)

# Amostrando com fs = 20 Hz
fs = 20
x_amostrado = amostragem(x, fs)

# Plotando
plt.figure(figsize=(12, 6))
plt.plot(t, x, 'b-', label='Sinal Original', alpha=0.7, linewidth=2)
plt.stem(t, x_amostrado, linefmt='r-', markerfmt='ro', basefmt='k-', label=f'Sinal Amostrado (fs={fs} Hz)')
plt.xlabel('Tempo (s)')
plt.ylabel('Amplitude')
plt.title('Amostragem de Sinal')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

print(f"Número de amostras: {sum(1 for v in x_amostrado if v != 0)}")





"""
    Processo completo de amostragem com análise no domínio do tempo e frequência.
    
    Parâmetros:
    - x_t: sinal contínuo x(t)
    - t: vetor de tempo correspondente
    - fs: frequência de amostragem
    - plotar: se True, gera os gráficos
    
    Retorna:
    - x_n: sinal amostrado (vetor esparso com zeros)
    - x_n_compacto: apenas os valores amostrados
    - indices_amostras: índices das amostras
    - info: dicionário com informações espectrais
"""