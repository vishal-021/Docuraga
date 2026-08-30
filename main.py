import sys
import os
import sqlite3

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextEdit, QScrollArea, QInputDialog, QMessageBox,
    QTabWidget
)
from PySide6.QtCore import Qt, QPropertyAnimation, Signal

from chat import ChatDisplay
from spinner import Spinner
from workspace import WorkSpace
from worker import GatherWorker, QueryWorker, IndexWorker
from style import DARK_STYLE

WORKSPACES_DIR = "workspaces"
DB_PATH = "program.db"


class NavbarItem(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setObjectName("NavItem")
        self.setMinimumHeight(40)
        self.setProperty("active", False)


class Navbar(QWidget):
    workspaceSelected = Signal(str, str)
    newWorkspaceRequested = Signal()

    def __init__(self):
        super().__init__()
        self.setObjectName("Navbar")

        self.expWidth = 250
        self.colWidth = 60
        self.collapsed = False
        self.anim = QPropertyAnimation(self, b"maximumWidth")
        self.setMaximumWidth(self.expWidth)

        self.mLayout = QVBoxLayout(self)
        self.mLayout.setContentsMargins(12, 12, 12, 12)
        self.mLayout.setSpacing(10)

        header = QHBoxLayout()
        self.title = QLabel("Workspaces")
        self.title.setObjectName("NavTitle")
        self.colButton = QPushButton("☰")
        self.colButton.setObjectName("CollapseButton")
        self.colButton.setFixedSize(32, 32)
        self.colButton.clicked.connect(self.Toggle)

        header.addWidget(self.title)
        header.addStretch()
        header.addWidget(self.colButton)
        self.mLayout.addLayout(header)

        self.newButton = QPushButton("+  New Workspace")
        self.newButton.setObjectName("NewWorkspaceButton")
        self.newButton.clicked.connect(self.newWorkspaceRequested.emit)
        self.mLayout.addWidget(self.newButton)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setObjectName("NavScroll")

        self.container = QWidget()
        self.itemLayout = QVBoxLayout(self.container)
        self.itemLayout.setSpacing(6)
        self.itemLayout.addStretch()

        self.scroll.setWidget(self.container)
        self.mLayout.addWidget(self.scroll)

        self.items = {}

    def AddItem(self, path, name):
        btn = NavbarItem(name)
        btn.clicked.connect(lambda: self.workspaceSelected.emit(path, name))
        self.itemLayout.insertWidget(self.itemLayout.count() - 1, btn)
        self.items[path] = btn
        return btn

    def SetActive(self, path):
        for p, btn in self.items.items():
            btn.setProperty("active", p == path)
            btn.style().unpolish(btn)
            btn.style().polish(btn)

    def Toggle(self):
        self.collapsed = not self.collapsed
        self.anim.stop()
        self.anim.setDuration(200)

        if self.collapsed:
            self.anim.setStartValue(self.expWidth)
            self.anim.setEndValue(self.colWidth)
            self.title.hide()
            self.newButton.setText("+")
        else:
            self.anim.setStartValue(self.colWidth)
            self.anim.setEndValue(self.expWidth)
            self.title.show()
            self.newButton.setText("+  New Workspace")

        self.anim.start()


class ChatTextEdit(QTextEdit):
    sendRequested = Signal()

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter) and not (event.modifiers() & Qt.ShiftModifier):
            self.sendRequested.emit()
            return
        super().keyPressEvent(event)


class ChatBar(QWidget):
    sendMessage = Signal(str)

    def __init__(self, placeholder="Ask something...", buttonText="Send"):
        super().__init__()
        self.setObjectName("ChatBar")

        self.mLayout = QHBoxLayout(self)
        self.mLayout.setContentsMargins(12, 12, 12, 12)
        self.mLayout.setSpacing(10)

        self.text = ChatTextEdit()
        self.text.setObjectName("ChatInput")
        self.text.setMaximumHeight(80)
        self.text.setPlaceholderText(placeholder)
        self.text.sendRequested.connect(self._emit)

        self.send = QPushButton(buttonText)
        self.send.setObjectName("SendButton")
        self.send.setFixedWidth(90)
        self.send.clicked.connect(self._emit)

        self.mLayout.addWidget(self.text)
        self.mLayout.addWidget(self.send)

    def _emit(self):
        content = self.text.toPlainText().strip()
        if not content:
            return
        self.sendMessage.emit(content)
        self.text.clear()

    def setEnabled(self, enabled):
        self.text.setEnabled(enabled)
        self.send.setEnabled(enabled)


