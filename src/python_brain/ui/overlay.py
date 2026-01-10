# overlay.py
from PyQt6.QtWidgets import QMainWindow, QLabel, QApplication, QFrame, QVBoxLayout, QHBoxLayout, QPushButton, QGraphicsDropShadowEffect
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QColor

class OverlayWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # TEAM C CONTRACT: Frameless, Topmost, Transparent, Tool (not in taskbar)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool |
            Qt.WindowType.WindowDoesNotAcceptFocus
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)

        # Main Container (The Card)
        self.card_frame = QFrame(self)
        self.card_frame.setObjectName("SuggestionCard")
        self.card_frame.setStyleSheet("""
            QFrame#SuggestionCard {
                background-color: #FFFFFF;
                border: 1px solid #E0E0E0;
                border-radius: 12px;
            }
        """)
        
        # Drop Shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 4)
        self.card_frame.setGraphicsEffect(shadow)
        
        # Layouts
        layout = QVBoxLayout(self.card_frame)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)
        
        # Header (Title + Logo placeholder)
        header_layout = QHBoxLayout()
        title_label = QLabel("FRAI SUGGESTION")
        title_label.setStyleSheet("color: #FF5A1F; font-weight: bold; font-size: 10px; letter-spacing: 1px;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        layout.addLayout(header_layout)
        
        # Suggestion Text
        self.suggestion_label = QLabel()
        self.suggestion_label.setStyleSheet("color: #1A1A1A; font-family: 'Segoe UI', sans-serif; font-size: 14px; font-weight: 500;")
        self.suggestion_label.setWordWrap(True)
        layout.addWidget(self.suggestion_label)
        
        # Action Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)
        
        self.accept_btn = QPushButton("Tab Accept")
        self.accept_btn.setStyleSheet("""
            QPushButton {
                background-color: #F5F5F5;
                color: #555555;
                border: none;
                border-radius: 4px;
                padding: 4px 8px;
                font-size: 10px;
                font-weight: 600;
            }
        """)
        
        self.dismiss_btn = QPushButton("Esc Dismiss")
        self.dismiss_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #999999;
                border: none;
                padding: 4px 8px;
                font-size: 10px;
            }
        """)
        
        btn_layout.addWidget(self.accept_btn)
        btn_layout.addWidget(self.dismiss_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        self.card_frame.hide()
        
        # Determine screen geometry
        screen = QApplication.primaryScreen()
        if screen:
            self.setGeometry(screen.geometry())
        else:
            self.resize(1920, 1080)

    def update_state(self, x: int, y: int, text: str, visible: bool):
        """
        Update the overlay state based on physical coordinates.
        """
        if not visible or not text:
            self.card_frame.hide()
            return
            
        self.suggestion_label.setText(text)
        
        # Adjust size based on content
        self.card_frame.adjustSize()
        
        # Move card to (x, y). 
        # Offset slightly to not block the exact cursor position (improving visibility)
        # Assuming y is the bottom of the caret.
        self.card_frame.move(x, y + 25) 
        self.card_frame.show()
