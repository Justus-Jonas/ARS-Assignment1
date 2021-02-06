import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
import gc
#def rosenbrock(x, y, a, b):
#    return a * (x - y ** 2) ** 2 + b * (y - x) ** 2


rosenbrock = lambda x,y,a,b: (a - x) ** 2 + b * (y - x ** 2) ** 2


gradient_rosenbrock = lambda x, y, a, b: np.asarray([(-2 * a + 4 * b * x ** 3 - 4 * b * x * y + 2 * x), 2 * b * (y - x ** 2)])



def gradient_descent_ros(starting_point, stepSize = 0.001, epsilon=1e-5, a=0, b=10):
    pos = starting_point
    print(pos)
    history = [np.asarray([pos[0], pos[1], rosenbrock(pos[0],pos[1], a, b)])]
    i = 0
    while True:
        #print(i)
        #print(gradient_rosenbrock(pos[0],pos[1],a,b))
        pos = pos - stepSize * gradient_rosenbrock(pos[0],pos[1], a, b)
        history.append(np.asarray([pos[0], pos[1], rosenbrock(pos[0],pos[1], a, b)]))
        if np.linalg.norm(gradient_rosenbrock(pos[0],pos[1],a,b)) < epsilon:
            return pos, history
        i+=1


final_pos, history = gradient_descent_ros([-1, 1])

print(final_pos)
print(history)

X = np.arange(-2, 2, 0.15)
Y = np.arange(-1, 3, 0.15)
X, Y = np.meshgrid(X, Y)

Z = rosenbrock(X, Y, a=0, b=10)
print(Y.shape)
print(Z.shape)
print(X.shape)

figRos = plt.figure(figsize=(12, 7))
axRos = figRos.gca(projection='3d')
surf = axRos.plot_surface(X, Y, Z, cmap=cm.gist_heat_r,
                       linewidth=0, antialiased=False)
axRos.set_zlim(0, 200)
figRos.colorbar(surf, shrink=0.5, aspect=10)
plt.savefig('math.png')

"""
def animateImage(index):
    print(index)
    gc.collect()
    fig = plt.figure(figsize=(15, 10))
    ax = fig.gca(projection='3d')
    ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0, antialiased=False, alpha=0.75)
    ax.plot(history[index][0], history[index][1], history[index][2], 'o', c='yellow', markersize=15, markeredgewidth=1,
            markeredgecolor='black')
    ax.view_init(30, -70)
    plt.tight_layout()
    return plt


fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)

size = range(0, len(history))
print(size)
# create animation
animated = animation.FuncAnimation(fig, animateImage, frames=size, repeat=False, save_count=0, interval=20, blit=True)

animated.save('GradientDescentRosenbrock.gif')
"""

i = 0
l = 0
for vector in history:
    if i%50 == 0:
        fig = plt.figure(figsize=(15, 10))
        ax = fig.gca(projection='3d')
        ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,linewidth=0, antialiased=False, alpha=0.75)
        ax.plot(vector[0], vector[1], vector[2], 'o', c='yellow',alpha=1, markersize=15,markeredgewidth=1, markeredgecolor='black')
        ax.view_init(30, -70)
        plt.tight_layout()
        plt.savefig('images/' + str(l) + '.png')
        l+=1
    i+=1
    print(i)