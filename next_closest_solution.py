from dcel import *

# q in (14, 13)
v1 = vertex(1, 0, 13)
v2 = vertex(2, 3, 11)
v3 = vertex(3, 7, 12)
v4 = vertex(4, 8, 11)
v5 = vertex(5, 10, 19)
v6 = vertex(6, 10, 15)
v7 = vertex(7, 13, 11)
v8 = vertex(8, 16, 14)
v9 = vertex(9, 14, 11)
v10 = vertex(10, 15, 7)

# f1 1 2 3
e12 = hedge(v1)
e23 = hedge(v2)
e31 = hedge(v3)
# f2 5 1 3
e51 = hedge(v5)
e13 = hedge(v1)
e35 = hedge(v3)
# f3 6 5 3
e65 = hedge(v6)
e53 = hedge(v5)
e36 = hedge(v3)
# f4 4 6 3
e46 = hedge(v4)
e63 = hedge(v6)
e34 = hedge(v3)
# f5 4 3 2
e43 = hedge(v4)
e32 = hedge(v3)
e24 = hedge(v2)
# f6 10 4 2
e104 = hedge(v10)
e42 = hedge(v4)
e210 = hedge(v2)
# f7 7 6 4
e76 = hedge(v7)
e64 = hedge(v6)
e47 = hedge(v4)
# f8 8 5 6
e85 = hedge(v8)
e56 = hedge(v5)
e68 = hedge(v6)
# f9 7 8 6
e78 = hedge(v7)
e86 = hedge(v8)
e67 = hedge(v6)
# f10 10 7 4
e107 = hedge(v10)
e74 = hedge(v7)
e410 = hedge(v4)
# f11 9 8 7
e98 = hedge(v9)
e87 = hedge(v8)
e79 = hedge(v7)
# f12 10 9 7
e109 = hedge(v10)
e97 = hedge(v9)
e710 = hedge(v7)
# f13 10 8 9
e108 = hedge(v10)
e89 = hedge(v8)
e910 = hedge(v9)
# f14 1 5 8 10 2
e15 = hedge(v1)
e58 = hedge(v5)
e810 = hedge(v8)
e102 = hedge(v10)
e21 = hedge(v2)

# vertex.set_edge
v1.set_edge(e15)
v2.set_edge(e21)
v3.set_edge(e31)
v4.set_edge(e410)
v5.set_edge(e51)
v6.set_edge(e63)
v7.set_edge(e710)
v8.set_edge(e810)
v9.set_edge(e910)
v10.set_edge(e102)

# e12.set_edges(prev, next, twin)
# f1 1 2 3
e12.set_edges(e31, e23, e21)
e23.set_edges(e12, e31, e32)
e31.set_edges(e23, e12, e13)
# f2 5 1 3
e51.set_edges(e35, e13, e15)
e13.set_edges(e51, e35, e31)
e35.set_edges(e13, e51, e53)
# f3 6 5 3
e65.set_edges(e36, e53, e56)
e53.set_edges(e65, e36, e35)
e36.set_edges(e53, e65, e63)
# f4 4 6 3
e46.set_edges(e34, e63, e64)
e63.set_edges(e46, e34, e36)
e34.set_edges(e63, e46, e43)
# f5 4 3 2
e43.set_edges(e24, e32, e34)
e32.set_edges(e43, e24, e23)
e24.set_edges(e32, e43, e42)
# f6 10 4 2
e104.set_edges(e210, e42, e410)
e42.set_edges(e104, e210, e24)
e210.set_edges(e42, e104, e102)
# f7 7 6 4
e76.set_edges(e47, e64, e67)
e64.set_edges(e76, e47, e46)
e47.set_edges(e64, e76, e74)
# f8 8 5 6
e85.set_edges(e68, e56, e58)
e56.set_edges(e85, e68, e65)
e68.set_edges(e56, e85, e86)
# f9 7 8 6
e78.set_edges(e67, e86, e87)
e86.set_edges(e78, e67, e68)
e67.set_edges(e86, e78, e76)
# f10 10 7 4
e107.set_edges(e410, e74, e710)
e74.set_edges(e107, e410, e47)
e410.set_edges(e74, e107, e104)
# f11 9 8 7
e98.set_edges(e79, e87, e89)
e87.set_edges(e98, e79, e78)
e79.set_edges(e87, e98, e97)
# f12 10 9 7
e109.set_edges(e710, e97, e910)
e97.set_edges(e109, e710, e79)
e710.set_edges(e97, e109, e107)
# f13 10 8 9
e108.set_edges(e910, e89, e810)
e89.set_edges(e108, e910, e98)
e910.set_edges(e89, e108, e109)
# f14 1 5 8 10 2
e15.set_edges(e21, e58, e51)
e58.set_edges(e15, e810, e85)
e810.set_edges(e58, e102, e108)
e102.set_edges(e810, e21, e210)
e21.set_edges(e102, e15, e12)

