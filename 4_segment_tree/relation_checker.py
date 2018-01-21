import matplotlib.pyplot as plt
from enum import Enum

class Relation(Enum):
    CONTAINS = 1
    INTERSECTS = 2
    DOES_NOT_INTERSECT = 3

def solve(s, i):
    if i[0] < s[0] and s[1] <= i[1]:
        return Relation.CONTAINS
    if s[0] <= i[1] and i[0] < s[1]:
        return Relation.INTERSECTS
    return Relation.DOES_NOT_INTERSECT

def show_ex(s, i):
    plt.axis([0, 9, 0, 4])
    plt.plot(s, [1,1], c='r')
    plt.scatter(s, [1,1], c='r')
    plt.plot(i, [2,2], c='b')
    plt.scatter(i, [2,2], c='b')
    plt.legend(['segment','interval'])
    plt.show()

def show_error(s, i, res):
    print('Неправильный ответ!!!')
    print('Ваш ответ на входных данных seg={}, int={}: {}'.format(s, i, res))
    print('Ось Оу не участвует в вычислениях, она приведена только для наглядности.')
    show_ex(s, i)
    
def test(relation):
    i = [3, 6]
    for a in range(1, 8):
        for b in range(a + 1, 9):
            s = [a, b]
            result = relation(s, i)
            expected = solve(s, i)
            if result != expected:
                show_error(s, i, result)
                return

    print('Поздравляем! Вы успешно справились с этим заданием!')