class StatusRow(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("StatusRow")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 4, 12, 4)
        layout.setSpacing(8)

        self.spinner = Spinner()
        self.spinner.hide()

        self.label = QLabel("")
        self.label.setObjectName("StatusLabel")

        layout.addWidget(self.spinner)
        layout.addWidget(self.label)
        layout.addStretch()

    def start(self, text="Working..."):
        self.label.setText(text)
        self.spinner.start()

    def update_text(self, text):
        self.label.setText(text)

    def stop(self):
        self.spinner.stop()
        self.label.setText("")


class GatherPanel(QWidget):

    indexRequested = Signal()

    def __init__(self):
        super().__init__()
        self.setObjectName("ChatArea")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.chat = ChatDisplay()
        self.status = StatusRow()

        bottomRow = QHBoxLayout()
        bottomRow.setContentsMargins(0, 0, 0, 0)
        bottomRow.setSpacing(0)

        self.chatBox = ChatBar(
            placeholder="Describe what documents to find (e.g. 'papers on transformer architectures')...",
            buttonText="Gather"
        )

        self.indexButton = QPushButton("Index Folder")
        self.indexButton.setObjectName("IndexButton")
        self.indexButton.setFixedHeight(self.chatBox.sizeHint().height() or 60)
        self.indexButton.clicked.connect(self.indexRequested.emit)

        bottomRow.addWidget(self.chatBox, 1)
        bottomRow.addWidget(self.indexButton)

        layout.addWidget(self.chat)
        layout.addWidget(self.status)
        layout.addLayout(bottomRow)

        self.chatBox.setEnabled(False)
        self.indexButton.setEnabled(False)


