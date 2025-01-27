import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from forms.design_master_form import design_master_form
from PIL import Image, ImageTk, ImageSequence
import customtkinter as ctk
import pygame 

# Configuración de la apariencia de CustomTkinter
ctk.set_appearance_mode("dark")  # Opciones: "light", "dark", "system"
ctk.set_default_color_theme("blue")  # Cambia el tema de color

class SelectDifficulty(ctk.CTkFrame):
    def __init__(self, parent, on_difficulty_selected):
        super().__init__(parent)
        self.pack(pady=20)

        label = ctk.CTkLabel(self, text="Selecciona la Dificultad", font=("Helvetica", 16))
        label.pack(pady=10)

        self.on_difficulty_selected = on_difficulty_selected

        easy_button = ctk.CTkButton(self, text="Fácil", command=lambda: self.set_difficulty("easy"), width=200, height=40, fg_color="#4CAF50", hover_color="#45A049")
        easy_button.pack(pady=5)
        medium_button = ctk.CTkButton(self, text="Medio", command=lambda: self.set_difficulty("medium"), width=200, height=40, fg_color="#9C27B0", hover_color="#8E24AA")
        medium_button.pack(pady=5)
        hard_button = ctk.CTkButton(self, text="Difícil", command=lambda: self.set_difficulty("hard"), width=200, height=40, fg_color="#F44336", hover_color="#E53935")
        hard_button.pack(pady=5)

    def set_difficulty(self, selected_difficulty):
        self.on_difficulty_selected(selected_difficulty)
        messagebox.showinfo("Dificultad Seleccionada", f"Has seleccionado la dificultad: {selected_difficulty.capitalize()}")

class SelectSymbol(ctk.CTkToplevel):
    def __init__(self, parent, difficulty, on_symbol_selected):
        super().__init__(parent)
        self.geometry("300x200")
        self.iconbitmap("./images/icono_juego.ico")
        self.title("Seleccionar Ficha")

        label = ctk.CTkLabel(self, text="Selecciona tu Ficha", font=("Helvetica", 16))
        label.pack(pady=10)

        self.difficulty = difficulty
        self.on_symbol_selected = on_symbol_selected

        if difficulty == "medium":
            ctk.CTkButton(self, text="Y", command=lambda: self.close_game("Y"), width=200, height=40, fg_color="#9C27B0", hover_color="#8E24AA").pack(pady=5)
            ctk.CTkButton(self, text="Z", command=lambda: self.close_game("Z"), width=200, height=40, fg_color="#9C27B0", hover_color="#8E24AA").pack(pady=5)
        elif difficulty == "hard":
            ctk.CTkButton(self, text="S", command=lambda: self.close_game("S"), width=200, height=40, fg_color="#F44336", hover_color="#E53935").pack(pady=5)
            ctk.CTkButton(self, text="M", command=lambda: self.close_game("M"), width=200, height=40, fg_color="#F44336", hover_color="#E53935").pack(pady=5)
        else:
            ctk.CTkButton(self, text="X", command=lambda: self.close_game("X"), width=200, height=40, fg_color="#4CAF50", hover_color="#45A049").pack(pady=5)
            ctk.CTkButton(self, text="O", command=lambda: self.close_game("O"), width=200, height=40, fg_color="#4CAF50", hover_color="#45A049").pack(pady=5)

    def close_game(self, symbol):
        self.on_symbol_selected(symbol)
        self.destroy()
        self.master.start_game()  # Llamar al método start_game de MainMenu

