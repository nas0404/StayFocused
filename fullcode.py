import os
import sys
import cv2
import random
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QVBoxLayout,
    QHBoxLayout, QStackedWidget, QMainWindow, QSpacerItem, QSizePolicy, QSpinBox, QCheckBox, QSlider, QGraphicsDropShadowEffect
)
from PyQt5.QtGui import QIcon, QFont, QImage, QPixmap, QColor, QPainter, QBrush
from PyQt5.QtCore import Qt, QTimer, QTime
 
 
class SessionPage(QWidget):
    def __init__(self, go_to_next_page):
        super().__init__()
        self.go_to_next_page = go_to_next_page
        self.initUI()
 
    def initUI(self):
        self.setStyleSheet("background-color: white;")
 
        self.circle_label = QLabel("Sit up\nstraight!")
        self.circle_label.setAlignment(Qt.AlignCenter)
        self.circle_label.setFont(QFont('Arial', 32))
        self.circle_label.setFixedSize(300, 300)
        self.circle_label.setStyleSheet("border: 4px solid black; border-radius: 150px; background-color: white; color: black; font-weight: bold;")
 
        self.countdown_label = QLabel("5")
        self.countdown_label.setAlignment(Qt.AlignCenter)
        self.countdown_label.setFont(QFont('Segoe UI', 72, QFont.Bold))
        self.countdown_label.setStyleSheet("""
            QLabel {
                color: #00fff0;
                background-color: transparent;
                border: none;
            }
        """)
 
        self.continue_btn = QPushButton("Start Session")
        # self.continue_btn.setStyleSheet("background-color: black; color: white; padding: 15px 30px; border-radius: 10px;")
        self.continue_btn.setFont(QFont('Arial', 18))
        self.continue_btn.clicked.connect(self.go_to_next_page)
        self.continue_btn.hide()
       
        self.continue_btn.setStyleSheet("""
            QPushButton {
                background-color: #00adb5;
                color: white;
                border: none;
                border-radius: 20px;
                padding: 14px 30px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #00cfd1;
            }
            QPushButton:pressed {
                background-color: #009a9e;
            }
        """)
        self.continue_btn.setFont(QFont('Segoe UI Semibold', 14))
 
        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(self.circle_label, alignment=Qt.AlignCenter)
        layout.addSpacing(30)
        layout.addWidget(self.countdown_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.continue_btn, alignment=Qt.AlignCenter)
        layout.addStretch()
        self.setLayout(layout)
 
        self.counter = 5
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_countdown)
        # self.timer.start(1000)
    def start_countdown(self, seconds):
        self.counter = seconds
        self.countdown_label.setText(str(self.counter))
        self.countdown_label.show()
        self.continue_btn.hide()
        self.timer.start(1000)  # No need to reassign or reconnect
   
    def update_countdown(self):
        self.counter -= 1
        self.countdown_label.setText(str(self.counter))
        if self.counter <= 0:
            self.timer.stop()
            self.countdown_label.hide()
            self.go_to_next_page()
 
 
 
