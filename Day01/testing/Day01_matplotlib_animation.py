import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig, ax = plt.subplots()
ax.set(xlim = [-1.5, 1.5], ylim = [-1.5, 1.5])

t = np.linspace(0, 2 * np.pi, 50)
t = np.append(t, t[:5])

x = np.cos(t)
y = np.sin(t)

scat = ax.scatter(x[0:5], y[0:5])

print(np.shape(np.vstack((x[1:(1+5)], y[1:(1+5)])).T))

def animate(i):
    print(i)
    print(np.vstack((x[i:(i+5)], y[i:(i+5)])).T)
    scat.set_offsets(np.vstack((x[i:(i+5)], y[i:(i+5)])).T)
    return scat

ani = animation.FuncAnimation(fig, animate, repeat=True,
                                    frames=len(t) - 8, interval=50)

# To save the animation using Pillow as a gif
writer = animation.PillowWriter(fps=15,
                                metadata=dict(artist='Me'),
                                bitrate=1800)
ani.save('Day01/scatter.gif', writer=writer)

plt.show()
