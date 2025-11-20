import os
import json
from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QSizePolicy, QScrollArea
from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QPainter, QColor, QFont, QFontMetrics
import utils.helpers as helpers
import utils.color_utils as color_utils

class tabs(QWidget):
    def __init__(self, theme=None, parent=None):
        super().__init__(parent)
        self.bg_color = None
        self.theme = theme
        self.path_tabs = os.path.join(helpers.get_project_root(), "config", "tabs_config.json")
        self.setup_ui()
        self.apply_theme()
        self.scroll_area.installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj == self.scroll_area and event.type() == QEvent.Wheel:
            scroll_bar = self.scroll_area.horizontalScrollBar()
            delta = event.angleDelta().y()
            scroll_bar.setValue(scroll_bar.value() - delta)
            return True
        return super().eventFilter(obj, event)

    def setup_ui(self):
        self.property_tabs = helpers.get_json_property(self.path_tabs)
        self.count_tabs = len(self.property_tabs)
        self.setObjectName("tabs")
        layout = QHBoxLayout(self)
        self.setFixedHeight(23)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.add_tab_btn = QPushButton("+")
        self.add_tab_btn.setFixedSize(50, 18)
        self.add_tab_btn.setCursor(Qt.PointingHandCursor)
        self.add_tab_btn.setProperty("class", "tab")
        self.add_tab_btn.setFont(QFont("Monospace", 10))
        self.add_tab_btn.clicked.connect(self.on_add_tab_clicked)
        layout.addWidget(self.add_tab_btn)
        
        self.tabs_container = QWidget()
        self.tabs_layout = QHBoxLayout(self.tabs_container)
        self.tabs_layout.setContentsMargins(0, 0, 0, 0)
        self.tabs_layout.setSpacing(0)
        self.tabs_layout.setAlignment(Qt.AlignLeft)
        self.tabs_width = 0
        self.tabs = {}

        self.add_tab()
        
        self.tabs_container.setFixedSize(self.tabs_width + 30, 20)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setFixedHeight(23)
        self.scroll_area.setWidget(self.tabs_container)

        self.scroll_area.setWidgetResizable(False)
        
        layout.addWidget(self.scroll_area)

    def on_add_tab_clicked(self):
        # add: load file
        file_name, directory = helpers.open_file_dialog(self)
        helpers.add_json_property(self.path_tabs, file_name, directory)
        self.reload_tabs()

    def on_remove_tab_clicked(self, name):
        # add: save file
        helpers.remove_json_property(self.path_tabs, name)
        self.reload_tabs()
        

    def reload_tabs(self):
        for i in reversed(range(self.tabs_layout.count())):
            widget = self.tabs_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        self.tabs.clear()
        self.tabs_width = 0
        self.property_tabs = helpers.get_json_property(self.path_tabs)
        self.count_tabs = len(self.property_tabs)
        
        self.add_tab()
        
        self.tabs_container.setMinimumWidth(self.tabs_width)
    
    def add_tab(self):
        font = QFont("Monospace", 10)
        metrics = QFontMetrics(font)
        
        for i in range(self.count_tabs):
            name = list(self.property_tabs.keys())[i]
            if len(name) > 15:
                display_name = name[:15] + '..'
            else:
                display_name = name
            
            text_width = metrics.horizontalAdvance(display_name)
            btn_width = text_width + 30
            
            tab_widget = QWidget()
            tab_widget.setProperty("class", "tab_widget")
            tab_layout = QHBoxLayout(tab_widget)
            tab_layout.setContentsMargins(0, 0, 0, 0)
            tab_layout.setSpacing(0)
            tab_layout.setAlignment(Qt.AlignLeft)
            
            btn = QPushButton(display_name)
            btn.setFixedSize(btn_width, 18)
            btn.setContentsMargins(0, 0, 0, 0)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setProperty("class", "tab")
            btn.setFont(font)
            
            btn_remove = QPushButton('x')
            btn_remove.setFixedSize(20, 18)
            btn_remove.setContentsMargins(0, 0, 0, 0)
            btn_remove.setCursor(Qt.PointingHandCursor)
            btn_remove.setProperty("class", "tab")
            btn_remove.setFont(QFont("Monospace", 10))
            btn_remove.clicked.connect(lambda checked, n=name: self.on_remove_tab_clicked(n))
            
            tab_layout.addWidget(btn)
            tab_layout.addWidget(btn_remove)
            
            tab_width = btn_width + 20
            self.tabs_width += tab_width
            
            tab_widget.setFixedSize(tab_width, 20)
            
            self.tabs_layout.addWidget(tab_widget)
            
            self.tabs[display_name] = {'container': tab_widget, 'btn': btn, 'btn_remove': btn_remove}
    
    def apply_theme(self):
        self.bg_card = self.theme.get('bg_card')
        self.bg_color = self.theme.get('bg_color')
        self.accent_color = self.theme.get('accent_color')
        self.accent_primary =  self.theme.get('accent_primary')
        self.text_main = self.theme.get('text_main')
        self.btn_bg_color = self.theme.get('btn_bg_color')
        self.btn_hover_bg_color = self.theme.get('btn_hover_bg_color')

        self.update()        
        self.setStyleSheet(f"""
            QPushButton[class="tab"] {{
                color: {self.text_main};
                background: transparent;
                padding-left: 5px;
                padding-right: 5px;
                border: none;
                border-radius: 3px;
                font-weight: 600;
            }}
            QPushButton[class="tab"]:hover {{ 
                background-color: {'#30' + color_utils.darken_color(self.accent_primary, factor=0.9)[1:]};
                border-radius: 3px;
                border: 1px solid {'#30' + color_utils.darken_color(self.accent_primary, factor=0.8)[1:]};
            }}
            QWidget[class="tab_widget"] {{
                background: transparent;
                border: none;
            }}
            QWidget[class="tab_widget"]:hover {{
                background-color: {'#47' + self.accent_primary[1:]};
                border-radius: 3px;
            }}
        """)

        self.scroll_area.setStyleSheet(f"""
            QScrollArea {{
                background: transparent;
                border: none;
            }}
            QScrollArea::viewport {{
                background: {self.bg_card};
            }}
            QScrollBar:horizontal {{
                background: white;
                border: none;
                height: 3px;
            }}
            QScrollBar::handle:horizontal {{
                background: {self.accent_color};
            }}
            QScrollBar::add-line:horizontal {{
                width: 0px;
            }}
            QScrollBar::sub-line:horizontal {{
                width: 0px;
            }}
        """)
    
    def paintEvent(self, event):
        if self.bg_color and self.accent_color:
            painter = QPainter(self)
            painter.fillRect(self.rect(), QColor(self.bg_color))

            painter.setPen(QColor(self.accent_color))
            painter.drawLine(0, 0, self.width(), 0)
            
            painter.drawLine(0, self.height()-1, self.width(), self.height()-1)
            from PySide6.QtGui import QPalette

            palette = self.tabs_container.palette()
            palette.setColor(QPalette.Window, QColor(self.bg_color))
            self.tabs_container.setPalette(palette)
            self.tabs_container.setAutoFillBackground(True)
        super().paintEvent(event)