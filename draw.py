import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import ConvexHull
def draw(A, B, dir, best, hpoints, hull, dist, points):
    plt.plot(hpoints[:,0], hpoints[:,1], 'o')
    for simplex in hull.simplices:
        plt.plot(points[simplex,0], points[simplex,1], 'k-')
    plt.plot(hpoints[A][0], hpoints[A][1], 'go')
    plt.plot(hpoints[B][0], hpoints[B][1], 'ro')
    plt.axis('equal')
    axes = plt.axis()
    plt.plot([hpoints[A][0] - dir[0] * 100, hpoints[A][0] + dir[0] * 100], [hpoints[A][1] - dir[1] * 100, hpoints[A][1] + dir[1] * 100], 'r')
    plt.plot([hpoints[B][0] - dir[0] * 100, hpoints[B][0] + dir[0] * 100], [hpoints[B][1] - dir[1] * 100, hpoints[B][1] + dir[1] * 100], 'r')

    plt.plot([hpoints[best[0]][0], hpoints[best[1]][0]], [hpoints[best[0]][1], hpoints[best[1]][1]], 'y')

    plt.xlim( [axes[0] - 0.5, axes[1] +0.5])
    plt.ylim( [axes[2] - 0.5, axes[3] +0.5])

    plt.show()