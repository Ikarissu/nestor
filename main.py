import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
import random

player_score = 0
computer_score = 0
empate_score = 0
difficulty = "easy"
player_symbol = ""
computer_symbol = ""
turn = ""



def select_difficulty():
    global difficulty_window
    difficulty_window = Toplevel(start_window)
    difficulty_window.geometry("300x200")
    difficulty_window.title("Seleccionar Dificultad")

    label = tk.Label(difficulty_window, text="Selecciona la Dificultad", font=("Helvetica", 12))
    label.pack(pady=10)

    def set_difficulty(selected_difficulty):
        global difficulty
        difficulty = selected_difficulty
        difficulty_window.destroy()
        select_symbol()

    easy_button = tk.Button(difficulty_window, text="Facil", command=lambda: set_difficulty("easy"))
    easy_button.pack(pady=5)
    hard_button = tk.Button(difficulty_window, text="Medio", command=lambda: set_difficulty("medium"))
    hard_button.pack(pady=5)
    medium_button = tk.Button(difficulty_window, text="Difícil", command=lambda: set_difficulty("hard"))
    medium_button.pack(pady=5)

def select_symbol():
    global symbol_window
    symbol_window = Toplevel(start_window)
    symbol_window.geometry("300x200")
    symbol_window.title("Seleccionar Ficha")

    label = tk.Label(symbol_window, text="Selecciona tu Ficha", font=("Helvetica", 12))
    label.pack(pady=10)

    def start_game(symbol):
        global player_symbol, computer_symbol, turn
        player_symbol = symbol
        
        if difficulty == "easy":
            computer_symbol = "O" if player_symbol == "X" else "X"
        elif difficulty == "medium":
            computer_symbol = "Z" if player_symbol == "Y" else "Y"
        elif difficulty == "hard":
            computer_symbol = "M" if player_symbol == "S" else "S"
        
        turn = player_symbol
        symbol_window.destroy()
        game_window()

    if difficulty == "medium":
        tk.Button(symbol_window, text="Y", command=lambda: start_game("Y")).pack(pady=5)
        tk.Button(symbol_window, text="Z", command=lambda: start_game("Z")).pack(pady=5)
    elif difficulty == "hard":
        tk.Button(symbol_window, text="S", command=lambda: start_game("S")).pack(pady=5)
        tk.Button(symbol_window, text="M", command=lambda: start_game("M")).pack(pady=5)
    else:
        tk.Button(symbol_window, text="X", command=lambda: start_game("X")).pack(pady=5)
        tk.Button(symbol_window, text="O", command=lambda: start_game("O")).pack(pady=5)

