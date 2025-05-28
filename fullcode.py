import os
import sys
import cv2
import random
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QVBoxLayout,
    QHBoxLayout, QStackedWidget, QMainWindow, QSpacerItem, QSizePolicy, QSpinBox, QCheckBox, QTableWidget, QTableWidgetItem, QGraphicsDropShadowEffect
)
from PyQt5.QtGui import QIcon, QFont, QImage, QPixmap, QColor, QPainter, QBrush
from PyQt5.QtCore import Qt, QTimer, QTime, QPropertyAnimation, QPoint
from plyer import notification
from win10toast_click import ToastNotifier
from pygame import mixer
import pyttsx3
import sqlite3
from datetime import datetime


class SessionPage(QWidget):
    def __init__(self, go_to_next_page):
        super().__init__()
        self.go_to_next_page = go_to_next_page
        self.initUI()
 
    def initUI(self):
        self.setStyleSheet("background-color: white;")
 
        # self.circle_label = QLabel("Sit up\nstraight!")
        # self.circle_label.setAlignment(Qt.AlignCenter)
        # self.circle_label.setFont(QFont('Arial', 32))
        # self.circle_label.setFixedSize(300, 300)
        # self.circle_label.setStyleSheet("border: 4px solid black; border-radius: 150px; background-color: white; color: black; font-weight: bold;")

        self.circle_label = QLabel("Sit up\nstraight!")
        self.circle_label.setAlignment(Qt.AlignCenter)
        self.circle_label.setFont(QFont('Arial', 24, QFont.Bold))  # Smaller font size
        self.circle_label.setFixedSize(300, 300)
        self.circle_label.setWordWrap(True)  # Allow text to wrap
        self.circle_label.setStyleSheet("""
            border: 4px solid black;
            border-radius: 150px;
            background-color: white;
            color: black;
            font-weight: bold;
            padding: 24px;  /* Add padding for better fit */
            """)
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
        
        # DISTRACTION TOLERANCE
        distraction_label = QLabel("Distraction Tolerance (seconds)")
        distraction_label.setFont(QFont('Segoe UI', 18))
        distraction_label.setStyleSheet("color: #cccccc; background: none; border: none;")
        layout.addWidget(distraction_label)

        self.distraction_input = QSpinBox()
        self.distraction_input.setRange(1, 60)
        self.distraction_input.setValue(10)
        self.distraction_input.setFont(QFont('Segoe UI', 18))
        self.distraction_input.setFixedWidth(150)
        self.distraction_input.setStyleSheet("""
            QSpinBox {
                background-color: white;
                color: black;
                border: 1px solid #ccc;
                border-radius: 6px;
                padding: 4px 6px;
            }
        """)
        layout.addWidget(self.distraction_input, alignment=Qt.AlignLeft)

        from PyQt5.QtWidgets import QRadioButton, QButtonGroup

        # SOUND SETTINGS
        self.sound_group = QButtonGroup(self)
        self.ding_radio = QRadioButton("🔔 Classic Ding")
        self.voice_radio = QRadioButton("🗣️ Voice Alert")

        for btn in [self.ding_radio, self.voice_radio]:
            btn.setFont(QFont('Segoe UI', 16))
            btn.setStyleSheet("color: white;")
            self.sound_group.addButton(btn)

        self.voice_radio.setChecked(True)  # Default to speech

        sound_layout = QHBoxLayout()
        sound_layout.addWidget(self.ding_radio)
        sound_layout.addWidget(self.voice_radio)
        layout.addLayout(sound_layout)



        


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
            'session_length': self.session_length_input.value(),
            'pre_session_countdown': self.countdown_input.value(),
            'distraction_tolerance': self.distraction_input.value(),
            'sound': 'ding' if self.ding_radio.isChecked() else 'voice'
        }



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

        # Scale title font based on width
        # font_size = max(24, min(52, int(panel_width * 0.08)))
        font_size = max(32, min(64, int(panel_width * 0.06)))
        self.title.setFont(QFont("Segoe UI", font_size, QFont.Bold))


    def get_dynamic_greeting(self):
        hour = QTime.currentTime().hour()
        user = os.getenv("USERNAME") or "friend"
        # user = "naseem"
        if hour < 12:
            
            return f"☀️ Good Morning, {user}"
        elif hour < 18:
            return f"🌤️ Good Afternoon, {user}"
        else:
            return f"🌙 Good Evening, {user}"

    def update_greeting(self):
        self.greeting.setText(self.get_dynamic_greeting())



