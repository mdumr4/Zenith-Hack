# overlay.py
from PyQt6.QtWidgets import (QMainWindow, QLabel, QApplication, QFrame, QVBoxLayout,
                             QHBoxLayout, QGraphicsDropShadowEffect, QWidget, QPushButton)
from PyQt6.QtCore import Qt, QPoint, QRect
from PyQt6.QtGui import QColor, QFont, QPalette, QCursor

from ui.theme import get_palette

# Load Dynamic Palette
P = get_palette()

COLOR_ACCENT = P["COLOR_ACCENT"]
COLOR_BG_CARD = P["COLOR_BG_CARD"]
COLOR_BORDER_CARD = P["COLOR_BORDER_CARD"]
COLOR_TEXT_MAIN = P["COLOR_TEXT_MAIN"]
COLOR_TEXT_SUB = P["COLOR_TEXT_SUB"]
COLOR_KEY_HINT = P["COLOR_KEY_HINT"]
COLOR_BG_BTN_HOVER = P["COLOR_BG_BTN_HOVER"]

import ctypes

def get_foreground_window_title():
    hwnd = ctypes.windll.user32.GetForegroundWindow()
    length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
    buff = ctypes.create_unicode_buffer(length + 1)
    ctypes.windll.user32.GetWindowTextW(hwnd, buff, length + 1)
    return buff.value

class GhostTextLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("GhostTextLabel")
        self.setContentsMargins(0, 0, 0, 0)

        # Fixed stylesheet with Windows font fixes
        self.setStyleSheet("""
            QLabel#GhostTextLabel {
                color: #000000;  /* Pure Black */
                background-color: transparent;
                padding: 0px;
                margin: 0px;
                border: none;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 11pt;
                font-style: italic;
                font-weight: 400;
                qproperty-alignment: AlignLeft | AlignVCenter;
            }
        """)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        # Critical: Disable smoothing/hinting for crisp monospace in overlays
        font = self.font()
        font.setHintingPreference(QFont.HintingPreference.PreferNoHinting)
        font.setStyleStrategy(QFont.StyleStrategy.NoAntialias)
        self.setFont(font)

class OverlayWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool |
            Qt.WindowType.WindowDoesNotAcceptFocus
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)

        self.container = QWidget(self)
        self.container.setStyleSheet("background: transparent;")
        self.setCentralWidget(self.container)

        self.label = GhostTextLabel(self.container)
        self.label.hide()

        # Transparent for mouse events -> Pass clicks through
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        self.setWindowOpacity(1.0) # Ensure visible by default

        # State Caching to prevent redundant repaints/smearing
        self.last_state = None

    def update_state(self, x: int, y: int, h: int, text: str, visible: bool):
        # Focus Check DISABLED for robustness
        # if "Notepad" not in get_foreground_window_title(): ...

        # Optimization: Don't redraw if nothing changed
        current_state = (x, y, h, text, visible)
        if self.last_state == current_state:
            return
        self.last_state = current_state

        if not visible or not text:
            if self.isVisible():
                self.hide()
                self.label.clear()
            return

        self.label.setText(text)
        self.label.show()

        # Force pixel-perfect sizing to prevent scaling blur (User Suggestion)
        self.label.resize(self.label.sizeHint())
        self.resize(self.label.sizeHint().width() + 2, self.label.sizeHint().height() + 2)

        # Calculate Final Geometry
        final_w = self.width()
        final_h = self.height()

        # DPI CORRECTION: C++ sends Physical Pixels, Qt uses Logical Pixels
        dpr = self.devicePixelRatio()

        # Position slightly offset to right of caret
        final_x = int(x / dpr) + 8

        # Simple Vertical Centering
        if h > 0:
            # Scale height too
            scaled_h = int(h / dpr)
            scaled_y = int(y / dpr)

            center_y = scaled_y + (scaled_h // 2)
            final_y = center_y - (final_h // 2)
        else:
            final_y = int(y / dpr)

        # Extra safety for screen bounds
        screen = QApplication.primaryScreen()
        screen_geo = screen.geometry()

        if final_x + final_w > screen_geo.right():
            pass

        self.setGeometry(final_x, final_y, final_w, final_h)
        self.label.move(0, 0) # Ensure label is at 0,0 relative to window

        if not self.isVisible():
            self.setWindowOpacity(1.0)
            self.show()
            self.raise_() # Ensure top
