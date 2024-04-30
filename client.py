import socket
import threading

# Server's IP address
SERVER_IP = "127.0.0.1"

# The server's port number
SERVER_PORT = 1235

# The client's socket
cliSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Attempt to connect to the server
cliSock.connect((SERVER_IP, SERVER_PORT))

# Authenticate user
authenticated = False
while not authenticated:
    response = cliSock.recv(1024).decode()
    print(response)
    if response == "Enter your username and password: ":
        username = input("username: ")
        password = input("password: ")
        user_pass = username + "," + password
        print("user_pass: ", user_pass)
        cliSock.send(user_pass.encode())
    else:
        if response == "Authentication successful. You are now online.":
            authenticated = True
        else:
            print("Invalid username or password. Please try again.")

# Main chat loop
while True:
    response = cliSock.recv(1024).decode()
    print(response)
    users_to_invite = input()
    cliSock.send(users_to_invite.encode())
    print(cliSock.recv(1024).decode())
    invite = input("Enter the user ids of users you wish to invite to chat (comma-separated): ")
    cliSock.send(invite.encode())

