import threading
import json
import socket
from numpy import empty
from random import random

HOST = '127.0.0.1'
PORT = 6666
LENGTH_BUFFER = 10**8

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
    s.connect((HOST, PORT))

    while True:
        N = int(input('количество решений: '))
        M = int(input('количество уравнений: '))

        A = empty((M, N)); b = empty(M)

        coefs = ''
        for i in range(M):
            for j in range(N):
                A[i, j] = random()
                coefs += str(A[i, j]) + ' '

        coefs_free = ''
        for i in range(M):
            b[i] = random()
            coefs_free += str(b[i]) + ' '

        print(b)

        message = {
            "task" : "solve", 
            "column" : N,
            "row" : M,
            "coefs" : coefs.strip(),
            "coefs_free" : coefs_free.strip()
        }
        data = json.dumps(message)
        s.sendall((bytes(data, encoding="utf-8")))

        request = json.loads(s.recv(LENGTH_BUFFER).decode("utf8"))
        print(request)
