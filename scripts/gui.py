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

refresh_rate = 2000
font_family = "Arial" #Unbounded
font_size = 12
font_style = (font_family, font_size)

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
        # центральная панель
        userInput_container = ctk.CTkFrame(main, fg_color="transparent")
        userInput_container.pack(side="left", fill="both", expand=True)

        def update_padding():
            width = userInput_container.winfo_width()
            user_input.configure(padx=int(width * 0.05))
            self.app.after(refresh_rate, update_padding)

        user_input = ctk.CTkTextbox(userInput_container, fg_color="transparent", font=font_style)
        user_input.pack(side="left",
                fill="both",
                expand=True,
                pady=5)
        
        update_padding()
        

# --------------------------------------------------------------------------------------------------------
        # left-aside color
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
        # left-aside style
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
        # left-aside panel
        left_aside_container = ctk.CTkFrame(aside,
            fg_color=ACCENT_PRIMARY,
            width=100,
            border_width=1,
            border_color=ACCENT_SECONDARY)
        left_aside_container.pack(side="left", fill="y")

# --------------------------------------------------------------------------------------------------------
        # Right-aside panel
        control_panel = ctk.CTkFrame(main, width=50,
                fg_color=ACCENT_PRIMARY,
                border_width=1,
                border_color=ACCENT_SECONDARY)
        control_panel.pack(side="right", fill="y")

        btn1 = ctk.CTkButton(control_panel,
                text="A",
                width=40,
                height=30,
                fg_color=ACCENT_PRIMARY,
                border_width=1,
                border_color=ACCENT_SECONDARY,
                hover_color=ACCENT_SECONDARY)
        btn1.pack(side="top", padx=5, pady=1)

        btn2 = ctk.CTkButton(control_panel,
                text="B",
                width=40,
                height=30,
                fg_color=ACCENT_PRIMARY,
                border_width=1,
                border_color=ACCENT_SECONDARY,
                hover_color=ACCENT_SECONDARY)
        btn2.pack(side="top", padx=5, pady=1)

        btn3 = ctk.CTkButton(control_panel,
                text="C",
                width=40,
                height=30,
                fg_color=ACCENT_PRIMARY,
                border_width=1,
                border_color=ACCENT_SECONDARY,
                hover_color=ACCENT_SECONDARY)
        btn3.pack(side="top", padx=5, pady=1)
        
        btn4 = ctk.CTkButton(control_panel,
                text="D",
                width=40,
                height=30,
                fg_color=ACCENT_PRIMARY,
                border_width=1,
                border_color=ACCENT_SECONDARY,
                hover_color=ACCENT_SECONDARY)
        btn4.pack(side="top", padx=5, pady=1)

        btn5 = ctk.CTkButton(control_panel,
                text="E",
                width=40,
                height=30,
                fg_color=ACCENT_PRIMARY,
                border_width=1,
                border_color=ACCENT_SECONDARY,
                hover_color=ACCENT_SECONDARY)
        btn5.pack(side="top", padx=5, pady=1)

        btn6 = ctk.CTkButton(control_panel,
                text="F",
                width=40,
                height=30,
                fg_color=ACCENT_PRIMARY,
                border_width=1,
                border_color=ACCENT_SECONDARY,
                hover_color=ACCENT_SECONDARY)
        btn6.pack(side="top", padx=5, pady=1)

        preferences = ctk.CTkButton(control_panel,
                text="☰",
                width=40,
                height=30,
                fg_color=ACCENT_PRIMARY,
                border_width=1,
                border_color=ACCENT_SECONDARY,
                hover_color=ACCENT_SECONDARY,
                )
        preferences.pack(side="bottom", padx=5, pady=1)

# --------------------------------------------------------------------------------------------------------
        # плавающее меню
        self.app_settings = ctk.CTkFrame(main,
                fg_color=ACCENT_PRIMARY,
                width=500,
                height=300,
                border_width=1,
                border_color=ACCENT_SECONDARY)
        self.app_settings.place(relx=1, rely=1, anchor="e", x=-60, y=-160)


    def run(self):
        self.app.mainloop()

if __name__ == "__main__":
    app = basicTextAnalyzer()
    app.run()