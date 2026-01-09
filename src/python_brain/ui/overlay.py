# overlay.py
from PyQt6.QtWidgets import QMainWindow, QLabel
from PyQt6.QtCore import Qt

class OverlayWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Team C: Transparent, Tool, TopMost
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.label = QLabel("Ghost Text", self)
        self.label.setStyleSheet("color: gray; font-size: 14pt;")
        self.label.move(100, 100)

    def update_position(self, x, y):
        self.label.move(x, y)
