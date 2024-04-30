import socket
import threading

# Dictionary to store user credentials
# Change it to use a secure storage mechanism
USER_CREDENTIALS = {
    "user1": "password1",
    "user2": "password2",
    "user3": "password3"
}

# Dictionary to store user statuses
USER_STATUS = {}

# Dictionary to store user sockets
USER_SOCKETS = {}

# A lock to prevent race conditions when modifying dictionaries
lock = threading.Lock()

####### THE TCP SERVER #######

# The port number on which to listen for incoming
# connections.
PORT_NUMBER = 1235

# Function to handle client connection
def handle_client_connection(cliSock):
    # Authenticate user
    authenticated_user = False
    while not authenticated_user:
        cliSock.send("Enter your username and password: ".encode())
        username_password = cliSock.recv(1024).decode().strip().split(',')
        username = username_password[0]
        password = username_password[1]
        
        if USER_CREDENTIALS.get(username) == password:
            authenticated_user = True
            with lock:
                USER_STATUS[username] = "online"
                USER_SOCKETS[username] = cliSock
            cliSock.send("Authentication successful. You are now online.".encode())
        else:
            cliSock.send("Invalid username or password. Please try again.".encode())

    # Main chat loop
    while True:
        cliSock.send("Enter the user ids of users you wish to chat with (comma-separated): ".encode())
        user_ids = cliSock.recv(1024).decode().strip().split(',')
        online_users = [user for user in user_ids if USER_STATUS.get(user) == "online"]
        
        cliSock.send(f"Online users: {', '.join(online_users)}\n".encode())
        invite = cliSock.recv(1024).decode().strip().split(',')
        for user in invite:
            if user in online_users:
                user_socket = USER_SOCKETS[user]
                user_socket.send(f"You have been invited to chat by {username}.\n".encode())

# Create a socket
serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# Associate the socket with the port
serverSock.bind(('', PORT_NUMBER)) 

# Start listening for incoming connections (we can have
# at most 100 connections waiting to be accepted before
# the server starts rejecting new connections)
serverSock.listen(100)

# Keep accepting connections forever
while True:
    print("Waiting for clients to connect...")
    
    # Accept a waiting connection
    cliSock, cliInfo = serverSock.accept()
    
    print("Client connected from: " + str(cliInfo))
    
    # Create a thread to handle client connection
    threading.Thread(target=handle_client_connection, args=(cliSock,)).start()
