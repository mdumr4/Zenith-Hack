# chat_window.py
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QFrame, QGraphicsDropShadowEffect, QLineEdit, QPushButton, 
                             QStackedWidget, QScrollArea, QSizePolicy, QAbstractButton)
from PyQt6.QtCore import Qt, QPoint, QPropertyAnimation, QEasingCurve, QRect, QTimer, pyqtSignal, QSize, QParallelAnimationGroup, QAbstractAnimation, pyqtProperty
from PyQt6.QtGui import QColor, QPainter, QPen, QBrush, QCursor, QLinearGradient, QPolygonF, QPainterPath, QAction, QKeySequence

# --- THEME PALETTE (PRODUCTION) ---
COLOR_ACCENT = "#FF5A1F"       
COLOR_BG_APP = "#F7F7F8"       
COLOR_BG_CARD = "#FFFFFF"      
COLOR_BORDER_CARD = "#E6E6E9"  
COLOR_BG_HOVER = "#F2F3F6"     
COLOR_BORDER_HOVER = "#D1D5DB" 
COLOR_TEXT_MAIN = "#111111"    
COLOR_TEXT_SUB = "#6B7280"     

class PremiumShadow(QGraphicsDropShadowEffect):
    def __init__(self, blur=40, offset=8, opacity=0.04):
        super().__init__()
        self.setBlurRadius(blur)
        self.setOffset(0, offset)
        self.setColor(QColor(0, 0, 0, int(255 * opacity)))

