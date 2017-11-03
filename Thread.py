from PyQt5.QtCore import QThread, pyqtSignal

class Thread(QThread):

    update_ui = pyqtSignal()

    def __init__(self, mesh):
        super().__init__()
        self._mesh = mesh

    def run(self):
        while not self._mesh.is_completed() and  self._mesh.is_running():
            self._mesh.next()
            self.update_ui.emit()
            self.wait(10)

