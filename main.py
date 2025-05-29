from src.MainApp import MainApp
from PyQt5.QtWidgets import QApplication, QMessageBox
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Consent popup
    consent_box = QMessageBox()
    consent_box.setIcon(QMessageBox.Question)
    consent_box.setWindowTitle("User Consent")
    consent_box.setText("Do you consent to allowing camera access and saving session data for your productivity tracking?")
    consent_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    consent_box.setDefaultButton(QMessageBox.Yes)
    consent = consent_box.exec_()

    if consent == QMessageBox.Yes:
        from src.MainApp import MainApp  # Replace with your actual main window class file
        window = MainApp()
        window.show()
        sys.exit(app.exec_())
    else:
        sys.exit()

