# main.py
import sys
from PyQt6.QtWidgets import QApplication
from ui.overlay import OverlayWindow

def start_ui():
    app = QApplication(sys.argv)
    window = OverlayWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    start_ui()
