from Mesh import Mesh

def load_mesh(path):
    with open(path, 'r') as f:
        width, height = f.readline().split(' ')
        mesh = Mesh(int(width), int(height))
        points = mesh.get_points()
        for line in f.read().splitlines():
            x, y, phase, id = line.split(' ')
            points[int(x)][int(y)].id = int(id)
            points[int(x)][int(y)].phase = int(phase)

        return mesh


def save_mesh(path, mesh):
    points = mesh.get_points()
    with open(path, 'w') as f:
        f.write("{0} {1}\n".format(len(points), len(points[0])))
        for i, row in enumerate(points):
            for j, item in enumerate(row):
                f.write("{0} {1} {2} {3}\n".format(i, j, item.phase, item.id))


