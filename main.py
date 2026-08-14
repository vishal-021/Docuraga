import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QTextEdit, QScrollArea
)
from PySide6.QtCore import Qt
from chat import ChatDisplay
from spinner import Spinner
from PySide6.QtCore import QPropertyAnimation




class Navbar(QWidget):
    def __init__(self):
        super().__init__()

        self.expWidth = 250
        self.colWidth = 60
        self.collapsed = False
        self.anim = QPropertyAnimation(self, b"maximumWidth")
        self.setMaximumWidth(self.expWidth)

        self.mLayout = QVBoxLayout(self)

        header = QHBoxLayout()

        self.title = QLabel("Projects")

        self.colButton = QPushButton("☰")
        self.colButton.clicked.connect(self.Toggle)

        header.addWidget(self.title)
        header.addStretch()
        header.addWidget(self.colButton)

        self.mLayout.addLayout(header)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        self.container = QWidget()
        self.itemLayout = QVBoxLayout(self.container)
        self.itemLayout.addStretch()

        self.scroll.setWidget(self.container)

        self.mLayout.addWidget(self.scroll)

    def AddItem(self, widget):
        self.itemLayout.insertWidget(self.itemLayout.count() - 1, widget)

    def Toggle(self):
        self.collapsed = not self.collapsed
        print(self.collapsed)
        self.anim.setDuration(200)

        if self.collapsed:
            self.anim.setStartValue(250)
            self.anim.setEndValue(60)
            self.title.hide()
        else:
            self.anim.setStartValue(60)
            self.anim.setEndValue(250)
            self.title.show()

        self.anim.start()
       
        
            

class NavbarItem(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setMinimumHeight(40)


class ChatBar(QWidget):
    def __init__(self):
        super().__init__()

        self.mLayout = QHBoxLayout(self)

        self.text = QTextEdit()
        self.text.setMaximumHeight(80)

        self.send = QPushButton("Send")

        self.mLayout.addWidget(self.text)
        self.mLayout.addWidget(self.send)



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Docuraga")
        self.setMinimumSize(600, 400)

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.mainLayout = QHBoxLayout(self.centralWidget)
        self.nav = Navbar()
        self.leftSide = QWidget()
        self.leftLayout = QVBoxLayout(self.leftSide)
        self.chat = ChatDisplay()
        self.chatBox = ChatBar()
        self.mainLayout.addWidget(self.nav)
        self.mainLayout.addWidget(self.leftSide)
        self.leftLayout.addWidget(self.chat)
        self.leftLayout.addWidget(self.chatBox)




def runapp():
    app = QApplication()
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

runapp()