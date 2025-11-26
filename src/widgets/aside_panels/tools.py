from PySide6.QtWidgets import QWidget, QVBoxLayout
# from PySide6.QtGui import QFont
# from PySide6.QtCore import Qt
# import os
# import utils.helpers as helpers

class ToolsPanel(QWidget):
    def __init__(self, base_path):
        super().__init__()
        self.base_path = base_path
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
        
        self.layout.addStretch()

    def on_tools_clicked(self, path, name_btn):
        """Tools click handler"""

        # Reload panel
        self.reload_tools()

    # def reload_tools(self):
    #     """Reload panel tools"""
    #     # Delite all
    #     # TODO: delete widgets
    #     # Cleaning layout
    #     while self.layout.count():
    #         child = self.layout.takeAt(0)
    #         if child.widget():
    #             child.widget().deleteLater()
        
        # Reload
        # self.load_tools()

    def show_panel(self):
        self.show()

    def hide_panel(self):
        self.hide()
    
    # def apply_theme(self):
    #     """
    #     Applies color theme to UI elements using CSS styling.
    #     Updates main widget and button styles with theme colors.
    #     """
    #     # Extract theme colors
    #     self.bg_card = self.theme.get('bg_card')
    #     self.bg_color = self.theme.get('bg_color')
    #     self.accent_color = self.theme.get('accent_color')
    #     self.accent_primary = self.theme.get('accent_primary')
    #     self.text_main = self.theme.get('text_main')
    #     self.btn_bg_color = self.theme.get('btn_bg_color')
    #     self.btn_hover_bg_color = self.theme.get('btn_hover_bg_color')

    #     # Refresh UI
    #     self.update()