# Checks header for message len, then loops until full message received.
def receive_message(sock):
    try:
        header = sock.recv(10)
        if not header:
            return None
        message_length = int(header.decode('utf-8').strip())
        message = b''
        while len(message) < message_length:
            chunk = sock.recv(min(message_length - len(message), 10))
            if not chunk:
                break
            message += chunk
        return message if len(message) == message_length else None
    except ConnectionResetError:
        return None
    except Exception as e:
        print(f"Error receiving message: {e}")
        return None

# Adds header to the message then sends it.
def send_message(sock, message):
    try:
        message_length = len(message)
        header = f'{message_length:<10}'.encode('utf-8')
        sock.send(header + message)
    except Exception as e:
        print(f"Error sending message: {e}")