# faces: face(outer_edge, inner_edges)
f1 = face(1, e21, None)
f2 = face(2, e21, None)
f3 = face(3, e21, None)
f4 = face(4, e21, None)
f5 = face(5, e21, None)
f6 = face(6, e21, None)
f7 = face(7, e21, None)
f8 = face(8, e21, None)
f9 = face(9, e21, None)
f10 = face(10, e21, None)
f11 = face(11, e21, None)
f12 = face(12, e21, None)
f13 = face(13, e21, None)
f14 = face(14, None, [e12, e51, e65, e46, e32, e42, e76, e85, e78, e74, e98, e109, e108])

#e.set_face()
# f1 1 2 3
e12.set_face(f1)
e23.set_face(f1)
e32.set_face(f1)
# f2 5 1 3
e51.set_face(f2)
e13.set_face(f2)
e35.set_face(f2)
# f3 6 5 3
e65.set_face(f3)
e53.set_face(f3)
e36.set_face(f3)
# f4 4 6 3
e46.set_face(f4)
e63.set_face(f4)
e34.set_face(f4)
# f5 4 3 2
e43.set_face(f5)
e32.set_face(f5)
e24.set_face(f5)
# f6 10 4 2
e104.set_face(f6)
e42.set_face(f6)
e210.set_face(f6)
# f7 7 6 4
e76.set_face(f7)
e64.set_face(f7)
e47.set_face(f7)
# f8 8 5 6
e85.set_face(f8)
e56.set_face(f8)
e68.set_face(f8)
# f9 7 8 6
e78.set_face(f9)
e86.set_face(f9)
e67.set_face(f9)
# f10 10 7 4
e107.set_face(f10)
e74.set_face(f10)
e410.set_face(f10)
# f11 9 8 7
e98.set_face(f11)
e87.set_face(f11)
e79.set_face(f11)
# f12 10 9 7
e109.set_face(f12)
e97.set_face(f12)
e710.set_face(f12)
# f13 10 8 9
e108.set_face(f13)
e89.set_face(f13)
e910.set_face(f13)
# f14 1 5 8 10 2
e15.set_face(f14)
e58.set_face(f14)
e810.set_face(f14)
e102.set_face(f14)
e21.set_face(f14)

q = vertex("q", 14, 13)
vprev = v1

def test_solution(find_triangle_step1, find_triangle_step2, find_closest_point):
    out1 = find_triangle_step1(q, vprev)
    ans1 = f2
    if (out1 != ans1):
        return (out1, ans1, "Ошибка в первом шаге")
    
    out2 = find_triangle_step2(q, out1)
    ans2 = f9
    if (out2 != ans2):
        return (out2, ans2, "Ошибка во втором шаге")
    
    out3 = find_closest_point(q, out2)
    ans3 = v9
    if (out3 != ans3):
        return (out3, ans3, "Ошибка в третьем шаге")
    
    return True