# chat_window.py
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QFrame, QGraphicsDropShadowEffect, QLineEdit, QPushButton, 
                             QStackedWidget, QScrollArea, QSizePolicy, QAbstractButton)
from PyQt6.QtCore import Qt, QPoint, QPropertyAnimation, QEasingCurve, QRect, QTimer, pyqtSignal, QSize, QParallelAnimationGroup, QAbstractAnimation, pyqtProperty
from PyQt6.QtGui import QColor, QPainter, QPen, QBrush, QCursor, QLinearGradient, QPolygonF, QPainterPath, QAction, QKeySequence

# --- THEME PALETTE ---
COLOR_ACCENT = "#FF5A1F"       
COLOR_BG_APP = "#F7F7F8"       
COLOR_BG_CARD = "#FFFFFF"      
COLOR_BORDER_CARD = "#E4E4E7"  # Slightly darker for crispness
COLOR_BG_HOVER = "#F2F3F6"     
COLOR_BORDER_HOVER = "#D4D4D8" 
COLOR_TEXT_MAIN = "#09090B"    # Almost black (Zinc-950) for primary text
COLOR_TEXT_SUB = "#52525B"     # Darker grey (Zinc-600) for readable secondary text

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
    def hoverProgress(self): return self._hover_progress
    @hoverProgress.setter
    def hoverProgress(self, value): self._hover_progress = value; self.update()
    
    @pyqtProperty(float)
    def pressProgress(self): return self._press_progress
    @pressProgress.setter
    def pressProgress(self, value): self._press_progress = value; self.update()

    def enterEvent(self, event):
        self.anim_hover = QPropertyAnimation(self, b"hoverProgress")
        self.anim_hover.setStartValue(self._hover_progress)
        self.anim_hover.setEndValue(1.0); self.anim_hover.setDuration(150); self.anim_hover.start()
        super().enterEvent(event)
    def leaveEvent(self, event):
        self.anim_hover = QPropertyAnimation(self, b"hoverProgress")
        self.anim_hover.setStartValue(self._hover_progress)
        self.anim_hover.setEndValue(0.0); self.anim_hover.setDuration(150); self.anim_hover.start()
        super().leaveEvent(event)
    def mousePressEvent(self, event):
        self.anim_press = QPropertyAnimation(self, b"pressProgress")
        self.anim_press.setStartValue(self._press_progress)
        self.anim_press.setEndValue(1.0); self.anim_press.setDuration(50); self.anim_press.start()
        super().mousePressEvent(event)
    def mouseReleaseEvent(self, event):
        self.anim_press = QPropertyAnimation(self, b"pressProgress")
        self.anim_press.setStartValue(self._press_progress)
        self.anim_press.setEndValue(0.0); self.anim_press.setDuration(150); self.anim_press.start()
        super().mouseReleaseEvent(event)

