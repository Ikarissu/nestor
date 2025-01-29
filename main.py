import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from customtkinter import CTkImage
from forms.design_master_form import design_master_form
from PIL import Image, ImageTk, ImageSequence, ImageDraw, ImageFilter
import pygame 

# Configuración de la apariencia de CustomTkinter
ctk.set_appearance_mode("dark")  # Opciones: "light", "dark", "system"
ctk.set_default_color_theme("blue")  # Cambia el tema de color

is_muted = False

class SelectDifficulty(ctk.CTkFrame):
    def __init__(self, parent, on_difficulty_selected):
        super().__init__(parent, fg_color="transparent")  # Establecer el fondo del frame como transparente
        self.pack(pady=20)

        label = ctk.CTkLabel(self, text="Selecciona la Dificultad", font=("Helvetica", 26), text_color="white")  # Establecer el color del texto como negro
        label.pack(pady=10)

        self.on_difficulty_selected = on_difficulty_selected

        easy_button = ctk.CTkButton(self, text="Fácil", command=lambda: self.set_difficulty("easy"), width=500, height=80, fg_color="transparent", hover_color="#45A049")
        easy_button.pack(pady=10)
        medium_button = ctk.CTkButton(self, text="Medio", command=lambda: self.set_difficulty("medium"), width=500, height=80, fg_color="transparent", hover_color="#8E24AA")
        medium_button.pack(pady=10)
        hard_button = ctk.CTkButton(self, text="Difícil", command=lambda: self.set_difficulty("hard"), width=500, height=80, fg_color="transparent", hover_color="#E53935")
        hard_button.pack(pady=10)

    def set_difficulty(self, selected_difficulty):
        self.on_difficulty_selected(selected_difficulty)
        messagebox.showinfo("Dificultad Seleccionada", f"Has seleccionado la dificultad: {selected_difficulty.capitalize()}")
# ...existing code...

