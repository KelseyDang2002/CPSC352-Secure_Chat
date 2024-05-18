import threading
import socket
from message_utils import send_message, receive_message

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 59000))

def get_credentials():
    username = input('Enter your username: ')
    password = input('Enter your password: ')
    return f'{username}:{password}'

def print_menu():
    print("\nMenu:")
    print("1. chat <users> - Start a chat and invite specified users (e.g., chat user2 user3)")
    print("2. status <username> - Check if a user is online (e.g., status user1)")
    print("3. all - List all online users")
    print("4. join - Join the chat room")
    print("5. quit - Quit the application")
    print()

credentials = get_credentials()
in_chat = False
prompt_command = False # This variable prevents the menu from being spammed.

# This thread just listens for messages. It will activate the chat room thread if it gets a Enter or Join message.
def client_receive():
    global credentials, in_chat, prompt_command
    while True:
        try:
            message = receive_message(client).decode('utf-8')
            if message == "credentials?":
                send_message(client, credentials.encode('utf-8'))
            elif message == "Invalid credentials. Try again.":
                print(message)
                credentials = get_credentials()
                send_message(client, credentials.encode('utf-8'))
            elif message.startswith('Enter a command'):
                prompt_command = True
            elif message.startswith('Entering chat room...'):
                print("Entering chat room...")
                in_chat = True
                chat_thread = threading.Thread(target=client_send)
                chat_thread.start()
            elif message.startswith('Joining chat room...'):
                print(message)
                in_chat = True
                chat_thread = threading.Thread(target=client_send)
                chat_thread.start()
            else:
                print(message)
        except Exception as e:
            print(f'Error: {e}')
            client.close()
            break


# This thread only sends messages for the chat room.
def client_send():
    global in_chat
    while in_chat:
        try:
            message = f'{credentials.split(":")[0]}: {input("")}'
            send_message(client, message.encode('utf-8'))
        except Exception as e:
            print(f'Error: {e}')
            client.close()
            break


# This thread only sends commands. When Client enters a chat room shuts off. 
def command_input():
    global prompt_command
    while True:
        if prompt_command:
            print_menu()
            command = input('Enter your choice: ')
            send_message(client, command.encode('utf-8'))
            if command == 'quit':  # Check if the command is 'quit'
                print("Disconnecting...")
                client.close()  # Close the client socket
                return  # Exit the function and the loop immediately
            prompt_command = False

receive_thread = threading.Thread(target=client_receive)
receive_thread.start()

command_thread = threading.Thread(target=command_input)
command_thread.start()

# Keep the main thread alive to avoid interpreter shutdown
receive_thread.join()
command_thread.join()
