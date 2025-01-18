import tkinter as tk
from tkinter import *
import customtkinter as ctk
from PIL import ImageTk, Image

# Variables globales
player_score = 0
computer_score = 0
empate_score = 0

# Configuración de la apariencia de CustomTkinter
ctk.set_appearance_mode("dark")  # Opciones: "light", "dark", "system"
ctk.set_default_color_theme("blue")  

class MainMenu(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Choclo Game")
        self.geometry("1080x720")

        # Cargar la imagen de fondo del menú
        self.original_image = Image.open("gif1.gif")  
        self.background_label = tk.Label(self)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)  

        self.title_label = ctk.CTkLabel(self, text="CHOCLO GAME", font=("Arial", 70), text_color="white")
        self.title_label.pack(pady=(100, 20))

        self.play_button = ctk.CTkButton(self, text="JUGAR", command=self.open_start_window, width=300, height=80, fg_color="#0b5345", hover_color="lightgreen", font=("Arial", 20))
        self.play_button.pack(pady=20)

        self.options_button = ctk.CTkButton(self, text="OPCIONES", command=self.open_options, width=300, height=80, fg_color="#0b5345", hover_color="lightgreen", font=("Arial", 20))
        self.options_button.pack(pady=20)

        self.quit_button = ctk.CTkButton(self, text="SALIR", command=self.quit, width=300, height=80, fg_color="#0b5345", hover_color="lightgreen", font=("Arial", 20))
        self.quit_button.pack(pady=20)

        self.bind("<Configure>", self.resize_background)

        self.update_background()

    def resize_background(self, event):
        self.update_background()

    def update_background(self):
        width = self.winfo_width()
        height = self.winfo_height()

        resized_image = self.original_image.resize((width, height), Image.LANCZOS)
        self.background_photo = ImageTk.PhotoImage(resized_image)

        self.background_label.configure(image=self.background_photo)
        self.background_label.image = self.background_photo 

    def open_start_window(self):
        self.withdraw() 
        start_window() 

    def open_options(self):
        self.withdraw()  
        options_window = OptionsWindow(self)  

def start_window():
    global start_window_instance
    start_window_instance = tk.Tk()
    start_window_instance.geometry("535x500")
    start_window_instance.title("Ventana de Inicio")
    start_window_instance.resizable(0,0)

    label = tk.Label(start_window_instance, text="Seleccione un símbolo para empezar", font=("Helvetica", 16))
    label.pack(pady=20)

    selected = tk.StringVar(value="X")
    x_radio = tk.Radiobutton(start_window_instance, text="X", variable=selected, value="X", font=("Helvetica", 12))
    x_radio.pack(pady=5)
    o_radio = tk.Radiobutton(start_window_instance, text="O", variable=selected, value="O", font=("Helvetica", 12))
    o_radio.pack(pady=5)

    start_button = tk.Button(start_window_instance, text="Comenzar", command=lambda: start_game(selected.get()), font=("Helvetica", 12), bg="yellow")
    start_button.pack(pady=10)

    start_window_instance.mainloop()

def start_game(selected_option):
    global player_symbol, computer_symbol, turn
    if selected_option == "X":
        player_symbol = "x"
        computer_symbol = "o"
    else:
        player_symbol = "o"
        computer_symbol = "x"
    turn = player_symbol
    start_window_instance.destroy()  
    game_window()  

