# Isaac Lee
# Computer Networks
# Final Project
# Really Really Bad Chess client

import pygame
import random
import socket
import sys
HOST_ADDRESS = ("192.168.56.1",1729)
BUFFER_SIZE = 4096
pygame.init()
PIECE_SIZE = 32
BB = pygame.transform.scale(pygame.image.load("blackbishop.jpg"),(PIECE_SIZE,PIECE_SIZE))
BK = pygame.transform.scale(pygame.image.load("blackking.png"),(PIECE_SIZE,PIECE_SIZE))
BN = pygame.transform.scale(pygame.image.load("blackknight.jpg"),(PIECE_SIZE,PIECE_SIZE))
BP = pygame.transform.scale(pygame.image.load("blackpawn.jpg"),(PIECE_SIZE,PIECE_SIZE))
BQ = pygame.transform.scale(pygame.image.load("blackqueen.jpg"),(PIECE_SIZE,PIECE_SIZE))
BR = pygame.transform.scale(pygame.image.load("blackrook.png"),(PIECE_SIZE,PIECE_SIZE))
WB = pygame.transform.scale(pygame.image.load("whitebishop.jpg"),(PIECE_SIZE,PIECE_SIZE))
bigWK = pygame.image.load("whiteking.png")
WK = pygame.transform.scale(bigWK,(PIECE_SIZE,PIECE_SIZE))
WN = pygame.transform.scale(pygame.image.load("whiteknight.jpg"),(PIECE_SIZE,PIECE_SIZE))
WP = pygame.transform.scale(pygame.image.load("whitepawn.jpg"),(PIECE_SIZE,PIECE_SIZE))
WQ = pygame.transform.scale(pygame.image.load("whitequeen.jpg"),(PIECE_SIZE,PIECE_SIZE))
WR = pygame.transform.scale(pygame.image.load("whiterook.jpg"),(PIECE_SIZE,PIECE_SIZE))
piecurfs = [BB,BK,BN,BP,BQ,BR,WB,WK,WN,WP,WQ,WR]
SCREEN_SIZE = 500
SQUARE_SIZE = SCREEN_SIZE // 10
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
WHITE = (255,255,255)
BORDER_WIDTH = 3
TIMEOUTTIME = 0.5
def jacobisymbol(x,n):
    result = 1
    while True:
        x %= n
        if not x:
            return 0
        numtwos = 0
        while not x % 2:
            numtwos += 1
            x //= 2
        if n % 8 in [3,5] and numtwos % 2:
            result = -result
        if x == 1:
            return result
        x,n = n,x
        if x % 4 == n % 4 == 3:
            result = -result
def randombit():
    if colour == "w":
        x = random.randint(1,nminusone)
        clientSocket.send(str((x * x) % n).encode())
        b = int(clientSocket.recv(BUFFER_SIZE).decode())
        clientSocket.send(str(x).encode())
        if jacobisymbol(x,n) == b:
            return 1
        return 0
    xsquared = int(clientSocket.recv(BUFFER_SIZE).decode())
    b = [-1,1][random.randint(0,1)]
    clientSocket.send(str(b).encode())
    x = int(clientSocket.recv(BUFFER_SIZE).decode())
    assert (x * x) % n == xsquared
    if jacobisymbol(x,n) == b:
        return 1
    return 0
def randomnumber(n):
    result = 0
    poweroftwo = 1
    for _ in range(n):
        result += randombit() * poweroftwo
        poweroftwo = poweroftwo + poweroftwo
    return result
