import numpy as np
from scipy.signal import lfilter
import matplotlib.pyplot as plt

# --- 1. Definição da Função de Transferência H(z) ---
# A função de transferência H(z) é uma razão de polinômios em z⁻¹:
#        b[0] + b[1]z⁻¹ + b[2]z⁻² + ...
# H(z) = ------------------------------------
#        a[0] + a[1]z⁻¹ + a[2]z⁻² + ...
#
# Exemplo: H(z) = (0.5 + 0.5z⁻¹) / (1 - 0.8z⁻¹)
#
# Coeficientes do numerador (b)
b = [0.5, 0.5]
# Coeficientes do denominador (a)
a = [1, -0.8]

# --- 2. Definição do Sinal de Entrada x[n] no tempo ---
# Vamos usar um sinal degrau unitário (step function) como entrada.
# O sinal terá 30 amostras de tempo.
n_samples = 30
# Cria um vetor de tempo discreto de 0 a 29
n = np.arange(n_samples)
# O sinal de entrada x[n] é 1 para todo n >= 0
x = np.ones(n_samples)

# Alternativa: Para um impulso unitário (delta de Kronecker)
# x = np.zeros(n_samples)
# x[0] = 1

# --- 3. Aplicação do Filtro para Obter a Resposta y[n] ---
# A função lfilter(b, a, x) calcula a saída y[n] do sistema.
y = lfilter(b, a, x)

# --- 4. Exibição dos Resultados ---
print("Função de Transferência:")
print(f"  Numerador (b): {b}")
print(f"  Denominador (a): {a}\n")

print("Sinal de Entrada x[n] (primeiras 10 amostras):")
print(f"  {x[:10]}\n")

print("Sinal de Saída (Resposta) y[n] (primeiras 10 amostras):")
print(f"  {np.round(y[:10], 4)}\n") # Arredondando para 4 casas decimais


# --- 5. Visualização Gráfica ---
plt.figure(figsize=(12, 6))
plt.stem(n, x, 'b', markerfmt='bo', basefmt=" ", label='Entrada x[n] (Degrau)')
plt.stem(n, y, 'r', markerfmt='ro', basefmt=" ", label='Saída y[n] (Resposta)')
plt.title('Resposta do Sistema ao Degrau Unitário')
plt.xlabel('Amostra de Tempo (n)')
plt.ylabel('Amplitude')
plt.grid(True)
plt.legend()
plt.show()