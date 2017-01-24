import matplotlib.pyplot as plt
import math
def draw(points1, points2, circles):#вспомогательная функция для рисования
    ax = plt.gca()
    ax.cla()
    if (len(points1) > 0):
        plt.plot(points1[:,0], points1[:,1], 'go')
    if (len(points2) > 0):
        plt.plot(points2[:,0], points2[:,1], 'wo')
    axes = plt.axis()

    plt.axis('equal')

    colors = ['r', 'b', 'y']
    for i in range(0, len(circles)):
        rad = math.sqrt(circles[i].radi)
        if (rad == 0):
                rad = 0.03
        circle = plt.Circle((circles[i].center[0], circles[i].center[1]), rad, color=colors[i], fill = False)
        ax.add_artist(circle)

    plt.xlim( [axes[0] *1.2 - 0.8, axes[1]*1.2 +0.8])
    plt.ylim( [axes[2] *1.2- 0.8, axes[3]*1.2 +0.8])


    plt.show()