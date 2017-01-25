class vertex:
    def __init__(self, name, x, y):
        self.x, self.y, self.z = x, y, 1
        self.triangles = []
        self.name = name
        
    def add_triangle(self, triangle):
        self.triangles.append(triangle) # список треугольников, инцидентных вершине, в порядке обхода по часовой стрелке

class triangle:
    def __init__(self, name, vertices):
        self.vertices = vertices # лист вершин в порядке обхода по часовой стрелке
        self.neighbours = []
        self.name = name
    
    def add_neighbour(self, neighbour):
        self.neighbours.append(neighbour) # лист смежных по ребру треугольников-соседей, в порядке обхода по часовой стрелке