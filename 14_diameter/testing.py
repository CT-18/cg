import matplotlib.pyplot as plt
def draw_bad(A, nextA, B, nextB, dir, wdir):

    plt.plot(A[0], A[1], 'go')
    plt.plot(nextA[0], nextA[1], 'bo')

    plt.plot(B[0], B[1], 'ro')
    plt.plot(nextB[0], nextB[1], 'bo')

    ax = plt.axes()
    axes = plt.axis()

    plt.plot([A[0] - dir[0] * 100, A[0] + dir[0] * 100], [A[1] - dir[1] * 100, A[1] + dir[1] * 100], 'r')
    plt.plot([B[0] - dir[0] * 100, B[0] + dir[0] * 100], [B[1] - dir[1] * 100, B[1] + dir[1] * 100], 'r')

    plt.plot([A[0] - wdir[0] * 100, A[0] + wdir[0] * 100], [A[1] - wdir[1] * 100, A[1] + wdir[1] * 100], 'y')
    plt.plot([B[0] - wdir[0] * 100, B[0] + wdir[0] * 100], [B[1] - wdir[1] * 100, B[1] + wdir[1] * 100], 'y')


    from math import sqrt
    length = sqrt((nextA[0] - A[0])**2 + (nextA[1] - A[1])**2)
    ax.arrow(A[0], A[1], (nextA[0] - A[0]) * 0.8, (nextA[1] - A[1]) * 0.8 , head_width=0.1, head_length=length*0.2, fc='k', ec='k')

    length = sqrt((nextB[0] - B[0])**2 + (nextB[1] - B[1])**2)
    ax.arrow(B[0], B[1], (nextB[0] - B[0]) * 0.8, (nextB[1] - B[1]) * 0.8, head_width=0.1, head_length=length*0.2, fc='k', ec='k')


    plt.plot([A[0], nextB[0]], [A[1], nextB[1]], 'b')

    plt.plot([B[0], nextA[0]], [B[1], nextA[1]], 'b')
    plt.axis('equal')

    plt.xlim( [axes[0] - 0.5, axes[1] +0.5])
    plt.ylim( [axes[2] - 0.5, axes[3] +0.5])

    plt.show()

def testing(choose_next_my, choose_next):
    A_test = [[0,0], [0, 0], [1,2.5], [5,5], [2,3],[1,3]]
    nextA_test = [[1,-1], [2, 0], [2,1.5], [2,4], [1,1], [1,1]]
    B_test = [[1.5,1.5], [2, 0], [3,3], [2,1], [4,2], [3,1]]
    nextB_test = [[1,2.5], [1, 1], [2,3], [3,1], [3,3], [3,3]]
    dir_l_test = [[0,1], [1, -3], [0,1], [1, -1], [1,1], [1,1]]
    equal = [False, False, False, False, False, True]
    print("Running tests")
    for i in range(0, len(A_test)):
        my = choose_next_my(A_test[i], nextA_test[i], B_test[i], nextB_test[i], dir_l_test[i])
        correct = choose_next(A_test[i], nextA_test[i], B_test[i], nextB_test[i], dir_l_test[i])
        if (my == 1):
            wdir = [nextB_test[i][0] - B_test[i][0], nextB_test[i][1] - B_test[i][1]]
        else:
            wdir = [nextA_test[i][0] - A_test[i][0], nextA_test[i][1] - A_test[i][1]]
        draw_bad(A_test[i], nextA_test[i], B_test[i], nextB_test[i], dir_l_test[i], wdir)
        if (my != correct and not equal[i]):
            print("Error on test ", i)
            break
        print("Test ", i, " Ok")
    print("Testing complete")

