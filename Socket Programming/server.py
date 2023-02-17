# import socket library
import socket

# import threading library
import threading

# Choose a port that is free
#PORT number cannot be bigger than 65536
#First 1024 is reserved
PORT = 52345

# An IPv4 address is obtained
# for the server.
SERVER = "172.20.10.6"




# the format in which encoding
# and decoding will occur
FORMAT = "utf-8"

# Lists that will contains
# all the clients connected to
# the server and their names.
clients, names = [], []

# Create a new TCP socket for
#We prefer to use TCP socket because there is no data loss..
# the server
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# bind the address of the
# server to the socket
server.bind((SERVER, PORT))


# function to start the connection


def startApp():
    print("server is working on " + SERVER)

    # listening for connections
    server.listen()

    while True:

        conn, addr = server.accept()
        conn.send("NAME".encode(FORMAT))

        # 1024 represents the max amount
        # of data that can be received (bytes)
        name = conn.recv(1024).decode(FORMAT)

        # append the name and client

        names.append(name)
        clients.append(conn)

        print(f"Name is :{name}")

        # broadcast message
        broadcastMessage(f"{name} has joined the chat!".encode(FORMAT))

        conn.send('Connection successful!'.encode(FORMAT))

        # Start the handling thread
        thread = threading.Thread(target=handle,
                                  args=(conn, addr))
        thread.start()

        # no. of clients connected
        # to the server
        print(f"active connections {threading.activeCount() - 1}")


# method to handle the
# incoming messages


def handle(conn, addr):
    print(f"new connection {addr}")
    connected = True

    while connected:
        # receive message
        message = conn.recv(1024)

        # broadcast message
        broadcastMessage(message)

    # close the connection
    conn.close()


# method for broadcasting
# messages to the each clients


def broadcastMessage(message):
    for client in clients:
        client.send(message)


# call the method to
# begin the communication
startApp()