class CloseBtn(AnimButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(32, 32)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        bg_alpha = int(0 + (self._hover_progress * 20) + (self._press_progress * 30))
        painter.setBrush(QBrush(QColor(0, 0, 0, bg_alpha)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 10, 10) 
        
        c1 = QColor(COLOR_TEXT_SUB); c2 = QColor(COLOR_TEXT_MAIN); c3 = QColor(COLOR_ACCENT) 
        r = c1.red() + (c2.red() - c1.red()) * self._hover_progress
        g = c1.green() + (c2.green() - c1.green()) * self._hover_progress
        b = c1.blue() + (c2.blue() - c1.blue()) * self._hover_progress
        
        if self._press_progress > 0:
             r = r + (c3.red() - r) * self._press_progress
             g = g + (c3.green() - g) * self._press_progress
             b = b + (c3.blue() - b) * self._press_progress

        pen = QPen(QColor(int(r), int(g), int(b))); pen.setWidthF(2.0); pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        painter.drawLine(10, 10, 22, 22); painter.drawLine(22, 10, 10, 22)

class ArrowBtn(AnimButton):
    def __init__(self, direction="right", parent=None):
        super().__init__(parent)
        self.direction = direction
        self.setFixedSize(36, 36) 
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        bg_alpha = int(0 + (self._hover_progress * 20) + (self._press_progress * 30))
        painter.setBrush(QBrush(QColor(0, 0, 0, bg_alpha)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 18, 18) 
        c1 = QColor(COLOR_TEXT_SUB); c2 = QColor(COLOR_TEXT_MAIN); c3 = QColor(COLOR_ACCENT) 
        r = c1.red() + (c2.red() - c1.red()) * self._hover_progress
        g = c1.green() + (c2.green() - c1.green()) * self._hover_progress
        b = c1.blue() + (c2.blue() - c1.blue()) * self._hover_progress
        if self._press_progress > 0:
             r = r + (c3.red() - r) * self._press_progress
             g = g + (c3.green() - g) * self._press_progress
             b = b + (c3.blue() - b) * self._press_progress
        pen = QPen(QColor(int(r), int(g), int(b))); pen.setWidthF(2.0); pen.setCapStyle(Qt.PenCapStyle.RoundCap); pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        mid_y = 18; path = QPainterPath()
        if self.direction == "right": 
            path.moveTo(11, mid_y); path.lineTo(25, mid_y); path.moveTo(25 - 5, mid_y - 5); path.lineTo(25, mid_y); path.lineTo(25 - 5, mid_y + 5)
        else: 
            path.moveTo(25, mid_y); path.lineTo(11, mid_y); path.moveTo(11 + 5, mid_y - 5); path.lineTo(11, mid_y); path.lineTo(11 + 5, mid_y + 5)
        painter.drawPath(path)

class MicBtn(AnimButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(36, 36)
        self._listening = False
        self._pulse_progress = 0.0
        
        self.anim_pulse = QPropertyAnimation(self, b"pulseProgress")
        self.anim_pulse.setDuration(2000)
        self.anim_pulse.setStartValue(0.0)
        self.anim_pulse.setEndValue(1.0)
        self.anim_pulse.setLoopCount(-1) 
        self.anim_pulse.setEasingCurve(QEasingCurve.Type.Linear)

    @pyqtProperty(float)
    def pulseProgress(self): return self._pulse_progress
    @pulseProgress.setter
    def pulseProgress(self, value): self._pulse_progress = value; self.update()

    def setListening(self, active):
        self._listening = active
        if active: self.anim_pulse.start()
        else: self.anim_pulse.stop(); self._pulse_progress = 0.0
        self.update()

    def paintEvent(self, event):
        try:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            bg_alpha = int(0 + (self._hover_progress * 20) + (self._press_progress * 30))
            bg_color = QColor(0, 0, 0, bg_alpha)

            if self._listening:
                painter.setBrush(Qt.BrushStyle.NoBrush)
                center = QPointF(18.0, 18.0)
                p1 = self._pulse_progress; alpha1 = int((1.0 - p1) * 120); r1 = 14 + (p1 * 10)
                color1 = QColor(COLOR_ACCENT); color1.setAlpha(alpha1)
                pen1 = QPen(color1); pen1.setWidthF(1.5); painter.setPen(pen1); painter.drawEllipse(center, r1, r1)
                p2 = (self._pulse_progress + 0.5) % 1.0; alpha2 = int((1.0 - p2) * 120); r2 = 14 + (p2 * 10)
                color2 = QColor(COLOR_ACCENT); color2.setAlpha(alpha2)
                pen2 = QPen(color2); pen2.setWidthF(1.5); painter.setPen(pen2); painter.drawEllipse(center, r2, r2)
                bg_color = QColor(COLOR_ACCENT); bg_color.setAlpha(30)

            painter.setBrush(QBrush(bg_color)); painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect(), 18, 18)
            
            c_icon = QColor(COLOR_TEXT_SUB)
            if self._hover_progress > 0.1: c_icon = QColor(COLOR_TEXT_MAIN)
            if self._listening: c_icon = QColor(COLOR_ACCENT)

            pen = QPen(c_icon); pen.setWidthF(2.0); pen.setCapStyle(Qt.PenCapStyle.RoundCap)
            painter.setPen(pen); painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawRoundedRect(15, 11, 6, 11, 3, 3) 
            path = QPainterPath(); path.moveTo(12, 18); path.arcTo(12, 16, 12, 10, 180, 180)
            painter.drawLine(18, 26, 18, 29); painter.drawLine(15, 29, 21, 29); painter.drawPath(path)
        except Exception as e:
            print(f"MicBtn Paint Error: {e}")

class RoundedPillBtn(QFrame):
    clicked = pyqtSignal()
    def __init__(self, icon_char, text, subtext=""):
        super().__init__()
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setFixedHeight(68)
        self.setObjectName("PillBtn")
        self.is_hovered = False
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(24, 0, 24, 0); layout.setSpacing(16)
        
        self.icon_lbl = QLabel(icon_char) 
        self.icon_lbl.setStyleSheet(f"border: none; background: transparent; font-size: 22px; font-weight: 500; color: {COLOR_TEXT_SUB};")
        layout.addWidget(self.icon_lbl)
        
        text_layout = QVBoxLayout(); text_layout.setSpacing(4); text_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.t_lbl = QLabel(text)
        self.t_lbl.setStyleSheet(f"border: none; background: transparent; font-family: 'Segoe UI'; font-size: 16px; font-weight: 700; color: {COLOR_TEXT_MAIN}; letter-spacing: -0.2px;")
        text_layout.addWidget(self.t_lbl)
        if subtext:
             s_lbl = QLabel(subtext)
             s_lbl.setStyleSheet(f"border: none; background: transparent; font-family: 'Segoe UI'; font-size: 14px; font-weight: 400; color: {COLOR_TEXT_SUB};")
             text_layout.addWidget(s_lbl)
        layout.addLayout(text_layout)
        layout.addStretch()
        self.update_style()

    def update_style(self):
        if self.is_hovered:
            self.setStyleSheet(f"QFrame#PillBtn {{ background-color: {COLOR_BG_HOVER}; border: 1px solid {COLOR_BORDER_HOVER}; border-radius: 34px; }}")
            self.icon_lbl.setStyleSheet(f"border: none; background: transparent; font-size: 22px; font-weight: 500; color: {COLOR_TEXT_MAIN};")
        else:
            self.setStyleSheet(f"QFrame#PillBtn {{ background-color: {COLOR_BG_CARD}; border: 1px solid {COLOR_BORDER_CARD}; border-radius: 34px; }}")
            self.icon_lbl.setStyleSheet(f"border: none; background: transparent; font-size: 22px; font-weight: 500; color: {COLOR_TEXT_SUB};")

    def enterEvent(self, event): self.is_hovered=True; self.update_style(); super().enterEvent(event)
    def leaveEvent(self, event): self.is_hovered=False; self.update_style(); super().leaveEvent(event)
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton: self.clicked.emit()

class CommandInput(QFrame):
    submitted = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.setFixedHeight(60) 
        self.setObjectName("CommandInput")
        self.is_focused = False
        
        self.sim_timer = QTimer()
        self.sim_timer.timeout.connect(self.stream_char)
        self.target_text = "I want to organize a team meeting for next Friday at 2 PM."
        self.char_idx = 0
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 4, 12, 4); layout.setSpacing(8)
        
        # Stack text input and listening label
        self.stack_inp = QStackedWidget()
        self.stack_inp.setStyleSheet("background: transparent;")
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Tell the AI what you want...")
        self.input_field.setStyleSheet(f"border: none; selection-background-color: {COLOR_ACCENT}; selection-color: white; background: transparent; font-family: 'Segoe UI'; font-size: 16px; font-weight: 500; color: {COLOR_TEXT_MAIN};")
        self.input_field.focusInEvent = self.on_focus_in
        self.input_field.focusOutEvent = self.on_focus_out
        self.input_field.returnPressed.connect(self.handle_submit)
        
        self.lbl_listening = QLabel("Listening...")
        self.lbl_listening.setStyleSheet(f"color: {COLOR_ACCENT}; font-size: 16px; font-weight: 700; font-family: 'Segoe UI'; letter-spacing: 0.5px;")
        
        self.stack_inp.addWidget(self.input_field)
        self.stack_inp.addWidget(self.lbl_listening)
        
        layout.addWidget(self.stack_inp)
        
        self.btn_mic = MicBtn()
        self.btn_mic.clicked.connect(self.toggle_listening)
        layout.addWidget(self.btn_mic)

        self.btn_arrow = ArrowBtn(direction="right")
        self.btn_arrow.clicked.connect(self.handle_submit)
        layout.addWidget(self.btn_arrow)
        
        self.update_style()

    def update_style(self):
        c_border = COLOR_ACCENT if (self.is_focused or self.btn_mic._listening) else COLOR_BORDER_CARD
        border_w = "2px" if (self.is_focused or self.btn_mic._listening) else "1px"
        self.setStyleSheet(f"QFrame#CommandInput {{ background-color: {COLOR_BG_CARD}; border: {border_w} solid {c_border}; border-radius: 30px; }} QFrame#CommandInput:hover {{ background-color: {COLOR_BG_CARD}; }}")

    def toggle_listening(self):
        active = not self.btn_mic._listening
        self.btn_mic.setListening(active)
        self.update_style()
        
        if active:
            self.input_field.clear()
            self.stack_inp.setCurrentWidget(self.lbl_listening) # Show "Listening..." label
            self.char_idx = 0
            self.sim_timer.stop()
            QTimer.singleShot(800, self.start_streaming)
        else:
            self.sim_timer.stop()
            self.stack_inp.setCurrentWidget(self.input_field) # Restore input
            if not self.input_field.text(): self.input_field.setPlaceholderText("Tell the AI what you want...")

    def start_streaming(self):
        if self.btn_mic._listening: 
            self.stack_inp.setCurrentWidget(self.input_field) # Switch back to input for text stream
            self.input_field.setFocus()
            self.sim_timer.start(50) 

    def stream_char(self):
        if not self.btn_mic._listening: return
        if self.char_idx < len(self.target_text):
             self.input_field.insert(self.target_text[self.char_idx])
             self.char_idx += 1
        else:
            self.stop_listening()

    def stop_listening(self):
        self.sim_timer.stop()
        self.btn_mic.setListening(False)
        self.stack_inp.setCurrentWidget(self.input_field)
        self.update_style()
        if not self.input_field.text(): self.input_field.setPlaceholderText("Tell the AI what you want...") 

    def on_focus_in(self, event): self.is_focused = True; self.update_style(); QLineEdit.focusInEvent(self.input_field, event)
    def on_focus_out(self, event): self.is_focused = False; self.update_style(); QLineEdit.focusOutEvent(self.input_field, event)
    def handle_submit(self):
        text = self.input_field.text().strip()
        if text: self.submitted.emit(text); self.input_field.clear(); self.btn_mic.setListening(False); self.stack_inp.setCurrentWidget(self.input_field)

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
        next_widget.setGeometry(QRect(width, 0, width, self.height())); next_widget.show(); next_widget.raise_() 
        self.animation_group = QParallelAnimationGroup()
        anim_curr = QPropertyAnimation(current_widget, b"pos"); anim_curr.setDuration(500); anim_curr.setStartValue(QPoint(0, 0)); anim_curr.setEndValue(QPoint(-width, 0)); anim_curr.setEasingCurve(QEasingCurve.Type.OutCubic)
        anim_next = QPropertyAnimation(next_widget, b"pos"); anim_next.setDuration(500); anim_next.setStartValue(QPoint(width, 0)); anim_next.setEndValue(QPoint(0, 0)); anim_next.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.animation_group.addAnimation(anim_curr); self.animation_group.addAnimation(anim_next); self.animation_group.finished.connect(lambda: self.on_push_finished(next_idx)); self.animation_group.start()

    def push_prev(self):
        current_idx = self.currentIndex()
        prev_idx = 0
        if current_idx == prev_idx: return
        current_widget = self.widget(current_idx)
        prev_widget = self.widget(prev_idx)
        width = self.width()
        prev_widget.setGeometry(QRect(-width, 0, width, self.height())); prev_widget.show(); prev_widget.raise_()
        self.animation_group = QParallelAnimationGroup()
        anim_curr = QPropertyAnimation(current_widget, b"pos"); anim_curr.setDuration(500); anim_curr.setStartValue(QPoint(0, 0)); anim_curr.setEndValue(QPoint(width, 0)); anim_curr.setEasingCurve(QEasingCurve.Type.OutCubic)
        anim_prev = QPropertyAnimation(prev_widget, b"pos"); anim_prev.setDuration(500); anim_prev.setStartValue(QPoint(-width, 0)); anim_prev.setEndValue(QPoint(0, 0)); anim_prev.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.animation_group.addAnimation(anim_curr); self.animation_group.addAnimation(anim_prev); self.animation_group.finished.connect(lambda: self.on_push_finished(prev_idx)); self.animation_group.start()

    def on_push_finished(self, idx):
        self.setCurrentIndex(idx)
        for i in range(self.count()): self.widget(i).move(0,0) if i==idx else self.widget(i).hide()

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
        self.main_layout.setContentsMargins(28, 28, 28, 28); self.main_layout.setSpacing(24) 
        
        # --- Header ---
        header = QWidget(); header.setStyleSheet("background: transparent; border: none;")
        header_layout = QHBoxLayout(header); header_layout.setContentsMargins(0, 0, 0, 0)
        
        brand_box = QVBoxLayout(); brand_box.setSpacing(0)
        title = QLabel("AI Keyboard"); title.setStyleSheet(f"color: {COLOR_ACCENT}; font-weight: 800; font-size: 20px; font-family: 'Segoe UI'; letter-spacing: -0.5px;")
        sub = QLabel("Plan mode"); sub.setStyleSheet(f"color: {COLOR_TEXT_SUB}; font-weight: 500; font-size: 14px; font-family: 'Segoe UI';")
        brand_box.addWidget(title); brand_box.addWidget(sub)
        header_layout.addLayout(brand_box)
        header_layout.addStretch()
        
        self.btn_back = ArrowBtn(direction="left"); self.btn_back.clicked.connect(self.go_back); self.btn_back.hide()
        header_layout.addWidget(self.btn_back)
        self.btn_close = CloseBtn(); self.btn_close.clicked.connect(self.hide_chat)
        header_layout.addWidget(self.btn_close)
        self.main_layout.addWidget(header)
        
        # --- Stack ---
        self.stack = ProStackedWidget(); self.stack.setStyleSheet("background: transparent; border: none;")
        
        # PAGE 1: Options
        self.page_options = QWidget()
        opt_layout = QVBoxLayout(self.page_options); opt_layout.setContentsMargins(0, 8, 0, 8); opt_layout.setSpacing(16)
        
        btn_1 = RoundedPillBtn("✎", "Rewrite", "Improve grammar and tone")
        btn_2 = RoundedPillBtn("📝", "Summarize", "Get the key points")
        btn_3 = RoundedPillBtn("💡", "Explain", "Make this easier to understand")
        
        btn_1.clicked.connect(lambda: self.go_chat("Rewrite"))
        btn_2.clicked.connect(lambda: self.go_chat("Summarize"))
        btn_3.clicked.connect(lambda: self.go_chat("Explain"))
        
        opt_layout.addWidget(btn_1); opt_layout.addWidget(btn_2); opt_layout.addWidget(btn_3); opt_layout.addStretch()
        
        self.smart_input = CommandInput()
        self.smart_input.submitted.connect(self.go_chat) 
        opt_layout.addWidget(self.smart_input)
        
        self.stack.addWidget(self.page_options)
        
        # PAGE 2: Chat Layout
        self.page_chat = QWidget()
        chat_layout = QVBoxLayout(self.page_chat)
        chat_layout.setContentsMargins(12, 10, 12, 24) # Adjusted margins
        chat_layout.setSpacing(16)
        chat_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # 1. Context Header (The User's Request)
        self.req_container = QHBoxLayout()
        self.req_container.setSpacing(8)
        
        icon_req = QLabel("✨") 
        icon_req.setStyleSheet("font-size: 16px; background: transparent;")
        
        self.user_bubble = QLabel("") # Will hold "Rewrite..."
        self.user_bubble.setStyleSheet(f"color: {COLOR_TEXT_SUB}; background: transparent; font-family: 'Segoe UI'; font-size: 14px; font-weight: 500;")
        
        self.req_container.addWidget(icon_req)
        self.req_container.addWidget(self.user_bubble)
        self.req_container.addStretch()
        chat_layout.addLayout(self.req_container)
        
        # 2. AI Result Card
        self.ai_surface = QFrame()
        self.ai_surface.setObjectName("AiCard")
        self.ai_surface.setStyleSheet(f"""
            QFrame#AiCard {{
                background-color: {COLOR_BG_CARD};
                border: 1px solid {COLOR_BORDER_CARD};
                border-radius: 16px;
            }}
        """)
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20); shadow.setOffset(0, 8); shadow.setColor(QColor(0,0,0, 15))
        self.ai_surface.setGraphicsEffect(shadow)
        
        card_layout = QVBoxLayout(self.ai_surface)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(16)
        
        self.ai_text = TypewriterLabel("Typing...")
        self.ai_text.setWordWrap(True)
        self.ai_text.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.ai_text.setStyleSheet(f"border: none; font-size: 15px; font-weight: 400; line-height: 1.6; color: {COLOR_TEXT_MAIN}; font-family: 'Segoe UI'; background: transparent;")
        
        card_layout.addWidget(self.ai_text)
        
        div = QFrame()
        div.setFixedHeight(1)
        div.setStyleSheet(f"background-color: {COLOR_BG_APP}; border: none;") 
        card_layout.addWidget(div)
        
        # Actions Footer
        footer = QHBoxLayout()
        footer.setSpacing(12)
        
        self.btn_copy = QPushButton("Copy")
        self.btn_copy.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_copy.setStyleSheet(f"QPushButton {{ background-color: transparent; color: {COLOR_TEXT_SUB}; border: none; font-size: 13px; font-weight: 600; text-align: left; }} QPushButton:hover {{ color: {COLOR_TEXT_MAIN}; }}")
        self.btn_copy.clicked.connect(self.copy_to_clipboard)

        self.btn_regen = QPushButton("Regenerate")
        self.btn_regen.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_regen.setStyleSheet(f"QPushButton {{ background-color: transparent; color: {COLOR_TEXT_SUB}; border: none; font-size: 13px; font-weight: 600; }} QPushButton:hover {{ color: {COLOR_TEXT_MAIN}; }}")
        self.btn_regen.clicked.connect(lambda: self.ai_text.start_typing(self.ai_text.full_text)) 

        self.btn_insert = QPushButton("Insert")
        self.btn_insert.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_insert.setStyleSheet(f"QPushButton {{ background-color: {COLOR_ACCENT}; color: white; border: none; border-radius: 6px; padding: 6px 12px; font-size: 13px; font-weight: 600; }} QPushButton:hover {{ background-color: #E04815; }}")
        self.btn_insert.clicked.connect(self.handle_insert) 
 
        footer.addWidget(self.btn_copy)
        footer.addWidget(self.btn_regen)
        footer.addStretch()
        footer.addWidget(self.btn_insert)
         
        card_layout.addLayout(footer)
         
        chat_layout.addWidget(self.ai_surface)
        chat_layout.addStretch()
        self.stack.addWidget(self.page_chat)
         
        self.main_layout.addWidget(self.stack)
         
        self.toggle_action = QAction("Toggle Plan Mode", self)
        self.toggle_action.setShortcut(QKeySequence("Ctrl+K"))
        self.toggle_action.triggered.connect(self.toggle_visibility)
        self.addAction(self.toggle_action)
 
        self.center_on_screen()
        self.hide() # Start hidden
 
    def copy_to_clipboard(self):
        try:
            cb = QApplication.clipboard()
            if cb and hasattr(self.ai_text, "full_text") and self.ai_text.full_text:
                cb.setText(self.ai_text.full_text)
                self.btn_copy.setText("Copied!")
                QTimer.singleShot(2000, lambda: self.btn_copy.setText("Copy"))
        except Exception as e:
            print(f"Clipboard Error: {e}")
 
    def handle_insert(self):
        self.btn_insert.setText("Inserted!")
        self.btn_insert.setStyleSheet(f"QPushButton {{ background-color: #10B981; color: white; border: none; border-radius: 6px; padding: 6px 12px; font-size: 13px; font-weight: 600; }}") # Green success
        QTimer.singleShot(1000, self.finish_insert)
 
    def finish_insert(self):
        print(f"INSERTING: {self.ai_text.full_text}")
        # self.hide_chat()  <-- User requested NOT to close
        # Reset button style for next time
        QTimer.singleShot(500, lambda: self.reset_insert_btn())
 
    def reset_insert_btn(self):
        self.btn_insert.setText("Insert")
        self.btn_insert.setStyleSheet(f"QPushButton {{ background-color: {COLOR_ACCENT}; color: white; border: none; border-radius: 6px; padding: 6px 12px; font-size: 13px; font-weight: 600; }} QPushButton:hover {{ background-color: #E04815; }}")

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
        self.anim_opacity = QPropertyAnimation(self, b"windowOpacity"); self.anim_opacity.setDuration(450); self.anim_opacity.setStartValue(0); self.anim_opacity.setEndValue(1); self.anim_opacity.setEasingCurve(QEasingCurve.Type.OutQuart)
        
        current_geo = self.geometry()
        start_rect = QRect(current_geo.x(), current_geo.y() + 40, current_geo.width(), current_geo.height())
        self.anim_geo = QPropertyAnimation(self, b"geometry"); self.anim_geo.setDuration(500); self.anim_geo.setStartValue(start_rect); self.anim_geo.setEndValue(current_geo); self.anim_geo.setEasingCurve(QEasingCurve.Type.OutQuart)
        
        self.anim_opacity.start(); self.anim_geo.start()

    def hide_chat(self): self.hide()
    def show_chat(self): self.show(); self.animate_entry(); self.activateWindow(); self.smart_input.input_field.setFocus()
    def toggle_visibility(self): self.hide_chat() if self.isVisible() else self.show_chat()
    def mousePressEvent(self, e): 
        if e.button() == Qt.MouseButton.LeftButton: 
           if e.position().y() < 120: self.dragging = True; self.offset = e.globalPosition().toPoint() - self.frameGeometry().topLeft()
    def mouseMoveEvent(self, e):
        if self.dragging: self.move(e.globalPosition().toPoint() - self.offset)
    def mouseReleaseEvent(self, e): self.dragging = False