# theme.py
import winreg
from PyQt6.QtGui import QColor

# --- PALETTE DEFINITIONS ---
PALETTE_LIGHT = {
    "COLOR_ACCENT": "#FF5A1F",
    "COLOR_BG_CARD": "#FFFFFF",
    "COLOR_BORDER_CARD": "#E4E4E7",
    "COLOR_TEXT_MAIN": "#09090B",
    "COLOR_TEXT_SUB": "#71717A",
    "COLOR_KEY_HINT": "#A1A1AA",
    "COLOR_BG_BTN_HOVER": "#F4F4F5",
    "SHADOW_ALPHA": 0.08
}

PALETTE_DARK = {
    "COLOR_ACCENT": "#FF5A1F",
    "COLOR_BG_CARD": "#18181B",      # Zinc-950
    "COLOR_BORDER_CARD": "#27272A",  # Zinc-800
    "COLOR_TEXT_MAIN": "#FAFAFA",    # Zinc-50
    "COLOR_TEXT_SUB": "#A1A1AA",     # Zinc-400
    "COLOR_KEY_HINT": "#52525B",     # Zinc-600
    "COLOR_BG_BTN_HOVER": "#27272A",
    "SHADOW_ALPHA": 0.3              # Stronger shadow for dark mode
}

def is_system_dark_mode() -> bool:
    """Checks Windows Registry for System Theme."""
    try:
        registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
        key = winreg.OpenKey(registry, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
        value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
        return value == 0
    except Exception:
        return True # Default to Dark if detection fails (Safe fallback)

def get_palette():
    """Returns the dict of colors based on system theme."""
    return PALETTE_DARK if is_system_dark_mode() else PALETTE_LIGHT
