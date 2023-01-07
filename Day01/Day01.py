# Import packages
import pandas as pd
import numpy as np
import opensimplex
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from PIL import Image

''' Set up data set '''
# Use t as parameter to go around the infinity sign/circle
data_set = pd.DataFrame({'t': np.linspace(0, 2 * np.pi, 100, endpoint=False)})

# Formulas for x and y loop around an infinity sign
data_set['scale'] = 2 / (3 - np.cos(2 * data_set['t']))
data_set['x'] = data_set['scale'] * np.cos(data_set['t'])
data_set['y'] = data_set['scale'] * np.sin(2 * data_set['t']) / 2

# Formulas for noise_x and noise_y loop around a circle
noise_amount = 1.5
data_set['noise_x'] = noise_amount * np.cos(data_set['t'])
data_set['noise_y'] = noise_amount * np.sin(data_set['t'])

# For each point, add noise that loops around a circle in 2-d space.
# This way, there's a smooth transition from start, to finish, and repeating.
point_count = 5
seed_value = 50
for i in range(1, point_count + 1):
    opensimplex.seed(i + seed_value)
    data_set[f'x{i}'] = data_set.apply(lambda x: opensimplex.noise2(x['noise_x'], x['noise_y']), axis=1)/10 + data_set['x']
    data_set[f'y{i}'] = data_set.apply(lambda x: opensimplex.noise2(x['noise_x'], x['noise_y']), axis=1)/10 + data_set['y']

# Add on a tail
tail_length = 75
data_set = pd.concat((data_set.iloc[-tail_length:], data_set))

''' Add the fade for the tail '''
fade = np.zeros((tail_length - 1, 4))
fade[:, 3] = [np.square(x / tail_length + 1 / tail_length) for x in range(1, tail_length)]

''' Set up the plotting '''
fig, ax = plt.subplots()

''' Print each image of the gif '''
for img in range(1, len(data_set.index) - tail_length):

    # Reset the image from clearing out old information
    ax.set(xlim = [-1.2, 1.2], ylim = [-1.2, 1.2])
    ax.set_aspect(1)
    plt.axis('off')

    # Pull the rows from data_set to draw
    lines_numbers = np.floor(np.arange(1, (tail_length) * 2) / 2)[:((tail_length - 1) * 2)] + img
    lines = data_set.iloc[lines_numbers]

    # Draw each point with tail (as line segments)
    for point_number in range(1, point_count + 1):
        segments = lines[[f'x{point_number}', f'y{point_number}']]
        segments = segments.to_numpy()
        segments = segments.reshape(tail_length - 1, 2, 2)

        lc = LineCollection(segments, colors=fade)
        line = ax.add_collection(lc)

    # Save image and reset
    plt.savefig(f'Day01/images/img{img:03d}.png', bbox_inches='tight')
    ax.cla()
    
''' Pull all the images '''
images = []
for img in range(1, len(data_set.index) - tail_length):
    images.append(Image.open(f'Day01/images/img{img:03d}.png'))

''' Save as a gif '''
images[0].save('Day01/Day01.gif',
                save_all=True, append_images=images[1:], optimize=False, duration=40, loop=0)