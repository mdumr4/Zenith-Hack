# router.py
"""
Team B - Input Routing Logic
Decides what action to take based on trigger key and context.
"""
from bridge.ipc import InputEvent
from core.local_llm import complete, chat_completion
from core.cloud_llm import chat as cloud_chat

# ... (omitted) ...

def route_chat(message: str, context: str = "") -> str:
    """
    Route chat requests to Local LLM (Mock/Quantized).
    """
    # Combine context and message
    full_prompt = f"{context}\n\nUser: {message}" if context else message

    # Call Local LLM
    response = chat_completion(full_prompt)
    return response

# Virtual Key Codes (Windows)
VK_SPACE = 32
VK_BACK = 8
VK_TAB = 9
VK_RETURN = 13

# Simple autocorrect dictionary (can be expanded)
AUTOCORRECT_MAP = {
    "teh": "the",
    "recieve": "receive",
    "occured": "occurred",
    "seperate": "separate",
    "definately": "definitely",
    "wiht": "with",
    "hte": "the",
    "taht": "that",
}

def route_input(event: InputEvent) -> dict:
    """
    Main routing function for input events.

    Logic per Instruction.md:
    - SPACE: Trigger autocorrect
    - TAB: Accept ghost text (handled by IME, we just clear state)
    - ESC: Dismiss ghost text
    - Other keys: Generate ghost text suggestion

    Returns:
        dict with action directives for C++ IME
    """
    trigger = event.trigger_key
    text = event.text.strip()

    # SPACE: Check for autocorrect
    if trigger == VK_SPACE:
        # Get the last word typed
        words = text.split()
        if words:
            last_word = words[-1].lower()
            if last_word in AUTOCORRECT_MAP:
                correction = AUTOCORRECT_MAP[last_word]
                return {
                    "action": "replace",
                    "range": [-len(last_word), 0],  # Replace last word
                    "text": correction,
                    "suggestion": None
                }

    # TAB: User accepted suggestion (clear ghost text)
    if trigger == VK_TAB:
        return {
            "action": "accept",
            "suggestion": None
        }

    # ESC: Dismiss ghost text
    if trigger == 27:  # VK_ESCAPE
        return {
            "action": "dismiss",
            "suggestion": None
        }

    # For other keys: Generate ghost text suggestion
    # Only if we have enough context (at least 3 chars)
    if len(text) >= 3:
        suggestion = complete(text)
        if suggestion:
            return {
                "action": "suggest",
                "suggestion": suggestion
            }

    # Default: No action
    return {
        "action": "none",
        "suggestion": None
    }

def route_chat(message: str, context: str = "") -> str:
    """
    Route chat requests to Cloud LLM.

    Args:
        message: User's chat message
        context: Optional context from document

    Returns:
        AI response string
    """
    # Combine context and message
    full_prompt = f"{context}\n\nUser: {message}" if context else message

    # Call cloud LLM
    response = cloud_chat(full_prompt)
    return response
