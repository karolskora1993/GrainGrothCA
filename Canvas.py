from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QColor
class Canvas(QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        self.setGeometry(0, 0, 600, 600)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(0, 0, 0))
        self.setPalette(p)