def game_window():
    global root, frame1, frame2, titleLabel, buttons, game_end, turn, player_symbol, computer_symbol, board, player_score, computer_score, empate_score

    root = Tk()
    root.geometry("535x500")
    root.title("Tic Tac Toe")
    root.resizable(0,0)

    frame1 = Frame(root)
    frame1.pack()
    titleLabel = Label(frame1 , text="Tic Tac Toe" , font=("Arial" , 26) , bg="orange" , width=27 )
    titleLabel.grid(row=0 , column=0)

    frame2 = Frame(root , bg="yellow")
    frame2.pack()

    board = { 1:" " , 2:" " , 3:" ",
              4:" " , 5:" " , 6:" ",
              7:" " , 8:" " , 9:" " }

    game_end = False
    mode = "singlePlayer"

    def updateBoard():
        for key in board.keys():
            buttons[key-1]["text"] = board[key]

    def checkForWin(player):
        # rows
        if board[1] == board[2] and board[2] == board[3] and board[3] == player:
            return True
        
        elif board[4] == board[5] and board[5] == board[6] and board[6] == player:
            return True
        
        elif board[7] == board[8] and board[8] == board[9] and board[9] == player:
            return True

        # columns
        elif board[1] == board[4] and board[4] == board[7] and board[7] == player:
            return True
        
        elif board[2] == board[5] and board[5] == board[8] and board[8] == player:
            return True
        
        elif board[3] == board[6] and board[6] == board[9] and board[9] == player:
            return True
        
        # diagonals
        elif board[1] == board[5] and board[5] == board[9] and board[9] == player:
            return True
        
        elif board[3] == board[5] and board[5] == board[7] and board[7] == player:
            return True

        return False

    def resetGame():
        global game_end, board, turn
        game_end = False
        board = {i: " " for i in range(1, 10)}  # Reiniciar el tablero
        updateBoard()  # Actualizar la interfaz
        titleLabel.config(text="Tic Tac Toe")
        turn = player_symbol

    def checkForDraw():
        for i in board.keys():
            if board[i] == " ":
                return False
        return True

    def minimax(board , isMaximizing):
        if checkForWin(computer_symbol):
            return 1 
        
        if checkForWin(player_symbol):
            return -1
        
        if checkForDraw():
            return 0
        
        if isMaximizing:
            bestScore = -100
            for key in board.keys():
                if board[key] == " ":
                    board[key] = computer_symbol
                    score = minimax(board , False) # minimax
                    board[key] = " "
                    if score > bestScore : 
                        bestScore = score 
            return bestScore
        else:
            bestScore = 100
            for key in board.keys():
                if board[key] == " ":
                    board[key] = player_symbol
                    score = minimax(board , True) # minimax
                    board[key] = " "
                    if score < bestScore : 
                        bestScore = score 
            return bestScore

    def playComputer():
        bestScore = -100
        bestMove = 0
        for key in board.keys():
            if board[key] == " ":
                board[key] = computer_symbol
                score = minimax(board , False) # minimax
                board[key] = " "
                if score > bestScore : 
                    bestScore = score 
                    bestMove = key
        board[bestMove] = computer_symbol
        updateBoard()

    def play(event):
        global turn, game_end, player_score, computer_score, empate_score
        if game_end:
            return
        
        button = event.widget
        button_index = buttons.index(button) + 1
        
        if button["text"] == " ":
            board[button_index] = turn
            updateBoard()
            if checkForWin(turn):
                if turn == player_symbol:
                    player_score += 1
                else:
                    computer_score += 1
                update_score_label()
                winningLabel = Label(frame1, text=f"{turn} gana el juego", bg="orange", font=("Arial", 26), width=16)
                winningLabel.grid(row=0, column=0, columnspan=3)
                game_end = True
            elif checkForDraw():
                empate_score += 1
                update_score_label()
                drawLabel = Label(frame1, text=f"empate", bg="orange", font=("Arial", 26), width=16)
                drawLabel.grid(row=0, column=0, columnspan=3)
                game_end = True
            else:
                turn = computer_symbol if turn == player_symbol else player_symbol
                if mode == "singlePlayer" and turn == computer_symbol and not game_end:
                    playComputer()
                    if checkForWin(turn):
                        computer_score += 1
                        update_score_label()
                        winningLabel = Label(frame1, text=f"{turn} gana el juego", bg="orange", font=("Arial", 26), width=16)
                        winningLabel.grid(row=0, column=0, columnspan=3)
                        game_end = True
                    turn = player_symbol
                    updateBoard()
    def update_score_label():
        score_label.config(text=f"Jugador: {player_score} - Computadora: {computer_score} - Empates: {empate_score}")      
    buttons = []
    for i in range(3):
        for j in range(1, 4):
            button = Button(frame2, text=" ", width=4, height=2, font=("Arial", 30), bg="yellow", relief=RAISED, borderwidth=5)
            button.grid(row=i, column=j)
            button.bind("<Button-1>", play)
            buttons.append(button)

    restartButton = Button(frame2 , text="Reiniciar" , width=19 , height=1 , font=("Arial" , 20) , bg="Green" , relief=RAISED , borderwidth=5 , command=resetGame )
    restartButton.grid(row=4 , column=1 , columnspan=3)
    score_label = Label(frame1, text=f"Jugador: {player_score} - Computadora: {computer_score} - Empates: {empate_score}", font=("Arial", 16), bg="white")
    score_label.grid(row=1, column=0)
    root.mainloop()

class OptionsWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        # Configuración de la ventana
        self.title("Opciones")
        self.geometry("1080x720")

        # Cargar la imagen de fondo de la ventana de opciones
        self.original_image = Image.open("img2.jpg")  
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
