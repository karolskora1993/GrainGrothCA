from PyQt5.QtCore import QSize
from Point import Point
from MainWindow import NHOODS

class Mesh:
    def __init__(self, x, y):
        self._size = QSize(x, y)
        self._x = x
        self._y = y
        self._init_points()
        self._periodic = False
        self._nhood = NHOODS[0]

    def _init_points(self):
        self._points = [[Point(x, y) for y in range(self._size.width())] for x in range(self._size.height())]

    def set_nhood(self, nhood):
        self._nhood = nhood

    def change_periodic(self):
        self._periodic = not self._periodic

    def is_completed(self):
        for row in self._points:
            if filter(lambda el: el.id == 0, row):
                return False

    def next(self):
        next_step = [row[:] for row in self._points]
        for i in range(self._size.height()):
            for j in range(self._size.width()):
                if self._points[i][j].id == 0:
                    temp = self._gen_temp_points(i, j)
                    neighbours = {}
                    for k in range(3):
                        for l in range(3):
                            id = temp[k][l].id
                            if id != 0:
                                if id in neighbours:
                                    value = neighbours[id]
                                    value += 1
                                    neighbours[id] = value
                                else:
                                    neighbours[id] = 1

                    point_id = max(neighbours, key=lambda key: neighbours[key])
                    next_step[i][j] = point_id

        self._points = [row[:] for row in next_step]

    def _gen_temp_points(self, i, j):
        temp = [[]]
        if self._periodic:
            if i == 0 and j == 0:
                temp[0][0] = self._points[self._size.width() - 1][self._size.height() - 1]
                temp[0][1] = self._points[self._size.width() - 1][0]
                temp[0][2] = self._points[self._size.width() - 1][1]
                temp[1][0] = self._points[0][self._size.height() - 1]
                temp[1][2] = self._points[0][1]
                temp[2][0] = self._points[1][self._size.height() - 1]
                temp[2][1] = self._points[1][0]
                temp[2][2] = self._points[1][1]
            elif i == 0 and j != 0 and j != self._size.height() - 1:
                temp[0][0] = self._points[self._size.width() - 1][j - 1]
                temp[0][1] = self._points[self._size.width() - 1][j]
                temp[0][2] = self._points[self._size.width() - 1][j + 1]
                temp[1][0] = self._points[0][j - 1]
                temp[1][2] = self._points[0][j]
                temp[2][0] = self._points[1][j - 1]
                temp[2][1] = self._points[1][j]
                temp[2][2] = self._points[1][j + 1]
            elif i == 0 and j == self._size.height() - 1:
                temp[0][0] = self._points[self._size.width() - 1][j - 1]
                temp[0][1] = self._points[self._size.width() - 1][j]
                temp[0][2] = self._points[self._size.width() - 1][0]
                temp[1][0] = self._points[0][j - 1]
                temp[1][2] = self._points[0][0]
                temp[2][0] = self._points[1][j - 1]
                temp[2][1] = self._points[1][j]
                temp[2][2] = self._points[1][0]
            elif i == self._size.width() - 1 and j == 0:
                temp[0][0] = self._points[i - 1][self._size.height() - 1]
                temp[0][1] = self._points[i - 1][j]
                temp[0][2] = self._points[i - 1][j + 1]
                temp[1][0] = self._points[i][self._size.height() - 1]
                temp[1][2] = self._points[i][j + 1]
                temp[2][0] = self._points[0][self._size.height() - 1]
                temp[2][1] = self._points[0][j]
                temp[2][2] = self._points[0][j + 1]
            elif i == self._size.width() - 1 and j != 0 and j != self._size.height() - 1:
                temp[0][0] = self._points[i - 1][j - 1]
                temp[0][1] = self._points[i - 1][j]
                temp[0][2] = self._points[i - 1][j + 1]
                temp[1][0] = self._points[i][j - 1]
                temp[1][2] = self._points[i][j + 1]
                temp[2][0] = self._points[0][j - 1]
                temp[2][1] = self._points[0][j]
                temp[2][2] = self._points[0][j + 1]
            elif i != 0 and j == self._size.height() - 1 and i != self._size.width() - 1:
                temp[0][0] = self._points[i - 1][j - 1]
                temp[0][1] = self._points[i - 1][j]
                temp[0][2] = self._points[i - 1][0]
                temp[1][0] = self._points[i][j - 1]
                temp[1][2] = self._points[i][0]
                temp[2][0] = self._points[i + 1][j - 1]
                temp[2][1] = self._points[i + 1][j]
                temp[2][2] = self._points[i + 1][0]
            elif i == self._size.width() - 1 and j == self._size.height() - 1:
                temp[0][0] = self._points[i - 1][j - 1]
                temp[0][1] = self._points[i - 1][j]
                temp[0][2] = self._points[i - 1][0]
                temp[1][0] = self._points[i][j - 1]
                temp[1][2] = self._points[i][0]
                temp[2][0] = self._points[0][j - 1]
                temp[2][1] = self._points[0][j]
                temp[2][2] = self._points[0][0]
            elif i != 0 and j == 0 and i != self._size.width() - 1:
                temp[0][0] = self._points[i - 1][self._size.height() - 1]
                temp[0][1] = self._points[i - 1][0]
                temp[0][2] = self._points[i - 1][1]
                temp[1][0] = self._points[i][self._size.height() - 1]
                temp[1][2] = self._points[i][1]
                temp[2][0] = self._points[i + 1][self._size.height() - 1]
                temp[2][1] = self._points[i + 1][0]
                temp[2][2] = self._points[i + 1][1]
            else:
                for k in range(-1, 2):
                    for l in range(-1, 2):
                        temp[k + 1][l + 1] = self._points[i + k][j + l]
        else:
            if i == 0 and j == 0:
                for k in range(2):
                    for l in range(2):
                        temp[k + 1][l + 1] = self._points[i + k][j + l]

            elif i == 0 and j != 0 and j != self._size.height() - 1:
                for k in range(2):
                    for l in range(-1, 2):
                        temp[k + 1][l + 1] = self._points[i + k][j + l]

            elif i == 0 and j == self._size.height() - 1:
                for k in range(2):
                    for l in range(-1, 2):
                        temp[k + 1][l + 1] = self._points[i + k][j + l]

            elif i == self._size.width() - 1 and j == 0:
                for k in range(-1, 2):
                    for l in range(2):
                        temp[k + 1][l + 1] = self._points[i + k][j + l]

            elif i == self._size.width() - 1 and j != 0 and j != self._size.height() - 1:
                for k in range(-1, 2):
                    for l in range(-1, 2):
                        temp[k + 1][l + 1] = self._points[i + k][j + l]

            elif i != 0 and j == self._size.height() - 1 and i != self._size.width() - 1:
                for k in range(-1, 2):
                    for l in range(-1, 2):
                        temp[k + 1][l + 1] = self._points[i + k][j + l]

            elif i == self._size.width() - 1 and j == self._size.height() - 1:
                for k in range(-1, 2):
                    for l in range(-1, 2):
                        temp[k + 1][l + 1] = self._points[i + k][j + l]

            elif i != 0 and j == 0 and i != self._size.width() - 1:
                for k in range(-1, 2):
                    for l in range(2):
                        temp[k + 1][l + 1] = self._points[i + k][j + l]
                        temp[0][0] = 0
                        temp[1][0] = 0
                        temp[2][0] = 0
            else:
                for k in range(-1, 2):
                    for l in range(-1, 2):
                        temp[k + 1][l + 1] = self._points[i + k][j + l]
        return temp
