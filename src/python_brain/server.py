# server.py
"""
Team B - AI Backend Server
Port: 18492 (HARDCODED per Instruction.md Section 6A)
"""
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bridge.ipc import InputEvent, UIState
from core.router import route_input, route_chat
from core.state_manager import StateManager

app = FastAPI(title="Frai AI Backend", version="1.0")

# Global state manager
state = StateManager()

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "Frai AI Backend Running", "port": 18492}

@app.post("/input")
async def handle_input(event: InputEvent):
    """
    PRIMARY ENDPOINT: Receives keystroke events from C++ IME.
    Schema: Instruction.md Section 6B
    
    Contract:
    - Field names are FIXED (text, trigger_key, app_name, caret)
    - Returns action directives for IME
    """
    try:
        # Route to appropriate handler based on trigger key
        result = route_input(event)
        
        # Update UI state if suggestion generated
        if result and result.get("suggestion"):
            state.update_ghost_text(
                text=result["suggestion"],
                x=event.caret.x,
                y=event.caret.y
            )
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/ui/state")
async def get_ui_state():
    """
    UI POLLING ENDPOINT: Team C queries this for overlay updates.
    Schema: Instruction.md Section 6B
    
    Returns: UIState with ghost_text, visible, x, y
    """
    return state.get_ui_state()

@app.post("/chat")
async def handle_chat(data: dict):
    """
    PLAN MODE ENDPOINT: Multi-turn conversation with AI.
    
    Input: { "message": str, "context": str (optional) }
    Returns: { "response": str }
    """
    try:
        message = data.get("message", "")
        context = data.get("context", "")
        
        response = route_chat(message, context)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # CRITICAL: Port 18492 is HARDCODED per contract
    # DO NOT make this dynamic or configurable
    print("=" * 60)
    print("Frai AI Backend Server Starting")
    print("=" * 60)
    print(f"Port: 18492 (HARDCODED)")
    print(f"Endpoints:")
    print(f"  POST /input      - Keystroke handler")
    print(f"  GET  /ui/state   - UI overlay state")
    print(f"  POST /chat       - Plan mode chat")
    print("=" * 60)
    
    # Initialize memory components
    from memory.clipboard import start_clipboard_watcher
    from memory.vector import get_memory_store
    
    # Get memory store instance
    memory = get_memory_store()
    
    # Start clipboard watcher with callback to add to memory
    def on_clipboard_change(text: str):
        """Callback when clipboard content changes"""
        print(f"Clipboard: {text[:50]}...")
        memory.add(text, metadata={"source": "clipboard"})
    
    start_clipboard_watcher(on_clipboard_change)
    
    print("Memory components initialized")
    print("=" * 60)
    
    uvicorn.run(
        app, 
        host="127.0.0.1", 
        port=18492,
        log_level="info"
    )
