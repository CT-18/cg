from test_creator import *

create_vertex(1, 0, 13)
create_vertex(2, 3, 11)
create_vertex(3, 7, 13)
create_vertex(4, 8, 11)
create_vertex(5, 10, 19)
create_vertex(6, 10, 15)
create_vertex(7, 13, 11)
create_vertex(8, 16, 14)
create_vertex(9, 14, 11)
create_vertex(10, 15, 7)

create_triangle(1, 3, 2)
create_triangle(1, 5, 3)
create_triangle(3, 5, 6)
create_triangle(3, 6, 4)
create_triangle(2, 3, 4)
create_triangle(2, 4, 10)
create_triangle(4, 6, 7)
create_triangle(6, 5, 8)
create_triangle(6, 8, 7)
create_triangle(4, 7, 10)
create_triangle(7, 8, 9)
create_triangle(7, 9, 10)
create_triangle(10, 9, 8)

claim_border([10, 8, 5, 1, 2])
update_neighbours()

q = vertex("q", 14, 13)
vprev = vertices[1]
vnext = vertices[9]

test = (q, vprev)

def check_answer(ans):
    if not ans is vnext:
        return (ans, vnext, 'Неправильно')    
    return True