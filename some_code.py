import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull

def example_pred(A0, A1, B0, B1) :
    return np.sign(np.linalg.det(np.array([A1 - A0,B1 - B0])))

def paint_point(this_plt, point, color):
    this_plt.plot(point[0], point[1], color)
    
def paint_line(this_plt, A, B, color):
    this_plt.plot([A[0], B[0]], [A[1], B[1]], color)

def check_pred(pred_to_check):
    iterations = 100
    i = 0;
    while i < iterations:
        A0, B0, A1, B1 = np.random.uniform(1, 4, size = (4, 2))
        if (pred_to_check(A0, A1, B0, B1) != example_pred(A0, A1, B0, B1)):
            print("Ошибка!, A0(кр), A1(жел), B0(син), B1(зел) = ")
            print(A0, A1, B0, B1)
            print("Данный предикат вывел: ", pred_to_check(A0, A1, B0, B1), " а ответ: ", example_pred(A0, A1, B0, B1))
            fig = plt.figure(figsize = (10, 5))
            new_plt = fig.add_subplot(121)
            list(map(lambda x, y, z: paint_line(new_plt, x, y, z), [A0, B0], [A1, B1], ["r", "b"]))
            list(map(lambda x, y: paint_point(new_plt, x, y), [A0, A1, B0, B1], ["ro", "yo", "bo", "go"]))
            #new_plt.plot([B0[0], B1[0]],[B0[1], B1[1]], "r")
            new_plt.axis([0, 5, 0, 5])
            new_plt = fig.add_subplot(122)
            A1 = A1 - A0
            B1 = B1 - B0
            B0 = B0 - B0
            A0 = A0 - A0
            list(map(lambda x, y, z: paint_line(new_plt, x, y, z), [A0, B0], [A1, B1], ["r", "b"]))
            list(map(lambda x, y: paint_point(new_plt, x, y), [A0, A1, B0, B1], ["ro", "yo", "bo", "go"]))
            plt.show()
            return
        i += 1
    print("Предикат реализован правильно")

def rand_figure():
    A_ch = ConvexHull(np.random.uniform(1, 9, size=(10, 2)))
    ans = []
    for i in A_ch.vertices:
        ans.append(A_ch.points[i])
    return ans
    
def paint_polygon(figure, place, Q, color1, color2, min_val, max_val):
    plt1 = figure.add_subplot(place)
    X, Y = np.transpose(Q)
    i = 0
    while i < len(Q):
        next_i = (i + 1) % len(Q) 
        plt1.plot([X[i], X[next_i]],[Y[i], Y[next_i]], color1, X[i], Y[i], color2) 
        i += 1
    plt1.axis([min_val, max_val, min_val, max_val])
    
        
def exapmle_find_first(A):
    X, Y = np.transpose(A)
    i = np.argmin(X)
    while (Y[i] >= Y[(i + 1) % len(X)]) and ((X[i] >= X[(i + 1) % len(X)])):
        i += 1
    return i

def example_alg(A, B):
    i_A = exapmle_find_first(A)
    i_B = exapmle_find_first(B)
    first_i_A = i_A
    first_i_B = i_B
    C = [A[i_A] + B[i_B]]
    i = 0;
    while (True):
        if (i > len(A) + len(B)):
            print("Smth went wrong, check your array of points")
            break
        next_i_A = (i_A + 1) % len(A)
        next_i_B = (i_B + 1) % len(B)
        p = example_pred(A[i_A], A[next_i_A], B[i_B], B[next_i_B])
        if (p > 0):
            i_A = next_i_A
        elif p == 0:
            i_A = next_i_A
            i_B = next_i_B
        else:
            i_B = next_i_B
        if first_i_A == i_A and first_i_B == i_B:
            break
        C.append(A[i_A] + B[i_B])
        i += 1;
    return C

def check_alg(alg_to_check):
    iterations = 100
    i = 0;
    while i < iterations:
        
        A = rand_figure()
        B = rand_figure()
        C = example_alg(A, B)
        C1 = alg_to_check(A, B)
        
        C_s = np.sort(C)
        C1_s = np.sort(C1)
                    
        if (not np.array_equal(C1_s, C_s)):
            print("Ошибка!")
            print("A")
            print(A)
            print("B")
            print(B)
            print("C у правильного  алгоритма")
            print(C)
            print("C у вашего алгоритма")
            print(C1)
            fig = plt.figure(figsize = (15, 5))
            paint_polygon(fig, 131, A, "r", "yo", 0, 10)
            paint_polygon(fig, 132, B, "g", "yo", 0, 10)
            paint_polygon(fig, 133, C, "b", "yo", 0, 20) 
            plt.show()
            return
        i += 1
    print("Алгоритм реализован правильно")
