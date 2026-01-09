# ipc.py
from pydantic import BaseModel

class InputEvent(BaseModel):
    text: str
    trigger_key: int
    app_name: str
    caret: dict
