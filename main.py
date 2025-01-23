import tkinter as tk
from tkinter import *
import customtkinter as ctk
from forms.design_master_form import design_master_form
from PIL import Image, ImageTk

# Configuración de la apariencia de CustomTkinter
ctk.set_appearance_mode("dark")  # Opciones: "light", "dark", "system"
ctk.set_default_color_theme("blue")  # Cambia el tema de color

class SelectDifficulty(tk.Toplevel):
    def __init__(self, parent, on_difficulty_selected):
        super().__init__(parent)
        self.geometry("300x200")
        self.title("Seleccionar Dificultad")

        label = tk.Label(self, text="Selecciona la Dificultad", font=("Helvetica", 12))
        label.pack(pady=10)

        self.on_difficulty_selected = on_difficulty_selected

        easy_button = tk.Button(self, text="Facil", command=lambda: self.set_difficulty("easy"))
        easy_button.pack(pady=5)
        medium_button = tk.Button(self, text="Medio", command=lambda: self.set_difficulty("medium"))
        medium_button.pack(pady=5)
        hard_button = tk.Button(self, text="Dificil", command=lambda: self.set_difficulty("hard"))
        hard_button.pack(pady=5)

    def set_difficulty(self, selected_difficulty):
        self.on_difficulty_selected(selected_difficulty)
        self.destroy()
        
class SelectSymbol(tk.Toplevel):
    def __init__(self, parent, difficulty, on_symbol_selected):
        super().__init__(parent)
        self.geometry("300x200")
        self.title("Seleccionar Ficha")

        label = tk.Label(self, text="Selecciona tu Ficha", font=("Helvetica", 12))
        label.pack(pady=10)

        self.difficulty = difficulty
        self.on_symbol_selected = on_symbol_selected

        if difficulty == "medium":
            tk.Button(self, text="Y", command=lambda: self.close_game("Y")).pack(pady=5)
            tk.Button(self, text="Z", command=lambda: self.close_game("Z")).pack(pady=5)
        elif difficulty == "hard":
            tk.Button(self, text="S", command=lambda: self.close_game("S")).pack(pady=5)
            tk.Button(self, text="M", command=lambda: self.close_game("M")).pack(pady=5)
        else:
            tk.Button(self, text="X", command=lambda: self.close_game("X")).pack(pady=5)
            tk.Button(self, text="O", command=lambda: self.close_game("O")).pack(pady=5)

    def close_game(self, symbol):
        self.on_symbol_selected(symbol)
        

class MainMenu(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Choclo Game")
        self.geometry("1080x720")

        # Cargar la imagen de fondo del menú
        try:
            self.original_image = Image.open("./images/gif1.gif")
        except Exception as e:
            print(f"Error al cargar la imagen: {e}")
            self.original_image = None  # O asigna una imagen por defecto

        self.background_label = tk.Label(self)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)  

        # Título
        self.title_label = ctk.CTkLabel(self, text="CHOCLO GAME", font=("Arial", 70), text_color="white")
        self.title_label.pack(pady=(100, 20))

        # Botones
        self.play_button = ctk.CTkButton(self, text="JUGAR", command=self.play, width=300, height=80, fg_color="#0b5345", hover_color="lightgreen", font=("Arial", 20))
        self.play_button.pack(pady=20)

        self.options_button = ctk.CTkButton(self, text="OPCIONES", command=self.open_options, width=300, height=80, fg_color="#0b5345", hover_color="lightgreen", font=("Arial", 20))
        self.options_button.pack(pady=20)

        self.quit_button = ctk.CTkButton(self, text="SALIR", command=self.quit, width=300, height=80, fg_color="#0b5345", hover_color="lightgreen", font=("Arial", 20))
        self.quit_button.pack(pady=20)

        # Redimensionar la imagen al tamaño de la ventana
        self.bind("<Configure>", self.resize_background)

        self.update_background()

    def update_background(self):
        if self.original_image is not None:
            width = self.winfo_width()
            height = self.winfo_height()

            resized_image = self.original_image.resize((width, height ), Image.LANCZOS)
            self.background_photo = ImageTk.PhotoImage(resized_image)

            self.background_label.configure(image=self.background_photo)
            self.background_label.image = self.background_photo  # Mantener una referencia
        else:
            print("No se pudo cargar la imagen de fondo.")  # Mensaje de error si la imagen no se carga


    def resize_background(self, event):
        self.update_background()

    def play(self):
        self.withdraw()  # Oculta el menú principal
        self.select_difficulty()

    def select_difficulty(self):
        SelectDifficulty(self, self.on_difficulty_selected)

    def on_difficulty_selected(self, difficulty):
        self.difficulty = difficulty
        self.select_symbol()

    def select_symbol(self):
        SelectSymbol(self, self.difficulty, self.on_symbol_selected)

    def on_symbol_selected(self, symbol):
        self.player_symbol = symbol
        if self.difficulty == "easy":
            self.computer_symbol = "O" if symbol == "X" else "X"
        elif self.difficulty == "medium":
            self.computer_symbol = "Y" if symbol == "Z" else "Z"
        elif self.difficulty == "hard":
            self.computer_symbol = "M" if symbol == "S" else "S"
        self.start_game()

    def start_game(self):
        self.destroy()
        game_window = design_master_form(self.difficulty, self.player_symbol, self.computer_symbol)
        game_window.mainloop()

    def open_options(self):
        self.withdraw()  # Oculta la ventana principal
        options_window = OptionsWindow(self)  # Abre la ventana de opciones

class OptionsWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        # Configuración de la ventana
        self.title("Opciones")
        self.geometry("1080x720")

        # Cargar la imagen de fondo de la ventana de opciones
        self.original_image = Image.open("./images/img2.jpg")  
        self.background_label = tk.Label(self)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1) 

        self.bind("<Configure>", self.resize_background)

        self.update_background()

        self.options_label = ctk.CTkLabel(self, text="Esta es la pantalla de OPCIONES", font=("Arial", 30))
        self.options_label.pack(pady=20)

        self.back_button = ctk.CTkButton(self, text="VOLVER", command=self.on_back, width=300, height=80, fg_color="#0b5345", hover_color="lightgreen", font=("Arial", 20))
        self.back_button.pack(pady=20)

        # Manejar el evento de cierre de la ventana
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def resize_background(self, event):
        self.update_background()

    def update_background(self):
        width = self.winfo_width()
        height = self.winfo_height()

        resized_image = self.original_image.resize((width, height), Image.LANCZOS)
        self.background_photo = ImageTk.PhotoImage(resized_image)

        self.background_label.configure(image=self.background_photo)
        self.background_label.image = self.background_photo  # Mantener una referencia a la imagen

    def on_back(self):
        self.destroy()  # Cierra la ventana de opciones
        self.master.deiconify()  # Muestra de nuevo la ventana principal

    def on_close(self):
        self.destroy()  # Cierra la ventana de opciones
        self.master.deiconify()  # Muestra

if __name__ == "__main__":
    app = MainMenu()
    app.mainloop()

if __name__ == "__main__":
    app = MainMenu()
    app.mainloop()
