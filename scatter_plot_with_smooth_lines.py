import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

x=np.array([0.1, 0.3, 0.5, 0.7, 0.9, 1.1, 1.3, 1.5, 1.7, 1.9, 2])
y=np.array([0.57,0.85,0.66,0.84,0.59,0.55,0.61,0.76,0.54,0.55,0.48])

x_new = np.linspace(x.min(), x.max(),500)

f = interp1d(x, y, kind='quadratic')
y_smooth=f(x_new)

plt.plot (x_new,y_smooth)
plt.scatter (x, y)
plt.show()