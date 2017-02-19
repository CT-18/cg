from TMapClasses import *
import solution

# Набор методов для проверки корректности локализацоинной структуры и трапецоидной карты
def segmentEqual(s0, s1):
    if s0 == None:
        return s1 == None
    elif s1 == None:
        return False
    else:
        return s0.p == s1.p and s0.q == s1.q

def dataEqual(tr0, tr1):
    # Проверка на то, совпадают ли точки и отрезки трапецоидов
    if tr0.leftp != tr1.leftp:
        return False
    if tr0.rightp != tr1.rightp:
        return False
    if segmentEqual(tr0.top, tr1.top):
        if segmentEqual(tr0.bottom, tr1.bottom):
            return True
    return False

def neighbourEqual(tr0, tr1):
    if tr0 == None:
        return tr1 == None
    elif tr1 == None:
        return False
    else:
        return dataEqual(tr0, tr1)

def trapezoidEqual(tr0, tr1):
    if not dataEqual(tr0, tr1):
        return False
    for i in range(2):
        if not neighbourEqual(tr0.leftnb[i], tr1.leftnb[i]):
            return False
        if not neighbourEqual(tr0.rightnb[i], tr1.rightnb[i]):
            return False
    return True

def nodeEqual(n0, n1):
    if n0 == None:
        return n1 == None
    elif n1 == None:
        return False
    if type(n0) != type(n1):
        return False
    
    if n0.__name__ == TrapezoidNode.__name__:
        if len(n0.links) != len(n1.links):
            return False
        return trapezoidEqual(n0.tr, n1.tr)
    if n0.__name__ == XNode.__name__:
        if n0.point != n1.point:
            return False
    elif n0.__name__ == YNode.__name__:
        if not segmentEqual(n0.segment, n1.segment):
            return False
    return nodeEqual(n0.left, n1.left) and nodeEqual(n0.right, n1.right)

def isMapEqual(map0, map1):
    """Проверка двух трапецоидных карт на идентичность"""
    return nodeEqual(map0.root, map1.root)


def buildTMap():
    """Построение трапецоидной карты из примера"""
    # Пока что в float координатах, надо бы в целые перевести
    tmap = TrapezoidMap()
    f = open("tests/example.off", "r")
    f.readline()
    line = f.readline()
    n = int(line[0:2])
    m = int(line[5:7])
    pointsList = []
    segments = []
    i = 0
    while i < n:
        pair = f.readline().split(' ')
        pointsList.append([float(pair[0]),float(pair[1])])
        i += 1
    i = 0
    while i < m:
        pair = f.readline().split(' ')
        p1 = int(pair[0]) - 1
        p2 = int(pair[1]) - 1
        if (pointsList[p2][0] < pointsList[p1][0]):
            p1,p2 = p2,p1
        solution.insert(tmap, Segment(pointsList[p1], pointsList[p2]))
        i += 1
    f.close()
    return tmap

def intersection_test(func):
    tmap = buildTMap()
    isCorrect = True
    with open('tests/example_segments.txt') as f:
        n = int(next(f))
        for i in range(n):
            px, py, qx, qy = [float(x) for x in next(f).split()]
            s = Segment([px, py], [qx, qy])
            firstTr = solution.localize(tmap, [px, py])[0]
            answer = solution.intersectSegment(s, firstTr)
            check = func(s, firstTr)
            if type(check) == type(answer):
                temp = []
                item = next(check, None)
                while item != None:
                    temp.append(item)
                    item = next(check, None)
                check = temp
            nextTr = next(answer, None)
            pos = 0
            while nextTr != None:
                if pos >= len(check):
                    isCorrect = False
                    break
                tr = check[pos]
                if not dataEqual(tr, nextTr):
                    isCorrect = False
                    break
                pos = pos + 1
                nextTr = next(answer, None)
            if pos != len(check):
                isCorrect = False
                break
    return isCorrect


def simple_insert_test(insert):
    for i in range(7):
        with open('tests/'+str(i)) as f:
            n = int(next(f))
            answer = TrapezoidMap()
            check = TrapezoidMap()
            segmentList = []
            for j in range(n):
                px, py, qx, qy = [float(x) for x in next(f).split()]
                s = Segment([px, py], [qx, qy])
                segmentList.append(s)
                solution.insert(answer, s)
                insert(check, s)
            if not isMapEqual(answer, check):
                return False
            if i in [2, 6]:
                for j in range(100):
                    answer = TrapezoidMap()
                    check = TrapezoidMap()
                    for pos in np.random.permutation(n):
                        solution.insert(answer, segmentList[pos])
                        insert(check, segmentList[pos])
                    if not isMapEqual(answer, check):
                        return False
    return True