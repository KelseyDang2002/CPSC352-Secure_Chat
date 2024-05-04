import socket
import sys
import threading
from users import serverAuthenticateUser
from sendReceive import recvAll
from secureChat import serverSecureChat
from userStatus import serverUserStatus, serverUserStatusAll


# Main function, is called at end of program
def main():
    listenPort = str()
    # Open socket for incoming connection from client with desired port #
    if len(sys.argv) < 2:
        print("\nCorrect format: python", sys.argv[0], "<server port>\n")
        print("Default format: python", sys.argv[0], "1235\n")
    else:
        listenPort = sys.argv[1]
    welcomeSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    welcomeSock.bind(("", int(listenPort)))
    welcomeSock.listen(1)

    # Forever wait for incoming connection from client
    while True:
        print("\nWaiting for connection...\n")
        clientSock, addr = welcomeSock.accept()
        print("Control connection accepted from client:", addr, "\n")

        # Start a new thread for each client
        client_thread = threading.Thread(target=handle_client, args=(clientSock, addr))
        client_thread.start()


def handle_client(clientSock, addr):

    # Authenticate user
    print("Authenticating user...\n")
    authenticated = False
    while not authenticated:
        authenticated, username = serverAuthenticateUser(clientSock)

    print("\n" + username + " Authenticated!\n")

    # Receive command from client through control connection
    # and call a funcion accordingly
    while True:
        commandSize = recvAll(clientSock, 10)
        if commandSize.decode():
            command = recvAll(clientSock, int(commandSize.decode())).decode()
        if command == "chat":
            serverSecureChat(clientSock, addr)
        if command == "status":
            serverUserStatus(clientSock, addr)
        if command == "all":
            serverUserStatusAll(clientSock, addr)
        if command == "quit":
            break

    clientSock.close()
    print("\nControl connection closed.\n")
    print(f"Bye {username} :D\n")
    return



main()
