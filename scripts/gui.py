import customtkinter as ctk
import tkinter as tk

# Базовые цвета
BG_DARK = '#111111'      # Основной фон
BG_CARD = '#121212'      # Карточки, панели

# Акцентные (тускло-синие)
ACCENT_PRIMARY = "#202020"   # Основной акцент
ACCENT_SECONDARY = "#252525" # Второстепенный
ACCENT_LIGHT = "#7a7a7a"     # Светлый акцент

# Текст
TEXT_MAIN = '#e0e0e0'    # Основной текст
TEXT_MUTED = '#a0a0a0'   # Второстепенный текст

selected_color = ACCENT_PRIMARY

class basicTextAnalyzer:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.app = ctk.CTk()
        self.app.geometry("400x300")
        self.app.title("basicTextAnalyzer")
        self._create_widgets()

    def darken_color(self, hex_color, factor=0.8):
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        darkened = tuple(max(0, int(c * factor)) for c in rgb)
        return f"#{darkened[0]:02x}{darkened[1]:02x}{darkened[2]:02x}"
        
    def _create_widgets(self):
        main = ctk.CTkFrame(self.app, fg_color=BG_DARK)
        main.pack(fill="both", expand=True)

        aside = ctk.CTkFrame(main, width=100, fg_color=ACCENT_SECONDARY)
        aside.pack(side="left", fill="y")

# --------------------------------------------------------------------------------------------------------


        aside_color_container = ctk.CTkFrame(aside, fg_color=ACCENT_PRIMARY, width=100, height=120)
        aside_color_container.pack(side="bottom")

        colorPicker = ctk.CTkButton(aside_color_container,
            text="",
            width=80,
            height=60,
            fg_color=ACCENT_PRIMARY,
            hover_color=self.darken_color(selected_color, 0.8),
            border_width=2,
            border_color=ACCENT_SECONDARY)
        colorPicker.pack(side="left")

        open_colorPicker = ctk.CTkButton(aside_color_container,
            text=">>",
            width=20,
            height=60,
            fg_color=ACCENT_PRIMARY,
            hover_color=self.darken_color(selected_color, 0.8),
            border_width=1,
            border_color=ACCENT_SECONDARY)
        open_colorPicker.pack()

# --------------------------------------------------------------------------------------------------------

        aside_style_container = ctk.CTkFrame(aside, fg_color=ACCENT_PRIMARY, width=100, height=120)
        aside_style_container.pack(side="bottom")

        stylePicker = ctk.CTkButton(aside_style_container,
            text="",
            width=80,
            height=60,
            fg_color=ACCENT_PRIMARY,
            hover_color=self.darken_color(selected_color, 0.8),
            border_width=2,
            border_color=ACCENT_SECONDARY)
        stylePicker.pack(side="left")

        open_stylePicker = ctk.CTkButton(aside_style_container,
            text=">>",
            width=20,
            height=60,
            fg_color=ACCENT_PRIMARY,
            hover_color=self.darken_color(selected_color, 0.8),
            border_width=1,
            border_color=ACCENT_SECONDARY)
        open_stylePicker.pack()

# --------------------------------------------------------------------------------------------------------

        aside_style_container = ctk.CTkFrame(aside,
            fg_color=ACCENT_PRIMARY,
            width=100,
            border_width=1,
            border_color=ACCENT_SECONDARY)
        aside_style_container.pack(side="left", fill="y")


    def run(self):
        self.app.mainloop()

if __name__ == "__main__":
    app = basicTextAnalyzer()
    app.run()