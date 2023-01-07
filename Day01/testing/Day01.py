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

data_set = pd.DataFrame({'t': np.linspace(0, 2 * np.pi, 100, endpoint=False)})
data_set['scale'] = 2 / (3 - np.cos(2 * data_set['t']))
data_set['x'] = data_set['scale'] * np.cos(data_set['t'])
data_set['y'] = data_set['scale'] * np.sin(2 * data_set['t']) / 2
data_set['noise_x'] = np.cos(data_set['t'])
data_set['noise_y'] = np.sin(data_set['t'])

point_count = 5
for i in range(1, point_count + 1):
    opensimplex.seed(i)
    data_set[f'x{i}'] = data_set.apply(lambda x: opensimplex.noise2(x['noise_x'], x['noise_y']), axis=1)/10 + data_set['x']
    data_set[f'y{i}'] = data_set.apply(lambda x: opensimplex.noise2(x['noise_x'], x['noise_y']), axis=1)/10 + data_set['y']

tail_length = 10
data_set = pd.concat((data_set.iloc[-tail_length:], data_set))

fade = np.zeros((tail_length - 1, 4))
fade[:, 3] = [np.square(x / tail_length + 1 / tail_length) for x in range(1, tail_length)]

# clean up one image then move over to Day01_PIL_base.py
img = 1
    
ax.set(xlim = [-1.2, 1.2], ylim = [-1.2, 1.2])
ax.set_aspect(1)

lines_numbers = np.floor(np.arange(1, (tail_length) * 2) / 2)[:((tail_length - 1) * 2)] + img
lines = data_set.iloc[lines_numbers]

for point_number in range(1, point_count + 1):
    segments = lines[[f'x{point_number}', f'y{point_number}']]
    segments = segments.to_numpy()
    segments = segments.reshape(tail_length - 1, 2, 2)

    lc = LineCollection(segments, colors=fade)
    line = ax.add_collection(lc)

plt.axis('off')
plt.savefig(f'Day01/images/img{img:03d}.png', bbox_inches='tight')
ax.cla()

# need to add more noise, slow down