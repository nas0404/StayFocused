import sys
import cv2
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QVBoxLayout,
    QHBoxLayout, QStackedWidget, QMainWindow, QSpacerItem, QSizePolicy, QSpinBox, QCheckBox, QSlider
)
from PyQt5.QtGui import QIcon, QFont, QImage, QPixmap
from PyQt5.QtCore import Qt, QTimer
 
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
        self.countdown_label.setFont(QFont('Arial', 48))
 
        self.continue_btn = QPushButton("Start Session")
        self.continue_btn.setStyleSheet("background-color: black; color: white; padding: 15px 30px; border-radius: 10px;")
        self.continue_btn.setFont(QFont('Arial', 18))
        self.continue_btn.clicked.connect(self.go_to_next_page)
        self.continue_btn.hide()
 
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
        self.timer.start(1000)
 
    def update_countdown(self):
        self.counter -= 1
        if self.counter > 0:
            self.countdown_label.setText(str(self.counter))
        else:
            self.timer.stop()
            self.countdown_label.hide()
            self.continue_btn.show()
 
 
class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
 
    def initUI(self):
        self.setStyleSheet("background-color: white;")
 
        title = QLabel("Settings")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont('Arial', 36, QFont.Bold))
 
        subtitle = QLabel("Set Timer")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setFont(QFont('Arial', 20))
 
        timer_frame = QWidget()
        timer_frame.setStyleSheet("background-color: #2C2C2E; border-radius: 20px; color: white;")
        timer_layout = QVBoxLayout()
        timer_layout.setContentsMargins(30, 30, 30, 30)
 
        reminder_label = QLabel("Set Reminder (minutes : seconds)")
        reminder_label.setFont(QFont('Arial', 14))
        reminder_label.setStyleSheet("color: lightgray;")
 
        time_input_layout = QHBoxLayout()
        self.minute_input = QSpinBox()
        self.minute_input.setRange(0, 59)
        self.minute_input.setFont(QFont('Arial', 20))
        self.minute_input.setFixedWidth(100)
 
        self.second_input = QSpinBox()
        self.second_input.setRange(0, 59)
        self.second_input.setFont(QFont('Arial', 20))
        self.second_input.setFixedWidth(100)
 
        colon = QLabel(":")
        colon.setFont(QFont('Arial', 24))
        colon.setAlignment(Qt.AlignCenter)
 
        time_input_layout.addWidget(QLabel("Min"))
        time_input_layout.addWidget(colon)
        time_input_layout.addWidget(self.minute_input)
        colon2 = QLabel(":")
        colon2.setFont(QFont('Arial', 24))
        colon2.setAlignment(Qt.AlignCenter)
        time_input_layout.addWidget(QLabel("Sec"))
        time_input_layout.addWidget(self.second_input)
 
        button_layout = QHBoxLayout()
        self.cancel_btn = QPushButton("Cancel")
        self.ok_btn = QPushButton("OK")
        for btn in [self.cancel_btn, self.ok_btn]:
            btn.setStyleSheet("color: white;")
            btn.setFont(QFont('Arial', 12))
        self.cancel_btn.clicked.connect(self.return_home)
        self.ok_btn.clicked.connect(self.confirm_settings)
        button_layout.addWidget(self.cancel_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.ok_btn)
 
        timer_layout.addWidget(reminder_label)
        timer_layout.addLayout(time_input_layout)
        timer_layout.addSpacing(10)
        timer_layout.addLayout(button_layout)
        timer_frame.setLayout(timer_layout)
 
 
 
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(50)
        self.volume_slider.setFixedWidth(300)
        self.volume_slider.setStyleSheet("QSlider::handle:horizontal { background: white; border: 1px solid #999999; width: 14px; margin: -4px 0; border-radius: 7px; }")
 
        session_length_label = QLabel("Set Session Length (minutes)")
        session_length_label.setAlignment(Qt.AlignCenter)
        session_length_label.setFont(QFont('Arial', 20, QFont.Bold))
 
        self.session_length_input = QSpinBox()
        self.session_length_input.setRange(1, 180)
        self.session_length_input.setValue(25)
        self.session_length_input.setFont(QFont('Arial', 18))
        self.session_length_input.setFixedWidth(150)
 
        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addSpacing(10)
        layout.addWidget(subtitle)
        layout.addSpacing(10)
        layout.addWidget(timer_frame, alignment=Qt.AlignCenter)
 
        button_row = QHBoxLayout()
        self.cancel_btn = QPushButton("Cancel")
        self.ok_btn = QPushButton("OK")
        for btn in [self.cancel_btn, self.ok_btn]:
            btn.setStyleSheet("background-color: black; color: white; padding: 20px 40px; border-radius: 12px;")
            btn.setFont(QFont('Arial', 20))
        self.cancel_btn.clicked.connect(self.return_home)
        self.ok_btn.clicked.connect(self.confirm_settings)
        button_row.addStretch()
        button_row.addWidget(self.cancel_btn)
        button_row.addSpacing(40)
        button_row.addWidget(self.ok_btn)
        button_row.addStretch()
       
        layout.addSpacing(30)
        layout.addWidget(self.volume_slider, alignment=Qt.AlignCenter)
        layout.addSpacing(30)
        layout.addWidget(session_length_label)
        layout.addWidget(self.session_length_input, alignment=Qt.AlignCenter)
        layout.addSpacing(30)
        layout.addLayout(button_row)
        layout.addStretch()
 
        self.setLayout(layout)
 
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
            'session_length': self.session_length_input.value()
        }
 
 
