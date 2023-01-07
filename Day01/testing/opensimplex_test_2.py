import pandas as pd
import numpy as np
import opensimplex
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from PIL import Image

fig, ax = plt.subplots()

colors = [[0, 0, 0, .25],
          [0, 0, 0, .5],
          [0, 0, 0, .75],
          [0, 0, 0, 1]]

data_set = pd.DataFrame({'t': np.linspace(0, 2 * np.pi, 50, endpoint=False)})
data_set['scale'] = 2 / (3 - np.cos(2 * data_set['t']))
data_set['x'] = data_set['scale'] * np.cos(data_set['t'])
data_set['y'] = data_set['scale'] * np.sin(2 * data_set['t']) / 2

point_count = 5
for i in range(1, point_count + 1):
    opensimplex.seed(i)
    data_set[f'x{i}'] = data_set.apply(lambda x: opensimplex.noise2(x['x'], x['y']), axis=1)/10 + data_set['x']
    data_set[f'y{i}'] = data_set.apply(lambda x: opensimplex.noise2(x['x'], x['y']), axis=1)/10 + data_set['y']

tail_length = 5
data_set = pd.concat((data_set.iloc[-tail_length:], data_set))

# clean up one image then move over to Day01_PIL_base.py
img = 2
    
ax.set(xlim = [-1.2, 1.2], ylim = [-1.2, 1.2])
ax.set_aspect(1)

ax.scatter(data_set['x3'], data_set['y3'])
plt.show()
