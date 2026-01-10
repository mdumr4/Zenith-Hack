# chat_window.py
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLineEdit, QTextEdit
from PyQt6.QtCore import Qt

class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Spotlight Style: Frameless, Centered
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        
        # translucent background for glass effect (simplified for now)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.central_widget = QWidget()
        self.central_widget.setStyleSheet("""
            QWidget {
                background-color: #F0F0F0;
                border-radius: 10px;
                border: 1px solid #CCCCCC;
            }
        """)
        self.setCentralWidget(self.central_widget)
        
        layout = QVBoxLayout(self.central_widget)
        
        # Chat History
        self.history = QTextEdit()
        self.history.setReadOnly(True)
        self.history.setStyleSheet("background: transparent; border: none;")
        layout.addWidget(self.history)
        
        # Input Bar
        self.input = QLineEdit()
        self.input.setPlaceholderText("Ask AI...")
        self.input.setStyleSheet("""
            QLineEdit {
                background: white;
                border: 1px solid #DDD;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
            }
        """)
        layout.addWidget(self.input)
        
        self.resize(600, 400)
        self.center_on_screen()
        self.hide() # Hidden by default

    def center_on_screen(self):
        screen = self.screen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

    def show_chat(self):
        self.show()
        self.activateWindow()
        self.input.setFocus()

    def hide_chat(self):
        self.hide()
