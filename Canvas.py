from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QColor, QPainter, QPixmap
from PyQt5.QtCore import QSize, Qt
from ColorPicker import ColorPicker

class Canvas(QLabel):

    def __init__(self, geometry, mesh, width, height):
        super().__init__()
        self._init_ui(geometry)
        self._mesh = mesh
        self._nmb_of_points = QSize(width, height)
        self._pixmap = None

    def _init_ui(self, geometry):
        self.setGeometry(geometry)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(0, 0, 0))
        self.setPalette(p)

    def paintEvent(self, e):
        super().paintEvent(e)
        if not self._pixmap:
            qp = QPainter()
            qp.begin(self)
            self._draw_points(qp)
            qp.end()


    def _draw_points(self, qp):
        point_size = self.size().width() // self._nmb_of_points.width()
        for i, row in enumerate(self._mesh.get_points()):
            for j, item in enumerate(row):
                qp.setPen(ColorPicker.color(item.id))
                qp.fillRect(j * point_size, i * point_size, point_size, point_size, ColorPicker.color(item.id))

    def take_screenshot(self):
        return self.grab()

    def build_from_screenshot(self, filename):
        self._pixmap = QPixmap(filename).scaled(self.width(), self.height(), Qt.KeepAspectRatio)
        self.setPixmap(self._pixmap)






