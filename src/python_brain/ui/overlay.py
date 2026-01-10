# overlay.py
from PyQt6.QtWidgets import QMainWindow, QLabel, QApplication
from PyQt6.QtCore import Qt, QPoint

class OverlayWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # TEAM C CONTRACT: Frameless, Topmost, Transparent, Tool (not in taskbar)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool |
            Qt.WindowType.WindowDoesNotAcceptFocus # Important: Don't steal focus!
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)

        # Ghost Text Label
        self.ghost_label = QLabel(self)
        self.ghost_label.setStyleSheet("color: #888888; font-family: 'Segoe UI'; font-size: 14px;") # Basic styling
        self.ghost_label.hide()
        
        # Determine screen geometry for positioning
        screen = QApplication.primaryScreen()
        if screen:
            self.setGeometry(screen.geometry())
        else:
            self.resize(1920, 1080) # Fallback

    def update_state(self, x: int, y: int, text: str, visible: bool):
        """
        Update the overlay state based on physical coordinates.
        """
        if not visible or not text:
            self.ghost_label.hide()
            return
            
        self.ghost_label.setText(text)
        self.ghost_label.adjustSize()
        
        # Move label to (x, y). 
        # Since this window covers the whole screen (ideally), 
        # we move the label relative to 0,0 of this window which is 0,0 of screen.
        self.ghost_label.move(x, y)
        self.ghost_label.show()
