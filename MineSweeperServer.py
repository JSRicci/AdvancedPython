import socket
import threading
import time
import random
import operator

Players=[]
stop = False
timer = 1
playerNum = 0
score = 0
playerScores = {}
echo_queue = []
minecoord = []
neighborCoord = []
status = ''
neighbor = []
checkcoord = []
NeighborMines = []
up_right, up_left, up, left, right, down_left, down_right, down = [], [], [], [] ,[] ,[] ,[] ,[]
removedcoord = []

#Generate random mines as put into neighbormines and minecoord lists
for i in range(0, 40):
    x = random.randrange(1, 17)
    y = random.randrange(1, 17)
    coord = x, y
    neighborCoord.append(coord)
    minecoord.append(str(x) + ',' + str(y))

#Keep track of score for each player
def scoreKeeper(playerNum, score):
    global playerScores
    playerScores = {playerNum:score}
    print(playerScores)
#Check if the clicked coordinate are mines or not
def checkMine(clickcoord, neighborCoord):
    if ':' not in clickcoord:
        clickcoord = clickcoord.split(',')
        x = clickcoord[0]
        x = int(x)
        y = clickcoord[1]
        y = int(y)
        up_right = x + 1, y + 1
        checkcoord.append(up_right)
        up_left = x -1, y + 1
        checkcoord.append(up_left)
        up = x, y + 1
        checkcoord.append(up)
        left = x - 1, y
        checkcoord.append(left)
        right = x + 1, y
        checkcoord.append(right)
        down_right = x + 1, y - 1
        checkcoord.append(down_right)
        down_left = x - 1, y - 1
        checkcoord.append(down_left)
        down = x, y - 1
        checkcoord.append(down)
        NeighborMines = set(neighborCoord).intersection(checkcoord)
        del checkcoord[:] #Erase the surrounding coordinates for the next click coordinates
        return(NeighborMines)

#Recieve packets from each minesweeper client
def clientecho (sock, score, playerNum):
    global removedcoord
    global minecoord
    while True:
        data = sock.recv(4096)
        clickcoord = data.decode()
        clickcoord = str(clickcoord)
        if 'I WIN!' in clickcoord:
            print('last mine')
            print('game over')
            Winner = '1'
            print('Player ' + Winner + ' won!')
            status = 'Winner'
        else:
            SendNeighbors = checkMine(clickcoord, neighborCoord)
            # ':' determines whether or not a flag should be used
            if ':' not in clickcoord:
                if any(x in clickcoord for x in removedcoord):
                    status = 'used'
                elif any(x in clickcoord for x in minecoord):
                    removedcoord.append(str(clickcoord))
                    if clickcoord in minecoord:
                        minecoord.remove(clickcoord)
                    else:
                        status = 'MINE!'
                    if len(minecoord)== 0:
                        print('last mine')
                        print('game over')
                        Winner = max(playerScores.iteritems(), key=operator.itemgetter(1))[0] #Determine the winner by comparing scores
                        print('Player ' + Winner + ' won!')
                        status = 'Winner'
                    else:
                        score = score - 5 #Deduct points for clicking mine
                else:
                    status = 'CLEAR' #Clear spot, there is no mine
                    if len(SendNeighbors) >= 1: #add a point to score if the click coordinates are next to a mine
                        score = score + 1
                    else:
                        score = score + 0
            # ',' is used to reveal a button
            elif ',' not in clickcoord:
                flagcoord = clickcoord.replace(':',',')
                print(flagcoord)
                print(minecoord)
                if any(x in flagcoord for x in minecoord):
                    minecoord.remove(str(flagcoord))
                    status = 'FlaggedMine'
                    score = score + 1
                    if len(minecoord)== 0:
                        print('last mine')
                        print('game over')
                        Winner = max(playerScores.iteritems(), key=operator.itemgetter(1))[0] #Determine the winner by comparing scores
                        print('Player ' + Winner + ' won!')
                        status = 'Winner'
                else:
                    status = 'FlaggedCLEAR' #Clear spot, there is no mine
                    score = score + 0
            sendScore = str(score)
            if ':' not in clickcoord:
                NumNeighbors = len(SendNeighbors)
                NumNeighbors = str(NumNeighbors)
                sock.send(str.encode(NumNeighbors))
            else:
                NumNeighbors = '0'
                sock.send(str.encode(NumNeighbors))
            sock.send(str.encode(sendScore))
            sock.send(str.encode(status))
            playerScores = scoreKeeper(playerNum, score) #Update player score
            if data:
                peerName = sock.getpeername()
                scoreList = peerName, score
                if data.decode() != "getmesome":
                    queuelock.acquire()
                    echo_queue.append(data.decode())
                    queuelock.release()
                else:
                    queuelock.acquire()
                    data = echo_queue[0]
                    del echo_queue[0]
                    queuelock.release()
                    sock.send(b"Echoing: " + str.encode(data))
            else:
                print("Ending connection with: ", sock.getpeername())
                sock.close()
                break

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("", 2001))
sock.listen(5)
queuelock = threading.Lock()

while True:
    scoreKeeper(playerNum, 0)
    clientsock, addr = sock.accept()
    playerNum += 1
    Players.append(addr[1])
    t = threading.Thread(target=clientecho, args=(clientsock, score, playerNum))
    t.start()





