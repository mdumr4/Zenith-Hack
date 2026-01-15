# Frai AI Keyboard 🧠⌨️

**Frai** is an experimental AI-powered Input Method Editor (IME) for Windows. It provides intelligent "Ghost Text" code completions and a contextual Chat Assistant directly inside any application (Notepad, VS Code, etc.).

## ✨ Features

*   **👻 Ghost Text Overlay**: Real-time autocomplete suggestions displayed as gray text ahead of your cursor.
    *   **Usage**: Just type! Press **TAB** to accept a suggestion.
*   **💬 AI Chat Mode**: A floating assistant window for complex queries.
    *   **Usage**: Press `Ctrl + Space` anywhere to toggle.
*   **⚡ Native Performance**: Core logic written in C++ for ultra-low latency, bridging to a flexible Python brain for AI logic.

## 🛠️ Prerequisites

*   **OS**: Windows 10/11 (64-bit).
*   **Build Tools**: Visual Studio with C++ Desktop Development support (MSVC) and CMake.
*   **Python**: Python 3.8 or newer.

## 🚀 Installation & Setup

1.  **Initialize Python Environment**:
    ```cmd
    setup_env.bat
    ```
    *Creates a virtual environment and installs dependencies.*

2.  **Build C++ Core**:
    ```cmd
    build_all.bat
    ```
    *Compiles the `FraiIME.dll` and registers it.*

## ▶️ How to Run

1.  **Start the Keyboard**:
    ```cmd
    start_frai.bat
    ```
    *Must be run as **Administrator** because it interacts with Windows Input Methods.*

    *   You will see a console window titled "Frai AI Backend". Keep this open!
    *   Logs will confirm "UI Overlay Started".

2.  **Stop**:
    ```cmd
    stop_frai.bat
    ```
    *Cleanly shuts down the Python backend and unregisters the IME.*

## 🐛 Troubleshooting

*   **"DLL failed to load" / Updates didn't apply**:
    If you modified C++ code and the build failed to overwrite the DLL because it was locked:
    1.  Close all apps using the keyboard (Notepad, etc.).
    2.  Run `rebuild_and_update.bat`.

*   **Ghost Text not visible**:
    Ensure `start_frai.bat` logs "UI Overlay Active". The overlay is formatted as a light gray box with black text.
