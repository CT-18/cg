import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull
from cg import *

def example_pred(A0:Point, A1:Point, B0:Point, B1:Point):
    A = A1 - A0
    B = B1 - B0
    return np.sign(A[0]*B[1] - A[1]*B[0])

def paint_point(this_plt, point, color):
    this_plt.plot(point[0], point[1], color)
    
def paint_line(this_plt, A, B, color):
    this_plt.plot([A[0], B[0]], [A[1], B[1]], color)

def check_pred(pred_to_check):
    test0 = np.array([[3, 3], [3, 4], [2, 2], [2, 1]])
    test1 = np.array([[3, 3], [3, 4], [2, 2], [3, 2]])
    test2 = np.array([[3, 3], [3, 4], [2, 2], [1, 2]])
    tests = np.array([test0, test1, test2])
    iterations = 1000
    i = 0
    while i < iterations:
        if (i < 3):
            A0, A1, B0, B1 = tests[i]
        else:
            A0, A1, B0, B1 = np.random.uniform(1, 4, size = (4, 2))
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
            new_plt.set_title("vectors");
            new_plt = fig.add_subplot(122)
            new_plt.axis([-4, 4, -4, 4])
            A1 = A1 - A0
            B1 = B1 - B0
            B0 = B0 - B0
            A0 = A0 - A0
            list(map(lambda x, y, z: paint_line(new_plt, x, y, z), [A0, B0], [A1, B1], ["r", "b"]))
            list(map(lambda x, y: paint_point(new_plt, x, y), [A0, A1, B0, B1], ["ro", "yo", "bo", "go"]))
            new_plt.set_title("shifted vectors");
            plt.show()
            return
        i += 1
    print("Предикат реализован правильно")

def rand_figure():
    A_ch = ConvexHull(np.random.randint(1, 9, size=(10, 2)))
    ans = []
    for i in A_ch.vertices:
        p = Point(int(A_ch.points[i][0]), int(A_ch.points[i][1]))
        ans.append(p)
    ans = PointSet(ans)
    return ans
    
def paint_polygon(figure, place, Q, color1, color2, min_val, max_val, name):
    plt1 = figure.add_subplot(place)
    i = 0
    while i < len(Q):
        next_i = (i + 1) % len(Q)
        A = Q[i]
        B = Q[next_i]
        plt1.plot([A[0], B[0]],[A[1], B[1]], color1, A[0], A[1], color2) 
        i += 1
    plt1.set_title(name)
    plt1.axis([min_val, max_val, min_val, max_val])
    
        
def exapmle_find_first(A):
    return A.argmax(lambda Q, W: Q[0] == W[0] if Q[1] > W[1] else Q[0] > W[0])

def example_alg(A, B):
    i_A = A.argmax(lambda q, w: q > w)
    i_B = B.argmax(lambda q, w: q > w)
    first_i_A = i_A
    first_i_B = i_B
    C = [A[i_A] + B[i_B]]
    i = 0;
    while (True):
        if (i > len(A) + len(B)):
            #print("Smth went wrong, check your array of points")
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
            print("A (красный)")
            print(A)
            print("B (зеленый)")
            print(B)
            print("C у правильного  алгоритма(синий)")
            print(C)
            print("C у вашего алгоритма(желтый)")
            print(C1)
            fig = plt.figure(figsize = (10, 10))
            paint_polygon(fig, 221, A, "r", "yo", 0, 10, "A")
            paint_polygon(fig, 222, B, "g", "yo", 0, 10, "B")
            paint_polygon(fig, 223, C, "b", "yo", 0, 20, "C")
            paint_polygon(fig, 224, C1, "y", "ro", 0, 20, "C1") 
            plt.show()
            return
        i += 1
    print("Алгоритм реализован правильно")
