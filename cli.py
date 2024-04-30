import socket, sys

# Main function, called at the end
def main():
    if len(sys.argv) < 3:
        print("\nCorrect format: python3", sys.argv[0], "<server hostname> <server port>\n")
        print("Default format: python3", sys.argv[0], "127.0.0.1 1235\n")
    else:
        host = sys.argv[1]
        port = int(sys.argv[2])
        connSock = controlCONN(host, port)
    # Show menu
    menuCMD()
    # User terminal command handling
    while True:
        userInput = input("\nSecChat> ").split()
        if len(userInput) > 1:
            command = userInput[0]
            userName = userInput[1]
        elif len(userInput) == 1:
            command = userInput[0]
        else:
            print("\nPlease provide a command. Type 'menu' for a list of appropriate commands")
            continue
        if command == "menu":
            menuCMD()
        elif command == "chat":
            if len(userInput) == 2:
                secureChat(connSock, userName)
            else:
                print("invalid input: please provide a username")
        elif command == "status":
            if len(userInput) == 2:
                userStatus(connSock, userName)
            else:
                print("invalid input: please provide a username")
        elif command == "all":
            userStatusAll(connSock)
        elif command == "quit":
            quit(connSock)
            break
        else:
            print("\nInvalid command. Type 'menu' for a list of appropriate commands")

    connSock.close()
    print("Control connection to the Secure Chat server closed.\n")
    print("Bye :D\n")
    return

# Control connection function
def controlCONN(host, port):
    connSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"\nConnecting to the Secure Chat server: ({host}, {port})\n")
    connSock.connect((host, port))
    print("Control connection to the Secure Chat server successful.")
    return connSock

# Client requests data connection from server and creates socket with 
# ephemeral port for incoming connection from server
def requestDataConnection(connSock):
    # Generate random ephemeral port for data connection from server
    welcomeSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    welcomeSock.bind(('',0))
    ephemeralPort = welcomeSock.getsockname()[1]
    ephemeralPortCopy = ephemeralPort

    # Send ephemeral port to server and wait for data connection
    ephemeralPortSizeStr = str(len(str(ephemeralPort)))
    while len(ephemeralPortSizeStr) < 10:
        ephemeralPortSizeStr = "0" + ephemeralPortSizeStr
    ephemeralPort = ephemeralPortSizeStr.encode() + str(ephemeralPort).encode()
    numSent = 0 
    while len(ephemeralPort) > numSent:
        numSent += connSock.send(ephemeralPort[numSent:])
    welcomeSock.listen(1)
    serverSock, addr = welcomeSock.accept()
    return serverSock, addr, ephemeralPortCopy

# Send data to server using control connection socket
def sendData(connSock, data):
    dataSizeStr = str(len(str(data)))
    while len(dataSizeStr) < 10:
        dataSizeStr = "0" + dataSizeStr
    data = dataSizeStr.encode() + str(data).encode()
    numSent = 0 
    while len(data) > numSent:
        numSent += connSock.send(data[numSent:])
    return

# Receive incoming bytes from data connection socket initiated by server
def recvAll(serverSock, numBytes):
  data = str()
  tmpData = str()
  data = data.encode()
  while len(data) < numBytes:
     tmpData =  serverSock.recv(numBytes)
     if not tmpData:
        break
     data += tmpData
  return data

# Create the secure chat between users
def secureChat(connSock, userName):
    sendData(connSock, 'chat')
    sendData(connSock, userName)
    serverSock, addr, ephemeralPort = requestDataConnection(connSock)
    data = str()
    dataSize = str()
    dataSize = recvAll(serverSock, 10)
    data = recvAll(serverSock, int(dataSize.decode()))
    data = data.decode("utf-8")
    print(f"\n{data}\n")
    serverSock.close()
    return

# Check a user's status
def userStatus(connSock, userName):
    sendData(connSock, 'status')
    sendData(connSock, userName)
    serverSock, addr, ephemeralPort = requestDataConnection(connSock)
    data = str()
    dataSize = str()
    dataSize = recvAll(serverSock, 10)
    data = recvAll(serverSock, int(dataSize.decode()))
    data = data.decode("utf-8")
    print(f"\n{data}\n")
    serverSock.close()
    return

# List out all registered users statuses
def userStatusAll(connSock):
    sendData(connSock, 'all')
    serverSock, addr, ephemeralPort = requestDataConnection(connSock)
    data = str()
    dataSize = str()
    dataSize = recvAll(serverSock, 10)
    data = recvAll(serverSock, int(dataSize.decode()))
    data = data.decode("utf-8")
    print(f"\n{data}\n")
    serverSock.close()
    return

# Send quit command to server to let server know contoll connection has ended
def quit(connSock):
    sendData(connSock, 'quit')
    return

#Function controlling menu command
def menuCMD():
    print("\nClient Main Menu:\n")
    print("menu - list commands")
    print("chat <username> - initiate secure chat with provided user")
    print("status <username> - check if provided user is online")
    print("all - list status of all registered users")
    print("quit - exit the connection")
    return
main()