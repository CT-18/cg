import numpy as np
from numpy import pi

# returns max angle of log(|sin * cos|) 
def task1_ans():
    angles = np.arange(10, 360, 10)
    radians = angles * pi / 180
    fs  = np.log(np.abs(np.cos(radians) * np.sin(radians)))

    return angles[fs.argmax()]

def check_task1(task1):
    if task1() == task1_ans():
        print("Great work")
    else:
        print("You are so stupid, try again")

def task2_ans(img, t):
    new_img = img.copy()
    near_zero = new_img < t
    new_img[near_zero] = 0
    new_img[~near_zero] = 255

    return new_img

def test_task2_impl(img, t, task2):
    o_img = img.copy()
    expexted_res = task2_ans(img, t)
    given_res = task2(img, t)

    if np.array_equal(expexted_res, given_res):
        if np.array_equal(img, o_img):
            return True
        else:
            print("Oh no you corrupt source image !!! =(")

    else:
        print("img:", img)
        print("t:", t)
        print("expected: ", expexted_res)
        print("given: ", given_res)

    return False

def test_task2(task2):
    img = np.array([[1, 2],
                    [3, 4]])
    t = 3

    img2 = np.arange(0, 1000)
    img2.reshape((20, 50))
    t2 = 340

    if test_task2_impl(img, t, task2) and test_task2_impl(img2, t2, task2):
        print("Oh yes man!")
    else:
        print("Are you kidding me? - It's very simple!")

