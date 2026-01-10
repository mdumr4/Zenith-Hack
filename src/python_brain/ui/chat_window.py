# chat_window.py
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QFrame, QGraphicsDropShadowEffect, QLineEdit, QPushButton)
from PyQt6.QtCore import Qt, QPoint, QPropertyAnimation, QEasingCurve, QRect
from PyQt6.QtGui import QColor, QPainter, QPen, QBrush, QCursor, QLinearGradient, QAction, QKeySequence

class VectorIcon(QWidget):
    """Custom widget to draw soft, friendly vector-style icons"""
    def __init__(self, icon_type, color_hex):
        super().__init__()
        self.setFixedSize(36, 36)
        self.icon_type = icon_type
        self.color = QColor(color_hex)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Soft Gradient Background
        grad = QLinearGradient(0, 0, 36, 36)
        grad.setColorAt(0, QColor(self.color.red(), self.color.green(), self.color.blue(), 20))
        grad.setColorAt(1, QColor(self.color.red(), self.color.green(), self.color.blue(), 10))
        
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(grad))
        painter.drawEllipse(0, 0, 36, 36)
        
        # Draw Icon Shape (Thicker, softer lines)
        pen = QPen(self.color, 2.5)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        
        if self.icon_type == "rewrite": 
            painter.drawLine(12, 24, 24, 12)
            painter.drawPoint(10, 26) 
            painter.drawPoint(26, 10)
        elif self.icon_type == "summarize": 
            painter.drawRoundedRect(10, 10, 16, 6, 2, 2)
            painter.drawRoundedRect(10, 18, 16, 6, 2, 2)
            painter.drawRoundedRect(10, 26, 10, 2, 1, 1)
        elif self.icon_type == "explain":
            painter.drawEllipse(13, 9, 10, 10)
            painter.drawLine(18, 19, 18, 23)
            painter.drawLine(16, 23, 20, 23)

class ActionCard(QFrame):
    def __init__(self, icon_type, title, subtitle, color_hex):
        super().__init__()
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setObjectName("ActionCard")
        self.color_hex = color_hex
        
        self.setStyleSheet(f"""
            QFrame#ActionCard {{
                background-color: #FFFFFF;
                border: 1px solid #F2F2F2;
                border-radius: 16px;
            }}
            QFrame#ActionCard:hover {{
                background-color: #FDFAFF;
                border: 1px solid {color_hex}40;
            }}
        """)
        self.setFixedHeight(72)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 14, 20, 14)
        layout.setSpacing(18)
        
        # Vector Icon
        icon = VectorIcon(icon_type, color_hex)
        layout.addWidget(icon)
        
        # Text Group
        text_layout = QVBoxLayout()
        text_layout.setSpacing(3)
        text_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        
        title_lbl = QLabel(title)
        title_lbl.setStyleSheet("font-family: 'Segoe UI'; font-size: 15px; font-weight: 700; color: #2D2D2D; border: none; background: transparent;")
        
        sub_lbl = QLabel(subtitle)
        sub_lbl.setStyleSheet("font-family: 'Segoe UI'; font-size: 12px; color: #757575; border: none; background: transparent;")
        
        text_layout.addWidget(title_lbl)
        text_layout.addWidget(sub_lbl)
        layout.addLayout(text_layout)
        
        layout.addStretch()
        
        # Chevron
        chev = QLabel("›")
        chev.setStyleSheet("color: #E0E0E0; font-size: 20px; font-weight: 300; border: none; background: transparent;")
        layout.addWidget(chev)

