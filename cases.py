import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

class Point_:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def points_from_array(points):
    return [Point_(p[0], p[1]) for p in points]
def draw_cases(case):
    case1 = np.array([
        [100, 1], [2, 1], [1.25, 1.5], [1, 2], [1.25, 2.5], [2, 3], [100, 3],
        [100, -3], [2, -3], [1.25, -2.5], [1, -2], [1.25, -1.5],[2, -1], [100, -1]
    ])
    case2 = np.array([
        [100, 1],[2, 1],[1.25, 1.5],[1, 2],[1.25, 2.5],[2, 3],[100, 3],
        [100, -3],[0.666, -3],[0.666, -3],[1, -2],[1.5, -1.25],[2, -1],[100, -1]
    ])
    case3 = np.array([
        [100, 1],[2, 1],[1.25, 1.5],[1, 2],[1.25, 2.5],[2, 3],[100, 3],
        [100, -3],[2, -3],[1.5, -2.75],[1, -2],[0.666, -1],[0.666, -1],[100, -1]
    ])
    case4 = np.array([
        [100, 1], [2, 1], [1.5, 1.25], [1, 2], [0.666, 3], [0.666, 3], [100, 3],
        [100, -3],[2, -3],[1.25, -2.5],[1, -2],[1.25, -1.5],[2, -1],[100, -1]
    ])
    case5 = np.array([
        [100, 1],[0.666, 1],[0.666, 1],[1,2],[1.5, 2.75],[2, 3],[100, 3],
        [100, -3],[2, -3],[1.25, -2.5],[1, -2],[1.25, -1.5],[2, -1],[100, -1]
    ])
    cases = [[case1, case2, case3], [case4, case5, case1], [case1, case1, case1]]
    bridges = [[[3,10], [3,11], [3, 9]],
               [[2,10], [4,10], [1,11]],
               [[4,12], [2, 8], [4, 8]]]
    t = [
        [[], [[0, 1, 2], [12, 13]], [[0, 1, 2], [8, 7]]],
        [[[0, 1], [11, 12, 13]], [[6, 5],  [11, 12, 13]],[[0], [12, 13]]],
        [[[], [13]], [[0, 1], []],[]]
    ]
    red_patch = mpatches.Patch(color='red')
    green_patch = mpatches.Patch(color='green')
    yellow_patch = mpatches.Patch(color='yellow')
    f, axes = plt.subplots(3, 3, sharex='col', sharey='row', figsize=(10, 10))
    for axes_row, cases_row, bridges_row, t_row in zip(axes, cases, bridges, t):
        for axis, _case, bridge, tt in zip(axes_row, cases_row, bridges_row, t_row):
            axis.set_xlim([0.2, 2.5])
            p_, q_ = bridge
            p_minus, p, p_plus, q_minus, q, q_plus = points_from_array(_case[[p_ - 1, p_, p_ + 1, q_ - 1, q_, q_ + 1]])
            case_num = case(p, q, p_plus, p_minus, q_plus, q_minus)
            axis.plot(_case[bridge].T[0], _case[bridge].T[1], linewidth=3, c='g', zorder=3)
            axis.plot(_case[range(7)].T[0], _case[range(7)].T[1], linewidth=3, c='r')
            axis.plot(_case[range(7, 14)].T[0], _case[range(7, 14)].T[1], linewidth=3, c='r')
            axis.scatter(_case.T[0], _case.T[1], c='r', s=40, zorder=4)
            if tt != []:
                if tt[0] != []:
                    axis.plot(_case[tt[0] + [p_]].T[0], _case[tt[0] + [p_]].T[1], c='y', linewidth=3)
                    axis.scatter(_case[tt[0]].T[0], _case[tt[0]].T[1], c='y',s=40, zorder=5)
                if tt[1] != []:
                    axis.plot(_case[[q_] + tt[1]].T[0], _case[[q_] + tt[1]].T[1], c='y', linewidth=3)
                    axis.scatter(_case[tt[1]].T[0], _case[tt[1]].T[1], c='y',s=40, zorder=5)
            axis.set_title('Case {}'.format(case_num))
    f.legend(handles=[red_patch, yellow_patch, green_patch], labels=['keep', 'discard','bridge'])


def draw_rest(case):
    case91 = np.array([
        [100, 0.25], [2, 0.25], [1, 0.5], [1.5, 1.25], [2, 1.5], [100, 1.5],
        [100, -1], [2.5, -1], [1.5, -0.75], [1, -0.5], [1.7, -0.125], [100, -0.125]
    ])
    case92 = np.array([
        [100, -0.25], [2, -0.25], [1, -0.5], [1.5, -1.25], [2, -1.5], [100, -1.5],
        [100, 1], [2.5, 1], [1.5, 0.75], [1, 0.5], [1.7, 0.125], [100, 0.125]
    ])
    ys = np.zeros(2)
    xs = np.linspace(-1., 4., 2)
    xs_up = np.linspace(0.5, 1.5, 2)
    ys_up = np.linspace(-0.25, 1.25, 2)
    xs_down = np.linspace(0.5, 1.5, 2)
    ys_down = np.linspace(-0.25, -0.75, 2)
    f, axes = plt.subplots(1, 2, sharex='col', sharey='row', figsize=(10, 3))
    cases = [case91, case92]
    point = [0.5, -0.25]
    pp = [[2,3,4, 7,8,9],
          [9,8,7, 4,3,2]]
    for axis, _case, p_ in zip(axes, cases, pp):
        axis.set_xlim([0.2, 2.7])
        axis.plot(xs, ys, c='black')
        axis.plot(xs_up, ys_up, c='black', zorder=-1)
        axis.plot(xs_down, ys_down, c='black', zorder=-1)
        axis.plot(_case[[6, 7, 8]].T[0], _case[[6, 7, 8]].T[1], c='y', zorder=3, linewidth=2)
        axis.scatter(point[0], point[1], c='black', s=10)
        axis.scatter(_case.T[0], _case.T[1], c='r', zorder=4)
        axis.scatter(_case[7].T[0], _case[7].T[1], c='y', zorder=5)
        axis.plot(_case[[3, 8]].T[0], _case[[3, 8]].T[1], c='g', linewidth=2)
        axis.plot(_case.T[0], _case.T[1], c='r', zorder=0, linewidth=2)
        p_minus, p, p_plus, q_minus, q, q_plus = points_from_array(_case[p_])
        c = case(p, q, p_plus, p_minus, q_plus, q_minus, m=0)
        axis.set_title('Case {0}'.format(c))
        ys_up = -ys_up
        ys_down = -ys_down
        point[1] = -point[1]


