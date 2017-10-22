from PyQt5.QtWidgets import QApplication
import sys
from MainWindow import MainWindow

def main():
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
