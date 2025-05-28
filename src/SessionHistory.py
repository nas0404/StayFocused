from PyQt5.QtWidgets import (
    QWidget, QPushButton, QLabel, QVBoxLayout,
    QTableWidget, QTableWidgetItem
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt



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

        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
        "Date", "Planned Duration", "Actual Duration", "Focus Duration",
        "Distraction Time", "Distractions", "Audio Type", "Ended Early", "Completion (%)"
        ])
        self.load_data()
        layout.addWidget(self.table)

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
        FROM sessions ORDER BY id
    """)
        for row_idx, row_data in enumerate(self.db.cursor.fetchall()):
            self.table.insertRow(row_idx)
            for col_idx, value in enumerate(row_data):
                print(f"[DEBUG] Column {col_idx}, Raw Value: {value}, Type: {type(value)}")
                if col_idx == 0:
                    value = value.split("T")[0] + " " + value.split("T")[1].split(".")[0]
                elif col_idx in [1, 2, 3, 4]:
                    try:
                        total_seconds = int(float(value)) if value is not None else 0
                        minutes = total_seconds // 60
                        seconds = total_seconds % 60
                        value = f"{minutes:02d}:{seconds:02d}"
                    except Exception as e:
                        print(f"[ERROR] Converting time: {value} – {e}")
                        value = "00:00"
                elif col_idx == 7: 
                    value = "Yes" if value else "No"
                elif col_idx == 8: 
                    value = f"{value:.1f}%"
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
        self.table.resizeColumnsToContents()