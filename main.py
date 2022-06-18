
# This is an animation inspired by the beauty within the Lorenz system
# I love the work by Jake Vanderplas (https://github.com/jakevdp) and I wanted to
# explore the creative potential this model has
# http://jakevdp.github.io/blog/2013/02/16/animating-the-lorentz-system-in-3d/


# Animation
# ————————————————————————————————————————————————————————————————————————
import numpy as np
from scipy import integrate

from matplotlib import pyplot as plt
from matplotlib import animation

plt.rcParams["figure.figsize"] = [9.50, 7.50]

N_trajectories = 50

def lorentz_deriv(params, t0, sigma=10., beta=8./3, rho=28.0):
    
    # Compute the time-derivative of a Lorentz system.
    x, y, z = params
    return [sigma * (y - x), x * (rho - z) - y, x * y - beta * z]


# Choose random starting points, uniformly distributed from -15 to 15
np.random.seed(1)
x0 = -15 + 30 * np.random.random((N_trajectories, 3))

# Solve for the trajectories
t = np.linspace(0, 4, 1310)
x_t = np.asarray([integrate.odeint(lorentz_deriv, x0i, t)
                  for x0i in x0])

# background color
bgc = (0.02, 0.0, 0.08)

# Set up figure & 3D axis for animation
fig = plt.figure(facecolor=bgc)
ax = fig.add_axes([0, 0, 1, 1], projection='3d')

ax.set_facecolor(bgc)
ax.grid(False)
ax.axis('off')


# These are some of my favorite color mixes for this animation, try them all!
# colors = plt.cm.viridis(np.linspace(0, 1, N_trajectories))
# colors = plt.cm.Greys(np.linspace(0, 0.8, N_trajectories))
# colors = plt.cm.Purples(np.linspace(0.3, 1, N_trajectories))
# colors = plt.cm.YlOrRd(np.linspace(0, 1, N_trajectories))
colors = plt.cm.GnBu(np.linspace(0, 1, N_trajectories))

# set up lines and points
# lines = sum([ax.plot([], [], [], linestyle=(0, (1, 10)), linewidth=np.random.randint(1,3.1),
#                      alpha=np.random.uniform(0.3, 1), c=c)
#              for c in colors], [])

lines = sum([ax.plot([], [], [], linestyle=(0, (3, 5, 1, 5, 1, 5)), linewidth=np.random.randint(1,3.1),
                     alpha=np.random.uniform(0.3, 1), c=c)
             for c in colors], [])
pts = sum([ax.plot([], [], [], 'o', markersize=np.random.randint(2, 7),
                   alpha=np.random.uniform(0.65, 1), c=c)
           for c in colors], [])


# prepare the axes limits
ax.set_xlim((-25, 25))
ax.set_ylim((-35, 35))
ax.set_zlim((5, 55))

# set point-of-view: specified by (altitude degrees, azimuth degrees)
ax.view_init(30, 0)

# initialization function: plot the background of each frame
def init():
    for line, pt in zip(lines, pts):
        line.set_data([], [])

        line.set_3d_properties([])
        pt.set_data([], [])
        pt.set_3d_properties([])
    return lines + pts

# animation function
def animate(i):

    for line, pt, xi in zip(lines, pts, x_t):
    
        x, y, z = xi[:i].T
        line.set_data(x, y)
        line.set_3d_properties(z)
        line.set_alpha(0.1 + 0.0006*i)

        pt.set_data(x[-1:], y[-1:])
        pt.set_3d_properties(z[-1:])
    
    ax.view_init(-0.2 * i, -0.2 * i) # disable this line to manually move the camera angle
    fig.canvas.draw()
    return lines + pts

# instantiate the animator
anim = animation.FuncAnimation(fig, animate, init_func=init, frames=1010, interval=8, blit=False)

plt.show()
