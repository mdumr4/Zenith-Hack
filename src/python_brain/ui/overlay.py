# overlay.py
from PyQt6.QtWidgets import (QMainWindow, QLabel, QApplication, QFrame, QVBoxLayout, 
                             QHBoxLayout, QGraphicsDropShadowEffect, QWidget, QPushButton)
from PyQt6.QtCore import Qt, QPoint, QPropertyAnimation, QEasingCurve, QRect, QParallelAnimationGroup, pyqtProperty
from PyQt6.QtGui import QColor, QFont, QPalette, QCursor

# --- THEME PALETTE ---
COLOR_ACCENT = "#FF5A1F"       
COLOR_BG_CARD = "#FFFFFF"      
COLOR_BORDER_CARD = "#E4E4E7"  
COLOR_TEXT_MAIN = "#09090B"    
COLOR_TEXT_SUB = "#71717A"     
COLOR_KEY_HINT = "#A1A1AA"
COLOR_BG_BTN_HOVER = "#F4F4F5"

class AutotypeCard(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("AutotypeCard")
        self.setStyleSheet(f"""
            QFrame#AutotypeCard {{
                background-color: rgba(255, 255, 255, 250);
                border: 1px solid {COLOR_BORDER_CARD};
                border-radius: 12px;
            }}
        """)
        
        # Soft, Diffuse Shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(24)
        shadow.setColor(QColor(0, 0, 0, 16))
        shadow.setOffset(0, 8)
        self.setGraphicsEffect(shadow)

        # Layout: Vertical (Header | Text)
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(16, 10, 12, 14) # Top, Right, Bottom, Left
        self.main_layout.setSpacing(8)

        # --- 1. Header Row: [AUTOTYPE ... Insert X] ---
        header_layout = QHBoxLayout()
        header_layout.setSpacing(10)
        
        # Brand Label
        self.lbl_brand = QLabel("Autotype")
        self.lbl_brand.setStyleSheet(f"color: {COLOR_KEY_HINT}; font-weight: 700; font-size: 10px; font-family: 'Segoe UI'; letter-spacing: 0.8px; text-transform: uppercase;")
        header_layout.addWidget(self.lbl_brand)
        
        header_layout.addStretch()
        
        # Insert Button: Soft Zenith Orange Pill
        self.btn_insert = QPushButton("Insert")
        self.btn_insert.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_insert.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_ACCENT}; 
                color: #FFFFFF;
                border: none;
                border-radius: 10px; /* Pill shape */
                padding: 4px 12px;
                font-family: 'Segoe UI';
                font-size: 12px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: #E04812;
            }}
        """)
        
        # Dismiss Button (X): Minimal Grey
        self.btn_dismiss = QPushButton("✕")
        self.btn_dismiss.setFixedSize(20, 20)
        self.btn_dismiss.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_dismiss.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {COLOR_KEY_HINT};
                border: none;
                border-radius: 10px;
                font-size: 11px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {COLOR_BG_BTN_HOVER};
                color: {COLOR_TEXT_MAIN};
            }}
        """)
        
        header_layout.addWidget(self.btn_insert)
        header_layout.addWidget(self.btn_dismiss)
        
        self.main_layout.addLayout(header_layout)

        # --- 2. Suggestion Text ---
        # Main focus, below header
        self.lbl_text = QLabel()
        self.lbl_text.setWordWrap(True)
        self.lbl_text.setStyleSheet(f"color: {COLOR_TEXT_MAIN}; font-weight: 400; font-size: 15px; font-family: 'Segoe UI'; line-height: 1.5; padding-top: 2px;")
        self.main_layout.addWidget(self.lbl_text)

class OverlayWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool |
            Qt.WindowType.WindowDoesNotAcceptFocus
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)

        self.container = QWidget(self)
        self.setCentralWidget(self.container)
        
        self.card = AutotypeCard(self.container)
        self.card.hide()
        
        self.card.btn_insert.clicked.connect(self.on_insert)
        self.card.btn_dismiss.clicked.connect(self.fade_out)
        
        self._opacity = 0.0
        self.anim_group = QParallelAnimationGroup()

    @pyqtProperty(float)
    def opacity(self): return self._opacity
    @opacity.setter
    def opacity(self, value): self._opacity = value; self.setWindowOpacity(value)
    
    def on_insert(self):
        # Insert logic placeholder
        self.fade_out()

    def update_state(self, x: int, y: int, text: str, visible: bool):
        if not visible or not text:
            if self.isVisible(): self.fade_out()
            return
            
        self.card.lbl_text.setText(text)
        self.card.adjustSize()
        self.card.show()
        
        padding_y = 12
        screen = QApplication.primaryScreen()
        screen_geo = screen.geometry()
        
        card_w = self.card.width()
        
        final_x = min(x, screen_geo.width() - card_w - 20)
        final_y = y + padding_y
        
        margin = 30
        self.setGeometry(final_x - margin, final_y - margin, self.card.width() + 2*margin, self.card.height() + 2*margin)
        self.card.move(margin, margin)
        
        if not self.isVisible() or self.windowOpacity() == 0:
            self.show()
            self.fade_in()

    def fade_in(self):
        self.anim_group.clear()
        
        anim_op = QPropertyAnimation(self, b"opacity")
        anim_op.setDuration(300) 
        anim_op.setStartValue(0.0)
        anim_op.setEndValue(1.0)
        anim_op.setEasingCurve(QEasingCurve.Type.OutQuad)
        
        start_pos = self.card.pos() + QPoint(0, 15)
        end_pos = self.card.pos()
        
        anim_move = QPropertyAnimation(self.card, b"pos")
        anim_move.setDuration(400)
        anim_move.setStartValue(start_pos)
        anim_move.setEndValue(end_pos)
        anim_move.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        self.anim_group.addAnimation(anim_op)
        self.anim_group.addAnimation(anim_move)
        self.anim_group.start()

    def fade_out(self):
        self.anim_group.clear()
        
        anim_op = QPropertyAnimation(self, b"opacity")
        anim_op.setDuration(200)
        anim_op.setStartValue(self.windowOpacity())
        anim_op.setEndValue(0.0)
        anim_op.setEasingCurve(QEasingCurve.Type.InQuad)
        
        anim_op.finished.connect(self.hide)
        self.anim_group.addAnimation(anim_op)
        self.anim_group.start()
