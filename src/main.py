import sys
from PyQt6.QtWidgets import QApplication
from controllers.character_controller import CharacterController
from views.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    
    # Initialize controller
    controller = CharacterController()
    
    # Create and show main window
    window = MainWindow(controller)
    window.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
