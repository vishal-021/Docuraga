from PySide6.QtWidgets import QWidget
from PySide6.QtCore import (
    QTimer,
    Qt
)
from PySide6.QtGui import (
    QPainter,
    QPen
)


class Spinner(QWidget):
    def __init__(self):
        super().__init__()

        self.angle = 0
        self.setFixedSize(32, 32)

        self.timer = QTimer()
        self.timer.timeout.connect(self.rotate)

    def start(self):
        self.show()
        self.timer.start(16)

    def stop(self):
        self.timer.stop()
        self.hide()

    def rotate(self):
        self.angle += 10
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)

        painter.setRenderHint(QPainter.Antialiasing)

        painter.translate(self.width()/2, self.height()/2)
        painter.rotate(self.angle)

        pen = QPen(Qt.white, 3)
        painter.setPen(pen)

        painter.drawArc(-10, -10, 20, 20, 0, 270 * 16)