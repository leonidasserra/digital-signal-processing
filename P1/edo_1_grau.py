import numpy as np
import matplotlib.pyplot as plt

tau=1
k=0
a=-1/tau
b=-k/tau

vo=5

c=vo-k

t=np.arange(50)
e=np.exp
y=(b/a)+np.multiply(c,np.exp(np.multiply(a,t)))



plt.plot(t,y)
plt.show()