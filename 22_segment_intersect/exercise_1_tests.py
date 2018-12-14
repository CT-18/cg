from entities import Point


def test(id):
    return {
        1: [Point(1, 1), Point(3, 3), Point(3, 3), Point(3, 2), Point(-6, -6, -2)],
        2: [Point(1, 1), Point(4, 5), Point(2, 1), Point(2, 5), Point(24, 28, 12)],
        3: [Point(-18, -34), Point(62, 15), Point(83, 7), Point(-8, 16), Point(277978, 51274, 5179)],
        4: [Point(0, 0), Point(1, 4), Point(2, 2), Point(0, 3), Point(6, 24, 9)],
        5: [Point(0, 0), Point(7, 1), Point(0, 1), Point(7, 0), Point(-49, -7, -14)],
        6: [Point(1, 2), Point(4, 2), Point(4, 2), Point(7, 2), Point(4, 2, 1)],
        7: [Point(0, 0), Point(5, 2), Point(3, 0), Point(2, 2), Point(30, 12, 12)],
        8: [Point(10, 1), Point(100, 80), Point(30, 2), Point(-60, 95), Point(330300, 169530, 15480)],
        
        9: [Point(-1, 1), Point(3, 1), Point(1, 1), Point(5, 1)],
        10: [Point(-2, -2), Point(-2, 6), Point(-2, 3), Point(-2, 10)],
        11: [Point(1, 1), Point(5, 5), Point(3, 3), Point(7, 7)],
        12: [Point(10, -10), Point(1, -1), Point(-5, 5), Point(5, -5)],
        13: [Point(-80, -80), Point(30, -80), Point(30, -80), Point(-80, -80)],
        14: [Point(8, -70), Point(8, 70), Point(8, -70), Point(8, 70)],
        15: [Point(-15, -15), Point(32, 32), Point(32, 32), Point(-15, -15)],
        16: [Point(-15, 132), Point(14, 14), Point(14, 14), Point(-15, 132)],
        17: [Point(4, 18), Point(4, 46), Point(4, 46), Point(4, 43)],
        18: [Point(6, -17), Point(8, -17), Point(33, -17), Point(6, -17)],
        19: [Point(3, 18), Point(15, 1), Point(27, -16), Point(3, 18)],
        20: [Point(-1, -1), Point(8, 8), Point(-1, -1), Point(101, 101)]
    }.get(id)
