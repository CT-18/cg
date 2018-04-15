from queue import Queue
import numpy as np

def bfs(points, ax):
    n = len(points)
    m = len(points[0])
    used = [[False for _ in range(0, m)] for _ in range(0, n)]
    queue = Queue()
    i = 0
    j = 0
    queue.put((i, j))

    while not queue.empty():
        (i, j) = queue.get()
        used[i][j] = True

        if i < n - 1 and used[i+1][j] is False:
            ax.plot([points[i][j][0], points[i+1][j][0]],
                    [points[i][j][1], points[i+1][j][1]],
                    [points[i][j][2], points[i+1][j][2]], '--', color='grey')
            queue.put((i + 1, j))

        if j < m - 1 and used[i][j+1] is False:
            ax.plot([points[i][j][0], points[i][j+1][0]],
                    [points[i][j][1], points[i][j+1][1]],
                    [points[i][j][2], points[i][j+1][2]], '--', color='grey')
            queue.put((i, j + 1))


def common_spline(P, W, u, v, func_coef):
    n = len(P)
    m = len(P[0])

    ans = np.zeros(shape=(3, len(u) * len(v)))
    divider = np.zeros(shape=(3, len(u) * len(v)))
    for i in range(0, n):
        for j in range(0, m):
            bU = func_coef(i, n - 1, u)
            bV = func_coef(j, m - 1, v)
            uvs = np.outer(bU, bV).ravel()
            ans += np.transpose(np.matrix(P[i][j])) * uvs * W[i][j]
            divider += uvs * W[i][j]
    return (ans) / divider