class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Window Setup
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(380, 520) 
        
        # Draggable State
        self.dragging = False
        self.offset = QPoint()
        
        # Main Card (Container)
        self.central_frame = QFrame()
        self.central_frame.setStyleSheet("""
            QFrame {
                background-color: #FCFCFC; 
                border-radius: 20px;
                border: 1px solid #EAEAEA;
            }
        """)
        self.setCentralWidget(self.central_frame)
        
        # Premium Shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(50)
        shadow.setColor(QColor(0, 0, 0, 35))
        shadow.setOffset(0, 15)
        self.central_frame.setGraphicsEffect(shadow)
        
        # Main Layout
        self.layout = QVBoxLayout(self.central_frame)
        self.layout.setContentsMargins(28, 28, 28, 28)
        self.layout.setSpacing(16)
        
        # --- HEADER ---
        header_container = QWidget()
        header_layout = QHBoxLayout(header_container)
        header_layout.setContentsMargins(0, 0, 0, 12)
        header_layout.setSpacing(12)
        
        # Title Group
        title_group = QVBoxLayout()
        title_group.setSpacing(2)
        
        brand = QLabel("AI Keyboard")
        brand.setStyleSheet("color: #FF5A1F; font-weight: 800; font-size: 16px; font-family: 'Segoe UI'; letter-spacing: 0.5px; border: none;")
        
        title_sub = QLabel("Plan Mode")
        title_sub.setStyleSheet("color: #999999; font-weight: 500; font-size: 12px; font-family: 'Segoe UI'; border: none;")
        
        title_group.addWidget(brand)
        title_group.addWidget(title_sub)
        
        header_layout.addLayout(title_group)
        header_layout.addStretch()
        
        # Close Button
        self.close_btn = QPushButton("×")
        self.close_btn.setFixedSize(32, 32)
        self.close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.close_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #CCCCCC;
                font-size: 24px;
                border: none;
                font-weight: 300;
                padding-bottom: 4px;
            }
            QPushButton:hover {
                color: #FF5A1F;
                background-color: #F8F8F8;
                border-radius: 16px;
            }
        """)
        self.close_btn.clicked.connect(self.hide_chat)
        header_layout.addWidget(self.close_btn)
        
        self.layout.addWidget(header_container)
        
        # --- CARDS ---
        self.layout.addWidget(ActionCard("rewrite", "Rewrite", "Improve grammar and tone", "#FF5A1F"))
        self.layout.addWidget(ActionCard("summarize", "Summarize", "Get the key points", "#5E35B1"))
        self.layout.addWidget(ActionCard("explain", "Explain", "Make this easier to understand", "#00BFA5"))
        
        self.layout.addStretch()
        
        # --- INPUT ---
        self.input = QLineEdit()
        self.input.setPlaceholderText("Tell the AI what you want...")
        self.input.setFixedHeight(56) 
        self.input.setStyleSheet("""
            QLineEdit {
                background-color: #FFFFFF;
                border: 1px solid #E8E8E8;
                border-radius: 14px;
                padding-left: 18px;
                padding-right: 18px;
                font-family: 'Segoe UI';
                font-size: 15px;
                color: #333333;
            }
            QLineEdit:focus {
                border: 1px solid #FF5A1F;
                background-color: #FFFFFF;
                color: #000000;
            }
        """)
        # Input Shadow
        input_shadow = QGraphicsDropShadowEffect()
        input_shadow.setBlurRadius(15)
        input_shadow.setColor(QColor(0,0,0,8)) 
        input_shadow.setOffset(0, 4)
        self.input.setGraphicsEffect(input_shadow)
        
        self.layout.addWidget(self.input)

        # Center + Animate
        self.center_on_screen()
        # self.animate_entry() # Only animate on show()
        self.hide()

        # Keyboard Shortcut (Ctrl+K to toggle)
        self.toggle_action = QAction("Toggle Plan Mode", self)
        self.toggle_action.setShortcut(QKeySequence("Ctrl+K"))
        self.toggle_action.triggered.connect(self.toggle_visibility)
        self.addAction(self.toggle_action)

    def center_on_screen(self):
        screen = self.screen().geometry() # Use self.screen() for multi-monitor correctness
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)
        
    def animate_entry(self):
        self.setWindowOpacity(0)
        self.anim_opacity = QPropertyAnimation(self, b"windowOpacity")
        self.anim_opacity.setDuration(450)
        self.anim_opacity.setStartValue(0)
        self.anim_opacity.setEndValue(1)
        self.anim_opacity.setEasingCurve(QEasingCurve.Type.OutQuart)
        
        current_geo = self.geometry()
        # Ensure we start from slight offset but end at current position
        target_rect = current_geo
        start_rect = QRect(current_geo.x(), current_geo.y() + 40, current_geo.width(), current_geo.height())
        
        self.anim_geo = QPropertyAnimation(self, b"geometry")
        self.anim_geo.setDuration(500)
        self.anim_geo.setStartValue(start_rect)
        self.anim_geo.setEndValue(target_rect)
        self.anim_geo.setEasingCurve(QEasingCurve.Type.OutQuart)
        
        self.anim_opacity.start()
        self.anim_geo.start()
    
    def hide_chat(self):
        self.hide()
        
    def show_chat(self):
        self.show()
        self.animate_entry()
        self.activateWindow()
        self.input.setFocus()

    def toggle_visibility(self):
        if self.isVisible():
            self.hide_chat()
        else:
            self.show_chat()

    # Draggable Logic
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if event.position().y() < 120: 
                self.dragging = True
                self.offset = event.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(event.globalPosition().toPoint() - self.offset)

    def mouseReleaseEvent(self, event):
        self.dragging = False
