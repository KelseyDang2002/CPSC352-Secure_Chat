import threading
import socket
from message_utils import send_message, receive_message
from aes_encryption import aes_encrypt_data, aes_decrypt_data

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 59000))

def get_credentials():
    username = input('Enter your username: ')
    password = input('Enter your password: ')
    return f'{username}:{password}'

def print_menu():
    print("\nMenu:")
    print("\t1. chat <users> - Start a chat and invite specified users (e.g., chat user2 user3)")
    print("\t2. status <username> - Check if a user is online (e.g., status user1)")
    print("\t3. all - List all online users")
    print("\t4. join - Join the chat room")
    print("\t5. quit - Quit the application")
    print()

credentials = get_credentials()
in_chat = False
prompt_command = False # This variable prevents the menu from being spammed.
global key

# This thread just listens for messages. It will activate the chat room thread if it gets a Enter or Join message.
def client_receive():
    global credentials, in_chat, prompt_command, key
    while True:
        try:
            message = receive_message(client)
            if message is None:
                break  # Break the loop if no message is received
            message = message.decode('utf-8')
            if message == "credentials?":
                send_message(client, credentials.encode('utf-8'))
            elif message == "Invalid credentials. Try again.":
                print(message)
                credentials = get_credentials()
                send_message(client, credentials.encode('utf-8'))
            elif message.startswith('Enter a command'):
                prompt_command = True
            elif message.startswith('Start Chatroom Verify'):
                # Send encrypted symmetric key to user
                message = receive_message(client).decode('utf-8')
                print ("Decrypt the following message using your private key:")
                print (message)
                key_attempt = input("Please enter the decrypted key: ")
                # Send decoded symmetic key to server
                send_message(client, key_attempt.encode('utf-8'))
                message = receive_message(client).decode('utf-8')
                if message.startswith('Success'):
                    print("Entering chat room...")
                    key = eval(key_attempt)
                    in_chat = True
                    chat_thread = threading.Thread(target=client_send)
                    chat_thread.start()
                else:
                    print ('Incorrect key.')
                
            elif message.startswith('Join Verify'):
                message = receive_message(client).decode('utf-8')
                print ("Decrypt the following message using your private key:")
                print (message)
                key_attempt = input("Please enter the decrypted key: ")
                # Send decoded symmetic key to server
                send_message(client, key_attempt.encode('utf-8'))
                message = receive_message(client).decode('utf-8')
                if message.startswith('Success'):
                    print("Entering chat room...")
                    key = eval(key_attempt)
                    in_chat = True
                    chat_thread = threading.Thread(target=client_send)
                    chat_thread.start()
            else:
                if message.startswith('b\''):
                    message = aes_decrypt_data(eval(message), key)
                print(message)
        except Exception as e:
            if client.fileno() == -1:  # Check if the client socket is closed
                break  # Break the loop if the socket is closed
            print(f'Error: {e}')
            client.close()
            break

# This thread only sends messages for the chat room.
def client_send():
    global in_chat, key
    while in_chat:
        try:
            message = f'{credentials.split(":")[0]}: {input("")}'
            message = str(aes_encrypt_data(message, key))
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
                exit(0)  # Close the client socket
                return  # Exit the function and the loop immediately
            prompt_command = False

receive_thread = threading.Thread(target=client_receive)
receive_thread.start()

command_thread = threading.Thread(target=command_input)
command_thread.start()

# Keep the main thread alive to avoid interpreter shutdown
receive_thread.join()
command_thread.join()
