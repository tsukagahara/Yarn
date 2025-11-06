import sys
import os
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PySide6.QtGui import QIcon

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_main_app()
    
    def setup_main_app(self):
        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle("Yarn")
        
        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                "resources", "icons", "ico", "Yarn-256.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout(central_widget)
        
        self.create_widgets()
    
    def create_widgets(self):
        print() #указывать виджеты тут
    
    def on_close(self):
        self.close()
    
    def run(self):
        self.show()