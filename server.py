import threading
import socket
import os
from command_handler import handle_commands

host = '127.0.0.1'
port = 59000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = {}  # Dictionary to store clients and their aliases
chat_room = []  # List to manage chat room members
key = os.urandom(16)

def receive():
    while True:
        print('Server is running and listening ...')
        client, address = server.accept()
        print(f'Connection is established with {str(address)}')
        thread = threading.Thread(target=handle_commands, args=(client, address, clients, chat_room, key))
        thread.start()

if __name__ == "__main__":
    receive()
