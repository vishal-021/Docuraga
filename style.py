DARK_STYLE = """
QWidget {
    background-color: #111318;
    color: #e5e7eb;
    font-family: 'Segoe UI', 'Inter', sans-serif;
    font-size: 13px;
}

#Navbar {
    background-color: #17191f;
    border-right: 1px solid #23262f;
}

#NavTitle {
    font-size: 15px;
    font-weight: 600;
    color: #f3f4f6;
}

#CollapseButton {
    background-color: transparent;
    border: none;
    border-radius: 6px;
    color: #9ca3af;
}
#CollapseButton:hover { background-color: #23262f; }

#NewWorkspaceButton {
    background-color: #3b82f6;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 8px;
    font-weight: 600;
}
#NewWorkspaceButton:hover { background-color: #2563eb; }

#NavScroll { border: none; background: transparent; }

QPushButton#NavItem {
    text-align: left;
    padding: 8px 10px;
    border-radius: 8px;
    background-color: transparent;
    color: #d1d5db;
    border: none;
}
QPushButton#NavItem:hover { background-color: #1f2229; }
QPushButton#NavItem[active="true"] {
    background-color: #23262f;
    color: #ffffff;
    font-weight: 600;
}

#ChatArea { background-color: #0d0f13; }

#StatusLabel { color: #9ca3af; font-size: 12px; }

#ChatBar {
    background-color: #17191f;
    border-top: 1px solid #23262f;
}

#ChatInput {
    background-color: #1c1f26;
    color: #f3f4f6;
    border: 1px solid #2a2d36;
    border-radius: 10px;
    padding: 8px;
}
#ChatInput:focus { border: 1px solid #3b82f6; }

#SendButton {
    background-color: #3b82f6;
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 600;
}
#SendButton:hover { background-color: #2563eb; }
#SendButton:disabled { background-color: #374151; color: #9ca3af; }

QScrollBar:vertical { background: transparent; width: 8px; }
QScrollBar::handle:vertical { background: #2a2d36; border-radius: 4px; min-height: 20px; }
QScrollBar::handle:vertical:hover { background: #3b3f4a; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
QTabWidget#MainTabs::pane {
    border: none;
    background-color: #0d0f13;
}

QTabWidget#MainTabs QTabBar::tab {
    background-color: #17191f;
    color: #9ca3af;
    padding: 10px 18px;
    border: none;
    border-bottom: 2px solid transparent;
}

QTabWidget#MainTabs QTabBar::tab:selected {
    color: #ffffff;
    border-bottom: 2px solid #3b82f6;
    background-color: #1c1f26;
}

QTabWidget#MainTabs QTabBar::tab:hover:!selected {
    color: #d1d5db;
}
#IndexButton {
    background-color: #23262f;
    color: #d1d5db;
    border: 1px solid #2a2d36;
    border-radius: 10px;
    padding: 8px 14px;
    margin-left: 10px;
    font-weight: 600;
}
#IndexButton:hover { background-color: #2a2d36; }
#IndexButton:disabled { background-color: #1a1c22; color: #6b7280; }
"""