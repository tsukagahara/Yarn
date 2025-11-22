import os
import sys
import json
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFileDialog)
from PySide6.QtCore import Qt

def open_file_dialog(self):
    file_path, _ = QFileDialog.getOpenFileName(
        self, 
        "Выберите файл",
        "",
        "All Files (*)"
    )
    
    if file_path:
        file_name = os.path.basename(file_path)
        directory = os.path.dirname(file_path) + '/' + file_name
        
        return file_name, directory
    return None, None

def get_project_root():
    if hasattr(sys, '_MEIPASS'):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def get_json_property(path, preference_name=""):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            if preference_name=="":
                return json.load(f)
            return json.load(f).get(preference_name)
    except FileNotFoundError:
        raise FileNotFoundError(f"JSON файл не найден: {path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Ошибка парсинга JSON в файле {path}: {e}")
    except Exception as e:
        raise RuntimeError(f"Ошибка при чтении файла {path}: {e}")
    
def add_json_property(path, property, value):
    try:
        if not property or not isinstance(property, str):
            return 'invalid_key_name'

        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if any(f'/{property}' in x for x in list(data.keys())):
            property = value.split('/')[-2] + '/' + property

        if property in data:
            if value != data[property]:
                if isinstance(value, str):
                    old_value = data[property]
                    del data[property]
                    res = ''
                    for j in range(1, len(old_value) + 1):
                        if old_value[-j] == value[-j]:
                            res += value[-j]
                        else:
                            break

                    new_name = (value[:-len(res)]).split('/')[-1] + (res[::-1])
                    old_name = (old_value[:-len(res)]).split('/')[-1] + (res[::-1])

                    data[new_name] = value
                    data[old_name] = old_value

        else: data[property] = value

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return 'success'

    except FileNotFoundError:
        return 'error: JSON файл не найден'
    except json.JSONDecodeError as e:
        return f'error: Ошибка парсинга JSON: {e}'
    except Exception as e:
        return f'error: Ошибка при работе с файлом: {e}'
    
def remove_json_property(path, property):
    # TODO: Clean up unused tab paths after removal
    try:
        if not property or not isinstance(property, str):
            return 'invalid_key_name'

        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if property in data:
            del data[property]
        else:
            return 'property_not_found'
        
        for j in list(data.keys()):
            count = 0
            if f'{property[property.find('/') + 1:]}' in j:
                count += 1


        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        # if any(f'{property[property.find('/') + 1:]}' in list(data.keys())):


        return 'success'

    except FileNotFoundError:
        return 'error: JSON файл не найден'
    except json.JSONDecodeError as e:
        return f'error: Ошибка парсинга JSON: {e}'
    except Exception as e:
        return f'error: Ошибка при работе с файлом: {e}'

class colors_is_suitable(QDialog):
    def __init__(self, theme_default, main_font_style, base_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Проверка контрасности шрифта на фоне")
        self.setFixedSize(1000, 500)
        self.setModal(True)
        self.theme_default = theme_default
        self.main_font_style = main_font_style
        self.base_path = base_path

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        label_title = QLabel("Проверка контрасности шрифта на фоне")
        label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_title.setStyleSheet("font-size: 16px; font-weight: bold; padding: 10px;")
        layout.addWidget(label_title)

        config_path = os.path.join(self.base_path, 'config', 'config.json')
        theme_name = get_json_property(config_path, "theme") or "default"
        fonts_name = get_json_property(config_path, "fonts") or "default"

        theme_file_path = os.path.join(self.base_path, "resources", "themes", f"{theme_name}.json")
        fonts_file_path = os.path.join(self.base_path, "resources", "fonts", f"{fonts_name}.json")

        label_text = QLabel(
            f'Параметр "isDark" в {theme_file_path} равен параметру\n'
            f'"fontIsDark" в {fonts_file_path}, что означает плохую контрасность текста'
        )

        label_text.setAlignment(Qt.AlignmentFlag.AlignLeft)
        label_text.setStyleSheet("font-size: 16px; font-weight: bold; padding: 10px, 2px; margin: 20px;")
        layout.addWidget(label_text)

        example_title = QLabel("вот так будет выглядеть ваш стиль, если он читаем - вы вольны его оставить")
        example_title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        example_title.setStyleSheet("font-size: 16px; font-weight: bold; padding: 10px, 2px; margin: 20px;")
        layout.addWidget(example_title)

        example = QLabel("example example example example example")
        example.setAlignment(Qt.AlignmentFlag.AlignLeft)
        example.setStyleSheet(f'font-size: 16px; font-weight: bold; padding: 10px, 2px; margin: 20px; background:{self.theme_default["bg_card"]}; color:{self.main_font_style["color"]};')
        layout.addWidget(example)

        button_layout = QHBoxLayout()

        reject_btn = QPushButton("поменять")
        reject_btn.clicked.connect(self.reject)
        button_layout.addWidget(reject_btn)

        accept_btn = QPushButton("оставить")
        accept_btn.clicked.connect(self.accept)
        button_layout.addWidget(accept_btn)

        layout.addLayout(button_layout)

        self.setStyleSheet("""
             QDialog {
                 background-color: white;
             }
             QLabel {
                 font-size: 14px;
                 padding: 10px;
             }
             QPushButton {
                 background-color: white;
                 color: black;
                 border: none;
                 padding: 10px 15px;
                 font-size: 14px;
                 border-radius: 5px;
                 margin: 5px;
             }
             QPushButton:hover {
                 background-color: #99d2ff;
             }
             QPushButton:pressed {
                 background-color: #66bcff;
             }
             QPushButton:focus {
                 outline: 1px solid #fff;
             }
        """)