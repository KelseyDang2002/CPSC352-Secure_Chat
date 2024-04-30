import socket, sys, os

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
    welcomeSock.bind(('', int(listenPort)))
    welcomeSock.listen(1)

    # Forever wait for incoming connection from client
    while True:
        print("\nWaiting for connection...\n")   
        clientSock, addr = welcomeSock.accept()
        print("Control connection accepted from client:", addr, "\n")

        # Receive command from client through control connection 
        # and call a funcion accordingly
        while True:
          command = str()
          commandSize = str()
          commandSize = recvAll(clientSock, 10)
          if commandSize.decode():
            command = recvAll(clientSock, int(commandSize.decode())).decode()
          if command == 'chat':
            secureChat(clientSock, addr)
          if command == 'status':
            userStatus(clientSock, addr)
          if command == 'all':
            userStatusAll(clientSock, addr)
          if command == 'quit':
             break

        clientSock.close()
        print("\nControl connection closed.\n")
        print("Bye :D\n")
        return

# Receive incoming bytes (including command, ephemeral port and other data)
def recvAll(clientSock, numBytes):
  data = str()
  tmpData = str()
  data = data.encode()
  while len(data) < numBytes:
     tmpData =  clientSock.recv(numBytes)
     if not tmpData:
        break
     data += tmpData
  return data

# Send data to server using control connection socket
def sendData(dataSock, data):
    dataSizeStr = str(len(str(data)))
    while len(dataSizeStr) < 10:
        dataSizeStr = "0" + dataSizeStr
    data = dataSizeStr.encode() + str(data).encode()
    numSent = 0 
    while len(data) > numSent:
        numSent += dataSock.send(data[numSent:])
    return

# Server retrieves ephemeral port and creates data connection when requested by client
# (ephemeral port generated and submited by client along with the request)
def createDataConnection(clientSock, addr):
    ephemeralPort = str()
    ephemeralPortSize = str()
    ephemeralPortSize = recvAll(clientSock, 10)
    ephemeralPort = int(recvAll(clientSock, int(ephemeralPortSize.decode())).decode())
    dataSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dataSock.connect((addr[0], ephemeralPort))
    return dataSock, ephemeralPort

# Get username from client
def getUserName(clientSock):
    userName = str()
    userNameSize = str()
    userNameSize = recvAll(clientSock, 10)
    userName = recvAll(clientSock, int(userNameSize.decode())).decode()
    return userName

# Setup secure chat
def secureChat(clientSock, addr):
    userName = getUserName(clientSock)
    dataSock, ephemeralPort = createDataConnection(clientSock, addr)  # Create data connection and connect to client to begin data transfer
    print("Data connection successfully established with client on ephemeral port #", ephemeralPort ,"\n")
    data = "Secure Chat functionality under construction"
    sendData(dataSock, data)
    dataSock.close()
    print("Data connection to client closed.\n")
    return

# Check status of a user
def userStatus(clientSock, addr):
    userName = getUserName(clientSock)
    dataSock, ephemeralPort = createDataConnection(clientSock, addr)  # Create data connection and connect to client to begin data transfer
    print("Data connection successfully established with client on ephemeral port #", ephemeralPort ,"\n")
    data = "Status functionality under construction"
    sendData(dataSock, data)
    dataSock.close()
    print("Data connection to client closed.\n")
    return

# Check status of all registered users
def userStatusAll(clientSock, addr):
  dataSock, ephemeralPort = createDataConnection(clientSock, addr)  # Create data connection and connect to client to begin data transfer
  print("Data connection successfully established with client on ephemeral port #", ephemeralPort ,"\n")
  data = "All functionality under construction"
  sendData(dataSock, data)
  dataSock.close()
  print("Data connection to client closed.\n")
  return

main()