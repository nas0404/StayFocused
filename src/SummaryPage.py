from PyQt5.QtWidgets import (
    QWidget, QPushButton, QLabel, QVBoxLayout, QTextEdit, QGraphicsDropShadowEffect, QMessageBox
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt

class SummaryPage(QWidget):
    def __init__(self, db, return_home_callback):
        super().__init__()
        self.db = db
        self.return_home_callback = return_home_callback
        self.initUI()
        self.populate_summary()

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

        self.focus_label = QLabel()
        self.distractions_label = QLabel()
        self.completion_label = QLabel()

        for lbl in [self.focus_label, self.distractions_label, self.completion_label]:
            lbl.setFont(QFont("Segoe UI", 20))
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setStyleSheet("color: #cccccc;")

        layout.addWidget(self.focus_label)
        layout.addWidget(self.distractions_label)
        layout.addWidget(self.completion_label)

        # NEW: Notes input field
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Optional: Reflect on your session or write notes...")
        self.notes_input.setStyleSheet("background-color: white; color: black; padding: 12px; border-radius: 10px;")
        self.notes_input.setFont(QFont("Segoe UI", 14))
        self.notes_input.setMinimumHeight(120)
        layout.addWidget(self.notes_input)

        # NEW: Save Notes button
        save_btn = QPushButton("💾 Save Notes")
        save_btn.setFont(QFont("Segoe UI Semibold", 14))
        save_btn.setCursor(Qt.PointingHandCursor)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 20px;
                padding: 14px 30px;
            }
            QPushButton:hover {
                background-color: #33c961;
            }
            QPushButton:pressed {
                background-color: #228c3c;
            }
        """)
        save_btn.clicked.connect(self.save_notes)
        layout.addWidget(save_btn, alignment=Qt.AlignCenter)

        # Back to Home button
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

        outer_layout = QVBoxLayout(self)
        outer_layout.addStretch()
        outer_layout.addWidget(self.panel, alignment=Qt.AlignCenter)
        outer_layout.addStretch()
        self.setLayout(outer_layout)

    def populate_summary(self):
        self.db.cursor.execute("SELECT COUNT(*), SUM(focus_time), AVG(completion_rate) FROM sessions")
        count, total_focus, avg_completion = self.db.cursor.fetchone()

        self.db.cursor.execute("""
            SELECT distractions, total_distraction_time, actual_session_length
            FROM sessions ORDER BY id DESC LIMIT 1
        """)
        latest = self.db.cursor.fetchone()


        if latest:
            distractions, distraction_time, actual_duration = latest
            self.distractions_label.setText(f"Distractions This Session: {distractions}")

            if actual_duration > 0:
                percent_distracted = (distraction_time / actual_duration) * 100
                self.focus_label.setText(f"Time Spent Distracted: {percent_distracted:.1f}%")
            else:
                self.focus_label.setText("Time Spent Distracted: N/A")
        else:
            self.distractions_label.setText("Distractions This Session: 0")
            self.focus_label.setText("Time Spent Distracted: N/A")

            self.distractions_label.setText(f"Distractions This Session: {latest[0] if latest else 0}")
        
        if avg_completion is not None:
            self.completion_label.setText(f"Average Completion Rate: {avg_completion:.1f}%")
        else:
            self.completion_label.setText("Average Completion Rate: N/A")

    def save_notes(self):
        notes = self.notes_input.toPlainText().strip()
        if notes:
            self.db.update_last_session_notes(notes)
            QMessageBox.information(self, "Notes Saved", "Your notes were saved successfully.")
        else:
            QMessageBox.information(self, "Empty Notes", "No notes entered.")
