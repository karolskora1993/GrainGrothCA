from PyQt5.QtCore import QSize
from Point import Point
from random import randint
from copy import deepcopy

NHOODS = ('moore',)

class Mesh:
    def __init__(self, x, y):
        self._size = QSize(x, y)
        self._init_points()
        self._periodic = False
        self._started = False
        self._nhood = NHOODS[0]
        self._next_id = 1

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

    def is_running(self):
        return self._started

    def get_points(self):
        return self._points

    def is_completed(self):
        for row in self._points:
            for el in row:
                if el.id == 0:
                    return False
        print("completed")
        return True

    def generate_grains(self, nmb_of_grains):
        for i in range(nmb_of_grains):
            x = randint(0, self._size.width() -1)
            y = randint(0, self._size.height() -1)
            while (self._points[x][y].id != 0):
                x = randint(0, self._size.width() -1)
                y = randint(0, self._size.height() -1)
            self._points[x][y].id = self._next_id
            self._next_id += 1

    def next(self):
        next_step = [[deepcopy(item) for item in row] for row in self._points]
        for i in range(self._size.height()):
            for j in range(self._size.width()):
                if self._points[i][j].id == 0:
                    temp = self._gen_temp_points(i, j)
                    neighbours = {}
                    for k in range(3):
                        for l in range(3):
                            id = temp[k][l]
                            if id != 0:
                                if id in neighbours:
                                    neighbours[id] += 1
                                else:
                                    neighbours[id] = 1
                    if neighbours:
                        point_id = max(neighbours, key=lambda key: neighbours[key])
                        next_step[i][j].id = point_id
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
        return temp

