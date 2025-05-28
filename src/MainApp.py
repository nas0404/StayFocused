import sys
from PyQt5.QtWidgets import (
    QApplication, QStackedWidget, QMainWindow
)
from src.MainMenu import MainMenu
from src.SessionDatabase import SessionDatabase
from src.SessionHistory import SessionHistoryPage
from src.SessionPage import SessionPage
from src.SettingsPage import SettingsPage
from src.SummaryPage import SummaryPage
from src.CameraViewPage import LiveViewPage, MLPage
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
        
        self.central_widget.addWidget(self.history_page)
        self.central_widget.addWidget(self.main_menu)
        self.central_widget.addWidget(self.live_view_page)
        self.central_widget.addWidget(self.session_page)
        self.central_widget.addWidget(self.ml_page)
        self.central_widget.addWidget(self.settings_page)
        self.central_widget.addWidget(self.summary_page)

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
        self.history_page.load_data()
        self.central_widget.setCurrentWidget(self.history_page)

    def go_to_ml_page(self):
        self.ml_page.start_camera()
        session_length_min = self.settings_page.session_length_input.value()
        session_length_sec = session_length_min * 60
        self.ml_page.start_session_timer(session_length_sec, planned_session_length=session_length_sec)

        settings = self.settings_page.get_settings()
        self.ml_page.max_distraction_duration = settings['distraction_tolerance']
        self.ml_page.selected_sound = settings['sound']


        self.central_widget.setCurrentWidget(self.ml_page)
 
    def go_to_settings(self):
        self.central_widget.setCurrentWidget(self.settings_page)
 

    def go_to_summary(self):
        self.ml_page.stop_camera()
        self.summary_page.populate_summary()
        self.central_widget.setCurrentWidget(self.summary_page)
        self.live_view_page.stop_camera()
            
    def return_to_home(self):
        self.live_view_page.stop_camera()
        self.ml_page.stop_camera()
        self.central_widget.setCurrentWidget(self.main_menu)
