import numpy as np
import matplotlib.pyplot as plt
import math


n = np.arange(80)
x=np.cos(np.pi*n/4)
x2=np.cos(np.pi*n*3/8)

x3=np.cos(np.pi*n*1.5)
x4=np.cos(np.pi*n*0.9)

# plt.stem(n,x,linecolor='red',marker='o')
# plt.stem(n,x2,label="x2")

# plt.plot(n,x3,color='red')
# plt.plot(n,x4,color='blue')


# Cria uma figura com dois subplots (1 linha, 2 colunas)
# 'fig' é a figura inteira e 'axs' é uma array com os dois subplots
fig, axs = plt.subplots(1, 2)

# Plota o primeiro stem no primeiro subplot (índice 0)
axs[0].stem(n, x3, linefmt='red', markerfmt='ro', basefmt=' ', label='1.5Pi')
axs[0].set_title('Gráfico 1.5Pi')
axs[0].set_xlabel('Índice (n)')
axs[0].set_ylabel('Amplitude')

# Plota o segundo stem no segundo subplot (índice 1)
axs[1].stem(n, x4, linefmt='blue', markerfmt='bo', basefmt=' ', label='0.9Pi')
axs[1].set_title('Gráfico 0.9Pi')
axs[1].set_xlabel('Índice (n)')
axs[1].set_ylabel('Amplitude')

# Ajusta o layout para evitar sobreposição de títulos e rótulos
plt.tight_layout()

# Exibe o gráfico
plt.show()

# print(3*math.pi/8)