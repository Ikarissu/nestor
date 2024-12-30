import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image

def start_game():
    start_window.destroy()
    game_window()

def game_window():
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

    turn = "x"
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
        global game_end, board
        game_end = False
        board = {i: " " for i in range(1, 10)}  # Reiniciar el tablero
        updateBoard()  # Actualizar la interfaz
        for button in buttons:
            button["text"] = " "
        for i in board.keys():
            board[i] = " "
        titleLabel.config(text="Tic Tac Toe")

    def checkForDraw():
        for i in board.keys():
            if board[i] == " ":
                return False
        return True

    def minimax(board , isMaximizing):
        if checkForWin("o"):
            return 1 
        
        if checkForWin("x"):
            return -1
        
        if checkForDraw():
            return 0
        
        if isMaximizing:
            bestScore = -100
            for key in board.keys():
                if board[key] == " ":
                    board[key] = "o"
                    score = minimax(board , False) # minimax
                    board[key] = " "
                    if score > bestScore : 
                        bestScore = score 
            return bestScore
        else:
            bestScore = 100
            for key in board.keys():
                if board[key] == " ":
                    board[key] = "x"
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
                board[key] = "o"
                score = minimax(board , False) # minimax
                board[key] = " "
                if score > bestScore : 
                    bestScore = score 
                    bestMove = key
        board[bestMove] = "o"

    def play(event):
        global turn,game_end
        if game_end:
            return
        
        button = event.widget
        buttonText = str(button)
        clicked = int(buttonText.split(".")[-1]) if buttonText.split(".")[-1].isdigit() else 1
        
        if button["text"] == " ":
            if turn == "x" :
                board[clicked] = turn
                if checkForWin(turn):
                    winningLabel = Label(frame1 , text=f"{turn} gana el juego", bg="orange", font=("Arial" , 26),width=16 )
                    winningLabel.grid(row = 0 , column=0 , columnspan=3)
                    game_end = True
                turn = "o"
                updateBoard()
                if mode == "singlePlayer":
                    playComputer()
                    if checkForWin(turn):
                        winningLabel = Label(frame1 , text=f"{turn} gana el juego", bg="orange", font=("Arial" , 26),width=16   )
                        winningLabel.grid(row = 0 , column=0 , columnspan=3)
                        game_end = True
                    turn = "x"
                    updateBoard()
            else:
                board[clicked] = turn
                updateBoard()
                if checkForWin(turn):
                    winningLabel = Label(frame1 , text=f"{turn} gana el juego" , bg="orange", font=("Arial" , 26),width=16)
                    winningLabel.grid(row = 0 , column=0 , columnspan=3)
                    game_end = True
                turn = "x"
            
            if checkForDraw():
                drawLabel = Label(frame1 , text=f"empate" , bg="orange", font=("Arial" , 26), width = 16)
                drawLabel.grid(row = 0 , column=0 , columnspan=3)
            turn="x"
            
    image1 = Image.open("../nestor/pj.jpg")  # Asegúrate de que la ruta sea correcta
    new_img = image1.resize((100, 100))
    new_img.save("pj2.jpg")
    photo1 = ImageTk.PhotoImage(new_img)
    image2 = Image.open("../nestor/chocol1.jpg")  # Asegúrate de que la ruta sea correcta
    new_img = image2.resize((100, 100))
    new_img.save("chocol1-2.jpg")
    photo2 = ImageTk.PhotoImage(new_img)

    canvas1 = Canvas(frame2, width=100, height=100)  # Ajusta el tamaño según tus imágenes
    canvas1.grid(row=1, column=0)
    canvas2 = Canvas(frame2, width=100, height=100)
    canvas2.grid(row=1, column=5)

    # Crear imágenes en los canvas
    canvas1.create_image(50, 50, image=photo1)
    canvas2.create_image(50, 50, image=photo2)

    buttons = []

    for i in range(3):
        for j in range(1, 4):
            button = Button(frame2 , text= " " , width=4 , height=2  , font=("Arial" , 30) , bg="yellow" , relief=RAISED , borderwidth=5)
            button.grid(row = i , column=j)
            button.bind("<Button-1>" , play)
            buttons.append(button)

    restartButton = Button(frame2 , text="Reiniciar" , width=19 , height=1 , font=("Arial" , 20) , bg="Green" , relief=RAISED , borderwidth=5 , command=resetGame )
    restartButton.grid(row=4 , column=1 , columnspan=3)

    root.mainloop()

start_window = tk.Tk()
start_window.geometry("535x500")
start_window.title("Ventana de Inicio")
start_window.resizable(0,0)

label = tk.Label(start_window, text="Bienvenido al Juego", font=("Helvetica", 16))
label.pack(pady=20)

start_button = tk.Button(start_window, text="Comenzar", command=start_game, font=("Helvetica", 12), bg="yellow")
start_button.pack(pady=10)

start_window.mainloop()
