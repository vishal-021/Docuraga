from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
    QVBoxLayout
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt


class Message(QWidget):

    def __init__(self, role: str, content):
        super().__init__()

        self.role = role

        outer = QHBoxLayout(self)

        bubble = QWidget()
        bubble_layout = QVBoxLayout(bubble)

        if isinstance(content, str):
            label = QLabel(content)
            label.setWordWrap(True)
            bubble_layout.addWidget(label)

        elif isinstance(content, QPixmap):
            image = QLabel()
            image.setPixmap(content)
            bubble_layout.addWidget(image)

        if role == "user":
            bubble.setStyleSheet("""
                background:#3b82f6;
                color:white;
                border-radius:10px;
                padding:8px;
            """)
            outer.addStretch()
            outer.addWidget(bubble)

        elif role == "assistant":
            bubble.setStyleSheet("""
                background:#2e2e2e;
                color:white;
                border-radius:10px;
                padding:8px;
            """)
            outer.addWidget(bubble)
            outer.addStretch()

        else:
            bubble.setStyleSheet("""
                background:#555;
                color:white;
                border-radius:10px;
                padding:8px;
            """)
            outer.addStretch()
            outer.addWidget(bubble)
            outer.addStretch()