class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
 
       
    def initUI(self):
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #1f1f1f, stop: 1 #2c2c2c
                );
                color: white;
                font-family: 'Segoe UI';
            }
            QLabel {
                color: white;
            }
                QSpinBox {
        background-color: white;
        color: black;
        border: 1px solid #aaa;
        border-radius: 6px;
        padding: 4px;
    }
    QSpinBox::up-button, QSpinBox::down-button {
        subcontrol-origin: border;
        width: 20px;
        background-color: #eee;
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
        layout.setSpacing(25)
        layout.setAlignment(Qt.AlignTop)
 
        title = QLabel("⚙️ Settings")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont('Segoe UI', 32, QFont.Bold))
        title.setStyleSheet("""
            color: #cccccc;
            background: none;
            border: none;
        """)
        layout.addWidget(title)
 
        # SESSION LENGTH
        session_label = QLabel("Set Session Length (minutes)")
        session_label.setFont(QFont('Segoe UI', 18))
        session_label.setStyleSheet("""
            color: #cccccc;
            background: none;
            border: none;
        """)
        layout.addWidget(session_label)
           
 
        self.session_length_input = QSpinBox()
        self.session_length_input.setRange(1, 180)
        self.session_length_input.setValue(25)
        self.session_length_input.setFont(QFont('Segoe UI', 18))
        self.session_length_input.setFixedWidth(150)
        self.session_length_input.setStyleSheet("""
            QSpinBox {
                background-color: white;
                color: black;
                border: 1px solid #ccc;
                border-radius: 6px;
                padding: 4px 6px;
            }
        """)
        layout.addWidget(self.session_length_input, alignment=Qt.AlignLeft)
       
       
                 # PRE-SESSION COUNTDOWN
        countdown_label = QLabel("Countdown Before Session (seconds)")
        countdown_label.setFont(QFont('Segoe UI', 18))
        countdown_label.setStyleSheet("""
            color: #cccccc;
            background: none;
            border: none;
        """)
        layout.addWidget(countdown_label)
 
        self.countdown_input = QSpinBox()
        self.countdown_input.setRange(1, 30)
        self.countdown_input.setValue(5)  # Default value
        self.countdown_input.setFont(QFont('Segoe UI', 18))
        self.countdown_input.setFixedWidth(150)
        self.countdown_input.setStyleSheet("""
            QSpinBox {
                background-color: white;
                color: black;
                border: 1px solid #ccc;
                border-radius: 6px;
                padding: 4px 6px;
            }
        """)
        layout.addWidget(self.countdown_input, alignment=Qt.AlignLeft)
       
        # REMINDER TIMER
        reminder_label = QLabel("Set Reminder (minutes : seconds)")
        reminder_label.setFont(QFont('Segoe UI', 18))
        reminder_label.setStyleSheet("color: #cccccc; background: transparent;")
        layout.addWidget(reminder_label)
       
        reminder_label.setStyleSheet("""
            color: #cccccc;
            background: none;
            border: none;
        """)
 
        time_input_layout = QHBoxLayout()
        self.minute_input = QSpinBox()
        self.minute_input.setRange(0, 59)
        self.minute_input.setFont(QFont('Segoe UI', 18))
        self.minute_input.setFixedWidth(100)
        self.minute_input.setStyleSheet("""
            QSpinBox {
                background-color: white;
                color: black;
                border: 1px solid #ccc;
                border-radius: 6px;
                padding: 4px 6px;
            }
        """)
 
 
        self.second_input = QSpinBox()
        self.second_input.setRange(0, 59)
        self.second_input.setFont(QFont('Segoe UI', 18))
        self.second_input.setFixedWidth(100)
        self.second_input.setStyleSheet("""
            QSpinBox {
                background-color: white;
                color: black;
                border: 1px solid #ccc;
                border-radius: 6px;
                padding: 4px 6px;
            }
        """)
 
        colon = QLabel(":")
        colon.setFont(QFont('Segoe UI', 24))
        colon.setAlignment(Qt.AlignCenter)
        colon.setStyleSheet("""
            QLabel {
                background-color: transparent;
                color: #cccccc;
            }
        """)
        colon.setFixedWidth(10)  # Shrink width
       
       
 
 
        time_input_layout.addWidget(self.minute_input)
        time_input_layout.addWidget(colon)
        time_input_layout.addWidget(self.second_input)
        layout.addLayout(time_input_layout, stretch=0)
        layout.setAlignment(time_input_layout, Qt.AlignCenter)
 
        # VOLUME SLIDER
        volume_label = QLabel("Volume")
        volume_label.setFont(QFont('Segoe UI', 18))
        volume_label.setStyleSheet("color: #cccccc; background: transparent;")
        layout.addWidget(volume_label)
 
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(50)
        self.volume_slider.setFixedWidth(300)
        self.volume_slider.setStyleSheet("""
            QSlider::handle:horizontal {
                background: white;
                border: 1px solid #999;
                width: 14px;
                margin: -4px 0;
                border-radius: 7px;
            }
        """)
        layout.addWidget(self.volume_slider)
 
        # BUTTONS
        button_row = QHBoxLayout()
        self.cancel_btn = QPushButton("Cancel")
        self.ok_btn = QPushButton("OK")
        for btn in [self.cancel_btn, self.ok_btn]:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #00adb5;
                    color: white;
                    border: none;
                    border-radius: 20px;
                    padding: 14px 30px;
                    font-size: 16px;
                }
                QPushButton:hover {
                    background-color: #00cfd1;
                }
                QPushButton:pressed {
                    background-color: #009a9e;
                }
            """)
            btn.setFont(QFont('Segoe UI Semibold', 14))
 
        self.cancel_btn.clicked.connect(self.return_home)
        self.ok_btn.clicked.connect(self.confirm_settings)
 
        button_row.addStretch()
        button_row.addWidget(self.cancel_btn)
        button_row.addSpacing(40)
        button_row.addWidget(self.ok_btn)
        button_row.addStretch()
 
        layout.addSpacing(30)
        layout.addLayout(button_row)
 
        self.setLayout(QVBoxLayout())
        self.layout().addStretch()
        self.layout().addWidget(self.panel, alignment=Qt.AlignCenter)
        self.layout().addStretch()
 
 
    def return_home(self):
        self.parent().parent().return_to_home()
 
    def confirm_settings(self):
        total_seconds = self.minute_input.value() * 60 + self.second_input.value()
        self.parent().parent().max_distraction_time = total_seconds
        self.return_home()
 
    def get_settings(self):
        return {
            'timeout': self.minute_input.value() * 60 + self.second_input.value(),
            'volume': self.volume_slider.value(),
            'session_length': self.session_length_input.value(),
            'pre_session_countdown': self.countdown_input.value()
        }
 
 
 
class MainMenu(QWidget):
    def __init__(self, go_live_view_callback, go_session_callback, go_to_settings_callback):
        super().__init__()
        self.go_live_view_callback = go_live_view_callback
        self.go_session_callback = go_session_callback
        self.go_to_settings_callback = go_to_settings_callback
        self.initUI()
 
    def initUI(self):
        self.setMinimumSize(800, 600)
        # self.setStyleSheet("""
        #     QWidget {
        #         background-color: #121212;
        #     }
        # """)
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
        # self.greeting.setStyleSheet("color: #cccccc;")
        self.greeting.setStyleSheet("color: #cccccc; background: transparent;")
        self.greeting.setAttribute(Qt.WA_TranslucentBackground)
 
        self.greeting.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.greeting)
 
        # title = QLabel("StayFocused")
        # title.setFont(QFont("Segoe UI", 44, QFont.Bold))
        # title.setAlignment(Qt.AlignCenter)
        # title.setStyleSheet("""
        #     color: #00fff0;
        # """)
        # layout.addWidget(title)
       
        self.title = QLabel("StayFocused")
        self.title.setFont(QFont("Segoe UI", 44, QFont.Bold))
        self.title.setAlignment(Qt.AlignCenter)
        # self.title.setStyleSheet("color: #00fff0;")
        self.title.setStyleSheet("color: #00fff0; background: transparent;")
        self.title.setAttribute(Qt.WA_TranslucentBackground)
        layout.addWidget(self.title)
 
 
        subtitle = QLabel("Your AI-powered focus assistant")
        subtitle.setFont(QFont("Segoe UI", 16))
        # subtitle.setStyleSheet("color: #888888; background: transparent;")
        subtitle.setStyleSheet("color: #777777;  background: transparent; font-style: italic;")
        subtitle.setAttribute(Qt.WA_TranslucentBackground)
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)
 
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)
 
        layout.addSpacing(20)
        layout.addWidget(self.create_button("🧠  Start Focus Session", self.go_session_callback))
        layout.addWidget(self.create_button("📷  Live View", self.go_live_view_callback))
        layout.addWidget(self.create_button("⚙️  Settings", self.go_to_settings_callback))
 
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
 
    # def resizeEvent(self, event):
    #     w, h = self.width(), self.height()
    #     self.panel.setGeometry(
    #         int(w * 0.25),
    #         int(h * 0.15),
    #         int(w * 0.5),
    #         int(h * 0.7)
    #     )
    def resizeEvent(self, event):
        w, h = self.width(), self.height()
        # panel_width = max(400, int(w * 0.5))
        # panel_height = max(300, int(h * 0.7))
        # panel_width = min(900, int(w * 0.85))
        # panel_height = min(600, int(h * 0.85))
        panel_width = int(w * 0.7)
        panel_height = int(h * 0.8)
 
        self.panel.setGeometry(
            int((w - panel_width) / 2),
            int((h - panel_height) / 2),
            panel_width,
            panel_height
        )
 
        # Scale title font based on width
        # font_size = max(24, min(52, int(panel_width * 0.08)))
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
 
 
 
