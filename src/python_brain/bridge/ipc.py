# ipc.py
"""
Strict JSON Schema definitions per Instruction.md Section 6B.
DO NOT modify field names - they are contractual.
"""
from pydantic import BaseModel, Field

class CaretPosition(BaseModel):
    """Physical screen coordinates of the text cursor"""
    x: int = Field(..., description="Screen X coordinate (physical pixels)")
    y: int = Field(..., description="Screen Y coordinate (physical pixels)")
    h: int = Field(..., description="Cursor height in pixels")

class InputEvent(BaseModel):
    """
    POST /input payload from C++ IME.
    Schema contract from Instruction.md Section 6B.
    """
    text: str = Field(..., description="Context text (last ~50 chars)")
    trigger_key: int = Field(..., description="Virtual Key Code (e.g., 32 for SPACE)")
    app_name: str = Field(..., description="Process name (e.g., notepad.exe)")
    caret: CaretPosition

class UIState(BaseModel):
    """
    GET /ui/state response for Team C overlay.
    Schema contract from Instruction.md Section 6B.
    """
    ghost_text: str = Field(default="", description="Suggestion text to display")
    visible: bool = Field(default=False, description="Whether overlay should be shown")
    x: int = Field(default=0, description="Ghost text X position")
    y: int = Field(default=0, description="Ghost text Y position")
