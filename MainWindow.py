from PyQt5.QtWidgets import *
from PyQt5.QtCore import QRect, QSize
from Canvas import Canvas
from Mesh import Mesh, NHOODS
from Thread import Thread

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 800

MENU_WIDTH = 400
MENU_HEIGHT = 400

DEF_POINTS_SIZE = QSize(100, 100)


class MainWindow(QMainWindow):

    geometry = QRect(700, 300, 400, 400)

    def __init__(self, app):
        super().__init__()
        self._app = app
        MainWindow.geometry = QRect(app.desktop().screenGeometry().width() - MENU_WIDTH, 300, MENU_WIDTH, MENU_HEIGHT)
        self._init_ui()
        self._started = False
        self._mesh = Mesh(DEF_POINTS_SIZE.width(), DEF_POINTS_SIZE.height())
        self._canvas = Canvas(self.get_canvas__geometry(), self._mesh, DEF_POINTS_SIZE.width(), DEF_POINTS_SIZE.height())
        self._nhood = NHOODS[0]
        self._periodic = False
        self._canvas.show()
        self._thread = None

    def _init_ui(self):
        self.setWindowTitle("Grain groth CA")
        self.setGeometry(MainWindow.geometry)
        self._create_widgets()
        self._create_menu()

    def get_canvas__geometry(self):
        geometry = QRect(MainWindow.geometry.topLeft().x() - CANVAS_WIDTH,
                         MainWindow.geometry.topLeft().y(),
                         CANVAS_WIDTH,
                         CANVAS_HEIGHT)
        return geometry

    def _create_menu(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('File')
        clear = QAction("Clear", self)
        file_menu.addAction(clear)

        microstructure_submenu = QMenu("Microstructure", self)

        import_txt = QAction("Import from txt file", self)
        import_bmp = QAction("Import from bmp file", self)
        export_txt = QAction("export to txt file", self)
        export_bmp = QAction("export to bmp file", self)

        microstructure_submenu.addAction(import_txt)
        microstructure_submenu.addAction(export_txt)
        microstructure_submenu.addAction(import_bmp)
        microstructure_submenu.addAction(export_bmp)

        file_menu.addMenu(microstructure_submenu)

        import_txt.triggered.connect(self._import_txt_triggered)
        import_bmp.triggered.connect(self._import_bmp_triggered)
        export_txt.triggered.connect(self._export_txt_triggered)
        export_bmp.triggered.connect(self._export_bmp_triggered)

    def _create_widgets(self):

        main_layout = QGridLayout()

        main_layout.addWidget(QLabel('width:'), 1, 1)
        self._width = QLineEdit(str(DEF_POINTS_SIZE.width()))
        main_layout.addWidget(self._width, 1, 2)

        main_layout.addWidget(QLabel('height:'), 1, 3)
        self._height = QLineEdit(str(DEF_POINTS_SIZE.height()))
        main_layout.addWidget(self._height, 1, 4)

        gen_space_btn = QPushButton("change space")
        gen_space_btn.clicked.connect(self._gen_space_btn_clicked)
        main_layout.addWidget(gen_space_btn, 2, 1, 1, 4)

        main_layout.addWidget(QLabel('number of grains:'), 3, 1)
        self._grains = QLineEdit("10")
        main_layout.addWidget(self._grains, 3, 2)
        gen_grains_btn = QPushButton("generate grains")
        gen_grains_btn.clicked.connect(self._gen_grains_btn_clicked)
        main_layout.addWidget(gen_grains_btn, 3, 3, 1, 2)

        main_layout.addWidget(QLabel('number of inclusions:'), 4, 1)
        self._inclusions = QLineEdit("10")
        main_layout.addWidget(self._inclusions, 4, 2)
        gen_inclusions_btn = QPushButton("generate inclusions")
        gen_inclusions_btn.clicked.connect(self.gen_inclusions_btn_clicked)
        main_layout.addWidget(gen_inclusions_btn, 4, 3, 1, 2)

        self._start_btn = QPushButton("START")
        self._start_btn.clicked.connect(self.start_btn_clicked)
        main_layout.addWidget(self._start_btn, 5, 1, 1, 4)

        clear_btn = QPushButton("CLEAR")
        clear_btn.clicked.connect(self.clear_btn_clicked)
        main_layout.addWidget(clear_btn, 6, 1, 1, 4)

        central_w = QWidget()
        central_w.setLayout(main_layout)

        self.setCentralWidget(central_w)


    def _gen_space_btn_clicked(self):
        width = int(self._width.text())
        height = int(self._height.text())
        if self._canvas:
            self._canvas.close()
        self._mesh = Mesh(width, height)
        self._canvas = Canvas(self.get_canvas__geometry(), self._mesh, width, height)
        self._canvas.show()

    def _gen_grains_btn_clicked(self):
        nmb_grains = int(self._grains.text())
        self._mesh.generate_grains(nmb_grains)
        self._canvas.repaint()

    def gen_inclusions_btn_clicked(self):
        print("generate inclusions")

    def start_btn_clicked(self):
        btn = self.sender()
        if self._mesh.is_running():
            btn.setText("START")
        else:
            btn.setText("STOP")
            self._thread = Thread(self._mesh)
            self._thread.update_ui.connect(self._update_UI)
            self._thread.update_btn.connect(self._update_button)

            self._thread.start()
        self._mesh.change_started()

    def clear_btn_clicked(self):
        width = int(self._width.text())
        height = int(self._height.text())
        self._mesh = Mesh(width, height)
        self._canvas.close()
        self._canvas = Canvas(self.get_canvas__geometry(), self._mesh, width, height)
        self._canvas.show()
        self._canvas.repaint()

    def _import_txt_triggered(self):
        print("import txt")

    def _import_bmp_triggered(self):
        file_name = QFileDialog.getOpenFileName(self)[0]
        self._canvas.build_from_screenshot(file_name)

    def _export_txt_triggered(self):
        print("export txt")

    def _export_bmp_triggered(self):
        file_name = QFileDialog.getSaveFileName(self)[0]
        img = self._canvas.take_screenshot()
        img.save(file_name, 'bmp')

    def _update_UI(self):
        self._canvas.repaint()

    def _update_button(self):
        if self._mesh.is_running():
            self._start_btn.setText("START")
        else:
            self._start_btn.setText("STOP")



