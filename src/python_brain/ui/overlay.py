# overlay.py
from PyQt6.QtWidgets import (QMainWindow, QLabel, QApplication, QFrame, QVBoxLayout, 
                             QHBoxLayout, QGraphicsDropShadowEffect, QWidget)
from PyQt6.QtCore import Qt, QPoint, QPropertyAnimation, QEasingCurve, QRect, QParallelAnimationGroup, pyqtProperty
from PyQt6.QtGui import QColor, QFont, QPalette

# --- THEME PALETTE ---
COLOR_ACCENT = "#FF5A1F"       
COLOR_BG_CARD = "#FFFFFF"      
COLOR_BORDER_CARD = "#E4E4E7"  
COLOR_TEXT_MAIN = "#09090B"    
COLOR_TEXT_SUB = "#71717A"     
COLOR_KEY_HINT = "#A1A1AA"

class AutotypeCard(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("AutotypeCard")
        self.setStyleSheet(f"""
            QFrame#AutotypeCard {{
                background-color: rgba(255, 255, 255, 245);
                border: 1px solid {COLOR_BORDER_CARD};
                border-radius: 16px;
            }}
        """)
        
        # Soft Shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(24)
        shadow.setColor(QColor(0, 0, 0, 20))
        shadow.setOffset(0, 8)
        self.setGraphicsEffect(shadow)

        # Layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(16, 12, 16, 12)
        self.main_layout.setSpacing(6)

        # 1. Header Row (Label + Actions)
        header_layout = QHBoxLayout()
        header_layout.setSpacing(8)
        
        self.lbl_brand = QLabel("Autotype")
        self.lbl_brand.setStyleSheet(f"color: {COLOR_ACCENT}; font-weight: 600; font-size: 11px; font-family: 'Segoe UI'; letter-spacing: 0.5px; text-transform: uppercase;")
        header_layout.addWidget(self.lbl_brand)
        
        header_layout.addStretch()
        
        # Action Hints (Tab / Esc)
        self.lbl_actions = QLabel("Tab to accept  •  Esc to dismiss")
        self.lbl_actions.setStyleSheet(f"color: {COLOR_KEY_HINT}; font-weight: 400; font-size: 11px; font-family: 'Segoe UI';")
        header_layout.addWidget(self.lbl_actions)
        
        self.main_layout.addLayout(header_layout)

        # 2. Suggestion Text
        self.lbl_text = QLabel()
        self.lbl_text.setWordWrap(True)
        self.lbl_text.setStyleSheet(f"color: {COLOR_TEXT_MAIN}; font-weight: 600; font-size: 15px; font-family: 'Segoe UI'; line-height: 1.4;")
        self.main_layout.addWidget(self.lbl_text)

class OverlayWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Frameless, Topmost, Transparent, Tool (not in taskbar)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool |
            Qt.WindowType.WindowDoesNotAcceptFocus
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)

        # Container Widget because QMainWindow needs a central widget
        self.container = QWidget(self)
        self.setCentralWidget(self.container)
        
        # The Card
        self.card = AutotypeCard(self.container)
        self.card.hide()
        
        # Animation Properties
        self._opacity = 0.0
        self.anim_group = QParallelAnimationGroup()

    @pyqtProperty(float)
    def opacity(self):
        return self._opacity

    @opacity.setter
    def opacity(self, value):
        self._opacity = value
        self.setWindowOpacity(value)

    def update_state(self, x: int, y: int, text: str, visible: bool):
        """
        Update the overlay state based on physical coordinates.
        """
        # Minimal validation
        if not visible or not text:
            if self.isVisible():
                self.fade_out()
            return
            
        # Update Text
        self.card.lbl_text.setText(text)
        self.card.adjustSize()
        self.card.show()
        
        # 1. Update Geometry (Position)
        # Anchor just above or below the cursor. 
        # y is typically the bottom of the caret.
        # Let's align top-left of card to (x, y + padding)
        padding_y = 12
        
        # Ensure we don't go off screen (basic check)
        screen = QApplication.primaryScreen()
        screen_geo = screen.geometry()
        
        card_w = self.card.width()
        card_h = self.card.height()
        
        # Final X/Y
        final_x = min(x, screen_geo.width() - card_w - 20)
        final_y = y + padding_y
        
        # If too low, flip to above? (Future improvement)
        
        # Resize window to fit card + shadow margins
        # We make the window larger than the card to clip shadows correctly if needed,
        # but for simplicity, we'll just match size + margins or set window large and move card relative.
        # Actually simpler: Move the Window itself to x,y and let card fill it? 
        # No, card has shadow. Let's make window big enough.
        
        margin = 30
        self.setGeometry(final_x - margin, final_y - margin, card_w + 2*margin, card_h + 2*margin)
        self.card.move(margin, margin)
        
        if not self.isVisible() or self.windowOpacity() == 0:
            self.show()
            self.fade_in()

    def fade_in(self):
        self.anim_group.clear()
        
        # Opacity
        anim_op = QPropertyAnimation(self, b"opacity")
        anim_op.setDuration(200)
        anim_op.setStartValue(0.0)
        anim_op.setEndValue(1.0)
        anim_op.setEasingCurve(QEasingCurve.Type.OutQuad)
        
        # Slide Up/Down (Card position relative to window)
        # Let's slide the card from slightly lower
        start_pos = self.card.pos() + QPoint(0, 10)
        end_pos = self.card.pos()
        
        anim_move = QPropertyAnimation(self.card, b"pos")
        anim_move.setDuration(250)
        anim_move.setStartValue(start_pos)
        anim_move.setEndValue(end_pos)
        anim_move.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        self.anim_group.addAnimation(anim_op)
        self.anim_group.addAnimation(anim_move)
        self.anim_group.start()

    def fade_out(self):
        self.anim_group.clear()
        
        anim_op = QPropertyAnimation(self, b"opacity")
        anim_op.setDuration(150)
        anim_op.setStartValue(self.windowOpacity())
        anim_op.setEndValue(0.0)
        anim_op.setEasingCurve(QEasingCurve.Type.InQuad)
        
        anim_op.finished.connect(self.hide)
        
        self.anim_group.addAnimation(anim_op)
        self.anim_group.start()
