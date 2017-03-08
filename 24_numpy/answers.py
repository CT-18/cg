import numpy as np
import numpy.ma as ma
from numpy import pi

# returns max angle of log(|sin * cos|) 
def task1_ans():
    angles = np.arange(10, 360, 10)
    radians = angles * pi / 180
    fs  = np.log(np.abs(np.cos(radians) * np.sin(radians)))

    return angles[fs.argmax()]

def task2_ans(img, t):
    new_img = img.copy()
    near_zero = new_img < t
    new_img[near_zero] = 0
    new_img[~near_zero] = 255

    return new_img

def task3_ans(img):
    img = ma.masked_outside(img, 0, 255)
    return img.filled(img.mean())

def check_task1(task1):
    if task1() == task1_ans():
        print("Great work")
    else:
        print("WRONG, try again!")

def check_task2(task2):
    img = np.array([[1, 2],
                    [3, 4]])
    t = 3

    img2 = np.arange(0, 1000)
    img2.reshape((20, 50))
    t2 = 340

    if test_task2_impl(img, t, task2) and test_task2_impl(img2, t2, task2):
        print("Oh yes man!")
    else:
        print("WRONG, try again!")

def check_task3(task3):
    img = np.array([[-100,  0,   1, 255, 256, 257],
                    [-1  , 10, 300, 300, 300, 300],
                    [0   ,  0,   0,   0,   0,   0]])

    
    exp = task3_ans(img)
    given = task3(img)
    if type(given) is np.ndarray:
        if np.array_equal(exp, given):
            print("Best of the best")
        else:
            print("WRONG, try again!")
            print("origin:  ", img)
            print("expected:", exp)
            print("given:   ", given)
    else:
        print("You have returned not a ndarray.")

def test_task2_impl(img, t, task2):
    o_img = img.copy()
    expexted_res = task2_ans(img, t)
    given_res = task2(img, t)

    if np.array_equal(expexted_res, given_res):
        if np.array_equal(img, o_img):
            return True
        else:
            print("Oh no you have corrupted source image !!! =(")

    else:
        print("img:", img)
        print("t:", t)
        print("expected: ", expexted_res)
        print("given: ", given_res)

    return False


