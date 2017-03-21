from cg import Point, Vertex, Face

points = [
    (0, 13),
    (3, 11),
    (7, 13),
    (8, 11),
    (10, 19),
    (10, 15),
    (13, 11),
    (16, 14),
    (14, 11),
    (15, 7)
]
points = [Point.infinity(2)] + [Point(*args) for args in points]
points = [Vertex(p, None) for p in points]
for i, v in enumerate(points):
    v.name = i
points[0].name = "infinity"

faces = [
    [2, 3, 1],
    [3, 5, 1],
    [6, 5, 3],
    [4, 6, 3],
    [4, 3, 2],
    [10, 4, 2],
    [7, 6, 4],
    [8, 5, 6],
    [7, 8, 6],
    [10, 7, 4],
    [9, 8, 7],
    [10, 9, 7],
    [8, 9, 10],
    [1, 5, 0],#13
    [5, 8, 0],#14
    [8, 10, 0],#15
    [10, 2, 0],#16
    [2, 1, 0]#17
]

res_faces = []
for i, j, k in faces:
    res_faces.append(Face([points[i], points[j], points[k]], None))
    res_faces[-1].name = "({}, {}, {})".format(points[i].name, points[j].name, points[k].name)
faces = res_faces

connections = [0, 0, 0, 0, 3, 2, 2, 6, 8, 12, 12]
for i, v in enumerate(points):
    v.face = faces[connections[i]]
    
neighbours = [
    [1, 17, 4],
    [13, 0, 2],
    [1, 3, 7],
    [2, 4, 6],
    [0, 5, 3],
    [4, 16, 9],
    [3, 9, 8],
    [2, 8, 14],
    [7, 6, 10],
    [6, 5, 11],
    [8, 11, 12],
    [10, 9, 12],
    [11, 15, 10],
    [14, 17, 1],
    [15, 13, 7],
    [16, 14, 12],
    [17, 15, 5],
    [13, 16, 0]
]
for f, (i, j, k) in zip(faces, neighbours):
    f.neighbours = [faces[i], faces[j], faces[k]]

#============================================================

q = Point(14, 13)
q.name = "q"
vprev = points[1]
vnext = points[9]

test = (q, vprev)

def check_answer(ans):
    if not ans is vnext:
        return (ans, vnext, 'Неправильно')    
    return True