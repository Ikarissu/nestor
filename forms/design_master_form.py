import tkinter as tk
from tkinter import font, messagebox
from PIL import Image, ImageTk
import useful.useful_image as useful_img
import useful.useful_window as useful_window
import random

from config import (
    Top_Bar_color_easy, Top_Bar_color_medium, Top_Bar_color_hard,
    Sidebar_color_easy, Sidebar_color_medium, Sidebar_color_hard,
    Main_Body_color_easy, Main_Body_color_medium, Main_Body_color_hard,
    Hover_Menu_color_easy, Hover_Menu_color_medium, Hover_Menu_color_hard
)

class design_master_form(tk.Toplevel):
    
    def __init__(self, difficulty, player_symbol, computer_symbol):
        super().__init__()
        self.title('Choclo Game')
        self.geometry("1280x720")
        self.iconbitmap("./images/icono_juego.ico")

        # Deshabilitar la opción de maximizar la ventana
        self.resizable(False, False)

        # Fijar el tamaño mínimo y máximo de la ventana
        self.minsize(1280, 720)
        self.maxsize(1280, 720)

        self.difficulty = difficulty
        self.player_symbol = player_symbol
        self.computer_symbol = computer_symbol
        self.turn = self.player_symbol

        # Variables globales del juego
        self.player_score = 0
        self.computer_score = 0
        self.empate_score = 0
        self.game_end = False
        self.waiting_for_computer = False
        self.mode = "singlePlayer"
        self.board = {i: " " for i in range(1, 10)}

        # Declarar self.perfil
        self.perfil = useful_img.read_image("./images/jugador.png", (100, 100))

        # Cargar las imágenes
        self.load_images()

        # Ajustar colores según la dificultad
        if self.difficulty == "easy":
            self.Top_Bar_color = Top_Bar_color_easy
            self.Sidebar_color = Sidebar_color_easy
            self.Main_Body_color = Main_Body_color_easy
            self.Hover_Menu_color = Hover_Menu_color_easy
        elif self.difficulty == "medium":
            self.Top_Bar_color = Top_Bar_color_medium
            self.Sidebar_color = Sidebar_color_medium
            self.Main_Body_color = Main_Body_color_medium
            self.Hover_Menu_color = Hover_Menu_color_medium
        elif self.difficulty == "hard":
            self.Top_Bar_color = Top_Bar_color_hard
            self.Sidebar_color = Sidebar_color_hard
            self.Main_Body_color = Main_Body_color_hard
            self.Hover_Menu_color = Hover_Menu_color_hard
            
        self.create_widgets()
        self.updateBoard()

    def load_images(self):
        self.image1_initial = Image.open("./images/C_Base.png").resize((100, 100), Image.Resampling.LANCZOS)
        self.image2_initial = Image.open("./images/P_Base.png").resize((100, 100), Image.Resampling.LANCZOS)
        self.image1_victory = Image.open("./images/C_Gana.png").resize((100, 100), Image.Resampling.LANCZOS)
        self.image2_victory = Image.open("./images/P_Gana.png").resize((100, 100), Image.Resampling.LANCZOS)
        self.image1_defeat = Image.open("./images/C_Pierde.png").resize((100, 100), Image.Resampling.LANCZOS)
        self.image2_defeat = Image.open("./images/P_Pierde.png").resize((100, 100), Image.Resampling.LANCZOS)
        self.image_draw1 = Image.open("./images/C_Empata.png").resize((100, 100), Image.Resampling.LANCZOS)
        self.image_draw2 = Image.open("./images/P_Empata.png").resize((100, 100), Image.Resampling.LANCZOS)

        self.image1_initial = ImageTk.PhotoImage(self.image1_initial)
        self.image2_initial = ImageTk.PhotoImage(self.image2_initial)
        self.image1_victory = ImageTk.PhotoImage(self.image1_victory)
        self.image2_victory = ImageTk.PhotoImage(self.image2_victory)
        self.image1_defeat = ImageTk.PhotoImage(self.image1_defeat)
        self.image2_defeat = ImageTk.PhotoImage(self.image2_defeat)
        self.image_draw1 = ImageTk.PhotoImage(self.image_draw1)
        self.image_draw2 = ImageTk.PhotoImage(self.image_draw2)

    def create_widgets(self):
        # Cargar la imagen de fondo
        self.original_image = Image.open("./images/habitacion.gif")
        self.background_photo = ImageTk.PhotoImage(self.original_image)

        self.background_label = tk.Label(self, image=self.background_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Crear el marco principal
        main_frame = tk.Frame(self, bg="")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Crear la barra superior
        self.top_bar_controls(main_frame)

        # Crear la barra lateral
        self.side_bar_controls(main_frame)

        # Crear el marco del juego
        game_frame = tk.Frame(main_frame, bg="white")
        game_frame.pack(expand=True)

        self.buttons = []
        for i in range(9):
            button = tk.Button(game_frame, text="", font=("Helvetica", 24), width=5, height=2,
                               command=lambda i=i: self.on_button_click(i))
            button.grid(row=i // 3, column=i % 3, padx=5, pady=5)
            self.buttons.append(button)

        # Añadir los Canvas para las imágenes
        self.canvas1 = tk.Canvas(game_frame, width=100, height=100)
        self.canvas1.grid(row=0, column=3)
        self.canvas2 = tk.Canvas(game_frame, width=100, height=100)
        self.canvas2.grid(row=0, column=4)

        # Inicializar imágenes en los canvas
        self.canvas1.create_image(50, 50, image=self.image1_initial)
        self.canvas2.create_image(50, 50, image=self.image2_initial)

        self.bind("<Configure>", self.resize_background)

    def top_bar_controls(self, main_frame):
        top_bar = tk.Frame(main_frame, bg=self.Top_Bar_color, height=50)
        top_bar.pack(side=tk.TOP, fill=tk.X)

        font_awesome = font.Font(family='fontAwesome', size=12)

        self.labelTitle = tk.Label(top_bar, text="Choclo game")
        self.labelTitle.config(fg="#fff", font=("Helvetica", 15), bg=self.Top_Bar_color, pady=10, width=16)
        self.labelTitle.pack(side=tk.LEFT)

        self.buttonsidebar = tk.Button(top_bar, text="\uf0c9", font=font_awesome,
                                       command=self.toggle_panel, bd=0, bg=self.Top_Bar_color, fg="white")
        self.buttonsidebar.pack(side=tk.LEFT)

        self.labelTitle = tk.Label(top_bar, text="¡Bienvenido a choclo game!")
        self.labelTitle.config(fg="#fff", font=("Helvetica", 15), bg=self.Top_Bar_color, padx=20, width=20)
        self.labelTitle.pack(side=tk.RIGHT)

    def side_bar_controls(self, main_frame):
        side_bar = tk.Frame(main_frame, bg=self.Sidebar_color, width=200)
        side_bar.pack(side=tk.LEFT, fill=tk.Y)

        width_menu = 20
        height_menu = 2
        font_awesome = font.Font(family='FontAwesome', size=12)

        self.labelperfil = tk.Label(side_bar, image=self.perfil, bg=self.Sidebar_color)
        self.labelperfil.pack(side=tk.TOP, pady=15)

        self.buttonScore = tk.Button(side_bar)
        self.buttonProfile = tk.Button(side_bar)
        self.buttonPicture = tk.Button(side_bar)
        self.buttonInfo = tk.Button(side_bar)
        self.buttonMenu = tk.Button(side_bar, text="Volver al Menú", command=self.open_menu)
        self.buttonReset = tk.Button(side_bar, text="Reiniciar Partida", command=self.resetGame)
        
        self.score_label = tk.Label(side_bar, text=f"Partidas Ganadas: {self.player_score}\nPartidas Perdidas: {self.computer_score}\nPartidas Empatadas: {self.empate_score}",pady=10, font=("Helvetica", 12), bg=self.Sidebar_color, fg="white")
        self.score_label.pack(pady=10)

        buttons_info = [
            ("Reiniciar Partida", "\uf0ad", self.buttonReset),
            ("Volver al Menú", "\uf0ad", self.buttonMenu)
        ]

        for text, icon, button in buttons_info:
            self.bar_button_config(button, text, icon, font_awesome, width_menu, height_menu)

    def bar_button_config(self, button, text, icon, font_awesome, width_menu, height_menu):
        button.config(text=f'  {icon}   {text}', anchor='w', font=font_awesome,
                      bd=0, bg=self.Sidebar_color, fg='white', width=width_menu, height=height_menu)
        button.pack(side=tk.TOP)
        self.bind_hover_events(button)

    def bind_hover_events(self, button):
        button.bind("<Enter>", lambda event: self.on_enter(event, button))
        button.bind("<Leave>", lambda event: self.on_leave(event, button))

    def on_enter(self, event, button):
        button.config(bg=self.Hover_Menu_color, fg='white')

    def on_leave(self, event, button):
        button.config(bg=self.Sidebar_color, fg='white')

    def toggle_panel(self):
        if self.side_bar.winfo_ismapped():
            self.side_bar.pack_forget()
        else:
            self.side_bar.pack(side=tk.LEFT, fill='y')

    def updateBoard(self):
        for key in self.board.keys():
            self.buttons[key-1]["text"] = self.board[key]

    def checkForWin(self, player):
        if self.board[1] == self.board[2] == self.board[3] == player:
            return True
        elif self.board[4] == self.board[5] == self.board[6] == player:
            return True
        elif self.board[7] == self.board[8] == self.board[9] == player:
            return True
        elif self.board[1] == self.board[4] == self.board[7] == player:
            return True
        elif self.board[2] == self.board[5] == self.board[8] == player:
            return True
        elif self.board[3] == self.board[6] == self.board[9] == player:
            return True
        elif self.board[1] == self.board[5] == self.board[9] == player:
            return True
        elif self.board[3] == self.board[5] == self.board[7] == player:
            return True
        return False

    def resetGame(self):
        self.game_end = False
        self.waiting_for_computer = False
        self.board = {i: " " for i in range(1, 10)}
        self.updateBoard()
        self.update_images("initial")  # Resetear imágenes a las iniciales
        self.turn = self.player_symbol
        self.enable_buttons()

    def checkForDraw(self):
        return all(self.board[i] != " " for i in self.board.keys())

    def minimax(self, board, depth, isMaximizing, max_depth):
        if depth == max_depth:
            return 0  # Retorna un valor neutral si se alcanza la profundidad máxima
        
        if self.checkForWin(self.computer_symbol):
            return 1 
        
        if self.checkForWin(self.player_symbol):
            return -1
        
        if self.checkForDraw():
            return 0
        
        if isMaximizing:
            bestScore = -float('inf')
            for key in board.keys():
                if board[key] == " ":
                    board[key] = self.computer_symbol
                    score = self.minimax(board, depth + 1, False, max_depth)  # Llamada recursiva con profundidad incrementada
                    board[key] = " "
                    bestScore = max(score, bestScore)
            return bestScore
        else:
            bestScore = float('inf')
            for key in board.keys():
                if board[key] == " ":
                    board[key] = self.player_symbol
                    score = self.minimax(board, depth + 1, True, max_depth)  # Llamada recursiva con profundidad incrementada
                    board[key] = " "
                    bestScore = min(score, bestScore)
            return bestScore

    def playComputer(self):
        bestMove = None
        if self.difficulty == "easy":
            while True:
                r = random.randrange(1, 10)
                if self.board[r] == " ":
                    self.board[r] = self.computer_symbol
                    break
        
        elif self.difficulty == "medium":
            bestScore = -float('inf')
            bestMove = 0
            max_depth = 2  # Profundidad máxima limitada
            for key in self.board.keys():
                if self.board[key] == " ":
                    self.board[key] = self.computer_symbol
                    score = self.minimax(self.board, 0, False, max_depth)  # Llamada a minimax con profundidad limitada
                    self.board[key] = " "
                    if score > bestScore: 
                        bestScore = score 
                        bestMove = key
            self.board[bestMove] = self.computer_symbol

        elif self.difficulty == "hard":
            bestScore = -float('inf')
            bestMove = 0
            max_depth = 12  # Profundidad máxima limitada
            for key in self.board.keys():
                if self.board[key] == " ":
                    self.board[key] = self.computer_symbol
                    score = self.minimax(self.board, 0, False, max_depth)  # Llamada a minimax con profundidad limitada
                    self.board[key] = " "
                    if score > bestScore: 
                        bestScore = score 
                        bestMove = key
            self.board[bestMove] = self.computer_symbol

        self.updateBoard()

    def on_button_click(self, index):
        if self.board[index + 1] == " " and not self.game_end:
            self.board[index + 1] = self.turn
            self.updateBoard()
            if self.checkForWin(self.turn):
                if self.turn == self.player_symbol:
                    self.player_score += 1
                    self.update_images("victory")
                else:
                    self.computer_score += 1
                    self.update_images("defeat")
                self.update_score_label()
                self.labelTitle.config(text=f"{self.turn} gana el juego")
                self.game_end = True
            elif self.checkForDraw():
                self.empate_score += 1
                self.update_images("draw")
                self.update_score_label()
                self.labelTitle.config(text="Empate")
                self.game_end = True
            else:
                self.turn = self.computer_symbol if self.turn == self.player_symbol else self.player_symbol
                if self.mode == "singlePlayer" and self.turn == self.computer_symbol and not self.game_end:
                    self.disable_buttons()
                    self.waiting_for_computer = True
                    self.after(1000, self.playComputerAndCheckWin)

    def playComputerAndCheckWin(self):
        self.playComputer()
        if self.checkForWin(self.computer_symbol):
            self.computer_score += 1
            self.update_score_label()
            self.labelTitle.config(text=f"{self.computer_symbol} gana el juego")
            self.update_images("defeat")
            self.game_end = True
        elif self.checkForDraw():
            self.empate_score += 1
            self.update_images("draw")
            self.update_score_label()
            self.labelTitle.config(text="Empate")
            self.game_end = True
        else:
            self.turn = self.player_symbol
        self.waiting_for_computer = False
        self.enable_buttons()

    def update_images(self, result):
        if result == "victory":
            self.canvas1.create_image(50, 50, image=self.image1_victory)
            self.canvas2.create_image(50, 50, image=self.image2_defeat)
        elif result == "defeat":
            self.canvas1.create_image(50, 50, image=self.image1_defeat)
            self.canvas2.create_image(50, 50, image=self.image2_victory)
        elif result == "draw":
            self.canvas1.create_image(50, 50, image=self.image_draw1)
            self.canvas2.create_image(50, 50, image=self.image_draw2)
        elif result == "initial":
            self.canvas1.create_image(50, 50, image=self.image1_initial)
            self.canvas2.create_image(50, 50, image=self.image2_initial)

    def update_score_label(self):
        self.score_label.config(text=f"Partidas Ganadas: {self.player_score}\nPartidas Perdidas: {self.computer_score}\nPartidas Empatadas: {self.empate_score}")

    def disable_buttons(self):
        for button in self.buttons:
            button.config(state="disabled")

    def enable_buttons(self):
        for button in self.buttons:
            button.config(state="normal")

    def resize_background(self, event):
        width = self.winfo_width()
        height = self.winfo_height()
        resized_image = self.original_image.resize((width, height), Image.LANCZOS)
        self.background_photo = ImageTk.PhotoImage(resized_image)
        self.background_label.config(image=self.background_photo)

    def open_menu(self):
        self.destroy()  # Cierra la ventana actual
        self.master.deiconify()  # Muestra el menú