def game_window():
    global root, frame1, frame2, titleLabel, buttons, game_end, waiting_for_computer, canvas1, canvas2
    global image1_initial, image2_initial, image1_victory, image2_victory, image1_defeat, image2_defeat, image_draw1, image_draw2

    root = Toplevel()
    root.geometry("600x600")  # Aumentar el tamaño de la ventana
    root.title("Tic Tac Toe")
    root.resizable(0, 0)

    bg_color = "lightgreen" if difficulty == "easy" else "lightblue" if difficulty == "medium" else "salmon"
    root.configure(bg=bg_color)

    frame1 = Frame(root)
    frame1.pack()
    
    titleLabel = Label(frame1, text="Tic Tac Toe", font=("Arial", 26), bg=bg_color, width=27)
    titleLabel.grid(row=0, column=0)

    frame2 = Frame(root, bg=bg_color)
    frame2.pack()

    # Redimensionar y cargar las imágenes después de crear la ventana principal
    # Redimensionar y cargar las imágenes después de crear la ventana principal
    image1_initial = Image.open("C_Base.jpg").resize((100, 100), Image.Resampling.LANCZOS)
    image2_initial = Image.open("P_Base.jpg").resize((100, 100), Image.Resampling.LANCZOS)
    image1_victory = Image.open("C_Gana.jpg").resize((100, 100), Image.Resampling.LANCZOS)
    image2_victory = Image.open("P_Gana.jpg").resize((100, 100), Image.Resampling.LANCZOS)
    image1_defeat = Image.open("C_Pierde.jpg").resize((100, 100), Image.Resampling.LANCZOS)
    image2_defeat = Image.open("P_Pierde.jpg").resize((100, 100), Image.Resampling.LANCZOS)
    image_draw1 = Image.open("C_Empata.jpg").resize((100, 100), Image.Resampling.LANCZOS)
    image_draw2 = Image.open("P_Empata.jpg").resize((100, 100), Image.Resampling.LANCZOS)

    image1_initial = ImageTk.PhotoImage(image1_initial)
    image2_initial = ImageTk.PhotoImage(image2_initial)
    image1_victory = ImageTk.PhotoImage(image1_victory)
    image2_victory = ImageTk.PhotoImage(image2_victory)
    image1_defeat = ImageTk.PhotoImage(image1_defeat)
    image2_defeat = ImageTk.PhotoImage(image2_defeat)
    image_draw1 = ImageTk.PhotoImage(image_draw1)
    image_draw2 = ImageTk.PhotoImage(image_draw2)

    canvas1 = Canvas(frame2, width=100, height=100)  # Ajusta el tamaño según tus imágenes
    canvas1.grid(row=1, column=0)
    canvas2 = Canvas(frame2, width=100, height=100)
    canvas2.grid(row=1, column=5)

    # Inicializar imágenes en los canvas
    canvas1.create_image(50, 50, image=image1_initial)
    canvas2.create_image(50, 50, image=image2_initial)

    global board
    board = {i: " " for i in range(1, 10)}

    global game_end, waiting_for_computer
    game_end = False
    waiting_for_computer = False
    mode = "singlePlayer"

    def update_images(result):
        if result == "victory":
            canvas1.create_image(50, 50, image=image1_victory)
            canvas2.create_image(50, 50, image=image2_defeat)
        elif result == "defeat":
            canvas1.create_image(50, 50, image=image1_defeat)
            canvas2.create_image(50, 50, image=image2_victory)
        elif result == "draw":
            canvas1.create_image(50, 50, image=image_draw1)
            canvas2.create_image(50, 50, image=image_draw2)
        elif result == "initial":
            canvas1.create_image(50, 50, image=image1_initial)
            canvas2.create_image(50, 50, image=image2_initial)


    def updateBoard():
        for key in board.keys():
            buttons[key-1]["text"] = board[key]

    def checkForWin(player):
        if board[1] == board[2] == board[3] == player:
            return True
        elif board[4] == board[5] == board[6] == player:
            return True
        elif board[7] == board[8] == board[9] == player:
            return True
        elif board[1] == board[4] == board[7] == player:
            return True
        elif board[2] == board[5] == board[8] == player:
            return True
        elif board[3] == board[6] == board[9] == player:
            return True
        elif board[1] == board[5] == board[9] == player:
            return True
        elif board[3] == board[5] == board[7] == player:
            return True
        return False

    def resetGame():
        global game_end, board, turn, waiting_for_computer
        game_end = False
        waiting_for_computer = False
        board = {i: " " for i in range(1, 10)}
        updateBoard()
        titleLabel.config(text="Tic Tac Toe")
        update_images("initial")  # Resetear imágenes a las iniciales
        turn = player_symbol
        enable_buttons()

    def checkForDraw():
        return all(board[i] != " " for i in board.keys())

    def minimax(board, isMaximizing, depth, max_depth):
        if depth == max_depth:
            return 0  # Retorna un valor neutral si se alcanza la profundidad máxima
        
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
                    score = minimax(board, False, depth + 1, max_depth)  # Llamada recursiva con profundidad incrementada
                    board[key] = " "
                    if score > bestScore: 
                        bestScore = score 
            return bestScore
        else:
            bestScore = 100
            for key in board.keys():
                if board[key] == " ":
                    board[key] = player_symbol
                    score = minimax(board, True, depth + 1, max_depth)  # Llamada recursiva con profundidad incrementada
                    board[key] = " "
                    if score < bestScore: 
                        bestScore = score 
            return bestScore

    def playComputer():
        global turn
        bestMove = None
        if difficulty == "easy":
            while True:
                r = random.randrange(1, 10) 
                if board[r] == " ":
                    board[r] = computer_symbol
                    break  
        
        elif difficulty == "hard":
            bestScore = -100
            bestMove = 0
            max_depth = 12 # Profundidad máxima limitada
            for key in board.keys():
                if board[key] == " ":
                    board[key] = computer_symbol
                    score = minimax(board, False, 0, max_depth)  # Llamada a minimax con profundidad limitada
                    board[key] = " "
                    if score > bestScore: 
                        bestScore = score 
                        bestMove = key
            board[bestMove] = computer_symbol

        elif difficulty == "medium":
            bestScore = -100
            bestMove = 0
            max_depth = 2 # Profundidad máxima limitada
            for key in board.keys():
                if board[key] == " ":
                    board[key] = computer_symbol
                    score = minimax(board, False, 0, max_depth)  # Llamada a minimax con profundidad limitada
                    board[key] = " "
                    if score > bestScore: 
                        bestScore = score 
                        bestMove = key
            board[bestMove] = computer_symbol

        updateBoard()

    def play(event):
        global turn, game_end, player_score, computer_score, empate_score, waiting_for_computer
        if game_end or waiting_for_computer:
            return
        
        button = event.widget
        button_index = buttons.index(button) + 1
        
        if button["text"] == " ":
            board[button_index] = turn
            updateBoard()
            if checkForWin(turn):
                if turn == player_symbol:
                    player_score += 1
                    update_images("victory")
                else:
                    computer_score += 1
                    update_images("defeat")
                update_score_label()
                titleLabel.config(text=f"{turn} gana el juego")
                game_end = True
            elif checkForDraw():
                empate_score += 1
                update_images("draw")
                update_score_label()
                titleLabel.config(text="Empate")
                game_end = True
            else:
                turn = computer_symbol if turn == player_symbol else player_symbol
                if mode == "singlePlayer" and turn == computer_symbol and not game_end:
                    disable_buttons()
                    waiting_for_computer = True
                    root.after(1000, lambda: playComputerAndCheckWin())

    def playComputerAndCheckWin():
        global turn, game_end, computer_score, empate_score, waiting_for_computer
        playComputer()
        if checkForWin(computer_symbol):
            computer_score += 1
            update_score_label()
            titleLabel.config(text=f"{computer_symbol} gana el juego")
            update_images("defeat")
            game_end = True
        elif checkForDraw():
            empate_score += 1
            update_images("draw")
            update_score_label()
            titleLabel.config(text="Empate")
            game_end = True
        else:
            turn = player_symbol
        waiting_for_computer = False
        enable_buttons()

    def update_score_label():
        score_label.config(text=f"Jugador: {player_score} - Computadora: {computer_score} - Empates: {empate_score}")      
    
    def disable_buttons():
        for button in buttons:
            button.config(state="disabled")

    def enable_buttons():
        for button in buttons:
            button.config(state="normal")

    buttons = []
    for i in range(3):
        for j in range(1, 4):
            button = Button(frame2, text=" ", width=4, height=2, font=("Arial", 30), bg=bg_color, relief=RAISED, borderwidth=5)
            button.grid(row=i, column=j)
            button.bind("<Button-1>", play)
            buttons.append(button)

    restartButton = Button(frame2, text="Reiniciar", width=19, height=1, font=("Arial", 20), bg="Green", relief=RAISED, borderwidth=5, command=resetGame)
    restartButton.grid(row=4, column=1, columnspan=3)

    exitButton = Button(frame2, text="Salir", width=19, height=1, font=("Arial", 20), bg="red", relief=RAISED, borderwidth=5, command=exit_game)
    exitButton.grid(row=5, column=1, columnspan=3)

    score_label = Label(frame1, text=f"Jugador: {player_score} - Computadora: {computer_score} - Empates: {empate_score}", font=("Arial", 16), bg="white")
    score_label.grid(row=1, column=0)
    
    start_window.withdraw()  # Ocultar la ventana de inicio

    root.mainloop()

def exit_game():
    global root
    root.destroy()  # Cerrar la ventana del juego
    start_window.deiconify()  # Mostrar la ventana de inicio

start_window = tk.Tk()
start_window.geometry("535x500")
start_window.title("Ventana de Inicio")
start_window.resizable(0, 0)

label = tk.Label(start_window, text="Bienvenido al Juego", font=("Helvetica", 16))
label.pack(pady=20)

start_button = tk.Button(start_window, text="Iniciar Juego", command=select_difficulty, font=("Helvetica", 12), bg="yellow")
start_button.pack(pady=10)

start_window.mainloop()
