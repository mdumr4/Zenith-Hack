# clipboard.py
"""
Team B - Clipboard Monitoring
Background thread that watches clipboard for semantic memory indexing.
"""
import threading
import time
import pyperclip
from typing import Callable, Optional

class ClipboardWatcher:
    """Background service that monitors clipboard changes"""
    
    def __init__(self, callback: Optional[Callable[[str], None]] = None):
        """
        Args:
            callback: Function to call when new clipboard content is detected
        """
        self.callback = callback
        self._running = False
        self._thread = None
        self._last_content = ""
    
    def start(self):
        """Start the clipboard monitoring thread"""
        if self._running:
            return
        
        self._running = True
        self._thread = threading.Thread(target=self._watch_loop, daemon=True)
        self._thread.start()
        print("Clipboard watcher started")
    
    def stop(self):
        """Stop the clipboard monitoring thread"""
        self._running = False
        if self._thread:
            self._thread.join(timeout=2)
        print("Clipboard watcher stopped")
    
    def _watch_loop(self):
        """Main monitoring loop (runs in background thread)"""
        while self._running:
            try:
                # Get current clipboard content
                current = pyperclip.paste()
                
                # Check if content changed
                if current and current != self._last_content:
                    self._last_content = current
                    
                    # Call callback if provided
                    if self.callback:
                        self.callback(current)
                
                # Sleep to avoid CPU spinning
                time.sleep(0.5)
            except Exception as e:
                print(f"Clipboard watcher error: {e}")
                time.sleep(1)

# Global instance
_watcher = None

def start_clipboard_watcher(callback: Callable[[str], None]):
    """Start the global clipboard watcher"""
    global _watcher
    if _watcher is None:
        _watcher = ClipboardWatcher(callback)
        _watcher.start()

def stop_clipboard_watcher():
    """Stop the global clipboard watcher"""
    global _watcher
    if _watcher:
        _watcher.stop()
        _watcher = None
