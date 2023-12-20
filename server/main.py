import socket
import json
import asyncio
from numpy import zeros, dot, empty

HOST = '192.168.242.136'
PORT = 6666
LENGTH_BUFFER = 10**8

def conjugate_gradient_method(A, b, x, N):
    s = 1
    p = zeros(N)
    while s <=N:
        if s == 1:
            r = dot(A.T, dot(A, x) - b)
        else:
            r = r - q/dot(p, q)
        p = p + r/dot(r,r)
        q = dot(A.T, dot(A, p))
        x = x - p/dot(p, q)
        s = s + 1
    return x


async def solve_slau(conn, message):
    loop = asyncio.get_event_loop()

    N = message["column"]
    M = message["row"]
    coefs = message["coefs"]
    coefs_free = message["coefs_free"]

    #print (coefs)
    #print (coefs_free)

    A = empty((M, N)); b = empty(M)

    coefs_list = coefs.split()
    #print(coefs_list)

    for i in range(M):
        for j in range(N):
            A[i, j] = coefs_list[j + i * N]
    
    coefs_free_list = coefs_free.split()
    #print(coefs_free_list)

    for i in range(M):
        b[i] = coefs_free_list[i]

    x = zeros(N)

    x = conjugate_gradient_method(A, b, x, N)

    # проверка
    for i in range(M):
        sum = 0
        for j in range(N):
            sum += A[i, j] * x[j]
        print(sum)

    data = ''
    for i in range(N):
        data += str(x[i])
        data += ' '

    response = {
        "task" : "solve", 
        "column" : message["column"],
        "solutions" : data.split()
    }

    await loop.sock_sendall(conn, bytes(json.dumps(response), encoding="utf-8"))


async def client_handler(conn):
    loop = asyncio.get_event_loop()
    while True:
        data = (await loop.sock_recv(conn, LENGTH_BUFFER)).decode('utf8')
        if(data==None):
            continue
        #print(data)
        try:
            message = json.loads(data)
        except Exception as e:
            print(e)
            print("SS")
            conn.close()
            break
        try:
            match message["task"]:
                case "solve":
                    await solve_slau(conn, message)
                case _:
                    await loop.sock_sendall(conn, str.encode(json.dumps({"task" : "", "response" : {"code" : 400, "body" : "No such command"}})))

        except Exception as e:
            print(e)
            print('e')
            await loop.sock_sendall(conn, str.encode(json.dumps({"error" : str(e)})))
            conn.close()
            break

async def run_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    server.setblocking(False)

    loop = asyncio.get_event_loop()

    while True:
        client,_ = await loop.sock_accept(server)
        try:
            loop.create_task(client_handler(client))
        except asyncio.CancelledError:
            print('cancel_me(): отмена ожидания')

asyncio.run(run_server())