def updateboard():
    for left in range(SQUARE_SIZE,SCREEN_SIZE - SQUARE_SIZE,SQUARE_SIZE):
        for top in range(SQUARE_SIZE,SCREEN_SIZE - SQUARE_SIZE,SQUARE_SIZE):
            if (left + top) % (SQUARE_SIZE + SQUARE_SIZE):
                screen.fill(RED,pygame.Rect(left,top,SQUARE_SIZE,SQUARE_SIZE))
            else:
                screen.fill(GREEN,pygame.Rect(left,top,SQUARE_SIZE,SQUARE_SIZE))
            piecenum = board[top // SQUARE_SIZE - 1][left // SQUARE_SIZE - 1]
            if piecenum > -1:
                screen.blit(piecurfs[piecenum],pygame.Rect(left + (SQUARE_SIZE - PIECE_SIZE) // 2,top + (SQUARE_SIZE - PIECE_SIZE) // 2,PIECE_SIZE,PIECE_SIZE))
def ischecked():
    if colour == "w":
        kingindex = wkpos[0]
        kingjindex = wkpos[1]
        desiredquotient = 0
    else:
        kingindex = bkpos[0]
        kingjindex = bkpos[1]
        desiredquotient = 1
    for index in range(8):
        for jindex in range(8):
            piece = board[index][jindex]
            if piece // 6 == desiredquotient:
                piece %= 6
                if not piece:
                    if jindex - index == kingjindex - kingindex:
                        attacked = True
                        for ind in range(min(index,kingindex) + 1,max(index,kingindex)):
                            if board[ind][ind + jindex - index] > -1:
                                attacked = False
                                break
                        if attacked:
                            return True
                    if index + jindex == kingindex + kingjindex:
                        attacked = True
                        for ind in range(min(index,kingindex) + 1,max(index,kingindex)):
                            if board[ind][jindex + index - ind] > -1:
                                attacked = False
                                break
                        if attacked:
                            return True
                if piece == 1:
                    if abs(kingindex - index) < 2 and abs(kingjindex - jindex) < 2:
                        return True
                if piece == 2:
                    if [kingindex,kingjindex] in [[index - 2,jindex + 1],[index - 1,jindex + 2],[index + 1,jindex + 2],[index + 2,jindex + 1],[index + 2,jindex - 1],[index + 1,jindex - 2],[index - 1,jindex - 2],[index - 2,jindex - 1]]:
                        return True
                if piece == 3:
                    if index == kingindex - 1 and jindex in [kingjindex - 1,kingjindex + 1]:
                        return True
                if piece == 4:
                    if jindex - index == kingjindex - kingindex:
                        attacked = True
                        for ind in range(min(index,kingindex) + 1,max(index,kingindex)):
                            if board[ind][ind + jindex - index] > -1:
                                attacked = False
                                break
                        if attacked:
                            return True
                    if index + jindex == kingindex + kingjindex:
                        attacked = True
                        for ind in range(min(index,kingindex) + 1,max(index,kingindex)):
                            if board[ind][jindex + index - ind] > -1:
                                attacked = False
                                break
                        if attacked:
                            return True
                    if jindex == kingjindex:
                        attacked = True
                        for ind in range(min(index,kingindex) + 1,max(index,kingindex)):
                            if board[ind][jindex] > -1:
                                attacked = False
                                break
                        if attacked:
                            return True
                    if index == kingindex:
                        attacked = True
                        for ind in range(min(jindex,kingjindex) + 1,max(jindex,kingjindex)):
                            if board[index][ind] > -1:
                                attacked = False
                                break
                        if attacked:
                            return True
                if piece == 5:
                    if jindex == kingjindex:
                        attacked = True
                        for ind in range(min(index,kingindex) + 1,max(index,kingindex)):
                            if board[ind][jindex] > -1:
                                attacked = False
                                break
                        if attacked:
                            return True
                    if index == kingindex:
                        attacked = True
                        for ind in range(min(jindex,kingjindex) + 1,max(jindex,kingjindex)):
                            if board[index][ind] > -1:
                                attacked = False
                                break
                        if attacked:
                            return True
    return False
def isvalidmove(fromindex,fromjindex,toindex,tojindex):
    piece = board[fromindex][fromjindex]
    board[fromindex][fromjindex] = -1
    otherpiece = board[toindex][tojindex]
    board[toindex][tojindex] = piece
    if piece % 6 == 1:
        if colour == "w":
            wkpos[0] = toindex
            wkpos[1] = tojindex
        else:
            bkpos[0] = toindex
            bkpos[1] = tojindex
    checked = ischecked()
    board[fromindex][fromjindex] = piece
    board[toindex][tojindex] = otherpiece
    piece %= 6
    if piece == 1:
        if colour == "w":
            wkpos[0] = fromindex
            wkpos[1] = fromjindex
        else:
            bkpos[0] = fromindex
            bkpos[1] = fromjindex
    if checked:
        return False
    if not piece:
        if fromjindex - fromindex == tojindex - toindex:
            valid = True
            for ind in range(min(fromindex,toindex) + 1,max(fromindex,toindex)):
                if board[ind][ind + fromjindex - fromindex] > -1:
                    valid = False
                    break
            return valid
        if fromindex + fromjindex == toindex + tojindex:
            valid = True
            for ind in range(min(fromindex,toindex) + 1,max(fromindex,toindex)):
                if board[ind][fromjindex + fromindex - ind] > -1:
                    valid = False
                    break
            return valid
        return False
    if piece == 1:
        return abs(fromindex - toindex) < 2 and abs(fromjindex - tojindex) < 2
    if piece == 2:
        return [fromindex,fromjindex] in [[toindex - 2,tojindex + 1],[toindex - 1,tojindex + 2],[toindex + 1,tojindex + 2],[toindex + 2,tojindex + 1],[toindex + 2,tojindex - 1],[toindex + 1,tojindex - 2],[toindex - 1,tojindex - 2],[toindex - 2,tojindex - 1]]
    if piece == 3:
        if fromindex == toindex + 1 and fromjindex == tojindex:
            return otherpiece == -1
        if fromindex == toindex + 2 and fromjindex == tojindex:
            return (fromindex == 7 or (fromindex == 6 and unmovedpawns[fromjindex])) and board[fromindex - 1][fromjindex] == otherpiece == -1
        if fromindex == toindex + 1 and abs(fromjindex - tojindex) == 1:
            return otherpiece > -1
        return False
    if piece == 4:
        if fromjindex - fromindex == tojindex - toindex:
            valid = True
            for ind in range(min(fromindex,toindex) + 1,max(fromindex,toindex)):
                if board[ind][ind + fromjindex - fromindex] > -1:
                    valid = False
                    break
            return valid
        if fromindex + fromjindex == toindex + tojindex:
            valid = True
            for ind in range(min(fromindex,toindex) + 1,max(fromindex,toindex)):
                if board[ind][fromjindex + fromindex - ind] > -1:
                    valid = False
                    break
            return valid
        if fromjindex == tojindex:
            valid = True
            for ind in range(min(fromindex,toindex) + 1,max(fromindex,toindex)):
                if board[ind][fromjindex] > -1:
                    valid = False
                    break
            return valid
        if fromindex == toindex:
            valid = True
            for ind in range(min(fromjindex,tojindex) + 1,max(fromjindex,tojindex)):
                if board[fromindex][ind] > -1:
                    valid = False
                    break
            return valid
        return False
    if piece == 5:
        if fromjindex == tojindex:
            valid = True
            for ind in range(min(fromindex,toindex) + 1,max(fromindex,toindex)):
                if board[ind][fromjindex] > -1:
                    valid = False
                    break
            return valid
        if fromindex == toindex:
            valid = True
            for ind in range(min(fromjindex,tojindex) + 1,max(fromjindex,tojindex)):
                if board[fromindex][ind] > -1:
                    valid = False
                    break
            return valid
        return False
def canmove():
    if colour == "w":
        quotient = 1
    else:
        quotient = 0
    for fromindex in range(8):
        for fromjindex in range(8):
            if board[fromindex][fromjindex] // 6 == quotient:
                for toindex in range(8):
                    for tojindex in range(8):
                        if board[toindex][tojindex] // 6 != quotient:
                            if isvalidmove(fromindex,fromjindex,toindex,tojindex):
                                return True
    return False
def drawbyrepetition():
    strboard = str(board)
    return strboard in dejavu and dejavu[strboard] == 2
def drawbydeadposition():
    knightpresent = False
    wbpresent = False
    bbpresent = False
    for index in range(8):
        for jindex in range(8):
            piece = board[index][jindex]
            if piece > -1:
                piecetype = piece % 6
                if piecetype > 2:
                    return False
                if piecetype == 2:
                    if knightpresent:
                        return False
                    knightpresent = True
                if not piecetype:
                    if piece:
                        if wbpresent:
                            return False
                        wbpresent = True
                        if (index + jindex) % 2:
                            wbcol = "b"
                        else:
                            wbcol = "w"
                    else:
                        if bbpresent:
                            return False
                        bbpresent = True
                        if (index + jindex) % 2:
                            bbcol = "b"
                        else:
                            bbcol = "w"
    if knightpresent:
        return not wbpresent and not bbpresent
    if wbpresent and bbpresent:
        return wbcol == bbcol
    return True
pygame.display.set_caption("Really Really Bad Chess")
pygame.display.set_icon(pygame.transform.flip(BN,False,True))
screen = pygame.display.set_mode((SCREEN_SIZE,SCREEN_SIZE))
screen.blit(bigWK,bigWK.get_rect())
fontsy = pygame.font.Font(pygame.font.get_default_font(),42)
fontsyjr = pygame.font.Font(pygame.font.get_default_font(),21)
screen.blit(fontsy.render("Welcome to Really",True,BLUE),pygame.Rect(0,42,100,50))
screen.blit(fontsy.render("Really Bad Chess!",True,BLUE),pygame.Rect(0,90,100,50))
screen.blit(fontsyjr.render("To continue, please answer the",True,BLUE),pygame.Rect(0,200,100,50))
screen.blit(fontsyjr.render("question posed at your terminal.",True,BLUE),pygame.Rect(0,225,100,50))
pygame.display.flip()
print("What's your favourite 4 digit number?")
port = int(input())
print("Issuing a challenge...")
clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientSocket.bind((socket.gethostname(),port))
clientSocket.connect(HOST_ADDRESS)
colour = clientSocket.recv(BUFFER_SIZE).decode()
n = int(clientSocket.recv(BUFFER_SIZE).decode())
nminusone = n - 1
address = clientSocket.recv(BUFFER_SIZE).decode().split(" ")
address = (address[0][2:-2],int(address[1][:-1]))
clientSocket.close()
clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientSocket.bind((socket.gethostname(),port))
clientSocket.connect(address)
clientSocket.settimeout(TIMEOUTTIME)
print("Challenge accepted!")
if colour == "w":
    print("You are white.")
else:
    print("You are black.")
print("Please redirect your attention to the Really Really Bad Chess window, for your game is about to begin!")
board = [[-1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1]]
screen.fill(WHITE)
updateboard()
screen.blit(fontsy.render("Initialising...",True,BLUE),pygame.Rect(125,229,100,50))
for event in pygame.event.get():
    if event.type == pygame.QUIT:
        sys.exit()
pygame.display.flip()
for col in range(2):
    index = 7 - 6 * col
    jindex = 7
    if colour == "b":
        index = 7 - index
        jindex = 7 - jindex
    for _ in range(16):
        number = randomnumber(3)
        while number > 4:
            number = randomnumber(3)
        board[index][jindex] = ((number + 2) % 6) + (1 - col) * 6
        if colour == "w":
            if jindex:
                jindex -= 1
            else:
                index -= 1
                jindex = 7
        else:
            jindex += 1
            if jindex == 8:
                index += 1
                jindex = 0
wkpos = [7,randomnumber(3)]
if colour == "b":
    wkpos = [0,7 - wkpos[1]]
bkpos = [0,randomnumber(3)]
if colour == "b":
    bkpos = [7,7 - bkpos[1]]
board[wkpos[0]][wkpos[1]] = 7
board[bkpos[0]][bkpos[1]] = 1
updateboard()
for event in pygame.event.get():
    if event.type == pygame.QUIT:
        sys.exit()
pygame.display.flip()
turn = "w"
unmovedpawns = []
for index in range(8):
    unmovedpawns += [board[6][index] % 6 == 3]
dejavu = {}
outcome = "dunno"
while outcome == "dunno":
    hijacktime = randomnumber(7)
    if turn == colour:
        packet = ""
        for row in board:
            for pos in row:
                packet += str(pos) + ","
        for prawn in unmovedpawns:
            packet += str(prawn) + ","
        clientSocket.send((packet + str(wkpos[0]) + "," + str(wkpos[1]) + "," + str(bkpos[0]) + "," + str(bkpos[1]) + "," + colour).encode())
        ack = clientSocket.recv(BUFFER_SIZE).decode()
        if canmove():
            if drawbyrepetition():
                outcome = "repetition"
                clientSocket.send(outcome.encode())
                if colour == "w":
                    ack = clientSocket.recv(BUFFER_SIZE).decode()
            else:
                strboard = str(board)
                if strboard in dejavu:
                    dejavu[strboard] = 2
                else:
                    dejavu[strboard] = 1
                if drawbydeadposition():
                    outcome = "dead position"
                    clientSocket.send(outcome.encode())
                    if colour == "w":
                        ack = clientSocket.recv(BUFFER_SIZE).decode()
                else:
                    screen.blit(fontsy.render("It's your turn!",True,BLUE),pygame.Rect(111,454,100,50))
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            sys.exit()
                    pygame.display.flip()
                    notmoved = True
                    previndex = -1
                    prevjindex = -1
                    promotion = False
                    while notmoved:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                sys.exit()
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                x,y = event.pos
                                if not promotion and SQUARE_SIZE <= x < SCREEN_SIZE - SQUARE_SIZE and SQUARE_SIZE <= y < SCREEN_SIZE - SQUARE_SIZE:
                                    index = y // SQUARE_SIZE - 1
                                    jindex = x // SQUARE_SIZE - 1
                                    if prevjindex == -1:
                                        if (colour == "w" and board[index][jindex] // 6 == 1) or (colour == "b" and not board[index][jindex] // 6):
                                            previndex = index
                                            prevjindex = jindex
                                            pygame.draw.rect(screen,BLUE,(x - (x % SQUARE_SIZE),y - (y % SQUARE_SIZE),SQUARE_SIZE,SQUARE_SIZE),BORDER_WIDTH)
                                            pygame.display.flip()
                                    else:
                                        if (colour == "w" and board[index][jindex] // 6 == 1) or (colour == "b" and not board[index][jindex] // 6):
                                            if (previndex + prevjindex) % 2:
                                                pygame.draw.rect(screen,RED,((prevjindex + 1) * SQUARE_SIZE,(previndex + 1) * SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE),BORDER_WIDTH)
                                            else:
                                                pygame.draw.rect(screen,GREEN,((prevjindex + 1) * SQUARE_SIZE,(previndex + 1) * SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE),BORDER_WIDTH)
                                            previndex = index
                                            prevjindex = jindex
                                            pygame.draw.rect(screen,BLUE,(x - (x % SQUARE_SIZE),y - (y % SQUARE_SIZE),SQUARE_SIZE,SQUARE_SIZE),BORDER_WIDTH)
                                            pygame.display.flip()
                                        elif isvalidmove(previndex,prevjindex,index,jindex):
                                            try:
                                                fromindex,fromjindex,toindex,tojindex = map(int,clientSocket.recv(BUFFER_SIZE).decode().split(","))
                                                overruled = True
                                            except socket.timeout:
                                                fromindex = previndex
                                                fromjindex = prevjindex
                                                toindex = index
                                                tojindex = jindex
                                                overruled = False
                                            clientSocket.send((str(7 - fromindex) + "," + str(7 - fromjindex) + "," + str(7 - toindex) + "," + str(7 - tojindex)).encode())
                                            board[toindex][tojindex] = board[fromindex][fromjindex]
                                            board[fromindex][fromjindex] = -1
                                            if board[toindex][tojindex] % 6 == 1:
                                                if colour == "w":
                                                    wkpos = [toindex,tojindex]
                                                else:
                                                    bkpos = [toindex,tojindex]
                                            if board[toindex][tojindex] % 6 == 3:
                                                if fromindex == 6:
                                                    unmovedpawns[fromjindex] = False
                                                if not toindex:
                                                    if overruled:
                                                        waiting = True
                                                        while waiting:
                                                            try:
                                                                piece = int(clientSocket.recv(BUFFER_SIZE).decode())
                                                                waiting = False
                                                            except socket.timeout:
                                                                waiting = True
                                                        board[toindex][tojindex] = piece
                                                        if colour == "b":
                                                            clientSocket.send("ack".encode())
                                                        screen.fill(WHITE)
                                                        updateboard()
                                                        pygame.display.flip()
                                                        notmoved = False
                                                        break
                                                    else:
                                                        screen.blit(fontsyjr.render("Pick a piece:",True,BLUE),pygame.Rect(50,14,100,50))
                                                        if colour == "w":
                                                            offset = 6
                                                        else:
                                                            offset = 0
                                                        screen.blit(piecurfs[offset],pygame.Rect(259,9,PIECE_SIZE,PIECE_SIZE))
                                                        screen.blit(piecurfs[2 + offset],pygame.Rect(309,9,PIECE_SIZE,PIECE_SIZE))
                                                        screen.blit(piecurfs[4 + offset],pygame.Rect(359,9,PIECE_SIZE,PIECE_SIZE))
                                                        screen.blit(piecurfs[5 + offset],pygame.Rect(409,9,PIECE_SIZE,PIECE_SIZE))
                                                        pygame.display.flip()
                                                        promotion = True
                                                        continue
                                            if colour == "w":
                                                ack = clientSocket.recv(BUFFER_SIZE).decode()
                                            screen.fill(WHITE)
                                            updateboard()
                                            pygame.display.flip()
                                            notmoved = False
                                            break
                                if promotion and 9 <= y < 41 and (259 <= x < 291 or 309 <= x < 341 or 359 <= x < 391 or 409 <= x < 441):
                                    if 259 <= x < 291:
                                        piece = offset
                                    if 309 <= x < 341:
                                        piece = offset + 2
                                    if 359 <= x < 391:
                                        piece = offset + 4
                                    if 409 <= x < 441:
                                        piece = offset + 5
                                    board[toindex][tojindex] = piece
                                    ack = clientSocket.recv(BUFFER_SIZE).decode()
                                    clientSocket.send(str(piece).encode())
                                    if colour == "w":
                                        ack = clientSocket.recv(BUFFER_SIZE).decode()
                                    screen.fill(WHITE)
                                    updateboard()
                                    pygame.display.flip()
                                    notmoved = False
                                    break
        else:
            if ischecked():
                outcome = "checkmate"
                if colour == "w":
                    winner = "b"
                else:
                    winner = "w"
            else:
                outcome = "stalemate"
            clientSocket.send(outcome.encode())
            if colour == "w":
                ack = clientSocket.recv(BUFFER_SIZE).decode()
    else:
        packet = clientSocket.recv(BUFFER_SIZE).decode().split(",")
        opponentboard = []
        for index in range(0,64,8):
            opponentboard += [list(map(int,packet[index:index + 8]))]
        opponentpawns = []
        for pawn in packet[64:72]:
            opponentpawns += [pawn == "True"]
        opponentwkpos = [int(packet[72]),int(packet[73])]
        opponentbkpos = [int(packet[74]),int(packet[75])]
        opponentcolour = packet[76]
        clientSocket.send("ack".encode())
        notmoved = True
        screen.blit(fontsyjr.render("Time until hijacking allowed:",True,BLUE),pygame.Rect(50,464,100,50))
        screen.blit(fontsy.render(str(hijacktime // 60) + ":" + "0" * (1 - (hijacktime % 60) // 10) + str(hijacktime % 60),True,BLUE),pygame.Rect(350,454,100,50))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        prevtime = pygame.time.get_ticks()
        pygame.display.flip()
        promotion = False
        previndex = -1
        prevjindex = -1
        while notmoved:
            try:
                if promotion:
                    raise socket.timeout()
                message = clientSocket.recv(BUFFER_SIZE).decode()
                if message in ["checkmate","stalemate","repetition","dead position"]:
                    outcome = message
                    winner = colour
                    if colour == "b":
                        clientSocket.send("ack".encode())
                    break
                fromindex,fromjindex,toindex,tojindex = map(int,message.split(","))
                if board[toindex][tojindex] % 6 == 3 and toindex == 6:
                    unmovedpawns[tojindex] = False
                board[toindex][tojindex] = board[fromindex][fromjindex]
                board[fromindex][fromjindex] = -1
                if board[toindex][tojindex] % 6 == 1:
                    if colour == "w":
                        bkpos = [toindex,tojindex]
                    else:
                        wkpos = [toindex,tojindex]
                if board[toindex][tojindex] % 6 == 3 and toindex == 7:
                    clientSocket.send("ack".encode())
                    waiting = True
                    while waiting:
                        try:
                            board[toindex][tojindex] = int(clientSocket.recv(BUFFER_SIZE).decode())
                            waiting = False
                        except socket.timeout:
                            waiting = True
                if colour == "b":
                    clientSocket.send("ack".encode())
                screen.fill(WHITE)
                updateboard()
                pygame.display.flip()
                notmoved = False
            except socket.timeout:
                if hijacktime:
                    hijacktime -= 1
                    pygame.draw.rect(screen,WHITE,pygame.Rect(350,454,100,50))
                    screen.blit(fontsy.render(str(hijacktime // 60) + ":" + "0" * (1 - (hijacktime % 60) // 10) + str(hijacktime % 60),True,BLUE),pygame.Rect(350,454,100,50))
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            sys.exit()
                    pygame.time.wait(1000 - pygame.time.get_ticks() + prevtime)
                    prevtime = pygame.time.get_ticks()
                    pygame.display.flip()
                else:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            sys.exit()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            x,y = event.pos
                            if not promotion and SQUARE_SIZE <= x < SCREEN_SIZE - SQUARE_SIZE and SQUARE_SIZE <= y < SCREEN_SIZE - SQUARE_SIZE:
                                index = y // SQUARE_SIZE - 1
                                jindex = x // SQUARE_SIZE - 1
                                if prevjindex == -1:
                                    if (colour == "b" and board[index][jindex] // 6 == 1) or (colour == "w" and not board[index][jindex] // 6):
                                        previndex = index
                                        prevjindex = jindex
                                        pygame.draw.rect(screen,BLUE,(x - (x % SQUARE_SIZE),y - (y % SQUARE_SIZE),SQUARE_SIZE,SQUARE_SIZE),BORDER_WIDTH)
                                        pygame.display.flip()
                                else:
                                    if (colour == "b" and board[index][jindex] // 6 == 1) or (colour == "w" and not board[index][jindex] // 6):
                                        if (previndex + prevjindex) % 2:
                                            pygame.draw.rect(screen,RED,((prevjindex + 1) * SQUARE_SIZE,(previndex + 1) * SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE),BORDER_WIDTH)
                                        else:
                                            pygame.draw.rect(screen,GREEN,((prevjindex + 1) * SQUARE_SIZE,(previndex + 1) * SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE),BORDER_WIDTH)
                                        previndex = index
                                        prevjindex = jindex
                                        pygame.draw.rect(screen,BLUE,(x - (x % SQUARE_SIZE),y - (y % SQUARE_SIZE),SQUARE_SIZE,SQUARE_SIZE),BORDER_WIDTH)
                                        pygame.display.flip()
                                    else:
                                        opponentboard,board = board,opponentboard
                                        unmovedpawns,opponentpawns = opponentpawns,unmovedpawns
                                        wkpos,opponentwkpos = opponentwkpos,wkpos
                                        opponentbkpos,bkpos = bkpos,opponentbkpos
                                        opponentcolour,colour = colour,opponentcolour
                                        if isvalidmove(7 - previndex,7 - prevjindex,7 - index,7 - jindex):
                                            opponentboard,board = board,opponentboard
                                            unmovedpawns,opponentpawns = opponentpawns,unmovedpawns
                                            wkpos,opponentwkpos = opponentwkpos,wkpos
                                            opponentbkpos,bkpos = bkpos,opponentbkpos
                                            opponentcolour,colour = colour,opponentcolour
                                            clientSocket.send((str(7 - previndex) + "," + str(7 - prevjindex) + "," + str(7 - index) + "," + str(7 - jindex)).encode())
                                            if board[index][jindex] % 6 == 3 and index == 6:
                                                unmovedpawns[jindex] = False
                                            board[index][jindex] = board[previndex][prevjindex]
                                            board[previndex][prevjindex] = -1
                                            if board[index][jindex] % 6 == 1:
                                                if colour == "b":
                                                    wkpos = [index,jindex]
                                                else:
                                                    bkpos = [index,jindex]
                                            if board[index][jindex] % 6 == 3 and index == 7:
                                                screen.blit(fontsyjr.render("Pick a piece:",True,BLUE),pygame.Rect(50,14,100,50))
                                                if colour == "b":
                                                    offset = 6
                                                else:
                                                    offset = 0
                                                screen.blit(piecurfs[offset],pygame.Rect(259,9,PIECE_SIZE,PIECE_SIZE))
                                                screen.blit(piecurfs[2 + offset],pygame.Rect(309,9,PIECE_SIZE,PIECE_SIZE))
                                                screen.blit(piecurfs[4 + offset],pygame.Rect(359,9,PIECE_SIZE,PIECE_SIZE))
                                                screen.blit(piecurfs[5 + offset],pygame.Rect(409,9,PIECE_SIZE,PIECE_SIZE))
                                                pygame.display.flip()
                                                promotion = True
                                                continue
                                            waiting = True
                                            while waiting:
                                                try:
                                                    ack = clientSocket.recv(BUFFER_SIZE).decode()
                                                    waiting = False
                                                except socket.timeout:
                                                    waiting = True
                                            if colour == "b":
                                                clientSocket.send("ack".encode())
                                            screen.fill(WHITE)
                                            updateboard()
                                            pygame.display.flip()
                                            notmoved = False
                                            break
                                        opponentboard,board = board,opponentboard
                                        unmovedpawns,opponentpawns = opponentpawns,unmovedpawns
                                        wkpos,opponentwkpos = opponentwkpos,wkpos
                                        opponentbkpos,bkpos = bkpos,opponentbkpos
                                        opponentcolour,colour = colour,opponentcolour
                            if promotion and 9 <= y < 41 and (259 <= x < 291 or 309 <= x < 341 or 359 <= x < 391 or 409 <= x < 441):
                                if 259 <= x < 291:
                                    piece = offset
                                if 309 <= x < 341:
                                    piece = offset + 2
                                if 359 <= x < 391:
                                    piece = offset + 4
                                if 409 <= x < 441:
                                    piece = offset + 5
                                board[index][jindex] = piece
                                waiting = True
                                while waiting:
                                    try:
                                        ack = clientSocket.recv(BUFFER_SIZE).decode()
                                        waiting = False
                                    except socket.timeout:
                                        waiting = True
                                clientSocket.send(str(piece).encode())
                                if colour == "w":
                                    ack = clientSocket.recv(BUFFER_SIZE).decode()
                                screen.fill(WHITE)
                                updateboard()
                                pygame.display.flip()
                                notmoved = False
                                break
    if turn == "w":
        turn = "b"
    else:
        turn = "w"
if outcome == "checkmate":
    if winner == "w":
        screen.blit(fontsyjr.render("White wins by checkmate!",True,BLUE),pygame.Rect(50,14,100,50))
    else:
        screen.blit(fontsyjr.render("Black wins by checkmate!",True,BLUE),pygame.Rect(50,14,100,50))
else:
    screen.blit(fontsyjr.render("Draw by " + outcome + "!",True,BLUE),pygame.Rect(50,14,100,50))
for event in pygame.event.get():
    if event.type == pygame.QUIT:
        sys.exit()
pygame.display.flip()
