from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout,
)
from PyQt5.QtGui import QFont, QColor, QPainter, QBrush
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QPoint
from win10toast_click import ToastNotifier


class Notification(QWidget):
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
        