class CameraView(QWidget):
    def __init__(self, return_home_callback):
        super().__init__()
        self.return_home_callback = return_home_callback
        self.cap = None
        self.last_label = None
        self.focus_time = 0
        self.total_distraction_time = 0
        self.distraction_count = 0
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
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
        self.title.setStyleSheet("color: #cccccc; background: transparent; border: none;")
        panel_layout.addWidget(self.title)

        self.video_label = QLabel("Loading camera...")
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setFont(QFont('Segoe UI', 20))
        self.video_label.setStyleSheet("background-color: white; border-radius: 10px;")
        self.video_label.setMinimumSize(640, 480)
        panel_layout.addWidget(self.video_label)

                # Only add back button if not in MLPage
        if not isinstance(self, MLPage):
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
            self.timer.start(16)

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
            # Reset state
        self.inactive_seconds = 0
        self.active_seconds = 0
        self.last_distraction_warning = False
        self.last_label = None

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
class Toast(QWidget):
    def __init__(self, title="⚠️ Focus Alert!", message="You've been inactive too long!", duration=4000):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint | Qt.X11BypassWindowManagerHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(320, 100)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        self.title_label = QLabel(title)
        self.title_label.setFont(QFont('Segoe UI Semibold', 12))
        self.title_label.setStyleSheet("color: #00fff0;")

        self.message_label = QLabel(message)
        self.message_label.setFont(QFont('Segoe UI', 10))
        self.message_label.setStyleSheet("color: white;")
        self.message_label.setWordWrap(True)

        layout.addWidget(self.title_label)
        layout.addWidget(self.message_label)
        self.setLayout(layout)

        # Slide-in animation
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        self.move(screen_geometry.width(), screen_geometry.height() - 120)

        self.anim = QPropertyAnimation(self, b"pos")
        self.anim.setDuration(600)
        self.anim.setStartValue(QPoint(screen_geometry.width(), screen_geometry.height() - 120))
        self.anim.setEndValue(QPoint(screen_geometry.width() - 340, screen_geometry.height() - 120))
        self.anim.start()

        QTimer.singleShot(duration, self.close)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = self.rect()
        painter.setBrush(QBrush(QColor(30, 30, 30, 220)))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(rect, 15, 15)
