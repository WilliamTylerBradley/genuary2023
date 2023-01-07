import opensimplex
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data_set = pd.DataFrame({'t': np.linspace(0, 2 * np.pi, 50, endpoint=False)})
data_set['x'] = np.cos(data_set['t'])
data_set['y'] = np.sin(data_set['t'])

data_set['noise'] = data_set.apply(lambda x: opensimplex.noise2(x['x'], x['y']), axis=1)
# print(data_set)

fig, ax = plt.subplots()
ax.set(xlim = [-1.2, 6.5], ylim = [-1.2, 1.2])
ax.set_aspect(1)

ax.scatter(data_set['t'], data_set['noise'])
plt.show()