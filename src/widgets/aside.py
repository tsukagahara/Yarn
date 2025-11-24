from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QPushButton
from PySide6.QtCore import Qt
import json
import os
import utils.helpers as helpers
import utils.aside_manager as al
# from PySide6.QtGui import

class aside(QWidget):
    def __init__(self, parent=None, theme=None):
        super().__init__(parent)
        self.theme = theme
        self.setMouseTracking(True)
        self.setFixedWidth(50)
        
        # Создаем widget1 ДО setup_ui()
        self.widget1 = QFrame()
        self.btn_toggle = QPushButton(">>")
        
        al.init_widget(self)  # ← передаем self в al
        
        self.setup_ui()
        self.apply_theme()
        self.btn_toggle.clicked.connect(al.aside_state)
    
    def setup_ui(self):
        """
Creates a layout with two main panels:
- Left panel (widget1): fixed control panel with buttons
- Right panel (widget2): hidden by default side panel with content

UI Architecture:
┌────────────────────────────────────────┐
│ main_layout (QVBoxLayout)              │
│ ┌────────────────────────────────────┐ │
│ │ content_frame (QFrame)             │ │
│ │ ┌─────────────┐ ┌────────────────┐ │ │
│ │ │ widget1     │ │ widget2        │ │ │
│ │ │ (50px wide) │ │ (aside panel)  │ │ │
│ │ │ ┌─────────┐ │ │ ┌────────────┐ │ │ │
│ │ │ │ btn_a   │ │ │ │ label2     │ │ │ │
│ │ │ │ btn_b   │ │ │ │            │ │ │ │
│ │ │ │ ...     │ │ │ │            │ │ │ │
│ │ │ └─────────┘ │ │ └────────────┘ │ │ │
│ │ └─────────────┘ └────────────────┘ │ │
│ └────────────────────────────────────┘ │
└────────────────────────────────────────┘

Widgets:
- self.btn_a: button to toggle side panel visibility
- btn_b, btn_c, btn_d, btn_e: additional buttons (placeholders)
- self.widget2: hidden side panel, controlled by btn_a

States:
- Default: widget1 visible, widget2 hidden
- When btn_a is clicked: widget2 appears/disappears
        """
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        self.content_frame = QFrame()
        
        content_layout = QHBoxLayout(self.content_frame)
        content_layout.setAlignment(Qt.AlignTop)
        content_layout.setSpacing(0)
        content_layout.setContentsMargins(0, 0, 0, 0)

        # left control panel
        self.widget1.setFixedWidth(50)
        self.btn_toggle = QPushButton(">>")
        self.btn_toggle.setToolTip("Боковая панель")

        self.btn_workspaces = QPushButton("🗂")
        self.btn_workspaces.setToolTip("Пространства")
        self.btn_workspaces.clicked.connect(al.btn_workspaces_clicked)

        self.btn_tools = QPushButton("🛠") 
        self.btn_tools.setToolTip("Инструменты")
        self.btn_tools.clicked.connect(al.btn_tools_clicked)

        self.btn_plugins = QPushButton("🧩")
        self.btn_plugins.setToolTip("Плагины")
        self.btn_plugins.clicked.connect(al.btn_plugins_clicked)

        self.btn_settings = QPushButton("⚙")
        self.btn_settings.setToolTip("Настройки")
        self.btn_settings.clicked.connect(al.btn_settings_clicked)
        
        widget1_layout = QVBoxLayout(self.widget1)
        widget1_layout.addWidget(self.btn_toggle)
        widget1_layout.addWidget(self.btn_workspaces)
        widget1_layout.addWidget(self.btn_tools)
        widget1_layout.addWidget(self.btn_plugins)
        widget1_layout.addWidget(self.btn_settings)
        
        # right side panel 
        self.widget2 = QFrame()
        self.widget2.hide()
        
        label2 = QLabel()
        widget2_layout = QVBoxLayout(self.widget2)
        widget2_layout.addWidget(label2)
        
        # add_widgets_to_main_layout 
        content_layout.addWidget(self.widget1)
        content_layout.addWidget(self.widget2)
        
        main_layout.addWidget(self.content_frame)

    def apply_theme(self):
        """
        Applies color theme to UI elements using CSS styling.
        Updates main widget and button styles with theme colors.
        """
        # Extract theme colors
        self.bg_card = self.theme.get('bg_card')
        self.bg_color = self.theme.get('bg_color')
        self.accent_color = self.theme.get('accent_color')
        self.accent_primary = self.theme.get('accent_primary')
        self.text_main = self.theme.get('text_main')
        self.btn_bg_color = self.theme.get('btn_bg_color')
        self.btn_hover_bg_color = self.theme.get('btn_hover_bg_color')

        # Refresh UI
        self.update()
        
        # Apply main widget styling
        self.setStyleSheet(f"""
                background-color: {self.bg_card}; 
                color: {self.text_main};
            """)
    
    # Apply button styling to content frame
        self.content_frame.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.btn_bg_color};
                color: {self.text_main};
                border: 1px solid {self.accent_color};
                padding: 5px;
                border-radius: 3px;
            }}
            
            QPushButton:hover {{
                background-color: {self.btn_hover_bg_color};
                border: 1px solid {self.accent_primary};
            }}
            
            QPushButton:pressed {{
                background-color: {self.accent_primary};
                color: {self.accent_color}
            }}
            QToolTip {{
                background-color: #2b2b2b;
                color: #ffffff;
                border: 1px solid #555555;
                padding: 4px;
                border-radius: 3px;
            }}
            """)