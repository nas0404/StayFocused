from PyQt5.QtWidgets import (
    QWidget, QPushButton, QLabel, QVBoxLayout,
     QGraphicsDropShadowEffect
)
from PyQt5.QtGui import QIcon, QFont, QImage, QPixmap, QColor, QPainter, QBrush
import cv2
from PyQt5.QtCore import Qt, QTimer, QTime, QPropertyAnimation, QPoint
import numpy as np
import pygame
import pyttsx3
from tensorflow.keras.models import load_model

from src.Notifications import Notification

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
        self.inactive_seconds = 0
        self.active_seconds = 0
        self.last_distraction_warning = False
        self.last_label = None

    def close_Event(self, event):
        self.stop_camera()
        event.accept()
        
        
class MLPage(CameraView):

    def __init__(self,db, go_to_summary_callback, return_home_callback):
        self.db = db
        self.go_to_summary_callback = go_to_summary_callback
        super().__init__(return_home_callback)
        self.inactive_seconds = 0
        self.active_seconds = 0
        self.max_distraction_duration = 10 
        self.last_distraction_warning = False
        self.voice_engine = pyttsx3.init()
        self.activity_timer = 0
        self.last_label = None
        self.focus_time = 0
        self.total_distraction_time = 0
        self.distraction_count = 0

        self.title.setText("You're now free to work")

        self.session_timer_label = QLabel("")
        self.session_timer_label.setFont(QFont('Arial', 24))
        self.panel.layout().insertWidget(1, self.session_timer_label)

        self.end_session_btn = QPushButton("End Session")
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
        self.end_session_btn.clicked.connect(self.handle_manual_session_end)
        self.layout().addWidget(self.end_session_btn, alignment=Qt.AlignCenter)

        self.session_timer = QTimer()
        self.session_timer.timeout.connect(self.update_session_timer)
        self.session_seconds_left = 0

        self.emotion_model = load_model('./mobilenetv2.keras')
        self.emotion_labels = ['Active', 'Inactive']


    def start_session_timer(self, seconds, planned_session_length):
        self.session_seconds_left = seconds
        self.planned_session_length = planned_session_length  
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
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

        predicted_label = 'Inactive'

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
            self.total_distraction_time += 1
            print(f"DEBUG — label: {predicted_label}, inactive_seconds: {self.inactive_seconds}, last_label: {self.last_label}")
            
            if self.inactive_seconds == self.max_distraction_duration and not self.last_distraction_warning:
                print("⚠️ You've been distracted too long! Get back to focus.")
                self.last_distraction_warning = True
                self.distraction_count += 1 

                self.toast = Notification(
                    title="⚠️ Distraction Warning!",
                    message="You've been inactive too long. Time to refocus, big boss",
                    duration=5000
                )
                self.toast.show()

                if self.selected_sound == 'voice':
                    self.voice_engine.say("Come on, you got this, get your head in the game!")
                    self.voice_engine.runAndWait()
                elif self.selected_sound == 'ding':
                    pygame.mixer.init()
                    pygame.mixer.music.load("./dingsound.mp3")  
                    pygame.mixer.music.set_volume(0.6)
                    pygame.mixer.music.play()


        elif predicted_label == 'Active':
            self.active_seconds += 1
            self.focus_time += 1
            if self.last_label == 'Inactive':
                print("✅ You're back on track!")
            if self.active_seconds > 0:
                print(f"DEBUG — label: {predicted_label}, active_seconds: {self.active_seconds}, last_label: {self.last_label}")
            self.inactive_seconds = 0
            self.last_distraction_warning = False
        print(f"[FOCUS DEBUG] Focus Time: {self.focus_time} seconds")
        
        self.last_label = predicted_label

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
        
class LiveViewPage(CameraView):
    def __init__(self, return_home_callback):
        super().__init__(return_home_callback)
 
    def add_back_button(self):
        self.back_btn = QPushButton("Back to Home")
        self.back_btn.setStyleSheet("background-color: black; color: white; padding: 12px 24px; border-radius: 10px;")
        self.back_btn.setFont(QFont('Arial', 16))
        self.back_btn.clicked.connect(self.return_home_callback)
        self.layout().addWidget(self.back_btn, alignment=Qt.AlignCenter)