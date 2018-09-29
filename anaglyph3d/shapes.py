class Shape:
    def __init__(self):
        self.vertices = []
        self.edges = []
    
    def get_vertices(self):
        return self.vertices
    
    def get_edges(self):
        return self.edges
    
    def get_lines(self):
        verts = self.get_vertices()
        return [[verts[i] for i in edge] for edge in self.get_edges()]

class Cube(Shape):
    def __init__(self, x, y, z, width, depth, height):
        super().__init__()
        
        self.vertices = [
            (x, y, z),
            (x + width, y, z),
            (x, y + height, z),
            (x + width, y + height, z),
            (x, y, z + depth),
            (x + width, y, z + depth),
            (x, y + height, z + depth),
            (x + width, y + height, z + depth)
        ]
        
        self.edges = [
            (0, 1),
            (0, 2),
            (0, 4),
            (1, 3),
            (1, 5),
            (2, 3),
            (2, 6),
            (3, 7),
            (4, 6),
            (4, 5),
            (5, 7),
            (6, 7)
        ]

def load_obj(path):
    file = open(path, "r")
    content = file.read()
    file.close()
    
    shape = Shape()
    
    for line in content.splitlines():
        elements = line.split(" ")
        if elements[0] == "v":
            shape.vertices.append(tuple([float(x) for x in elements[1:]]))
        elif elements[0] == "f":
            face = [int(x.split("/")[0]) - 1 for x in elements[1:]]
            for i in range(len(face)):
                j = (i + 1) % len(face)
                line = (face[i], face[j])
                if line not in shape.edges and line[::-1] not in shape.edges:
                    shape.edges.append(line)

    return shape