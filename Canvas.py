from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtCore import QPoint, QRect
from ColorPicker import ColorPicker

class Canvas(QWidget):

    def __init__(self, geometry, mesh, width, height):
        super().__init__()
        self._init_ui(geometry)
        self._mesh = mesh
        self._size = QPoint(width, height)

    def _init_ui(self, geometry):
        self.setGeometry(geometry)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(0, 0, 0))
        self.setPalette(p)

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self._draw_points(qp)
        qp.end()

    def _draw_points(self, qp):
        point_size = self.size().width() // self._size.x()
        for i, row in enumerate(self._mesh):
            for j, col in enumerate(row):
                qp.setPen(ColorPicker.color(col.id))
                qp.fillRect(j * point_size, i * point_size, point_size, point_size, ColorPicker.color(col.id))





