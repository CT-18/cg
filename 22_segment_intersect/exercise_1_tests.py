import numpy as np


def test(id) :
    return {
        1: [np.array([1, 1]), np.array([3, 3]), np.array([3, 3]), np.array([3, 2]), np.array([-6, -6, -2])],
        2: [np.array([1, 1]), np.array([4, 5]), np.array([2, 1]), np.array([2, 5]), np.array([24, 28, 12])],
        3: [np.array([-18, -34]), np.array([62, 15]), np.array([83, 7]), np.array([-8, 16]), np.array([277978, 51274, 5179])],
        4: [np.array([0, 0]), np.array([1, 4]), np.array([2, 2]), np.array([0, 3]), np.array([6, 24, 9])],
        5: [np.array([0, 0]), np.array([7, 1]), np.array([0, 1]), np.array([7, 0]), np.array([-49, -7, -14])],
        6: [np.array([1, 2]), np.array([4, 2]), np.array([4, 2]), np.array([7, 2]), np.array([4, 2, 1])],
        7: [np.array([0, 0]), np.array([5, 2]), np.array([3, 0]), np.array([2, 2]), np.array([30, 12, 12])],
        8: [np.array([10, 1]), np.array([100, 80]), np.array([30, 2]), np.array([-60, 95]), np.array([330300, 169530, 15480])],
        
        9: [np.array([-1, 1]), np.array([3, 1]), np.array([1, 1]), np.array([5, 1])],
        10: [np.array([-2, -2]), np.array([-2, 6]), np.array([-2, 3]), np.array([-2, 10])],
        11: [np.array([1, 1]), np.array([5, 5]), np.array([3, 3]), np.array([7, 7])],
        12: [np.array([10, -10]), np.array([1, -1]), np.array([-5, 5]), np.array([5, -5])],
        13: [np.array([-80, -80]), np.array([30, -80]), np.array([30, -80]), np.array([-80, -80])],
        14: [np.array([8, -70]), np.array([8, 70]), np.array([8, -70]), np.array([8, 70])],
        15: [np.array([-15, -15]), np.array([32, 32]), np.array([32, 32]), np.array([-15, -15])],
        16: [np.array([-15, 132]), np.array([14, 14]), np.array([14, 14]), np.array([-15, 132])],
        17: [np.array([4, 18]), np.array([4, 46]), np.array([4, 46]), np.array([4, 43])],
        18: [np.array([6, -17]), np.array([8, -17]), np.array([33, -17]), np.array([6, -17])],
        19: [np.array([3, 18]), np.array([15, 1]), np.array([27, -16]), np.array([3, 18])],
        20: [np.array([-1, -1]), np.array([8, 8]), np.array([-1, -1]), np.array([101, 101])]
    }.get(id)
