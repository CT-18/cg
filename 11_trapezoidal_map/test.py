from TMapClasses import *
import solution

def buildTMap():
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
    step = 25
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
            correct = solution.intersectSegment(s, firstTr)
            answer = func(s, firstTr)
            if type(answer) == type(correct):
                temp = []
                item = next(answer, None)
                while item != None:
                    temp.append(item)
                    item = next(answer, None)
                answer = temp
            nextTr = next(correct, None)
            pos = 0
            while nextTr != None:
                if pos >= len(answer):
                    isCorrect = False
                    break
                tr = answer[pos]
                if tr.top != nextTr.top or tr.bottom != nextTr.bottom or tr.leftp != nextTr.leftp or tr.rightp != nextTr.rightp:
                    isCorrect = False
                    break
                pos = pos + 1
                nextTr = next(correct, None)
            if pos != len(answer):
                isCorrect = False
    return isCorrect