# state_manager.py
"""
Global state manager for UI overlay coordination.
Manages the ghost text state that Team C polls via GET /ui/state.
"""
from bridge.ipc import UIState
import threading

class StateManager:
    """Thread-safe state manager for UI overlay"""
    
    def __init__(self):
        self._lock = threading.Lock()
        self._ui_state = UIState(
            ghost_text="",
            visible=False,
            x=0,
            y=0
        )
    
    def update_ghost_text(self, text: str, x: int, y: int):
        """Update the ghost text suggestion and position"""
        with self._lock:
            self._ui_state.ghost_text = text
            self._ui_state.visible = bool(text)
            self._ui_state.x = x
            self._ui_state.y = y
    
    def clear_ghost_text(self):
        """Clear the ghost text (e.g., when user accepts suggestion)"""
        with self._lock:
            self._ui_state.ghost_text = ""
            self._ui_state.visible = False
    
    def get_ui_state(self) -> UIState:
        """Get current UI state (called by GET /ui/state endpoint)"""
        with self._lock:
            # Return a copy to avoid race conditions
            return UIState(
                ghost_text=self._ui_state.ghost_text,
                visible=self._ui_state.visible,
                x=self._ui_state.x,
                y=self._ui_state.y
            )
