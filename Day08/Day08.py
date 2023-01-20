# Import packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import product

''' Set up data '''
data_set = pd.DataFrame(data = list(product(np.arange(-100, 100, 1), np.arange(-100, 100, 1))),
                        columns=['x', 'y'])

''' SDF circle '''
def sdf_circle(x, y, cx, cy, r):
    x -= cx
    y -= cy
    value = abs(np.sqrt(x*x + y*y) - r) - 2.5
    if value < -1:
        return -1
    elif value < 1:
        return 0
    else:
        return 1
sdf_circle_vectorized = np.vectorize(sdf_circle, otypes=[float],cache=False)

''' 10 random smaller circle (radius between 0 and 30) on a big circle (radius = 50) '''
n_circles = 10
np.random.seed(8)
for circle_number in np.arange(n_circles): 
    random_point = np.random.random(1) * 2 * np.pi
    random_radius = np.random.random(1) * 30
    data_set[f'circle_{circle_number}'] = list(sdf_circle_vectorized(data_set['x'],data_set['y'],
                                                                     50 * np.cos(random_point),
                                                                     50 * np.sin(random_point),
                                                                     random_radius))

''' Find all points that are on those circles '''                                                                     
column_list = [f'circle_{x}' for x in np.arange(n_circles)]
data_set['value'] = data_set[column_list].min(axis=1)

''' Contour plot '''
## https://alex.miller.im/posts/contour-plots-in-python-matplotlib-x-y-z/
Z = data_set.pivot_table(index='x', columns='y', values='value').T.values
X_unique = np.sort(data_set.x.unique())
Y_unique = np.sort(data_set.y.unique())
X, Y = np.meshgrid(X_unique, Y_unique)

plt.contourf(X, Y, Z, levels = [-1, 0, 1], colors=['#FFD700', '#4682B4', '#4682B4'])
plt.gca().set_aspect('equal')
plt.axis('off')
plt.savefig('Day08/Day08.png')