class MainMenu(QWidget):
    def __init__(self, go_live_view_callback, go_session_callback, go_to_settings_callback):
        super().__init__()
        self.go_live_view_callback = go_live_view_callback
        self.go_session_callback = go_session_callback
        self.go_to_settings_callback = go_to_settings_callback
        self.initUI()
 
    def initUI(self):
        self.setStyleSheet("background-color: white;")
        self.title = QLabel("Welcome to StayFocused")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setFont(QFont('Arial', 48))
 
        self.calibrate_btn = QPushButton("Calibrate")
        self.start_btn = QPushButton("Start Session")
        self.live_view_btn = QPushButton("Live View")
        self.live_view_btn.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: white;
                padding: 12px 24px;
                border-radius: 10px;
                font-size: 16px;
            }
        """)
        self.live_view_btn.setFont(QFont('Arial', 16))
        self.live_view_btn.setFixedSize(180, 40)
        self.settings_icon = QPushButton("⚙️")
 
        for btn in [self.calibrate_btn, self.start_btn]:
            btn.setStyleSheet("background-color: black; color: white; padding: 30px 60px; border-radius: 16px;")
            btn.setFont(QFont('Arial', 28))
            btn.setMinimumWidth(500)
            btn.setMinimumHeight(80)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
 
        self.live_view_btn.setStyleSheet("background-color: black; color: white; padding: 12px 24px; border-radius: 10px;")
        self.live_view_btn.setFont(QFont('Arial', 16))
        self.live_view_btn.setFixedWidth(140)
        self.live_view_btn.clicked.connect(self.go_live_view_callback)
        self.start_btn.clicked.connect(self.go_session_callback)
 
        self.settings_icon.setFont(QFont('Arial', 32))
        self.settings_icon.setFixedSize(70, 70)
        self.settings_icon.setStyleSheet("border: none;")
        self.settings_icon.clicked.connect(self.go_to_settings_callback)
 
        self.vbox_center = QVBoxLayout()
        self.vbox_center.setSpacing(60)
        self.vbox_center.addWidget(self.title)
        self.vbox_center.addWidget(self.calibrate_btn, alignment=Qt.AlignCenter)
        self.vbox_center.addWidget(self.start_btn, alignment=Qt.AlignCenter)
        self.vbox_center.addWidget(self.settings_icon, alignment=Qt.AlignCenter)
 
        self.hbox_bottom = QHBoxLayout()
        self.hbox_bottom.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.hbox_bottom.addWidget(self.live_view_btn)
        self.hbox_bottom.setContentsMargins(0, 0, 40, 40)
 
        self.outer_layout = QVBoxLayout()
        self.outer_layout.addStretch()
        self.outer_layout.addLayout(self.vbox_center)
        self.outer_layout.addStretch()
        self.outer_layout.addLayout(self.hbox_bottom)
        self.setLayout(self.outer_layout)
 
 
 
 
from tensorflow.keras.models import load_model
import numpy as np
 
class CameraView(QWidget):
    def __init__(self, return_home_callback):
        super().__init__()
        self.return_home_callback = return_home_callback
        self.cap = None  # Initialize cap as None
        # Load your trained CNN model
        self.model = load_model("C:/Users/nasee/OneDrive/Documents/GitHub/Stay/vgg16dropout.keras")

# Load face detector (Haar cascade)
        self.face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
 
# Map numeric model output to labels
        self.label_map = {0: "INACTIVE", 1: "ACTIVE"}
        self.initUI()
 
    def initUI(self):
        self.setStyleSheet("background-color: white;")
 
        self.title = QLabel("Say Hi!")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setFont(QFont('Arial', 36))
 
        self.video_label = QLabel("Loading camera...")
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setFont(QFont('Arial', 24))
 
        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.video_label)
        layout.addSpacing(30)
        layout.setContentsMargins(40, 40, 40, 40)
        self.setLayout(layout)
 
    def start_camera(self):
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not self.cap.isOpened():
            self.video_label.setText("No camera detected.")
        else:
            self.timer = QTimer()
            self.timer.timeout.connect(self.update_frame)
            self.timer.start(30)
 
def update_frame(self):
    ret, frame = self.cap.read()
    if not ret:
        self.video_label.setText("Camera error.")
        return
 
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
 
    # Face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
 
    for (x, y, w, h) in faces:
        face = rgb_frame[y:y+h, x:x+w]
        if face.size == 0:
            continue
 
        # Preprocess face for CNN
        face_resized = cv2.resize(face, (224, 224))
        face_normalized = face_resized / 255.0
        face_input = np.expand_dims(face_normalized, axis=0)  # Shape (1, 224, 224, 3)
 
        # Predict expression
        prediction = self.model.predict(face_input)[0]
        label = self.label_map[np.argmax(prediction)]
 
        # Draw bounding box and label
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 255, 0), 2)
 
    # (Optional) Draw Mediapipe landmarks
    results = pose.process(rgb_frame)
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(
            frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
 
    # Convert for display
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = QImage(frame.data, frame.shape[1], frame.shape[0],
                   frame.strides[0], QImage.Format_RGB888)
    self.video_label.setPixmap(QPixmap.fromImage(image))
    # def update_frame(self):
    #     ret, frame = self.cap.read()
    #     if not ret:
    #         self.video_label.setText("Camera error.")
    #         return
 
    #     frame = cv2.flip(frame, 1)
    #     rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
 
    #     # MediaPipe pose detection
    #     results = pose.process(rgb_frame)
 
    #     # Draw landmarks on the original BGR frame
    #     if results.pose_landmarks:
    #         mp_drawing.draw_landmarks(
    #             frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
 
    #     # Convert to RGB for QImage
    #     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
 
    #     # Convert to QImage and display in QLabel
    #     image = QImage(frame.data, frame.shape[1], frame.shape[0],
    #                 frame.strides[0], QImage.Format_RGB888)
    #     self.video_label.setPixmap(QPixmap.fromImage(image))
 
 
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
        self.add_back_button()
 
    def add_back_button(self):
        self.back_btn = QPushButton("Back to Home")
        self.back_btn.setStyleSheet("background-color: black; color: white; padding: 12px 24px; border-radius: 10px;")
        self.back_btn.setFont(QFont('Arial', 16))
        self.back_btn.clicked.connect(self.return_home_callback)
        self.layout().addWidget(self.back_btn, alignment=Qt.AlignCenter)
 
# class MLPage(CameraView):
#     def __init__(self, go_to_summary_callback, return_home_callback):
#         self.go_to_summary_callback = go_to_summary_callback
#         super().__init__(return_home_callback)  # Initializes layout
 
#         self.title.setText("You're now free to work")
 
#         self.end_session_btn = QPushButton("End Session")
#         self.end_session_btn.setStyleSheet("background-color: black; color: white; padding: 15px 30px; border-radius: 10px;")
#         self.end_session_btn.setFont(QFont('Arial', 18))
#         self.end_session_btn.clicked.connect(self.go_to_summary_callback)
 
#         self.layout().addWidget(self.end_session_btn, alignment=Qt.AlignCenter)
 
class MLPage(CameraView):
    def __init__(self, go_to_summary_callback, return_home_callback):
        self.go_to_summary_callback = go_to_summary_callback
        super().__init__(return_home_callback)  # Initializes layout
 
        self.title.setText("You're now free to work")
 
        self.session_timer_label = QLabel("")
        self.session_timer_label.setFont(QFont('Arial', 24))
        self.layout().insertWidget(1, self.session_timer_label)  # Show timer under title
 
        self.end_session_btn = QPushButton("End Session")
        self.end_session_btn.setStyleSheet("background-color: black; color: white; padding: 15px 30px; border-radius: 10px;")
        self.end_session_btn.setFont(QFont('Arial', 18))
        self.end_session_btn.clicked.connect(self.go_to_summary_callback)
 
        self.layout().addWidget(self.end_session_btn, alignment=Qt.AlignCenter)
 
        self.session_timer = QTimer()
        self.session_timer.timeout.connect(self.update_session_timer)
        self.session_seconds_left = 0
 
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
        self.setStyleSheet("background-color: white;")
        self.setMinimumSize(1024, 768)
        self.showMaximized()
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
 
        self.settings_page = SettingsPage()
        # self.summary_page = SummaryPage()
        self.summary_page = SummaryPage(self.return_to_home)
        self.max_distraction_time = self.settings_page.get_settings()['timeout']
        self.ml_page = MLPage(self.go_to_summary, self.return_to_home)
        self.focus_timer_page = FocusTimerPage(self.go_to_ml_page)
        self.session_page = SessionPage(self.go_to_focus_timer)
        self.live_view_page = LiveViewPage(self.return_to_home)
        self.main_menu = MainMenu(self.go_to_live_view, self.go_to_session, self.go_to_settings)
 
        self.central_widget.addWidget(self.main_menu)
        self.central_widget.addWidget(self.live_view_page)
        self.central_widget.addWidget(self.session_page)
        self.central_widget.addWidget(self.focus_timer_page)
        self.central_widget.addWidget(self.ml_page)
        self.central_widget.addWidget(self.settings_page)
        self.central_widget.addWidget(self.summary_page)
 
    def go_to_live_view(self):
        self.ml_page.stop_camera()
        self.live_view_page.stop_camera()
        self.live_view_page.start_camera()
        self.central_widget.setCurrentWidget(self.live_view_page)
 
 
    def go_to_session(self):
        self.central_widget.setCurrentWidget(self.session_page)
 
    def go_to_focus_timer(self):
        # self.focus_timer_page.seconds = self.settings_page.get_settings()['timeout']
        # mins = self.focus_timer_page.seconds // 60
        # secs = self.focus_timer_page.seconds % 60
        # self.focus_timer_page.timer_display.setText(f"{mins:02d}:{secs:02d}")
        # self.focus_timer_page.timer.start(1000)
        # self.central_widget.setCurrentWidget(self.focus_timer_page)
        self.focus_timer_page.seconds = 5  # Always 10 seconds for pre-session countdown
        self.focus_timer_page.timer_display.setText("00:05")
        self.focus_timer_page.timer.start(1000)
        self.central_widget.setCurrentWidget(self.focus_timer_page)
 
    # def go_to_ml_page(self):
    #     self.ml_page.start_camera()  # ← Explicitly start camera
    #     self.central_widget.setCurrentWidget(self.ml_page)
    def go_to_ml_page(self):
        self.ml_page.start_camera()
        session_length_min = self.settings_page.session_length_input.value()
        session_length_sec = session_length_min * 60
        self.ml_page.start_session_timer(session_length_sec)
        self.central_widget.setCurrentWidget(self.ml_page)
 
    def go_to_settings(self):
        self.central_widget.setCurrentWidget(self.settings_page)
 
    def go_to_summary(self):
        self.central_widget.setCurrentWidget(self.summary_page)
 
    # def return_to_home(self):
    #     self.central_widget.setCurrentWidget(self.main_menu)
   
    def return_to_home(self):
        self.live_view_page.stop_camera()
        self.ml_page.stop_camera()
        self.central_widget.setCurrentWidget(self.main_menu)
 
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())