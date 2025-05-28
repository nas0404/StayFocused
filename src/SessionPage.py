
from PyQt5.QtWidgets import (
    QWidget, QPushButton, QLabel, QVBoxLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer
from plyer import notification

class SessionPage(QWidget):
    def __init__(self, go_to_next_page):
        super().__init__()
        self.go_to_next_page = go_to_next_page
        self.initUI()
 
    def initUI(self):
        self.setStyleSheet("background-color: white;")
 
        self.circle_label = QLabel("Sit up\nstraight!")
        self.circle_label.setAlignment(Qt.AlignCenter)
        self.circle_label.setFont(QFont('Arial', 24, QFont.Bold)) 
        self.circle_label.setFixedSize(300, 300)
        self.circle_label.setWordWrap(True)  
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
    def start_countdown(self, seconds):
        self.counter = seconds
        self.countdown_label.setText(str(self.counter))
        self.countdown_label.show()
        self.continue_btn.hide()
        self.timer.start(1000)  
    
    def update_countdown(self):
        self.counter -= 1
        self.countdown_label.setText(str(self.counter))
        if self.counter <= 0:
            self.timer.stop()
            self.countdown_label.hide()
            self.go_to_next_page()