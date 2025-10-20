import numpy as np
import matplotlib.pyplot as plt

# 1. Definição do Sistema
num = [0.038, 0.034]
den = [1, -1.63, 0.70]

# 2. Definição do Sinal de Entrada Senoidal
A_in = 1
omega_0 = np.pi / 4
phi_in = 0

print(f"Sinal de Entrada: x[n] = {A_in:.2f} * cos({omega_0:.2f}*n + {phi_in:.2f})\n")

# 3. Cálculo da Resposta em Frequência para ω0
z = np.exp(1j * omega_0)
H_em_omega_0 = np.polyval(num, z) / np.polyval(den, z)

# 4. Amplitude e fase da resposta
mag_H = np.abs(H_em_omega_0)
fase_H = np.angle(H_em_omega_0)

print(f"Na frequência Ω₀ = {omega_0:.2f} rad/amostra:")
print(f"   - Ganho de Amplitude |H(e^jΩ₀)| = {mag_H:.4f}")
print(f"   - Deslocamento de Fase ∠H(e^jΩ₀) = {fase_H:.4f} rad\n")

# 5. Sinal de saída previsto
A_out = A_in * mag_H
phi_out = phi_in + fase_H

print(f"Sinal de Saída Previsto: y[n] = {A_out:.2f} * cos({omega_0:.2f}*n + {phi_out:.2f})")

# 6. Geração e plotagem dos sinais
n = np.arange(0, 51)
x_n = A_in * np.cos(omega_0 * n + phi_in)
y_n = A_out * np.cos(omega_0 * n + phi_out)

# Plot
plt.figure(figsize=(8, 4))
plt.plot(n, x_n, 'b-o', label='Sinal de Entrada x[n]', linewidth=1.5)
plt.plot(n, y_n, 'r-s', label='Sinal de Saída y[n]', linewidth=1.5)
plt.title('Resposta do Sistema a uma Entrada Senoidal')
plt.xlabel('Amostra (n)')
plt.ylabel('Amplitude')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()


# Deslocamento para direita (atraso):
# x[n]u[n] <=> X[z]
# x[n - 1]u[n - 1] <=> (1/z) * X[z]
# x[n - m]u[n - m] <=> (1/z**m) * X[z]
# x[n - 1]u[n] <=> (1/z) * X[z] + x[-1]
# x[n - 2]u[n] <=> (1/z**2) * X[z] + (1/z) * x[-1] + x[-2]

# Deslocamento para esquerda (avanço):
# x[n]u[n] <=> X[z]
# x[n + 1]u[n] <=> z*X[z] - z*x[0]
# x[n + 2]u[n] <=> (z**2)*X[z] - (z**2)*x[0] - z*x[1]