class MLPage(CameraView):

    def __init__(self,db, go_to_summary_callback, return_home_callback):
        self.db = db
        self.go_to_summary_callback = go_to_summary_callback
        super().__init__(return_home_callback)
        self.inactive_seconds = 0
        self.active_seconds = 0
        self.max_distraction_duration = 10  # this will be overwritten based on settings
        self.last_distraction_warning = False
        self.voice_engine = pyttsx3.init()
        # self.inactive_seconds = 0
        # self.last_distraction_warning = False
        self.activity_timer = 0  # track continuous seconds
        self.last_label = None
        self.focus_time = 0
        self.total_distraction_time = 0
        self.distraction_count = 0

        

        self.title.setText("You're now free to work")

        self.session_timer_label = QLabel("")
        self.session_timer_label.setFont(QFont('Arial', 24))
        # self.layout().insertWidget(1, self.session_timer_label)
        self.panel.layout().insertWidget(1, self.session_timer_label)


        self.end_session_btn = QPushButton("End Session")
        # self.end_session_btn.setStyleSheet("background-color: black; color: white; padding: 15px 30px; border-radius: 10px;")
        self.end_session_btn.setStyleSheet("""
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
        self.end_session_btn.setFont(QFont('Arial', 18))
        # self.end_session_btn.clicked.connect(self.go_to_summary_callback)
        self.end_session_btn.clicked.connect(self.handle_manual_session_end)
        self.layout().addWidget(self.end_session_btn, alignment=Qt.AlignCenter)

        self.session_timer = QTimer()
        self.session_timer.timeout.connect(self.update_session_timer)
        self.session_seconds_left = 0

        # Load face detector and emotion model
        self.face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.emotion_model = load_model("C:/Users/nextg/Downloads/vgg16dropout.keras")
        self.emotion_labels = ['Active', 'Inactive']

    # def start_session_timer(self, seconds):
    #     self.session_seconds_left = seconds
    #     self.update_session_timer()
    #     self.session_timer.start(1000)
    def start_session_timer(self, seconds, planned_session_length):
        self.session_seconds_left = seconds
        self.planned_session_length = planned_session_length  # ✅ Store it for later
        self.update_session_timer()
        self.session_timer.start(1000)

    def update_session_timer(self):
        mins = self.session_seconds_left // 60
        secs = self.session_seconds_left % 60
        self.session_timer_label.setText(f"Session Time Left: {mins:02d}:{secs:02d}")
        if self.session_seconds_left <= 0:
            self.session_timer.stop()
            self.finalize_and_save_session(interrupted=False)
            self.go_to_summary_callback()
        else:
            self.session_seconds_left -= 1
    def handle_manual_session_end(self):
        self.session_timer.stop()
        self.finalize_and_save_session(interrupted=True)
        self.go_to_summary_callback()

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            self.video_label.setText("Camera error.")
            return

        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_classifier.detectMultiScale(gray, 1.3, 5)

        predicted_label = 'Inactive'  # Default when no face is found

        if len(faces) > 0:
            (x, y, w, h) = faces[0]
            roi_color = frame[y:y + h, x:x + w]
            roi_color = cv2.resize(roi_color, (224, 224))
            roi = roi_color.astype('float32') / 255.0
            roi = np.expand_dims(roi, axis=0)

            prediction = self.emotion_model.predict(roi, verbose=0)[0]
            predicted_label = self.emotion_labels[int((prediction > 0.5).astype(int))]

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, predicted_label, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        if predicted_label == 'Inactive':
            self.inactive_seconds += 1
            self.total_distraction_time += 1  # new
            print(f"DEBUG — label: {predicted_label}, inactive_seconds: {self.inactive_seconds}, last_label: {self.last_label}")
            
            if self.inactive_seconds == self.max_distraction_duration and not self.last_distraction_warning:
                print("⚠️ You've been distracted too long! Get back to focus.")
                self.last_distraction_warning = True
                self.distraction_count += 1 

                # Custom Toast
                self.toast = Toast(
                    title="⚠️ Distraction Warning!",
                    message="You've been inactive too long. Time to refocus, big boss",
                    duration=5000
                )
                self.toast.show()

                if self.selected_sound == 'voice':
                    self.voice_engine.say("Come on, you got this, get your head in the game!")
                    self.voice_engine.runAndWait()
                elif self.selected_sound == 'ding':
                    mixer.init()
                    mixer.music.load("./dingsound.mp3")  # or "ding.wav"
                    mixer.music.set_volume(0.6)
                    mixer.music.play()


        elif predicted_label == 'Active':
            self.active_seconds += 1
            self.focus_time += 1
            if self.last_label == 'Inactive':
                print("✅ You're back on track!")
            if self.active_seconds > 0:
                print(f"DEBUG — label: {predicted_label}, active_seconds: {self.active_seconds}, last_label: {self.last_label}")
            # ✅ Reset both timers and warning flags
            self.inactive_seconds = 0
            self.last_distraction_warning = False
            self.active_seconds += 1
        print(f"[FOCUS DEBUG] Focus Time: {self.focus_time} seconds")
        


        self.last_label = predicted_label

        # Show frame
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = QImage(rgb.data, rgb.shape[1], rgb.shape[0], rgb.strides[0], QImage.Format_RGB888)
        self.video_label.setPixmap(QPixmap.fromImage(image))
        
    def finalize_and_save_session(self, interrupted=False):
        actual_session_length = self.focus_time + self.total_distraction_time
        planned_session_length = self.planned_session_length
        focus_time = self.focus_time
        total_distraction_time = self.total_distraction_time
        distractions = self.distraction_count
        audio_alert_type = self.selected_sound
        distraction_limit = self.max_distraction_duration
        
        print("DEBUG — Saving session with values:")
        print(f"Planned Session Length: {planned_session_length}")
        print(f"Actual Session Length: {actual_session_length}")
        print(f"Focus Time: {focus_time}")
        print(f"Distractions: {distractions}")

        self.db.save_session(
        planned_session_length=int(planned_session_length),
        actual_session_length=int(actual_session_length),
        focus_time=int(focus_time),
        total_distraction_time=int(total_distraction_time),
        distractions=int(distractions),
        audio_alert_type=audio_alert_type,
        distraction_limit=distraction_limit,
        notes="",
        interrupted=interrupted
    )

class SummaryPage(QWidget):
    def __init__(self, db, return_home_callback):
        super().__init__()
        self.db = db
        self.return_home_callback = return_home_callback
        self.initUI()
        self.populate_summary()  # ✅ Populate data immediately

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
        """)

        self.panel = QWidget(self)
        self.panel.setStyleSheet("""
            QWidget {
                background-color: rgba(30, 30, 30, 0.9);
                border-radius: 24px;
                padding: 40px;
            }
        """)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(50)
        shadow.setOffset(0, 0)
        shadow.setColor(QColor(0, 0, 0, 180))
        self.panel.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self.panel)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(25)

        title = QLabel("📈 Session Summary")
        title.setFont(QFont("Segoe UI", 32, QFont.Bold))
        title.setStyleSheet("color: #00fff0; background: none;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Labels to be populated
        self.sessions_label = QLabel()
        self.focus_label = QLabel()
        self.distractions_label = QLabel()
        self.completion_label = QLabel()

        for lbl in [self.sessions_label, self.focus_label, self.distractions_label, self.completion_label]:
            lbl.setFont(QFont("Segoe UI", 20))
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setStyleSheet("color: #cccccc;")

        layout.addWidget(self.sessions_label)
        layout.addWidget(self.focus_label)
        layout.addWidget(self.distractions_label)
        layout.addWidget(self.completion_label)

        # Back button
        back_btn = QPushButton("⬅️ Back to Home")
        back_btn.setFont(QFont("Segoe UI Semibold", 14))
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #00adb5;
                color: white;
                border: none;
                border-radius: 20px;
                padding: 14px 30px;
            }
            QPushButton:hover {
                background-color: #00cfd1;
            }
            QPushButton:pressed {
                background-color: #009a9e;
            }
        """)
        back_btn.clicked.connect(self.return_home_callback)
        layout.addSpacing(20)
        layout.addWidget(back_btn, alignment=Qt.AlignCenter)

        # Wrap everything
        outer_layout = QVBoxLayout(self)
        outer_layout.addStretch()
        outer_layout.addWidget(self.panel, alignment=Qt.AlignCenter)
        outer_layout.addStretch()
        self.setLayout(outer_layout)

    def populate_summary(self):
        # Overall stats
        self.db.cursor.execute("SELECT COUNT(*), SUM(focus_time), AVG(completion_rate) FROM sessions")
        count, total_focus, avg_completion = self.db.cursor.fetchone()

        # Last session distraction count
        self.db.cursor.execute("SELECT distractions FROM sessions ORDER BY id DESC LIMIT 1")
        latest = self.db.cursor.fetchone()

        self.sessions_label.setText(f"Sessions Completed: {count or 0}")

        if total_focus:
            mins = int(total_focus) // 60
            secs = int(total_focus) % 60
            self.focus_label.setText(f"Total Focus Time: {mins:02d}:{secs:02d}")
        else:
            self.focus_label.setText("Total Focus Time: 00:00")

        self.distractions_label.setText(f"Distractions This Session: {latest[0] if latest else 0}")

        if avg_completion is not None:
            self.completion_label.setText(f"Average Completion Rate: {avg_completion:.1f}%")
        else:
            self.completion_label.setText("Average Completion Rate: N/A")

    
# class SummaryPage(QWidget):
#     def __init__(self,return_home_callback):
#         super().__init__()
#         self.return_home_callback = return_home_callback
#         self.initUI()
 
#     def initUI(self):
#         self.setStyleSheet("background-color: white;")
 
#         title = QLabel("Summary")
#         title.setFont(QFont('Arial', 36, QFont.Bold))
#         title.setAlignment(Qt.AlignCenter)
 
#         tab1 = QLabel("Sessions Completed: waiting to be filled by NAS")
#         tab2 = QLabel("Total Focus Time: waiting to be filled by NAS")
#         tab3 = QLabel("Distractions This Session: waiting to be filled by NAS")
#         tab4 = QLabel("Comparison to Previous Session: waiting to be filled by NAS")
 
#         for label in [tab1, tab2, tab3, tab4]:
#             label.setFont(QFont('Arial', 20))
#             label.setAlignment(Qt.AlignCenter)
 
#         layout = QVBoxLayout()
#         layout.addWidget(title)
#         layout.addSpacing(30)
#         layout.addWidget(tab1)
#         layout.addWidget(tab2)
#         layout.addWidget(tab3)
#         layout.addWidget(tab4)
#         self.back_btn = QPushButton("Back to Home")
#         self.back_btn.setStyleSheet("background-color: black; color: white; padding: 15px 30px; border-radius: 10px;")
#         self.back_btn.setFont(QFont('Arial', 18))
#         self.back_btn.clicked.connect(self.return_home_callback)
#         layout.addWidget(self.back_btn, alignment=Qt.AlignCenter)
#         layout.addStretch()
 
#         self.setLayout(layout)
 


class SessionDatabase:
    def __init__(self, db_path="sessions.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.setup_database()

    def setup_database(self):
#         self.cursor.execute("""
#     DROP TABLE IF EXISTS sessions
# """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                planned_session_length INTEGER,
                actual_session_length INTEGER,
                focus_time INTEGER,
                total_distraction_time INTEGER,
                distractions INTEGER,
                audio_alert_type TEXT,
                distraction_limit INTEGER,
                notes TEXT,
                interrupted BOOLEAN,
                completion_rate REAL
            )
        """)
        self.conn.commit()

    def save_session(self, planned_session_length, actual_session_length, focus_time, total_distraction_time,
                 distractions, audio_alert_type, distraction_limit, notes="", interrupted=False):
        # completion_rate = round((planned_session_length / actual_session_length) * 100, 2) if actual_session_length > 0 else 0.0
        completion_rate = round((actual_session_length / planned_session_length) * 100, 2) if planned_session_length > 0 else 0.0
        timestamp = datetime.now().isoformat()

        self.cursor.execute("""
        INSERT INTO sessions (
            timestamp, planned_session_length, actual_session_length, focus_time,
            total_distraction_time, distractions, audio_alert_type, distraction_limit,
            notes, interrupted, completion_rate
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        timestamp, planned_session_length, actual_session_length, focus_time,
        total_distraction_time, distractions, audio_alert_type, distraction_limit,
        notes, interrupted, completion_rate
         ))
        self.conn.commit()
    

    def close(self):
        self.conn.close()
    
