from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QVBoxLayout,
    QHBoxLayout, QStackedWidget, QMainWindow, QSpacerItem, QSizePolicy, QSpinBox, QCheckBox, QTableWidget, QTableWidgetItem, QGraphicsDropShadowEffect
)
from PyQt5.QtGui import QIcon, QFont, QImage, QPixmap, QColor, QPainter, QBrush
from PyQt5.QtCore import Qt, QTimer, QTime, QPropertyAnimation, QPoint
import os
class MainMenu(QWidget):
    def __init__(self, go_live_view_callback, go_session_callback, go_to_settings_callback, go_to_history_callback):
        super().__init__()
        self.go_live_view_callback = go_live_view_callback
        self.go_session_callback = go_session_callback
        self.go_to_settings_callback = go_to_settings_callback
        self.go_to_history_callback = go_to_history_callback
        self.initUI()

    def initUI(self):
        self.setMinimumSize(800, 600)
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #1f1f1f, stop: 1 #2c2c2c
                );
            }
        """)

        self.panel = QWidget(self)
        self.panel.setStyleSheet("""
            QWidget {
                background-color: rgba(30, 30, 30, 0.9);
                border: 1px solid rgba(255, 255, 255, 0.05);
                border-radius: 24px;
            }
        """)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(50)
        shadow.setOffset(0, 0)
        shadow.setColor(QColor(0, 0, 0, 180))
        self.panel.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self.panel)
        layout.setContentsMargins(60, 60, 60, 60)
        layout.setSpacing(30)
        layout.setAlignment(Qt.AlignCenter)

        self.greeting = QLabel(self.get_dynamic_greeting())
        self.greeting.setFont(QFont("Segoe UI", 22, QFont.Medium))
        self.greeting.setStyleSheet("color: #cccccc; background: transparent;")
        self.greeting.setAttribute(Qt.WA_TranslucentBackground)

        self.greeting.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.greeting)


        
        self.title = QLabel("StayFocused")
        self.title.setFont(QFont("Segoe UI", 44, QFont.Bold))
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("color: #00fff0; background: transparent;")
        self.title.setAttribute(Qt.WA_TranslucentBackground)
        layout.addWidget(self.title)


        subtitle = QLabel("Your AI-powered focus assistant")
        subtitle.setFont(QFont("Segoe UI", 16))
        subtitle.setStyleSheet("color: #777777;  background: transparent; font-style: italic;")
        subtitle.setAttribute(Qt.WA_TranslucentBackground)
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)

        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)

        layout.addSpacing(20)
        layout.addWidget(self.create_button("  Start Focus Session", self.go_session_callback))
        layout.addWidget(self.create_button("  Live View", self.go_live_view_callback))
        layout.addWidget(self.create_button("  Settings", self.go_to_settings_callback))
        layout.addWidget(self.create_button("  View Session History", self.go_to_history_callback))

        self.setLayout(QVBoxLayout())
        self.layout().addStretch()
        self.layout().addWidget(self.panel, alignment=Qt.AlignCenter)
        self.layout().addStretch()

        self.greeting_timer = QTimer()
        self.greeting_timer.timeout.connect(self.update_greeting)
        self.greeting_timer.start(60000)

    def create_button(self, text, callback):
        button = QPushButton(text)
        button.setMinimumHeight(58)
        button.setFont(QFont("Segoe UI Semibold", 15))
        button.setCursor(Qt.PointingHandCursor)
        button.setStyleSheet("""
            QPushButton {
                background-color: #00adb5;
                color: white;
                border: none;
                border-radius: 28px;
                padding: 14px 30px;
                letter-spacing: 1px;
            }
            QPushButton:hover {
                background-color: #00cfd1;
            }
            QPushButton:pressed {
                background-color: #009a9e;
            }
        """)
        button.clicked.connect(callback)
        return button

    def resizeEvent(self, event):
        w, h = self.width(), self.height()

        panel_width = int(w * 0.7)
        panel_height = int(h * 0.8)

        self.panel.setGeometry(
            int((w - panel_width) / 2),
            int((h - panel_height) / 2),
            panel_width,
            panel_height
        )

        font_size = max(32, min(64, int(panel_width * 0.06)))
        self.title.setFont(QFont("Segoe UI", font_size, QFont.Bold))


    def get_dynamic_greeting(self):
        hour = QTime.currentTime().hour()
        user = os.getenv("USERNAME") or "friend"
        if hour < 12:
            
            return f"☀️ Good Morning, {user}"
        elif hour < 18:
            return f"🌤️ Good Afternoon, {user}"
        else:
            return f"🌙 Good Evening, {user}"

    def update_greeting(self):
        self.greeting.setText(self.get_dynamic_greeting())