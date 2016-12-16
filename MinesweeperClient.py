import socket
import tkinter

loop = True
flag = False
global sock
button = False
buttonLst = []
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#When the shift key and mouse button 1 are pressed change button to True
def keydown(e):
    global button
    button = True
#When the shift key and mouse button 1 are released change button to False
def keyup(e):
    global button
    button = False
#Verify what the button condition is and decide which action to take
def check(row, col):
    if button is True:
        right_click(row, col)
    else:
        left_click(row, col)
#When the user left clicks then they reveal the tile
def left_click(row, col):
    sock.send(str.encode(str(row) + ',' + str(col)))
    NumNeighbors = sock.recv(4096)
    NumNeighbors = str(NumNeighbors)
    NumNeighbors = NumNeighbors.strip("b'")
    NumNeighbors = NumNeighbors.strip("'")
    score = sock.recv(4096)
    showScore(score)
    status = sock.recv(4096)
    status = str(status)
    status = status.strip("b'")
    status = status.strip("'")
    print(status)
    #This button was already pressed
    if status == 'used':
        button = tkinter.Button(w, text="Mine", bg="red", height=1, width=3)
        button.grid(row=row, column=col)
    #There is a mine at these coordinates
    elif status == 'MINE!':
        button = tkinter.Button(w, text="Mine", bg="red", height=1, width=3)
        button.grid(row=row, column=col)
    #There is no mine, update button with the number of surrounding mines
    elif status == 'CLEAR':
        button = tkinter.Button(None, text="%s" % (NumNeighbors), bg="green", height=1, width=3)
        button.grid(row=row, column=col)
    #If the player flags a button but there is no mine then player does not get a point, change tile to yellow
    elif status == 'FlaggedCLEAR':
        button = tkinter.Button(w, text="Flag", bg="yellow", height=1, width=3)
        button.grid(row=row, column=col)
    #There is a mine under the flag, award player 1 point and change tile to yellow
    elif status == 'FlaggedMine':
        button = tkinter.Button(w, text="Flag", bg="yellow", height=1, width=3)
        button.grid(row=row, column=col)
    #If the player recieves this message then they have won
    elif status == 'Winner':
        print('You Won!')
    else:
        print('error')
#When the user shift clicks then they flag a tile
def right_click(row, col):
    sock.send(str.encode(str(row) + ':' + str(col)))
    NumNeighbors = sock.recv(4096)
    NumNeighbors = str(NumNeighbors)
    NumNeighbors = NumNeighbors.strip("b'")
    NumNeighbors = NumNeighbors.strip("'")
    score = sock.recv(4096)
    showScore(score)
    status = sock.recv(4096)
    status = str(status)
    status = status.strip("b'")
    status = status.strip("'")
    button = tkinter.Button(w, text="Flag", bg="yellow", height=1, width=3)
    button.grid(row=row, column=col)
#Keep track of score
def showScore(score):
    score = str(score)
    score = score.strip("b")
    score = score.strip("'")
    label = tkinter.Label(w, text="Testing")
    label.grid(row=0, column=0, columnspan=5, padx=10, pady=10)
    label.configure(text="Your score is: " + score)
#Create a tiled window
def startGame(n):
    btnStart.pack_forget()
    label = tkinter.Label(w, text="Server Message: ")
    label.configure(text="Your score is: 0")
    label.grid(row=0, column=0, columnspan=5, padx=10, pady=10)
    for row in range(1, 17):
        for col in range(1, 17):
            button = tkinter.Button(w, command=lambda row=row, col=col: check(row, col), height=1, width=3)
            button.myname = str(row)+','+str(col)
            buttonLst.append(str(row)+','+str(col))
            button.grid(row=row, column=col)
    sock.connect(("127.0.0.1", 2001))
#A quick way to check all buttons
def autoWin(e):
    sock.send(str.encode('I WIN!'))
w = tkinter.Tk()
w.title("Minesweeper Client")
w.bind("<Shift-Button-1>", keydown)
w.bind("<KeyRelease>", keyup)
w.bind("1", autoWin)
btnStart = tkinter.Button(w, text="Start Game")
btnStart.pack()
btnStart.bind('<Button-1>', startGame)
w.geometry("700x500+150+150")
w.mainloop()
sock.close()