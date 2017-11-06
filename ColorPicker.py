from PyQt5.QtGui import QColor
class ColorPicker:

    @staticmethod
    def color(id):
        if id == 0:
            return QColor(0, 0, 0)
        if id ==-1:
            return QColor(255, 255, 255)
        else:
            if id % 2 == 0:
                r = (255 - 15 * id) % 255
                g = (20 + 22 * id) % 255
                b = (100 - 17 * id) % 255
            elif id % 3 == 0:
                r = (100 + 15 * id) % 255
                g = (255 - 22 * id) % 255
                b = (20 + 17 * id) % 255

            elif id % 5 == 0:
                r = (200 - 5 * id) % 255
                g = (40 - 18 * id) % 255
                b = (120 + 17 * id) % 255
            else:
                r = (100 - 15 * id) % 255
                g = (255 - 5 * id) % 255
                b = (20 + 14 * id) % 255

            if r < 0:
                r = 0
            if g < 0:
                g = 0
            if b < 0:
                b = 0
            return QColor(r, g, b)