class AnimButton(QAbstractButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._hover_progress = 0.0
        self._press_progress = 0.0
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    @pyqtProperty(float)
    def hoverProgress(self):
        return self._hover_progress

    @hoverProgress.setter
    def hoverProgress(self, value):
        self._hover_progress = value
        self.update()

    @pyqtProperty(float)
    def pressProgress(self):
        return self._press_progress
    
    @pressProgress.setter
    def pressProgress(self, value):
        self._press_progress = value
        self.update()

    def enterEvent(self, event):
        self.anim_hover = QPropertyAnimation(self, b"hoverProgress")
        self.anim_hover.setStartValue(self._hover_progress)
        self.anim_hover.setEndValue(1.0)
        self.anim_hover.setDuration(150)
        self.anim_hover.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.anim_hover = QPropertyAnimation(self, b"hoverProgress")
        self.anim_hover.setStartValue(self._hover_progress)
        self.anim_hover.setEndValue(0.0)
        self.anim_hover.setDuration(150)
        self.anim_hover.start()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        self.anim_press = QPropertyAnimation(self, b"pressProgress")
        self.anim_press.setStartValue(self._press_progress)
        self.anim_press.setEndValue(1.0)
        self.anim_press.setDuration(50)
        self.anim_press.start()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.anim_press = QPropertyAnimation(self, b"pressProgress")
        self.anim_press.setStartValue(self._press_progress)
        self.anim_press.setEndValue(0.0)
        self.anim_press.setDuration(150)
        self.anim_press.start()
        super().mouseReleaseEvent(event)

class CloseBtn(AnimButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(32, 32)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        bg_alpha = int(0 + (self._hover_progress * 20) + (self._press_progress * 30))
        bg_color = QColor(0, 0, 0, bg_alpha)
        
        painter.setBrush(QBrush(bg_color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 10, 10) 
        
        c1 = QColor(COLOR_TEXT_SUB)
        c2 = QColor(COLOR_TEXT_MAIN)
        c3 = QColor(COLOR_ACCENT) 
        
        r = c1.red() + (c2.red() - c1.red()) * self._hover_progress
        g = c1.green() + (c2.green() - c1.green()) * self._hover_progress
        b = c1.blue() + (c2.blue() - c1.blue()) * self._hover_progress
        
        if self._press_progress > 0:
             r = r + (c3.red() - r) * self._press_progress
             g = g + (c3.green() - g) * self._press_progress
             b = b + (c3.blue() - b) * self._press_progress

        pen = QPen(QColor(int(r), int(g), int(b)))
        pen.setWidthF(2.0)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        
        margin = 10
        painter.drawLine(margin, margin, self.width()-margin, self.height()-margin)
        painter.drawLine(self.width()-margin, margin, margin, self.height()-margin)

class ArrowBtn(AnimButton):
    def __init__(self, direction="right", parent=None):
        super().__init__(parent)
        self.direction = direction
        self.setFixedSize(36, 36) 
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        bg_alpha = int(0 + (self._hover_progress * 20) + (self._press_progress * 30))
        bg_color = QColor(0, 0, 0, bg_alpha)
        
        painter.setBrush(QBrush(bg_color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 18, 18) 
        
        c1 = QColor(COLOR_TEXT_SUB)
        c2 = QColor(COLOR_TEXT_MAIN)
        c3 = QColor(COLOR_ACCENT) 
        
        r = c1.red() + (c2.red() - c1.red()) * self._hover_progress
        g = c1.green() + (c2.green() - c1.green()) * self._hover_progress
        b = c1.blue() + (c2.blue() - c1.blue()) * self._hover_progress
        
        if self._press_progress > 0:
             r = r + (c3.red() - r) * self._press_progress
             g = g + (c3.green() - g) * self._press_progress
             b = b + (c3.blue() - b) * self._press_progress
             
        pen = QPen(QColor(int(r), int(g), int(b)))
        pen.setWidthF(2.0)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        
        mid_y = 18
        path = QPainterPath()
        if self.direction == "right": 
            path.moveTo(11, mid_y)
            path.lineTo(25, mid_y)
            path.moveTo(25 - 5, mid_y - 5)
            path.lineTo(25, mid_y)
            path.lineTo(25 - 5, mid_y + 5)
        else: 
            path.moveTo(25, mid_y)
            path.lineTo(11, mid_y)
            path.moveTo(11 + 5, mid_y - 5)
            path.lineTo(11, mid_y)
            path.lineTo(11 + 5, mid_y + 5)
        painter.drawPath(path)

class RoundedPillBtn(QFrame):
    clicked = pyqtSignal()
    def __init__(self, icon_char, text, subtext=""):
        super().__init__()
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setFixedHeight(68)
        self.setObjectName("PillBtn")
        self.is_hovered = False
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(24, 0, 24, 0)
        layout.setSpacing(16)
        
        self.icon_lbl = QLabel(icon_char) 
        self.icon_lbl.setStyleSheet(f"border: none; background: transparent; font-size: 18px; color: {COLOR_TEXT_SUB};")
        layout.addWidget(self.icon_lbl)
        
        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)
        text_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        
        self.t_lbl = QLabel(text)
        self.t_lbl.setStyleSheet(f"border: none; background: transparent; font-family: 'Segoe UI'; font-size: 15px; font-weight: 500; color: {COLOR_TEXT_MAIN};")
        text_layout.addWidget(self.t_lbl)
        if subtext:
             s_lbl = QLabel(subtext)
             s_lbl.setStyleSheet(f"border: none; background: transparent; font-family: 'Segoe UI'; font-size: 13px; color: {COLOR_TEXT_SUB};")
             text_layout.addWidget(s_lbl)
        layout.addLayout(text_layout)
        layout.addStretch()
        self.update_style()

    def update_style(self):
        if self.is_hovered:
            self.setStyleSheet(f"""
                QFrame#PillBtn {{
                    background-color: {COLOR_BG_HOVER};
                    border: 1px solid {COLOR_BORDER_HOVER};
                    border-radius: 34px;
                }}
            """)
            self.icon_lbl.setStyleSheet(f"border: none; background: transparent; font-size: 18px; color: {COLOR_TEXT_MAIN};")
        else:
            self.setStyleSheet(f"""
                QFrame#PillBtn {{
                    background-color: {COLOR_BG_CARD};
                    border: 1px solid {COLOR_BORDER_CARD};
                    border-radius: 34px;
                }}
            """)
            self.icon_lbl.setStyleSheet(f"border: none; background: transparent; font-size: 18px; color: {COLOR_TEXT_SUB};")

    def enterEvent(self, event):
        self.is_hovered = True
        self.update_style()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.is_hovered = False
        self.update_style()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()

class CommandInput(QFrame):
    submitted = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.setFixedHeight(60) 
        self.setObjectName("CommandInput")
        self.is_focused = False
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 4, 12, 4) 
        layout.setSpacing(10)
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Tell the AI what you want...")
        self.input_field.setStyleSheet(f"""
            QLineEdit {{
                border: none;
                background: transparent;
                font-family: 'Segoe UI';
                font-size: 15px;
                color: {COLOR_TEXT_MAIN};
            }}
        """)
        self.input_field.focusInEvent = self.on_focus_in
        self.input_field.focusOutEvent = self.on_focus_out
        self.input_field.returnPressed.connect(self.handle_submit)
        self.input_field.textChanged.connect(self.on_text_changed)
        
        layout.addWidget(self.input_field)
        
        self.btn_arrow = ArrowBtn(direction="right")
        self.btn_arrow.clicked.connect(self.handle_submit)
        layout.addWidget(self.btn_arrow)
        
        self.update_container_style()

    def update_container_style(self):
        if self.is_focused:
            self.setStyleSheet(f"""
                QFrame#CommandInput {{
                    background-color: {COLOR_BG_CARD};
                    border: 2px solid {COLOR_ACCENT}; 
                    border-radius: 30px;
                }}
            """)
        else:
             self.setStyleSheet(f"""
                QFrame#CommandInput {{
                    background-color: {COLOR_BG_CARD};
                    border: 1px solid {COLOR_BORDER_CARD};
                    border-radius: 30px;
                }}
                QFrame#CommandInput:hover {{
                     border: 1px solid {COLOR_BORDER_HOVER};
                     background-color: {COLOR_BG_CARD};
                }}
            """)

    def on_focus_in(self, event):
        self.is_focused = True
        self.update_container_style()
        QLineEdit.focusInEvent(self.input_field, event)

    def on_focus_out(self, event):
        self.is_focused = False
        self.update_container_style()
        QLineEdit.focusOutEvent(self.input_field, event)
        
    def on_text_changed(self, text):
        if not self.is_focused:
             self.is_focused = True
             self.update_container_style()

    def handle_submit(self):
        text = self.input_field.text().strip()
        if text:
            self.submitted.emit(text)
            self.input_field.clear()

class TypewriterLabel(QLabel):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.full_text = text
        self.current_idx = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.add_char)
        self.setText("")

    def start_typing(self, text):
        self.full_text = text
        self.current_idx = 0
        self.setText("")
        self.timer.start(15) 

    def add_char(self):
        if self.current_idx < len(self.full_text):
            self.setText(self.full_text[:self.current_idx+1])
            self.current_idx += 1
        else:
            self.timer.stop()

class ProStackedWidget(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.animation_group = None

    def push_next(self):
        current_idx = self.currentIndex()
        next_idx = 1
        if current_idx == next_idx: return

        current_widget = self.widget(current_idx)
        next_widget = self.widget(next_idx)
        
        width = self.width()
        next_widget.setGeometry(QRect(width, 0, width, self.height()))
        next_widget.show()
        next_widget.raise_() 
        
        self.animation_group = QParallelAnimationGroup()
        anim_curr = QPropertyAnimation(current_widget, b"pos")
        anim_curr.setDuration(500)
        anim_curr.setStartValue(QPoint(0, 0))
        anim_curr.setEndValue(QPoint(-width, 0))
        anim_curr.setEasingCurve(QEasingCurve.Type.OutCubic)

        anim_next = QPropertyAnimation(next_widget, b"pos")
        anim_next.setDuration(500)
        anim_next.setStartValue(QPoint(width, 0))
        anim_next.setEndValue(QPoint(0, 0))
        anim_next.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        self.animation_group.addAnimation(anim_curr)
        self.animation_group.addAnimation(anim_next)
        self.animation_group.finished.connect(lambda: self.on_push_finished(next_idx))
        self.animation_group.start()

    def push_prev(self):
        current_idx = self.currentIndex()
        prev_idx = 0
        if current_idx == prev_idx: return

        current_widget = self.widget(current_idx)
        prev_widget = self.widget(prev_idx)
        
        width = self.width()
        prev_widget.setGeometry(QRect(-width, 0, width, self.height()))
        prev_widget.show()
        prev_widget.raise_()
        
        self.animation_group = QParallelAnimationGroup()
        anim_curr = QPropertyAnimation(current_widget, b"pos")
        anim_curr.setDuration(500)
        anim_curr.setStartValue(QPoint(0, 0))
        anim_curr.setEndValue(QPoint(width, 0))
        anim_curr.setEasingCurve(QEasingCurve.Type.OutCubic)

        anim_prev = QPropertyAnimation(prev_widget, b"pos")
        anim_prev.setDuration(500)
        anim_prev.setStartValue(QPoint(-width, 0))
        anim_prev.setEndValue(QPoint(0, 0))
        anim_prev.setEasingCurve(QEasingCurve.Type.OutCubic)

        self.animation_group.addAnimation(anim_curr)
        self.animation_group.addAnimation(anim_prev)
        self.animation_group.finished.connect(lambda: self.on_push_finished(prev_idx))
        self.animation_group.start()

    def on_push_finished(self, idx):
        self.setCurrentIndex(idx)
        for i in range(self.count()):
            w = self.widget(i)
            if i == idx:
                w.move(0, 0)
            else:
                w.hide()

class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(380, 560) 
        self.dragging = False
        self.offset = QPoint()
        
        self.central_frame = QFrame()
        self.central_frame.setStyleSheet(f"QFrame {{ background-color: {COLOR_BG_APP}; border-radius: 20px; border: 1px solid {COLOR_BORDER_CARD}; }}")
        self.setCentralWidget(self.central_frame)
        self.central_frame.setGraphicsEffect(PremiumShadow(blur=40, offset=12, opacity=0.08))
        
        self.main_layout = QVBoxLayout(self.central_frame)
        self.main_layout.setContentsMargins(28, 28, 28, 28)
        self.main_layout.setSpacing(24) 
        
        # --- Header ---
        header = QWidget()
        header.setStyleSheet("background: transparent; border: none;")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        brand_box = QVBoxLayout()
        brand_box.setSpacing(2)
        title = QLabel("AI Keyboard")
        title.setStyleSheet(f"color: {COLOR_ACCENT}; font-weight: 700; font-size: 16px; font-family: 'Segoe UI';")
        sub = QLabel("Plan mode")
        sub.setStyleSheet(f"color: {COLOR_TEXT_SUB}; font-weight: 400; font-size: 13px; font-family: 'Segoe UI';")
        brand_box.addWidget(title)
        brand_box.addWidget(sub)
        header_layout.addLayout(brand_box)
        
        header_layout.addStretch()
        
        # CUSTOM BACK BTN (LEFT)
        self.btn_back = ArrowBtn(direction="left")
        self.btn_back.clicked.connect(self.go_back)
        self.btn_back.hide()
        header_layout.addWidget(self.btn_back)
        
        # CUSTOM CLOSE BTN
        self.btn_close = CloseBtn()
        self.btn_close.clicked.connect(self.hide_chat) # WIRED TO HIDE
        header_layout.addWidget(self.btn_close)
        
        self.main_layout.addWidget(header)
        
        # --- Stack ---
        self.stack = ProStackedWidget() 
        self.stack.setStyleSheet("background: transparent; border: none;")
        
        # PAGE 1: Options
        self.page_options = QWidget()
        opt_layout = QVBoxLayout(self.page_options)
        opt_layout.setContentsMargins(0, 4, 0, 4)
        opt_layout.setSpacing(16)
        
        btn_1 = RoundedPillBtn("✎", "Rewrite", "Improve grammar and tone")
        btn_2 = RoundedPillBtn("📝", "Summarize", "Get the key points")
        btn_3 = RoundedPillBtn("💡", "Explain", "Make this easier to understand")
        
        btn_1.clicked.connect(lambda: self.go_chat("Rewrite"))
        btn_2.clicked.connect(lambda: self.go_chat("Summarize"))
        btn_3.clicked.connect(lambda: self.go_chat("Explain"))
        
        opt_layout.addWidget(btn_1)
        opt_layout.addWidget(btn_2)
        opt_layout.addWidget(btn_3)
        opt_layout.addStretch()
        
        self.smart_input = CommandInput()
        self.smart_input.submitted.connect(self.go_chat) 
        opt_layout.addWidget(self.smart_input)
        
        self.stack.addWidget(self.page_options)
        
        # PAGE 2: Chat Layout
        self.page_chat = QWidget()
        chat_layout = QVBoxLayout(self.page_chat)
        chat_layout.setContentsMargins(0, 10, 0, 10)
        chat_layout.setSpacing(16)
        chat_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.user_bubble_container = QHBoxLayout()
        self.user_bubble_container.addStretch()
        self.user_bubble = QLabel("")
        self.user_bubble.setFixedHeight(48)
        self.user_bubble.setStyleSheet(f"""
            padding: 0 20px;
            background-color: {COLOR_BG_CARD}; 
            color: {COLOR_TEXT_MAIN};
            border: 1px solid {COLOR_BORDER_CARD};
            border-radius: 24px;
            font-family: 'Segoe UI';
        """)
        self.user_bubble_container.addWidget(self.user_bubble)
        chat_layout.addLayout(self.user_bubble_container)
        
        self.ai_surface = QFrame()
        self.ai_surface.setStyleSheet(f"""
            QFrame {{
                background-color: {COLOR_BG_CARD};
                border: 1px solid {COLOR_BORDER_CARD};
                border-radius: 32px;
            }}
        """)
        ai_layout = QVBoxLayout(self.ai_surface)
        ai_layout.setContentsMargins(24, 24, 24, 24)
        
        self.ai_text = TypewriterLabel("Typing...")
        self.ai_text.setWordWrap(True)
        self.ai_text.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.ai_text.setStyleSheet(f"border: none; font-size: 15px; line-height: 1.5; color: {COLOR_TEXT_MAIN};")
        ai_layout.addWidget(self.ai_text)
        
        chat_layout.addWidget(self.ai_surface)
        
        self.stack.addWidget(self.page_chat)
        
        self.main_layout.addWidget(self.stack)
        
        # Keyboard Shortcut
        self.toggle_action = QAction("Toggle Plan Mode", self)
        self.toggle_action.setShortcut(QKeySequence("Ctrl+K"))
        self.toggle_action.triggered.connect(self.toggle_visibility)
        self.addAction(self.toggle_action)

        self.center_on_screen()
        self.hide() # Start hidden

    def go_chat(self, action):
        displayText = action if len(action) < 30 else action[:28] + "..."
        if "Rewrite" in action: displayText = "Rewrite this content."
        elif "Summarize" in action: displayText = "Summarize this."
        elif "Explain" in action: displayText = "Explain this."
        
        self.user_bubble.setText(displayText)
        self.ai_text.setText("Thinking...")
        
        self.stack.push_next() 
        self.btn_back.show()
        
        QTimer.singleShot(600, lambda: self.ai_text.start_typing("This is a placeholder for the actual AI response from the backend. The UI is now fully polished."))

    def go_back(self):
        self.stack.push_prev() 
        self.btn_back.hide()
        self.smart_input.input_field.setFocus()

    def center_on_screen(self):
        screen = self.screen().geometry()
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
        self.smart_input.input_field.setFocus()

    def toggle_visibility(self):
        if self.isVisible():
            self.hide_chat()
        else:
            self.show_chat()

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