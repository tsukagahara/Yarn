import os
from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QSizePolicy, QScrollArea, QMessageBox
from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QPainter, QColor, QFont, QFontMetrics
import utils.helpers as helpers

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
        # TODO: load file
        file_name, directory = helpers.open_file_dialog(self)
        helpers.add_json_property(self.path_tabs, file_name, directory)
        self.reload_tabs(file_name, directory)

    def check_file_access(self, path):
        """отработка ошибки чтения файла"""
        except_msg = (f"File exists: {os.path.exists(path)}\n")
        except_msg += (f"Readable: {os.access(path, os.R_OK)}\n")
        except_msg += (f"Writable: {os.access(path, os.W_OK)}\n")
        except_msg += (f"Executable: {os.access(path, os.X_OK)}")

        return except_msg
    
    def on_tab_clicked(self, path):
        """Загружаем файл в редактор при клике на вкладку"""
        if os.access(path, os.R_OK): # чтение
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                    # Передаем содержимое в текстовый редактор
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Read Error", 
                    f"Cannot read file: {path}\nError: {e}"
                ) # TODO: realisation in main window
        else:
            QMessageBox.critical(
                self,
                "Read Access Denied",
                f"No read permission: {path}\n-------\n{self.check_file_access(path)}"
            ) # TODO: realisation in main window

    def on_remove_tab_clicked(self, name):
        # add: save file
        helpers.remove_json_property(self.path_tabs, name)
        self.reload_tabs()
        

    def reload_tabs(self, file_name=None, directory=None):
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
            
            text_width = metrics.horizontalAdvance(name)
            btn_width = text_width + 40
            
            tab_widget = QWidget()
            tab_widget.setProperty("class", "tab_widget")
            tab_widget.setStyleSheet("margin-right: 10px;")
            tabs_layout = QHBoxLayout(tab_widget)
            tabs_layout.setAlignment(Qt.AlignLeft)
            tabs_layout.setContentsMargins(0, 0, 0, 0)
            
            btn = QPushButton(name)
            btn.setFixedSize(btn_width, 18)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setProperty("class", "tab")
            btn.setFont(font)
            btn.clicked.connect(lambda checked, n=name: self.on_tab_clicked(self.property_tabs[n]))
            
            btn_remove = QPushButton('x')
            btn_remove.setFixedSize(40, 18)
            btn_remove.setCursor(Qt.PointingHandCursor)
            btn_remove.setProperty("class", "tab")
            btn_remove.setFont(QFont("Monospace", 10))
            btn_remove.clicked.connect(lambda checked, n=name: self.on_remove_tab_clicked(n))
            
            tabs_layout.addWidget(btn)
            tabs_layout.addWidget(btn_remove)
            
            tab_width = btn_width + 20
            self.tabs_width += tab_width
            
            tab_widget.setFixedSize(tab_width, 20)
            
            self.tabs_layout.addWidget(tab_widget)
            
            self.tabs[name] = {'container': tab_widget, 'btn': btn, 'btn_remove': btn_remove}
    
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
                background-color: transparent;
                color: {self.text_main};
                border-radius: 3px;
                font-weight: 600;
            }}
            
            QPushButton[class="tab"]:hover {{
                background-color: {'#20' + self.btn_bg_color[1:]};
            }}
            
            QPushButton[class="tab"]:pressed {{
                background-color: {self.accent_primary};
            }}
            QWidget[class="tab_widget"] {{
                background-color: {'#60' + self.accent_primary[1:]};
                border: 1px solid {'#80' + self.accent_primary[1:]};
                border-radius: 3px;
            }}
            QWidget[class="tab_widget"]:hover {{
                background-color: {'#80' + self.accent_primary[1:]};
                border: 1px solid {self.accent_primary};
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