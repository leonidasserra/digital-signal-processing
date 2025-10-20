import numpy as np
import matplotlib.pyplot as plt

def convolucao(x, h):
    result = [0] * (len(x) + len(h) - 1)

    for i in range(len(result)):        
        for k in range(len(x)):         
            if 0 <= i - k < len(h):   
                result[i] += x[k] * h[i - k]
    print(result)
    return result

n=np.arange(0,3)
x = [500,500,500] 
h = 1 + 9901*(0.99)**n;    

y=convolucao(x,h)

print(np.convolve(x,h))

fig, axs = plt.subplots(3, 1, figsize=(6, 4), sharex=True)
t = np.arange(0, max(len(x), len(h)),1)

axs[0].stem(t[:len(x)], x, linefmt='red', markerfmt='ro', basefmt='k')
axs[0].set_title('Entrada')
axs[0].grid(True)

axs[1].stem(t[:len(h)], h, linefmt='blue', markerfmt='bo', basefmt='k')
axs[1].set_title('H')
axs[1].grid(True)

axs[2].stem(np.arange(len(y)), y, linefmt='green', markerfmt='go', basefmt='k')
axs[2].set_title('Convolução')
axs[2].grid(True)

plt.xlabel('Tempo (n)')
plt.tight_layout()
plt.show()


# np.convolve(x, h)
  