import sys
import os
import ctypes # For Windows DPI Awareness

# Fix Import Path: Add 'src/python_brain' to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer, Qt
from ui.overlay import OverlayWindow
from ui.chat_window import ChatWindow
from ui.client import UIClient

# START_UI_UPDATES: User requested crisp sizing
# We remove the old "Disable High DPI" contract and enable it fully.

def start_ui():
    # 1. Windows DPI Awareness (Per-Monitor DPI)
    # 1. Windows DPI Awareness (Per-Monitor DPI)
    # try:
    #     ctypes.windll.shcore.SetProcessDpiAwareness(1)
    # except Exception:
    #     pass

    # 2. Qt High DPI Attributes BEFORE App Creation
    if hasattr(Qt.ApplicationAttribute, "AA_EnableHighDpiScaling"):
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling)
    if hasattr(Qt.ApplicationAttribute, "AA_UseHighDpiPixmaps"):
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)

    # Initialize Components
    overlay = OverlayWindow()
    chat_window = ChatWindow()
    client = UIClient()

    # Polling Loop (Decoupled from Backend)
    # Poll every 16ms (~60 FPS) for UI updates
    timer = QTimer()

    def update_loop():
        try:
            # TEAM C CONTRACT: Poll /ui/state
            state = client.poll_state()
            if state:
                if "ghost_text" in state:
                    overlay.update_state(
                        x=state.get("x", 0),
                        y=state.get("y", 0),
                        h=state.get("h", 0),
                        text=state.get("ghost_text", ""),
                        visible=state.get("visible", False)
                    )

                # Check for Chat Window trigger (Future)
                if state.get("show_chat", False):
                    if not chat_window.isVisible():
                        chat_window.show_chat()
                elif state.get("hide_chat", False):
                    if chat_window.isVisible():
                        chat_window.hide_chat()

        except Exception as e:
            # Fail silently to keep UI responsive, maybe log to stdout for debug
            print(f"UI Polling Error: {e}")

    timer.timeout.connect(update_loop)
    timer.start(16) # ~60 FPS

    # Show overlay (it starts hidden/transparent but needs to be "active")
    # overlay.show() # DISABLED

    print("[INFO] Starting UI Overlay (HighDPI Enabled)...")

    sys.exit(app.exec())

if __name__ == "__main__":
    start_ui()
