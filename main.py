import sys
from PySide6.QtWidgets import QApplication
from gui import MancalaGUI  # Import the GUI


if __name__ == "__main__":
    # Initialize and run the application
    app = QApplication(sys.argv)
    window = MancalaGUI()
    window.show()
    sys.exit(app.exec())