class SessionHistoryPage(QWidget):
    def __init__(self, db, return_home_callback):
        super().__init__()
        self.db = db
        self.return_home_callback = return_home_callback
        self.initUI()

    def initUI(self):
        self.setStyleSheet("background-color: white;")
        layout = QVBoxLayout()

        title = QLabel("📊 Session History")
        title.setFont(QFont('Arial', 28, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        layout.addSpacing(20)

        # Table for sessions
        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
        "Date", "Planned Duration", "Actual Duration", "Focus Duration",
        "Distraction Time", "Distractions", "Audio Type", "Ended Early", "Completion (%)"
        ])
        self.load_data()
        layout.addWidget(self.table)

        # Back button
        back_btn = QPushButton("Back to Home")
        back_btn.setFont(QFont('Segoe UI', 14))
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #00adb5;
                color: white;
                border: none;
                border-radius: 20px;
                padding: 12px 24px;
            }
            QPushButton:hover {
                background-color: #00cfd1;
            }
            QPushButton:pressed {
                background-color: #009a9e;
            }
        """)
        back_btn.clicked.connect(self.return_home_callback)
        layout.addWidget(back_btn, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def load_data(self):
        self.table.setRowCount(0)
        self.db.cursor.execute("""
        SELECT timestamp, planned_session_length, actual_session_length, focus_time, total_distraction_time,
            distractions, audio_alert_type, interrupted, completion_rate
        FROM sessions ORDER BY id DESC
    """)
        for row_idx, row_data in enumerate(self.db.cursor.fetchall()):
            self.table.insertRow(row_idx)
            for col_idx, value in enumerate(row_data):
                print(f"[DEBUG] Column {col_idx}, Raw Value: {value}, Type: {type(value)}")
                if col_idx == 0:
                    # Format timestamp
                    value = value.split("T")[0] + " " + value.split("T")[1].split(".")[0]
                # elif col_idx == 1 or col_idx == 2:
                #     try:
                #         total_seconds = int(float(value)) if value is not None else 0
                #         minutes = total_seconds // 60
                #         seconds = total_seconds % 60
                #         value = f"{minutes:02d}:{seconds:02d}"
                #     except Exception as e:
                #         print(f"[ERROR] Converting time: {value} – {e}")
                #         value = "00:00"
                elif col_idx in [1, 2, 3, 4]:
                    try:
                        total_seconds = int(float(value)) if value is not None else 0
                        minutes = total_seconds // 60
                        seconds = total_seconds % 60
                        value = f"{minutes:02d}:{seconds:02d}"
                    except Exception as e:
                        print(f"[ERROR] Converting time: {value} – {e}")
                        value = "00:00"
                # elif col_idx == 5:
                #     value = "Yes" if value else "No"
                # elif col_idx == 6:
                #     value = f"{value:.1f}%"
                # elif col_idx == 6:  # This is 'interrupted' boolean
                #     value = "Yes" if value else "No"
                # elif col_idx == 7:  # This is 'completion_rate' float
                #     value = f"{value:.1f}%"
                elif col_idx == 7:  # interrupted boolean
                    value = "Yes" if value else "No"
                elif col_idx == 8:  # completion_rate float
                    value = f"{value:.1f}%"
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
        self.table.resizeColumnsToContents()

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
        self.max_distraction_time = self.settings_page.get_settings()['timeout']
        
        self.session_page = SessionPage(self.go_to_ml_page)
        self.live_view_page = LiveViewPage(self.return_to_home)
        self.main_menu = MainMenu(self.go_to_live_view, self.go_to_session, self.go_to_settings, self.go_to_history)
        self.db = SessionDatabase()
        self.summary_page = SummaryPage(self.db, self.return_to_home)
        self.history_page = SessionHistoryPage(self.db, self.return_to_home)
        self.central_widget.addWidget(self.history_page)
        self.ml_page = MLPage(self.db, self.go_to_summary, self.return_to_home)
        self.ml_page.selected_sound = self.settings_page.get_settings()['sound']
        self.ml_page.max_distraction_duration = self.settings_page.get_settings()['distraction_tolerance']
        
        # Add all pages
        self.central_widget.addWidget(self.history_page)
        self.central_widget.addWidget(self.main_menu)
        self.central_widget.addWidget(self.live_view_page)
        self.central_widget.addWidget(self.session_page)
        self.central_widget.addWidget(self.ml_page)
        self.central_widget.addWidget(self.settings_page)
        self.central_widget.addWidget(self.summary_page)

        # ✅ Set the starting page explicitly
        self.central_widget.setCurrentWidget(self.main_menu)
        
    

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
        
    def go_to_history(self):
        self.history_page.load_data()  # Refresh data each time
        self.central_widget.setCurrentWidget(self.history_page)

    def go_to_ml_page(self):
        self.ml_page.start_camera()
        session_length_min = self.settings_page.session_length_input.value()
        session_length_sec = session_length_min * 60
        self.ml_page.start_session_timer(session_length_sec, planned_session_length=session_length_sec)


        # Set distraction limit from settings
        settings = self.settings_page.get_settings()
        self.ml_page.max_distraction_duration = settings['distraction_tolerance']
        self.ml_page.selected_sound = settings['sound']


        # self.ml_page.start_session_timer(session_length_sec)
        self.central_widget.setCurrentWidget(self.ml_page)
 
    def go_to_settings(self):
        self.central_widget.setCurrentWidget(self.settings_page)
 
    # def go_to_summary(self):
    #     self.central_widget.setCurrentWidget(self.summary_page)
    def go_to_summary(self):
        self.summary_page.populate_summary()  # 💡 Refresh data
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