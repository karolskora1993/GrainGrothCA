from PyQt5.QtCore import QSize
from Point import Point
from random import randint
from copy import deepcopy
from numpy import array
from math import sqrt

NHOODS = ('moore',)

class Mesh:
    def __init__(self, x, y, prob_rule4=50):
        self._size = QSize(x, y)
        self._init_points()
        self._periodic = False
        self._started = False
        self._nhood = NHOODS[0]
        self._next_id = 1
        self._prob_rule4 = prob_rule4
        self._choosen_ids = []

    def _init_points(self):
        self._points = [[Point(x, y) for y in range(self._size.width())] for x in range(self._size.height())]

    def set_nhood(self, nhood):
        self._nhood = nhood

    def change_periodic(self):
        self._periodic = not self._periodic
        print("periodic: {0}".format(self._periodic))


    def change_started(self):
        self._started = not self._started
        print("started: {0}".format(self._started))

    def set_prob_for_rule4(self, prob):
        self._prob_rule4 = prob

    def is_running(self):
        return self._started

    def get_points(self):
        return self._points

    def get_size(self):
        return self._size

    def is_completed(self):
        for row in self._points:
            for el in row:
                if el.id == 0:
                    return False
        if self._started:
            self.change_started()
        return True

    def generate_grains(self, nmb_of_grains):
        for i in range(nmb_of_grains):
            x = randint(0, self._size.width() -1)
            y = randint(0, self._size.height() -1)
            while self._points[x][y].id != 0 or self._points[x][y].id == -1:
                x = randint(0, self._size.width() -1)
                y = randint(0, self._size.height() -1)
            self._points[x][y].id = self._next_id
            self._next_id += 1


    def generate_square_inclutions(self, nmb_of_inc, size):
        for i in range(nmb_of_inc):
            x = randint(size//2, self._size.width() -size//2 -1)
            y = randint(size//2, self._size.height() -size//2 -1)
            nhood = array(self._points)[x-size//2:x+size//2+1,y-size//2:y+size//2+1].tolist()
            if self.is_completed():
                while not self._gen_boundary_tab()[x][y] or self._points[x][y].id == -1 or -1 in set(x.id for lst in nhood for x in lst):
                    x = randint(size//2, self._size.width() - size//2 - 1)
                    y = randint(size//2, self._size.height() - size//2 - 1)
                    nhood = array(self._points)[x - size // 2:x + size // 2 + 1, y - size // 2:y + size // 2 + 1].tolist()
            else:
                while self._points[x][y].id == -1 or -1 in set(x.id for lst in nhood for x in lst):
                    x = randint(size//2, self._size.width() - size//2 - 1)
                    y = randint(size//2, self._size.height() - size//2 - 1)
                    nhood = array(self._points)[x - size // 2:x + size // 2 + 1, y - size // 2:y + size // 2 + 1].tolist()
            for row in nhood:
                for el in row:
                    el.id = -1

    def rule_1(self, nhood):
        neighbours = {}
        for k in range(3):
            for l in range(3):
                id = nhood[k][l]
                if id != 0 and id != -1:
                    if id in neighbours:
                        neighbours[id] += 1
                    else:
                        neighbours[id] = 1
        if neighbours:
            point_id = max(neighbours, key=lambda key: neighbours[key])
            if neighbours[point_id] >= 5:
                return point_id
        return 0

    def rule_2(self, nhood):
        nhood[0][0] = 0
        nhood[0][2] = 0
        nhood[2][0] = 0
        nhood[2][2] = 0
        neighbours = {}
        for k in range(3):
            for l in range(3):
                id = nhood[k][l]
                if id != 0 and id != -1:
                    if id in neighbours:
                        neighbours[id] += 1
                    else:
                        neighbours[id] = 1
        if neighbours:
            point_id = max(neighbours, key=lambda key: neighbours[key])
            if neighbours[point_id] >= 3:
                return point_id
        return 0

    def rule_3(self, nhood):
        nhood[0][1] = 0
        nhood[1][0] = 0
        nhood[1][2] = 0
        nhood[2][1] = 0
        neighbours = {}
        for k in range(3):
            for l in range(3):
                id = nhood[k][l]
                if id != 0 and id != -1:
                    if id in neighbours:
                        neighbours[id] += 1
                    else:
                        neighbours[id] = 1
        if neighbours:
            point_id = max(neighbours, key=lambda key: neighbours[key])
            if neighbours[point_id] >= 3:
                return point_id
        return 0

    def rule_4(self, nhood):
        neighbours = {}
        for k in range(3):
            for l in range(3):
                id = nhood[k][l]
                if id != 0 and id != -1:
                    if id in neighbours:
                        neighbours[id] += 1
                    else:
                        neighbours[id] = 1
        if neighbours:
            point_id = max(neighbours, key=lambda key: neighbours[key])
            rand_x = randint(1, 100)
            if rand_x <= self._prob_rule4:
                return point_id
        return 0

    def clear_rand(self, nb_of_grains, dual_phase = False):
        self._choosen_ids = []
        unique_ids = set(point.id for row in self._points for point in row)
        min_id = min(unique_ids)
        max_id = max(unique_ids)
        if nb_of_grains >= max_id:
            return
        ids = []
        for i in range(nb_of_grains):
            rand_id = randint(min_id, max_id)
            while rand_id in ids:
                rand_id = randint(min_id, max_id)
            ids.append(rand_id)

        if ids:
            self._choosen_ids = ids
            for row in self._points:
                for point in row:
                    if point.id not in self._choosen_ids and point.id != -1 and point.id != self._next_id:
                        point.id = 0
                    if dual_phase:
                        if point.id in self._choosen_ids:
                            point.id = self._next_id
        if dual_phase:
            self._choosen_ids = [self._next_id]
            self._next_id += 1


    def generate_circle_inclutions(self, nmb_of_inc, size):
        for i in range(nmb_of_inc):
            x = randint(size, self._size.width() - size - 2)
            y = randint(size, self._size.height() - size - 2)
            nhood = array(self._points)[x-size:x+size+1, y-size:y+size+1].tolist()
            if self.is_completed():
                while not self._gen_boundary_tab()[x][y] or self._points[x][y].id == -1 or -1 in set(x.id for lst in nhood for x in lst):
                    x = randint(size, self._size.width() - size - 2)
                    y = randint(size, self._size.height() - size - 2)
                    nhood = array(self._points)[x - size:x + size + 1, y - size:y + size + 1].tolist()
            else:
                while self._points[x][y].id == -1 or -1 in set(x.id for lst in nhood for x in lst):
                    x = randint(size, self._size.width() - size - 2)
                    y = randint(size, self._size.height() - size - 2)
                    nhood = array(self._points)[x - size:x + size + 1, y - size:y + size + 1].tolist()
            x = len(nhood)//2
            for k, row in enumerate(nhood):
                for l, el in enumerate(row):
                    if sqrt(abs(l - x)**2 + abs(k - x)**2) <= size:
                        el.id = -1

    def _gen_boundary_tab(self):
        bound_tab = [[False for _ in row] for row in self._points]
        for i in range(self._size.height()):
            for j in range(self._size.width()):
                if self._points[i][j].id != -1 and self._points[i][j].id != 0:
                    temp = self._gen_temp_points(i, j)
                    for k in range(2):
                        for l in range(1, 3):
                            if temp[k][l] != 0 and temp[k][l] != -1 and temp[k][l] != self._points[i][j].id:
                                bound_tab[i][j] = True
        return bound_tab

    def gen_boundary_lines(self, line_size):
        for row in self._points:
            for el in row:
                el.bound = False

        boundaries = self._gen_boundary_tab()
        line_size = line_size // 2
        for i, row in enumerate(boundaries):
            for j, el in enumerate(row):
                if el:
                    min_x = j
                    max_x = j + line_size if j + line_size < self._size.width() else self._size.width() - 1
                    min_y = i - line_size if i - line_size >= 0 else 0
                    max_y = i
                    for k in range(min_y, max_y + 1):
                        for l in range(min_x, max_x + 1):
                            self._points[k][l].bound = True




    def generate_rand_boundary(self, line_size, nb_of_grains):
        for row in self._points:
            for el in row:
                el.bound = False

        unique_ids = set(point.id for row in self._points for point in row)
        min_id = min(unique_ids)
        max_id = max(unique_ids)
        if nb_of_grains >= max_id:
            return
        ids = []
        for i in range(nb_of_grains):
            rand_id = randint(min_id, max_id)
            while rand_id in ids:
                rand_id = randint(min_id, max_id)
            ids.append(rand_id)

        if ids:
            boundaries = self._gen_boundary_tab()
            line_size = line_size // 2
            for i, row in enumerate(boundaries):
                for j, el in enumerate(row):
                    if el and self._check_for_bound(i, j, ids):
                        min_x = j
                        max_x = j + line_size if j + line_size < self._size.width() else self._size.width() - 1
                        min_y = i - line_size if i - line_size >= 0 else 0
                        max_y = i
                        for k in range(min_y, max_y + 1):
                            for l in range(min_x, max_x + 1):
                                self._points[k][l].bound = True

    def _check_for_bound(self, i, j, ids):
        temp = self._gen_temp_points(i, j)
        for k in range(3):
            for l in range(3):
                if temp[k][l] in ids:
                    return True
        return False

    def remove_grains(self):
        for row in self._points:
            for el in row:
                el.id = 0


    def remove_boundaries(self):
        for row in self._points:
            for el in row:
                el.bound = False


    def next(self):
        next_step = [[deepcopy(item) for item in row] for row in self._points]
        for i in range(self._size.height()):
            for j in range(self._size.width()):
                if self._points[i][j].id == 0:
                    temp = self._gen_temp_points(i, j)
                    selected_id = self.rule_1(deepcopy(temp))
                    if selected_id == 0:
                        selected_id = self.rule_2(deepcopy(temp))
                    if selected_id == 0:
                        selected_id = self.rule_3(deepcopy(temp))
                    if selected_id == 0:
                        selected_id = self.rule_4(deepcopy(temp))
                    if selected_id != 0:
                        next_step[i][j].id = selected_id
        self._points = [row[:] for row in next_step]

    def _gen_temp_points(self, i, j):
        temp = [[0, 0, 0] for _ in range(3)]
        if self._periodic:
            if i == 0 and j == 0:
                temp[0][0] = self._points[self._size.width() - 1][self._size.height() - 1].id
                temp[0][1] = self._points[self._size.width() - 1][0].id
                temp[0][2] = self._points[self._size.width() - 1][1].id
                temp[1][0] = self._points[0][self._size.height() - 1].id
                temp[1][2] = self._points[0][1].id
                temp[2][0] = self._points[1][self._size.height() - 1].id
                temp[2][1] = self._points[1][0].id
                temp[2][2] = self._points[1][1].id
            elif i == 0 and j != 0 and j != self._size.height() - 1:
                temp[0][0] = self._points[self._size.width() - 1][j - 1].id
                temp[0][1] = self._points[self._size.width() - 1][j].id
                temp[0][2] = self._points[self._size.width() - 1][j + 1].id
                temp[1][0] = self._points[0][j - 1].id
                temp[1][2] = self._points[0][j].id
                temp[2][0] = self._points[1][j - 1].id
                temp[2][1] = self._points[1][j].id
                temp[2][2] = self._points[1][j + 1].id
            elif i == 0 and j == self._size.height() - 1:
                temp[0][0] = self._points[self._size.width() - 1][j - 1].id
                temp[0][1] = self._points[self._size.width() - 1][j].id
                temp[0][2] = self._points[self._size.width() - 1][0].id
                temp[1][0] = self._points[0][j - 1].id
                temp[1][2] = self._points[0][0].id
                temp[2][0] = self._points[1][j - 1].id
                temp[2][1] = self._points[1][j].id
                temp[2][2] = self._points[1][0].id
            elif i == self._size.width() - 1 and j == 0:
                temp[0][0] = self._points[i - 1][self._size.height() - 1].id
                temp[0][1] = self._points[i - 1][j].id
                temp[0][2] = self._points[i - 1][j + 1].id
                temp[1][0] = self._points[i][self._size.height() - 1].id
                temp[1][2] = self._points[i][j + 1].id
                temp[2][0] = self._points[0][self._size.height() - 1].id
                temp[2][1] = self._points[0][j].id
                temp[2][2] = self._points[0][j + 1].id
            elif i == self._size.width() - 1 and j != 0 and j != self._size.height() - 1:
                temp[0][0] = self._points[i - 1][j - 1].id
                temp[0][1] = self._points[i - 1][j].id
                temp[0][2] = self._points[i - 1][j + 1].id
                temp[1][0] = self._points[i][j - 1].id
                temp[1][2] = self._points[i][j + 1].id
                temp[2][0] = self._points[0][j - 1].id
                temp[2][1] = self._points[0][j].id
                temp[2][2] = self._points[0][j + 1].id
            elif i != 0 and j == self._size.height() - 1 and i != self._size.width() - 1:
                temp[0][0] = self._points[i - 1][j - 1].id
                temp[0][1] = self._points[i - 1][j].id
                temp[0][2] = self._points[i - 1][0].id
                temp[1][0] = self._points[i][j - 1].id
                temp[1][2] = self._points[i][0].id
                temp[2][0] = self._points[i + 1][j - 1].id
                temp[2][1] = self._points[i + 1][j].id
                temp[2][2] = self._points[i + 1][0].id
            elif i == self._size.width() - 1 and j == self._size.height() - 1:
                temp[0][0] = self._points[i - 1][j - 1].id
                temp[0][1] = self._points[i - 1][j].id
                temp[0][2] = self._points[i - 1][0].id
                temp[1][0] = self._points[i][j - 1].id
                temp[1][2] = self._points[i][0].id
                temp[2][0] = self._points[0][j - 1].id
                temp[2][1] = self._points[0][j].id
                temp[2][2] = self._points[0][0].id
            elif i != 0 and j == 0 and i != self._size.width() - 1:
                temp[0][0] = self._points[i - 1][self._size.height() - 1].id
                temp[0][1] = self._points[i - 1][0].id
                temp[0][2] = self._points[i - 1][1].id
                temp[1][0] = self._points[i][self._size.height() - 1].id
                temp[1][2] = self._points[i][1].id
                temp[2][0] = self._points[i + 1][self._size.height() - 1].id
                temp[2][1] = self._points[i + 1][0].id
                temp[2][2] = self._points[i + 1][1].id
            else:
                for k in range(-1, 2):
                    for l in range(-1, 2):
                        temp[k + 1][l + 1] = self._points[i + k][j + l].id
        else:
            if i == 0 and j == 0:
                for k in range(2):
                    for l in range(2):
                        temp[k + 1][l + 1] = self._points[i + k][j + l].id

            elif i == 0 and j != 0 and j != self._size.height() - 1:
                for k in range(2):
                    for l in range(-1, 2):
                        temp[k + 1][l + 1] = self._points[i + k][j + l].id

            elif i == 0 and j == self._size.height() - 1:
                for k in range(2):
                    for l in range(-1, 1):
                        temp[k + 1][l + 1] = self._points[i + k][j + l].id

            elif i == self._size.width() - 1 and j == 0:
                for k in range(-1, 1):
                    for l in range(2):
                        temp[k + 1][l + 1] = self._points[i + k][j + l].id

            elif i == self._size.width() - 1 and j != 0 and j != self._size.height() - 1:
                for k in range(-1, 1):
                    for l in range(-1, 2):
                        temp[k + 1][l + 1] = self._points[i + k][j + l].id

            elif i != 0 and j == self._size.height() - 1 and i != self._size.width() - 1:
                for k in range(-1, 2):
                    for l in range(-1, 1):
                        temp[k + 1][l + 1] = self._points[i + k][j + l].id

            elif i == self._size.width() - 1 and j == self._size.height() - 1:
                for k in range(-1, 1):
                    for l in range(-1, 1):
                        temp[k + 1][l + 1] = self._points[i + k][j + l].id

            elif i != 0 and j == 0 and i != self._size.width() - 1:
                for k in range(-1, 2):
                    for l in range(2):
                        temp[k + 1][l + 1] = self._points[i + k][j + l].id
                        temp[0][0] = 0
                        temp[1][0] = 0
                        temp[2][0] = 0
            else:
                for k in range(-1, 2):
                    for l in range(-1, 2):
                        temp[k + 1][l + 1] = self._points[i + k][j + l].id
        for i, row in enumerate(temp):
            for j, el in enumerate(row):
                if el in self._choosen_ids:
                    temp[i][j] = 0
        return temp

