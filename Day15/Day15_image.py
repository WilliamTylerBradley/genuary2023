# Import packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import glob
from PIL import Image

# sine wave class
class sine_wave():
    frequency = 1

    def __init__(self, amplitude, phase, shift):
        self.amplitude = amplitude
        self.phase = phase
        self.shift = shift

    def location(self, time):
        return self.amplitude * np.sin( self.frequency * time + self.phase ) + self.shift

# Create collection of waves
num_sets = 3
num_waves = 100
wave_sets = [{} for _ in range(num_sets)]
for s in np.arange(0, num_sets):
    for w in np.arange(0, num_waves):
        wave_sets[s][f'wave_{w:03d}'] = sine_wave((np.random.random(1) - .5) * .3 + .5, 
                                                  (np.random.random(1) - .5) * .3 + .5,
                                                  (np.random.random(1) - .5) * .3)

''' Set up the plotting '''
fig, ax = plt.subplots()
img = 0
current_x = 0
ax.set(xlim = [current_x, current_x + np.pi/2], ylim = [-1.2, 1.2])
ax.set_aspect(1)
plt.axis('off')

ax.add_patch(patches.Rectangle((current_x, -1.2), np.pi/2, 2.4,
                                edgecolor = '#ECCCA2',
                                facecolor = '#ECCCA2',
                                fill = True))

wave_set_num = 0
for s in wave_sets:
    x_space = np.pi/2/num_sets
    for w in s.values():
        wave_height = w.location(current_x)[0]

        ax.add_patch(patches.Rectangle((current_x + x_space * wave_set_num, -1.2), x_space, wave_height + 1.2,
                                    edgecolor = 'white',
                                    facecolor = '#76b6c4',#
                                    alpha = .2,
                                    linewidth = 0,
                                    fill = True))
        ax.add_patch(patches.Rectangle((current_x + x_space * wave_set_num, wave_height), x_space, 0,
                                    edgecolor = 'white',
                                    facecolor = '#76b6c4',#
                                    alpha = .2,
                                    linewidth = 1,
                                    fill = True))
    
    wave_set_num = wave_set_num + 1

plt.show()

# Maybe just three waves, put in loop or something, maybe move drawing function into the class?