class QueryPanel(QWidget):
    """Chat panel for asking questions against the indexed PDFs."""

    def __init__(self):
        super().__init__()
        self.setObjectName("ChatArea")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.chat = ChatDisplay()
        self.status = StatusRow()
        self.chatBox = ChatBar(
            placeholder="Ask a question about the indexed documents...",
            buttonText="Send"
        )

        layout.addWidget(self.chat)
        layout.addWidget(self.status)
        layout.addWidget(self.chatBox)

        self.chatBox.setEnabled(False)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Docuraga")
        self.setMinimumSize(900, 600)

        self.currentWorkspace = None
        self.gatherWorker = None
        self.queryWorker = None

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.mainLayout = QHBoxLayout(self.centralWidget)
        self.mainLayout.setContentsMargins(10, 10, 10, 10)
        self.mainLayout.setSpacing(0)

        self.nav = Navbar()
        self.nav.workspaceSelected.connect(self.switch_workspace)
        self.nav.newWorkspaceRequested.connect(self.prompt_new_workspace)

        self.tabs = QTabWidget()
        self.tabs.setObjectName("MainTabs")

        self.gatherPanel = GatherPanel()
        self.gatherPanel.chatBox.sendMessage.connect(self.handle_gather)
        self.gatherPanel.indexRequested.connect(self.handle_index_folder)

        self.queryPanel = QueryPanel()
        self.queryPanel.chatBox.sendMessage.connect(self.handle_query)

        self.tabs.addTab(self.gatherPanel, "Gather Sources")
        self.tabs.addTab(self.queryPanel, "Ask Questions")

        self.mainLayout.addWidget(self.nav)
        self.mainLayout.addWidget(self.tabs)

        os.makedirs(WORKSPACES_DIR, exist_ok=True)
        self.load_workspaces()

    def load_workspaces(self):
        if not os.path.exists(DB_PATH):
            return
        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("SELECT path, name FROM workspaces")
            rows = cur.fetchall()
            conn.close()
        except sqlite3.OperationalError:
            return

        for path, name in rows:
            self.nav.AddItem(path, name)

    def prompt_new_workspace(self):
        name, ok = QInputDialog.getText(self, "New Workspace", "Workspace name:")
        if not ok or not name.strip():
            return
        name = name.strip()
        path = os.path.join(WORKSPACES_DIR, name)

        if os.path.exists(path):
            QMessageBox.warning(self, "Workspace exists", "A workspace with that name already exists.")
            return

        ws = WorkSpace(path, name)
        try:
            ws.BuildWorkSpace("index.faiss", "metadata.pkl", "pdfs", "conversations.db")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not create workspace:\n{e}")
            return

        self.nav.AddItem(path, name)
        self.switch_workspace(path, name)

    def switch_workspace(self, path, name):
        ws = WorkSpace(path, name)
        ws.faissPath = os.path.join(path, "index.faiss")
        ws.metaPath = os.path.join(path, "metadata.pkl")
        ws.pdfPath = os.path.join(path, "pdfs")
        ws.convoPath = os.path.join(path, "conversations.db")
        ws.built = True

        self.currentWorkspace = ws
        self.nav.SetActive(path)

        self.gatherPanel.chatBox.setEnabled(True)
        self.gatherPanel.indexButton.setEnabled(True)
        self.queryPanel.chatBox.setEnabled(True)
        
        self.gatherPanel.chat.clear()
        self.queryPanel.chat.clear()

        try:
            history = ws.LoadConversation(ws.convoPath)
        except Exception:
            history = []

        # Conversations are tagged with a "kind" prefix in role so each
        # panel only shows its own history. See handle_gather/handle_query.
        for entry in history:
            role = entry["role"]
            if role.startswith("gather:"):
                self.gatherPanel.chat.addMessage(role.split(":", 1)[1], entry["content"])
            elif role.startswith("query:"):
                self.queryPanel.chat.addMessage(role.split(":", 1)[1], entry["content"])
            else:
                # legacy rows with no prefix -> show in query panel
                self.queryPanel.chat.addMessage(role, entry["content"])

    def _save(self, kind, role, content):
        if self.currentWorkspace is None:
            return
        try:
            self.currentWorkspace.InsertConversation(
                self.currentWorkspace.convoPath, f"{kind}:{role}", content
            )
        except Exception as e:
            print(f"[SAVE ERROR] {e}")

    # ---- Gather tab ----

    def handle_gather(self, message):
        if self.currentWorkspace is None:
            QMessageBox.information(self, "No workspace", "Create or select a workspace first.")
            return

        self.gatherPanel.chat.addMessage("user", message)
        self._save("gather", "user", message)

        self.gatherPanel.chatBox.setEnabled(False)
        self.gatherPanel.status.start("Working...")

        self.gatherWorker = GatherWorker(self.currentWorkspace, message)
        self.gatherWorker.status.connect(self.gatherPanel.status.update_text)
        self.gatherWorker.finished.connect(self.handle_gather_finished)
        self.gatherWorker.error.connect(self.handle_gather_error)
        self.gatherWorker.start()

    def handle_gather_finished(self, summary, pdf_count):
        self.gatherPanel.status.stop()
        self.gatherPanel.chatBox.setEnabled(True)
        self.gatherPanel.chat.addMessage("assistant", summary)
        self._save("gather", "assistant", summary)

    def handle_gather_error(self, message):
        self.gatherPanel.status.stop()
        self.gatherPanel.chatBox.setEnabled(True)
        text = f"Something went wrong: {message}"
        self.gatherPanel.chat.addMessage("system", text)
        self._save("gather", "system", text)

    def handle_index_folder(self):
        if self.currentWorkspace is None:
            QMessageBox.information(self, "No workspace", "Create or select a workspace first.")
            return

        self.gatherPanel.chatBox.setEnabled(False)
        self.gatherPanel.indexButton.setEnabled(False)
        self.gatherPanel.status.start("Indexing...")

        self.indexWorker = IndexWorker(self.currentWorkspace)
        self.indexWorker.status.connect(self.gatherPanel.status.update_text)
        self.indexWorker.finished.connect(self.handle_index_finished)
        self.indexWorker.error.connect(self.handle_index_error)
        self.indexWorker.start()

    def handle_index_finished(self, summary, pdf_count):
        self.gatherPanel.status.stop()
        self.gatherPanel.chatBox.setEnabled(True)
        self.gatherPanel.indexButton.setEnabled(True)
        self.gatherPanel.chat.addMessage("assistant", summary)
        self._save("gather", "assistant", summary)

    def handle_index_error(self, message):
        self.gatherPanel.status.stop()
        self.gatherPanel.chatBox.setEnabled(True)
        self.gatherPanel.indexButton.setEnabled(True)
        text = f"Something went wrong: {message}"
        self.gatherPanel.chat.addMessage("system", text)
        self._save("gather", "system", text)

    # ---- Query tab ----

    def handle_query(self, message):
        if self.currentWorkspace is None:
            QMessageBox.information(self, "No workspace", "Create or select a workspace first.")
            return

        self.queryPanel.chat.addMessage("user", message)
        self._save("query", "user", message)

        self.queryPanel.chatBox.setEnabled(False)
        self.queryPanel.status.start("Thinking...")

        self.queryWorker = QueryWorker(self.currentWorkspace, message)
        self.queryWorker.status.connect(self.queryPanel.status.update_text)
        self.queryWorker.finished.connect(self.handle_query_finished)
        self.queryWorker.error.connect(self.handle_query_error)
        self.queryWorker.start()

    def handle_query_finished(self, answer, results):
        self.queryPanel.status.stop()
        self.queryPanel.chatBox.setEnabled(True)
        self.queryPanel.chat.addMessage("assistant", answer)
        self._save("query", "assistant", answer)

    def handle_query_error(self, message):
        self.queryPanel.status.stop()
        self.queryPanel.chatBox.setEnabled(True)
        text = f"Something went wrong: {message}"
        self.queryPanel.chat.addMessage("system", text)
        self._save("query", "system", text)


def runapp():
    app = QApplication(sys.argv)
    app.setStyleSheet(DARK_STYLE)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    runapp()