class MainMenu(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Música de fondo----------------------
        pygame.mixer.init()
        pygame.mixer.music.load("./music/Uma Thurman 8 Bit.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.4)

        self.title("Choclo Game")
        self.geometry("1280x720")
        self.resizable(False, False)
        self.maxsize(1280, 720)
        self.iconbitmap("./images/icono_juego.ico")

        # Establecer la dificultad por defecto a "fácil"
        self.difficulty = "easy"

        # Cargar la imagen de fondo del menú
        try:
            self.original_image = Image.open("./images/fondo_menu.gif")
            self.frames = [ImageTk.PhotoImage(img.copy().resize((1280, 720), Image.LANCZOS)) for img in ImageSequence.Iterator(self.original_image)]
        except Exception as e:
            print(f"Error al cargar la imagen: {e}")
            self.frames = []

        self.background_label = tk.Label(self)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Título
        self.title_label = ctk.CTkLabel(self, text="TIC TAC TOE", font=("Helvetica", 70), text_color="white", bg_color="#6a0000", padx=30)
        self.title_label.pack(pady=(100, 20))
        self.configure(bg="#6a0000")

        # Botones
        self.play_button = ctk.CTkButton(
            self,
            text="JUGAR",
            command=self.play,
            width=300,
            height=80,
            fg_color="#c60030",
            hover_color="#d23359",
            font=("Helvetica", 20),
            border_color="#6a0000",
            border_width=3,
            text_color="white"
        )
        self.play_button.pack(pady=20)

        self.options_button = ctk.CTkButton(
            self,
            text="OPCIONES",
            command=self.open_options,
            width=300,
            height=80,
            fg_color="#c60030",
            hover_color="#d23359",
            font=("Helvetica", 20),
            border_color="#6a0000",
            border_width=3,
            text_color="white"
        )
        self.options_button.pack(pady=20)

        self.options_button = ctk.CTkButton(
            self,
            text="SALIR",
            command=self.quit,
            width=300,
            height=80,
            fg_color="#c60030",
            hover_color="#d23359",
            font=("Helvetica", 20),
            border_color="#6a0000",
            border_width=3,
            text_color="white"
        )
        self.options_button.pack(pady=20)

        # Redimensionar la imagen al tamaño de la ventana
        self.bind("<Configure>", self.resize_background)

        self.update_background()
        self.animate_gif(0)

    def update_background(self):
        if self.frames:
            frame = self.frames[0]
            self.background_label.configure(image=frame)
            self.background_label.image = frame  # Mantener una referencia
        else:
            print("No se pudo cargar la imagen de fondo.")  # Mensaje de error si la imagen no se carga

    def resize_background(self, event):
        self.update_background()

    def animate_gif(self, frame_index):
        if self.frames:
            frame = self.frames[frame_index]
            self.background_label.configure(image=frame)
            self.after(100, self.animate_gif, (frame_index + 1) % len(self.frames))

    def play(self):
        pygame.mixer.music.stop()  # Detener la música de fondo
        self.withdraw()  # Oculta el menú principal
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

    def start_game(self):
        # Cargar música según la dificultad
        if self.difficulty == "easy":
            self.original_music = "./music/Ghostbusters 8 Bit.mp3"
        elif self.difficulty == "medium":
            self.original_music = "./music/Blue Da Ba Dee 8 Bit.mp3"
        elif self.difficulty == "hard":
            self.original_music = "./music/Take On Me 8 Bit.mp3"

        pygame.mixer.music.load(self.original_music)  # Cargar la música de la dificultad
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.4)
        game_window = design_master_form(self.difficulty, self.player_symbol, self.computer_symbol)
        game_window.mainloop()

    def open_options(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.load("./music/Sugar Were Goin Down 8 Bit.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.4)
        self.withdraw()
        OptionsWindow(self)

    def restart_menu_music(self):
        pygame.mixer.music.load("./music/Uma Thurman 8 Bit.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.4)

class OptionsWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        # Configuración de la ventana
        self.title("Opciones")
        self.geometry("1280x720")
        self.iconbitmap("./images/icono_juego.ico")

        # Cargar la imagen de fondo de la ventana de opciones
        try:
            self.original_image = Image.open("./images/fondo_menu.gif")
            self.frames = [ImageTk.PhotoImage(img.copy().resize((1280, 720), Image.LANCZOS)) for img in ImageSequence.Iterator(self.original_image)]
        except Exception as e:
            print(f"Error al cargar la imagen: {e}")
            self.frames = []

        self.background_label = tk.Label(self)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.bind("<Configure>", self.resize_background)

        self.update_background()

        self.options_label = ctk.CTkLabel(self, text="Esta es la pantalla de OPCIONES", font=("Arial", 30))
        self.options_label.pack(pady=20)

        self.difficulty_frame = SelectDifficulty(self, self.on_difficulty_selected)
        self.difficulty_frame.pack(pady=20)

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

    def on_difficulty_selected(self, difficulty):
        self.master.difficulty = difficulty

    def on_back(self):
        self.destroy()
        self.master.deiconify()
        self.master.restart_menu_music()

    def on_close(self):
        pygame.mixer.music.stop()
        self.destroy()
        self.master.deiconify()
        self.master.restart_menu_music()

if __name__ == "__main__":
    app = MainMenu()
    app.mainloop()