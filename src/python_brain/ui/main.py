# main.py
import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer, Qt
from ui.overlay import OverlayWindow
from ui.chat_window import ChatWindow
from ui.client import UIClient

# TEAM C CONTRACT: Disable High DPI Scaling to ensure Physical Pixel coordinates
# usage. The backend sends physical coordinates, so we must match them 1:1.
os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "0"
os.environ["QT_SCALE_FACTOR"] = "1"

def start_ui():
    # Enforce strict coordinate system
    if hasattr(Qt.ApplicationAttribute, "AA_DisableHighDpiScaling"):
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_DisableHighDpiScaling)
    if hasattr(Qt.ApplicationAttribute, "AA_Use96Dpi"):
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_Use96Dpi)

    # Double check scaling policy (Qt6) - Must be before QApplication creation
    if hasattr(QApplication, "setHighDpiScaleFactorRoundingPolicy"):
        QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.Floor)

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
                # Update Overlay
                if "ghost_text" in state:
                    overlay.update_state(
                        x=state.get("x", 0),
                        y=state.get("y", 0),
                        text=state.get("ghost_text", ""),
                        visible=state.get("visible", False)
                    )
                
                # Check for Chat Window trigger (Future)
                # For now, we assume Plan Mode might be triggered via separate flag 
                # or just by user hotkey handled by IME -> Backend -> UI State
                if state.get("show_chat", False):
                    chat_window.show_chat()
                elif state.get("hide_chat", False):
                    chat_window.hide_chat()
                    
        except Exception as e:
            # Fail silently to keep UI responsive, maybe log to stdout for debug
            print(f"UI Polling Error: {e}")

    timer.timeout.connect(update_loop)
    timer.start(16) # ~60 FPS

    # Show overlay (it starts hidden/transparent but needs to be "active")
    overlay.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    start_ui()
