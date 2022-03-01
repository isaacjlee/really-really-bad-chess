# Isaac Lee
# Computer Networks
# Final Project
# Really Really Bad Chess server

import random
import socket
PORT = 1729
NUMBER_SIZE = 128
NUMBER_OF_ROUNDS = 128
COLOURS = ["w".encode(),"b".encode()]
def millerrabin(n,base):
    nminusone = n - 1
    r = 0
    d = nminusone
    while not d % 2:
        r += 1
        d //= 2
    x = pow(base,d,n)
    if x in [1,nminusone]:
        return True
    for _ in range(r - 1):
        x = (x * x) % n
        if x == nminusone:
            return True
    return False
def isprobablyprime(n):
    nminustwo = n - 2
    for _ in range(NUMBER_OF_ROUNDS):
        if not millerrabin(n,random.randint(2,nminustwo)):
            return False
    return True
serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
serverSocket.bind((socket.gethostname(),PORT))
serverSocket.listen(1)
lowerBound = 2 ** (NUMBER_SIZE - 3)
upperBound = (2 ** (NUMBER_SIZE - 2)) - 1
while True:
    firstConnectionSocket,firstAddress = serverSocket.accept()
    secondConnectionSocket,secondAddress = serverSocket.accept()
    randomColour = random.randint(0,1)
    firstConnectionSocket.send(COLOURS[randomColour])
    secondConnectionSocket.send(COLOURS[1 - randomColour])
    n = 1
    for _ in range(2):
        p = 4 * random.randint(lowerBound,upperBound) + 3
        while not isprobablyprime(p):
            p = 4 * random.randint(lowerBound,upperBound) + 3
        n *= p
    n = str(n).encode()
    firstConnectionSocket.send(n)
    secondConnectionSocket.send(n)
    firstConnectionSocket.send(str(secondAddress).encode())
    secondConnectionSocket.send(str(firstAddress).encode())
    firstConnectionSocket.close()
    secondConnectionSocket.close()
