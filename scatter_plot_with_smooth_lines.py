import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

abc= [1.0, 3.0, 5.0, 5.0]
y= [6.0, 4.0, 2.0, 80.0]

x_new = np.linspace(min(abc), max(abc),500)

f = interp1d(abc, y, kind='quadratic')
y_smooth=f(x_new)

print(x_new, y_smooth)
print(abc, y)
plt.plot (x_new,y_smooth)
plt.scatter (abc, y)
plt.show()