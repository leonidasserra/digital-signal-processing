import numpy as np
import matplotlib.pyplot as plt
from impulse import impulse

# Função atraso
def atraso(array, k):
    newarray = []
    for i in range(len(array)):
        if i - k < 0:
            newarray.append(0)
        else:
            newarray.append(array[i - k])
    return newarray


#SE FOR USAR ATERASO COMO IMPORT, COMENTAR ESSE PLOT
# Parâmetros
n = 3
k = 2
x_impulso = impulse(n)
x_atrasado = atraso(x_impulso, k)
t = np.arange(-n, len(x_impulso) - n)

# Subplots
fig, axs = plt.subplots(2, 1, figsize=(6, 4), sharex=True)

axs[0].stem(t, x_impulso, linefmt='red', markerfmt='ro', basefmt='k')
axs[0].set_title('Impulso original')
axs[0].grid(True)

axs[1].stem(t, x_atrasado, linefmt='blue', markerfmt='bo', basefmt='k')
axs[1].set_title(f'Impulso atrasado de {k} unidades')
axs[1].grid(True)

plt.xlabel('Tempo (n)')
plt.tight_layout()
plt.show()