import sqlite3
from datetime import datetime

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