class SelectSymbol(ctk.CTkToplevel):
    def __init__(self, parent, difficulty, on_symbol_selected):
        super().__init__(parent)
        
        self.setup_music()
        self.geometry("1280x720")
        self.iconbitmap("./images/icono_juego.ico")
        self.title("Seleccionar Ficha")

        # Eliminar los botones de minimizar y maximizar
        self.overrideredirect(True)
        
        # Renderizar el texto del título con la misma fuente y estilo
        arcade_font = pygame.font.Font('./useful/fuente.ttf', 30)
        text_surface = arcade_font.render('Selecciona tu Ficha', True, (255, 255, 255))
        shadow_surface = arcade_font.render('Selecciona tu Ficha', True, (0, 0, 0))
        width, height = text_surface.get_size()
        border_surface = pygame.Surface((width + 20, height + 20), pygame.SRCALPHA)
        border_surface.fill((0, 0, 0, 0))
        border_surface.blit(shadow_surface, (10, 10))
        border_surface.blit(text_surface, (5, 5))
        pygame.image.save(border_surface, 'temp_text.png')
        image = Image.open('temp_text.png')
        photo = ImageTk.PhotoImage(image)

        label = tk.Label(self, image=photo, bg="#490029", bd=5, relief="ridge")
        label.image = photo  # Guardar una referencia de la imagen
        label.pack(pady=10)

        self.difficulty = difficulty
        self.on_symbol_selected = on_symbol_selected
        
        # Guardar referencias a las imágenes de los botones
        self.button_images = {}

        # Renderizar los botones con la misma fuente y estilo
        def render_button_text(text, font_size):
            button_font = pygame.font.Font('./useful/fuente.ttf', font_size)
            text_surface = button_font.render(text, True, (255, 255, 255))
            width, height = text_surface.get_size()
            button_surface = pygame.Surface((width, height), pygame.SRCALPHA)
            button_surface.blit(text_surface, (0, 0))
            pygame.image.save(button_surface, f'{text}_button.png')
            image = Image.open(f'{text}_button.png')
            self.button_images[text] = ImageTk.PhotoImage(image)  # Guardar referencia
            return self.button_images[text]

        if difficulty == "medium":
            ctk.CTkButton(self, text="", image=render_button_text("Y", 20), command=lambda: self.close_game("Y"), width=200, height=40, fg_color="#9C27B0", hover_color="#8E24AA").pack(pady=5)
            ctk.CTkButton(self, text="", image=render_button_text("Z", 20), command=lambda: self.close_game("Z"), width=200, height=40, fg_color="#9C27B0", hover_color="#8E24AA").pack(pady=5)
        elif difficulty == "hard":
            ctk.CTkButton(self, text="", image=render_button_text("S", 20), command=lambda: self.close_game("S"), width=200, height=40, fg_color="#F44336", hover_color="#E53935").pack(pady=5)
            ctk.CTkButton(self, text="", image=render_button_text("M", 20), command=lambda: self.close_game("M"), width=200, height=40, fg_color="#F44336", hover_color="#E53935").pack(pady=5)
        else:
            ctk.CTkButton(self, text="", image=render_button_text("X", 20), command=lambda: self.close_game("X"), width=200, height=40, fg_color="#4CAF50", hover_color="#45A049").pack(pady=5)
            ctk.CTkButton(self, text="", image=render_button_text("O", 20), command=lambda: self.close_game("O"), width=200, height=40, fg_color="#4CAF50", hover_color="#45A049").pack(pady=5)

        # Botón para volver al menú principal
        # back_button = ctk.CTkButton(self, text="", image=render_button_text("Volver al Menú Principal", 20), command=self.back_to_main_menu, width=200, height=40, fg_color="#607D8B", hover_color="#546E7A")
        # back_button.pack(pady=10)

        # # Botón para volver al menú principal
        back_button = ctk.CTkButton(self, text="", image=render_button_text("Volver al Menú Principal", 20), command=self.back_to_main_menu, width=200, height=40, fg_color="#607D8B", hover_color="#546E7A")
        back_button.pack(pady=10)

    def setup_music(self):
        if not is_muted:
            pygame.mixer.music.load("./music/Uma Thurman 8 Bit.mp3")
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.4)
        else:
            pygame.mixer.music.set_volume(0)  # Silenciar música si is_muted es True


    def close_game(self, symbol):
        self.on_symbol_selected(symbol)
        self.destroy()
        self.master.start_game()  # Llamar al método start_game de MainMenu

    def close_window(self):
        self.destroy()

    def back_to_main_menu(self):
        self.destroy()
        self.master.deiconify()  # Mostrar la ventana principal

# ...existing code...

