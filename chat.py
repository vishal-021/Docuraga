from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QScrollArea
)
from message import Message

class ChatDisplay(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        self.container = QWidget()

        self.messages = QVBoxLayout(self.container)
        self.messages.addStretch()

        self.scroll.setWidget(self.container)

        layout.addWidget(self.scroll)

    def addMessage(self, role, content):
        msg = Message(role, content)
        self.messages.insertWidget(
            self.messages.count() - 1,
            msg
        )

        self.scroll.verticalScrollBar().setValue(
            self.scroll.verticalScrollBar().maximum()
        )

    def clear(self):
        while self.messages.count() > 1:
            item = self.messages.takeAt(0)
            if item.widget():
                item.widget().deleteLater()