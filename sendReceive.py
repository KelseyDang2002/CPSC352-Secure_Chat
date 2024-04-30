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


# Receive incoming bytes from connection socket
def recvAll(serverSock, numBytes):
    data = str()
    tmpData = str()
    data = data.encode()
    while len(data) < numBytes:
        tmpData = serverSock.recv(numBytes)
        if not tmpData:
            break
        data += tmpData
    return data