class MainMenu(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Música de fondo----------------------
        pygame.mixer.init()
        pygame.mixer.music.load("./music/Uma Thurman 8 Bit.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.4)
        
        pygame.font.init()
        
        arcade_font = pygame.font.Font('./useful/fuente.ttf', 70)
        
        self.title("Choclo Game")
        self.geometry("1280x720")
        self.resizable(False, False)
        self.maxsize(1280, 720)
        self.iconbitmap("./images/icono_juego.ico")
        self.attributes('-toolwindow', True)  # Deshabilitar minimizar y maximizar

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

        # Crear una imagen de fondo difuminada
        background_image = Image.new('RGBA', (800, 600), (73, 0, 41, 255))
        background_image = background_image.filter(ImageFilter.GaussianBlur(10))

        # Crear una imagen con bordes redondeados
        def create_rounded_rectangle(width, height, radius, color):
            rectangle = Image.new('RGBA', (width, height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(rectangle)
            draw.rounded_rectangle((0, 0, width, height), radius, fill=color)
            return rectangle

        # Crear el fondo redondeado
        rounded_background = create_rounded_rectangle(820, 620, 50, (73, 0, 41, 255))
        rounded_background.paste(background_image, (10, 10), background_image)

        # Guardar la imagen temporalmente
        rounded_background.save('rounded_background.png')

        # Cargar la imagen de fondo redondeada
        background_photo = ImageTk.PhotoImage(rounded_background)

        # Crear un label para la imagen de fondo
        self.background_label = tk.Label(self, image=background_photo)
        self.background_label.image = background_photo  # Guardar una referencia de la imagen
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Renderizar el texto con color y sombra
        text_surface = arcade_font.render('TIC TAC TOE', True, (255, 255, 255))
        shadow_surface = arcade_font.render('TIC TAC TOE', True, (0, 0, 0))

        # Crear una superficie más grande para el borde y la sombra
        width, height = text_surface.get_size()
        border_surface = pygame.Surface((width + 20, height + 20), pygame.SRCALPHA)
        border_surface.fill((0, 0, 0, 0))  # Fondo transparente

        # Dibujar la sombra
        border_surface.blit(shadow_surface, (10, 10))

        # Dibujar el texto original encima de la sombra
        border_surface.blit(text_surface, (5, 5))

        # Guardar la superficie como una imagen temporal
        pygame.image.save(border_surface, 'temp_text.png')

        # Cargar la imagen temporal con PIL
        image = Image.open('temp_text.png')
        photo = ImageTk.PhotoImage(image)

        self.text_label = tk.Label(self, image=photo, bg="#490029", bd=5, relief="ridge")
        self.text_label.image = photo  # Guardar una referencia de la imagen
        self.text_label.pack(pady=(150, 20))  # Aumentar el margen superior

        def toggle_color():
            current_bg_color = self.text_label.cget("bg")
            new_bg_color = "#490029" if current_bg_color == "#8B004E" else "#8B004E"
            current_fg_color = "white" if new_bg_color == "#490029" else "#FFE89A"
            
            # Renderizar el texto con el nuevo color
            text_surface = arcade_font.render('TIC TAC TOE', True, (255, 255, 255) if current_fg_color == "white" else (255, 255, 0))
            shadow_surface = arcade_font.render('TIC TAC TOE', True, (0, 0, 0))
            border_surface = pygame.Surface((width + 20, height + 20), pygame.SRCALPHA)
            border_surface.fill((0, 0, 0, 0))
            border_surface.blit(shadow_surface, (10, 10))
            border_surface.blit(text_surface, (5, 5))
            pygame.image.save(border_surface, 'temp_text.png')
            image = Image.open('temp_text.png')
            photo = ImageTk.PhotoImage(image)
            
            self.text_label.config(image=photo, bg=new_bg_color)
            self.text_label.image = photo  # Guardar una referencia de la imagen
            self.after(500, toggle_color)  # Alternar cada 500 ms

        # Iniciar la alternancia de color
        toggle_color()
        
        # Función para renderizar texto en un botón con un tamaño de fuente específico
        def render_button_text(text, font_size):
            button_font = pygame.font.Font('./useful/fuente.ttf', font_size)
            text_surface = button_font.render(text, True, (255, 255, 255))
            width, height = text_surface.get_size()
            button_surface = pygame.Surface((width, height), pygame.SRCALPHA)
            button_surface.blit(text_surface, (0, 0))
            pygame.image.save(button_surface, f'{text}_button.png')
            return CTkImage(light_image=Image.open(f'{text}_button.png'),
                            dark_image=Image.open(f'{text}_button.png'),
                            size=(width, height))

        # Botones
        self.play_button = ctk.CTkButton(
            self,
            text="",
            image=render_button_text("JUGAR", 30),
            command=self.play,
            width=300,
            height=80,
            fg_color="#490029",
            hover_color="#8B004E",
            font=("Helvetica", 20),
            border_color="#6a0000",
            border_width=3,
            text_color="white"
        )
        self.play_button.pack(pady=20)

        self.options_button = ctk.CTkButton(
            self,
            text="",
            image=render_button_text("OPCIONES", 30),
            command=self.open_options,
            width=300,
            height=80,
            fg_color="#490029",
            hover_color="#8B004E",
            font=("Helvetica", 20),
            border_color="#6a0000",
            border_width=3,
            text_color="white"
        )
        self.options_button.pack(pady=20)

        self.exit_button = ctk.CTkButton(
            self,
            text="",
            image=render_button_text("SALIR", 30),
            command=self.quit,
            width=300,
            height=80,
            fg_color="#490029",
            hover_color="#8B004E",
            font=("Helvetica", 20),
            border_color="#6a0000",
            border_width=3,
            text_color="white"
        )
        self.exit_button.pack(pady=20)

        # Redimensionar la imagen al tamaño de la ventana
        self.bind("<Configure>", self.resize_background)

        self.update_background()
        self.animate_gif(0)

    def setup_music(self):
        if not is_muted:
            pygame.mixer.music.load("./music/Uma Thurman 8 Bit.mp3")
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.4)
        else:
            pygame.mixer.music.set_volume(0)  # Silenciar música si is_muted es True

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
        pygame.mixer.music.stop()  
        self.withdraw()  
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

        if not is_muted:
            pygame.mixer.music.load(self.original_music)  # Cargar la música de la dificultad
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.4)
        else:
            pygame.mixer.music.set_volume(0)  # Silenciar música si is_muted es True

        game_window = design_master_form(self.difficulty, self.player_symbol, self.computer_symbol)
        game_window.mainloop()

    def open_options(self):
        self.withdraw()
        OptionsWindow(self)

    def restart_menu_music(self):
        if not is_muted:  # Verificar si la música está silenciada
            pygame.mixer.music.load("./music/Uma Thurman 8 Bit.mp3")
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.4)
        else:
            pygame.mixer.music.set_volume(0)  # Silenciar música si is_muted es True

        
    def close_window(self):
        self.destroy()

class OptionsWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        # Configuración de la ventana
        self.title("Opciones")
        self.geometry("1280x720")
        self.resizable(False, False)
        self.maxsize(1280, 720)
        self.iconbitmap("./images/icono_juego.ico")
        self.attributes('-toolwindow', True)  # Deshabilitar minimizar y maximizar

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

        self.options_label = ctk.CTkLabel(self, text="Opciones del Juego", font=("Arial", 50))
        self.options_label.pack(pady=20)

        self.difficulty_frame = SelectDifficulty(self, self.on_difficulty_selected)
        self.difficulty_frame.pack(pady=20)

        self.back_button = ctk.CTkButton(self, text="VOLVER", command=self.on_back, width=300, height=80, fg_color="#0b5345", hover_color="lightgreen", font=("Arial", 20))
        self.back_button.pack(pady=20)

        # Botón de silenciar
        self.mute_button = ctk.CTkButton(self, text="", command=self.toggle_mute, width=300, height=80, fg_color="#0b5345", hover_color="lightgreen", font=("Arial", 20))
        self.mute_button.pack(pady=20)

        # Inicializar el texto del botón según el estado de silencio
        self.update_mute_button_text()

        # Manejar el evento de cierre de la ventana
        self.protocol("WM_DELETE_WINDOW", self.close_window)

    def update_mute_button_text(self):
        if is_muted:
            self.mute_button.configure(text="ACTIVAR MÚSICA")
        else:
            self.mute_button.configure(text="SILENCIAR MÚSICA")

    def toggle_mute(self):
        global is_muted 
        is_muted = not is_muted  
        if is_muted:
            pygame.mixer.music.set_volume(0)  # Silenciar música
        else:
            pygame.mixer.music.set_volume(0.4)  # Restaurar volumen
        self.master.setup_music()  
        self.update_mute_button_text() 



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

    def on_close(self):
        pygame.mixer.music.stop()
        self.destroy()
        self.master.deiconify()
        
    def close_window(self):
        self.destroy()
        
if __name__ == "__main__":
    app = MainMenu()
    app.mainloop()
