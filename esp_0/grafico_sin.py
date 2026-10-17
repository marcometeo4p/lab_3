import numpy as np
import matplotlib.pyplot as plt

x=np.linspace(0, 2*np.pi, 1000)
y=np.sin(x)
plt.plot(x, y,color='orange', alpha=0.8)
plt.title('Segnale Sinusoidale')
plt.xlabel('Tempo (secondi)')
plt.ylabel('Ampiezza')
plt.grid(True)
plt.savefig("plot.png")
plt.show()