from tensorflow.keras.models import load_model
import numpy as np
 
 
class CameraView(QWidget):
    def __init__(self, return_home_callback):
        super().__init__()
        self.return_home_callback = return_home_callback
        self.cap = None
 
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.initUI()
 
    # def initUI(self):
    #     self.setStyleSheet("background-color: white;")
 
    #     self.title = QLabel("Say Hi!")
    #     self.title.setAlignment(Qt.AlignCenter)
    #     self.title.setFont(QFont('Arial', 36))
 
    #     self.video_label = QLabel("Loading camera...")
    #     self.video_label.setAlignment(Qt.AlignCenter)
    #     self.video_label.setFont(QFont('Arial', 24))
 
    #     layout = QVBoxLayout()
    #     layout.addWidget(self.title)
    #     layout.addWidget(self.video_label)
    #     layout.addSpacing(30)
    #     layout.setContentsMargins(40, 40, 40, 40)
    #     self.setLayout(layout)
    def initUI(self):
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #1f1f1f, stop: 1 #2c2c2c
                );
                color: white;
                font-family: 'Segoe UI';
            }
            QLabel {
                color: white;
            }
        """)
 
        # Create central dark panel
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
 
        # Inside panel layout
        panel_layout = QVBoxLayout(self.panel)
       
        panel_layout.setContentsMargins(40, 40, 40, 40)
        panel_layout.setSpacing(30)
 
        self.title = QLabel("Say Hi!")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setFont(QFont('Segoe UI', 36, QFont.Bold))
        panel_layout.addWidget(self.title)
 
        self.video_label = QLabel("Loading camera...")
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setFont(QFont('Segoe UI', 20))
        self.video_label.setStyleSheet("background-color: white; border-radius: 10px;")
        self.video_label.setMinimumSize(640, 480)
        panel_layout.addWidget(self.video_label)
 
        self.back_btn = QPushButton("Back to Home")
        self.back_btn.setStyleSheet("""
            QPushButton {
                background-color: #00adb5;
                color: white;
                border: none;
                border-radius: 20px;
                padding: 14px 30px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #00cfd1;
            }
            QPushButton:pressed {
                background-color: #009a9e;
            }
        """)
        self.back_btn.setFont(QFont('Segoe UI Semibold', 14))
        self.back_btn.clicked.connect(self.return_home_callback)
        panel_layout.addWidget(self.back_btn, alignment=Qt.AlignCenter)
 
        # Center layout
        outer_layout = QVBoxLayout(self)
        outer_layout.addStretch()
        outer_layout.addWidget(self.panel, alignment=Qt.AlignCenter)
        outer_layout.addStretch()
        self.setLayout(outer_layout)
 
 
    def start_camera(self):
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not self.cap.isOpened():
            self.video_label.setText("No camera detected.")
        else:
            self.timer = QTimer()
            self.timer.timeout.connect(self.update_frame)
            # self.timer.start(30)
            self.timer.start(1000)
 
    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            self.video_label.setText("Camera error.")
            return
 
        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
 
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
 
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = QImage(frame.data, frame.shape[1], frame.shape[0],
                       frame.strides[0], QImage.Format_RGB888)
        self.video_label.setPixmap(QPixmap.fromImage(image))
 
    def stop_camera(self):
        if self.cap and self.cap.isOpened():
            self.cap.release()
        if hasattr(self, 'timer'):
            self.timer.stop()
 
    def close_Event(self, event):
        self.stop_camera()
        event.accept()
   
 
class LiveViewPage(CameraView):
    def __init__(self, return_home_callback):
        super().__init__(return_home_callback)
        # self.add_back_button()
 
    def add_back_button(self):
        self.back_btn = QPushButton("Back to Home")
        self.back_btn.setStyleSheet("background-color: black; color: white; padding: 12px 24px; border-radius: 10px;")
        self.back_btn.setFont(QFont('Arial', 16))
        self.back_btn.clicked.connect(self.return_home_callback)
        self.layout().addWidget(self.back_btn, alignment=Qt.AlignCenter)
 
 
   
import numpy as np
from tensorflow.keras.models import load_model
 
class MLPage(CameraView):
 
    def __init__(self, go_to_summary_callback, return_home_callback):
        self.go_to_summary_callback = go_to_summary_callback
        super().__init__(return_home_callback)
        self.inactive_seconds = 0
        self.max_distraction_duration = 10  # this will be overwritten based on settings
        self.last_distraction_warning = False
        # self.inactive_seconds = 0
        # self.last_distraction_warning = False
        self.activity_timer = 0  # track continuous seconds
        self.last_label = None
 
       
 
        self.title.setText("You're now free to work")
 
        self.session_timer_label = QLabel("")
        self.session_timer_label.setFont(QFont('Arial', 24))
        # self.layout().insertWidget(1, self.session_timer_label)
        self.panel.layout().insertWidget(1, self.session_timer_label)
 
 
        self.end_session_btn = QPushButton("End Session")
        self.end_session_btn.setStyleSheet("background-color: black; color: white; padding: 15px 30px; border-radius: 10px;")
        self.end_session_btn.setFont(QFont('Arial', 18))
        self.end_session_btn.clicked.connect(self.go_to_summary_callback)
        self.layout().addWidget(self.end_session_btn, alignment=Qt.AlignCenter)
 
        self.session_timer = QTimer()
        self.session_timer.timeout.connect(self.update_session_timer)
        self.session_seconds_left = 0
 
        # Load face detector and emotion model
        self.face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.emotion_model = load_model('./vgg16dropout.keras')
        self.emotion_labels = ['Active', 'Inactive']
 
    def start_session_timer(self, seconds):
        self.session_seconds_left = seconds
        self.update_session_timer()
        self.session_timer.start(1000)
 
    def update_session_timer(self):
        mins = self.session_seconds_left // 60
        secs = self.session_seconds_left % 60
        self.session_timer_label.setText(f"Session Time Left: {mins:02d}:{secs:02d}")
        if self.session_seconds_left <= 0:
            self.session_timer.stop()
            self.go_to_summary_callback()
        else:
            self.session_seconds_left -= 1
 
 
    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            self.video_label.setText("Camera error.")
            return
 
        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_classifier.detectMultiScale(gray, 1.3, 5)
 
        predicted_label = None
 
        for (x, y, w, h) in faces:
            roi_color = frame[y:y+h, x:x+w]
            roi_color = cv2.resize(roi_color, (224, 224))
            roi = roi_color.astype('float32') / 255.0
            roi = np.expand_dims(roi, axis=0)
 
            prediction = self.emotion_model.predict(roi, verbose=0)[0]
            predicted_label = self.emotion_labels[int((prediction > 0.5).astype(int))]
 
            # Draw face rectangle and label
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, predicted_label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
 
        # --- Process logic only after the loop ---
        if predicted_label:
            print(f"DEBUG — label: {predicted_label}, last_label: {self.last_label}")
            if predicted_label != self.last_label:
                self.activity_timer = 0
                self.last_label = predicted_label
            else:
                self.activity_timer += self.timer.interval() / 1000.0
 
            timestamp = f"{int(self.activity_timer // 60):02d}:{int(self.activity_timer % 60):02d}"
            print(f"{predicted_label}: {timestamp}")
 
            if predicted_label == 'Inactive':
                self.inactive_seconds += 1
            else:
                self.inactive_seconds = 0
                self.last_distraction_warning = False
 
            print(f"[DEBUG] inactive_seconds: {self.inactive_seconds}")
 
            if self.inactive_seconds >= self.max_distraction_duration and not self.last_distraction_warning:
                print("⚠️ User distracted! Get back to work.")
                self.last_distraction_warning = True
 
        # Show frame
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = QImage(rgb.data, rgb.shape[1], rgb.shape[0], rgb.strides[0], QImage.Format_RGB888)
        self.video_label.setPixmap(QPixmap.fromImage(image))
 
 
 
class FocusTimerPage(QWidget):
    def __init__(self, go_to_next_page):
        super().__init__()
        self.go_to_next_page = go_to_next_page
        self.seconds = 10
        self.initUI()
 
    def initUI(self):
        self.setStyleSheet("background-color: white;")
        self.instruction = QLabel("Focus begins in...")
        self.instruction.setAlignment(Qt.AlignCenter)
        self.instruction.setFont(QFont('Arial', 20))
 
        self.label = QLabel("Focus")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont('Arial', 36))
 
        self.timer_display = QLabel("00:10")
        self.timer_display.setAlignment(Qt.AlignCenter)
        self.timer_display.setFont(QFont('Arial', 36))
 
        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(self.instruction)
        layout.addWidget(self.label)
        layout.addWidget(self.timer_display)
        layout.addStretch()
        self.setLayout(layout)
 
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
 
    def update_timer(self):
        self.seconds -= 1
        minutes = self.seconds // 60
        seconds = self.seconds % 60
        self.timer_display.setText(f"{minutes:02d}:{seconds:02d}")
        if self.seconds <= 0:
            self.timer.stop()
            self.go_to_next_page()
 
 
 
class SummaryPage(QWidget):
    def __init__(self,return_home_callback):
        super().__init__()
        self.return_home_callback = return_home_callback
        self.initUI()
 
    def initUI(self):
        self.setStyleSheet("background-color: white;")
 
        title = QLabel("Summary")
        title.setFont(QFont('Arial', 36, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
 
        tab1 = QLabel("Sessions Completed: waiting to be filled by NAS")
        tab2 = QLabel("Total Focus Time: waiting to be filled by NAS")
        tab3 = QLabel("Distractions This Session: waiting to be filled by NAS")
        tab4 = QLabel("Comparison to Previous Session: waiting to be filled by NAS")
 
        for label in [tab1, tab2, tab3, tab4]:
            label.setFont(QFont('Arial', 20))
            label.setAlignment(Qt.AlignCenter)
 
        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addSpacing(30)
        layout.addWidget(tab1)
        layout.addWidget(tab2)
        layout.addWidget(tab3)
        layout.addWidget(tab4)
        self.back_btn = QPushButton("Back to Home")
        self.back_btn.setStyleSheet("background-color: black; color: white; padding: 15px 30px; border-radius: 10px;")
        self.back_btn.setFont(QFont('Arial', 18))
        self.back_btn.clicked.connect(self.return_home_callback)
        layout.addWidget(self.back_btn, alignment=Qt.AlignCenter)
        layout.addStretch()
 
        self.setLayout(layout)
 
 
class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("StayFocused")
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #1f1f1f, stop: 1 #2c2c2c
                );
            }
        """)
        self.setMinimumSize(1024, 768)
        self.showMaximized()
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
 
        self.settings_page = SettingsPage()
        self.summary_page = SummaryPage(self.return_to_home)
        self.max_distraction_time = self.settings_page.get_settings()['timeout']
        self.ml_page = MLPage(self.go_to_summary, self.return_to_home)
        # self.focus_timer_page = FocusTimerPage(self.go_to_ml_page)
        self.session_page = SessionPage(self.go_to_ml_page)
        self.live_view_page = LiveViewPage(self.return_to_home)
        self.main_menu = MainMenu(self.go_to_live_view, self.go_to_session, self.go_to_settings)
 
        self.central_widget.addWidget(self.main_menu)
        self.central_widget.addWidget(self.live_view_page)
        self.central_widget.addWidget(self.session_page)
        # self.central_widget.addWidget(self.focus_timer_page)
        self.central_widget.addWidget(self.ml_page)
        self.central_widget.addWidget(self.settings_page)
        self.central_widget.addWidget(self.summary_page)
 
    def go_to_live_view(self):
        self.ml_page.stop_camera()
        self.live_view_page.stop_camera()
        self.live_view_page.start_camera()
        self.central_widget.setCurrentWidget(self.live_view_page)
 
 
    def go_to_session(self):
        countdown_seconds = self.settings_page.countdown_input.value()
        self.session_page.start_countdown(countdown_seconds)
        self.central_widget.setCurrentWidget(self.session_page)
   
    def go_to_focus_timer(self):
        self.ml_page.start_camera()
        session_length_min = self.settings_page.session_length_input.value()
        session_length_sec = session_length_min * 60
        self.ml_page.start_session_timer(session_length_sec)
        self.central_widget.setCurrentWidget(self.ml_page)
 
    def go_to_ml_page(self):
        self.ml_page.start_camera()
        session_length_min = self.settings_page.session_length_input.value()
        session_length_sec = session_length_min * 60
 
        # Set distraction limit from settings
        self.ml_page.max_distraction_duration = self.settings_page.get_settings()['timeout']
 
        self.ml_page.start_session_timer(session_length_sec)
        self.central_widget.setCurrentWidget(self.ml_page)
 
    def go_to_settings(self):
        self.central_widget.setCurrentWidget(self.settings_page)
 
    def go_to_summary(self):
        self.central_widget.setCurrentWidget(self.summary_page)
 
 
   
    def return_to_home(self):
        self.live_view_page.stop_camera()
        self.ml_page.stop_camera()
        self.central_widget.setCurrentWidget(self.main_menu)
 
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())