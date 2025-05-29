from PyQt5.QtWidgets import (
    QWidget, QPushButton, QLabel, QVBoxLayout,
    QTableWidget, QTableWidgetItem
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox



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
        self.table.setColumnCount(10)
        self.table.setHorizontalHeaderLabels([
            "Date", "Planned Duration", "Actual Duration", "Focus Duration",
            "Distraction Time", "Distractions", "Audio Type", "Ended Early", "Completion (%)", "View Note"
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
    from PyQt5.QtWidgets import QMessageBox

    def show_note_popup(self, note):
        note = note.strip() if note else "(No notes for this session)"
        QMessageBox.information(self, "Session Note", note)
    def load_data(self):
        self.table.setRowCount(0)
        self.db.cursor.execute("""
            SELECT timestamp, planned_session_length, actual_session_length, focus_time,
                total_distraction_time, distractions, audio_alert_type, interrupted, completion_rate, notes
            FROM sessions ORDER BY id
        """)

        for row_idx, row in enumerate(self.db.cursor.fetchall()):
            self.table.insertRow(row_idx)
            timestamp, planned, actual, focus, distraction, distractions, audio_type, interrupted, completion, note = row

            values = [
                timestamp.split("T")[0] + " " + timestamp.split("T")[1].split(".")[0],  # formatted date
                planned, actual, focus, distraction, distractions,
                audio_type, "Yes" if interrupted else "No", f"{completion:.1f}%"
            ]

            # Format time columns
            for col_idx, val in enumerate(values):
                if col_idx in [1, 2, 3, 4]:  # Time columns
                    total_seconds = int(float(val)) if val is not None else 0
                    minutes = total_seconds // 60
                    seconds = total_seconds % 60
                    val = f"{minutes:02d}:{seconds:02d}"
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(val)))

            # Add "View" button for the note
            view_btn = QPushButton("View")
            view_btn.setStyleSheet("""
                QPushButton {
                    background-color: #00adb5;
                    color: white;
                    border: none;
                    border-radius: 12px;
                    padding: 6px 16px;
                }
                QPushButton:hover {
                    background-color: #00cfd1;
                }
                QPushButton:pressed {
                    background-color: #009a9e;
                }
            """)
            view_btn.clicked.connect(lambda _, n=note: self.show_note_popup(n))
            self.table.setCellWidget(row_idx, 9, view_btn)
