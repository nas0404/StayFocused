from PyQt5.QtWidgets import (
    QWidget, QPushButton, QLabel, QVBoxLayout,
    QHBoxLayout, QSpinBox, QGraphicsDropShadowEffect
)
from PyQt5.QtGui import QIcon, QFont, QImage, QPixmap, QColor, QPainter, QBrush
from PyQt5.QtCore import Qt, QTimer, QTime, QPropertyAnimation, QPoint
from plyer import notification
from win10toast_click import ToastNotifier
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
        self.countdown_input.setValue(5)
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
        colon.setFixedWidth(10)
        
       


        time_input_layout.addWidget(self.minute_input)
        time_input_layout.addWidget(colon)
        time_input_layout.addWidget(self.second_input)
        layout.addLayout(time_input_layout, stretch=0)
        layout.setAlignment(time_input_layout, Qt.AlignCenter)
        
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

        self.sound_group = QButtonGroup(self)
        self.ding_radio = QRadioButton("🔔 Classic Ding")
        self.voice_radio = QRadioButton("🗣️ Voice Alert")

        for btn in [self.ding_radio, self.voice_radio]:
            btn.setFont(QFont('Segoe UI', 16))
            btn.setStyleSheet("color: white;")
            self.sound_group.addButton(btn)

        self.voice_radio.setChecked(True) 

        sound_layout = QHBoxLayout()
        sound_layout.addWidget(self.ding_radio)
        sound_layout.addWidget(self.voice_radio)
        layout.addLayout(sound_layout)



        


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