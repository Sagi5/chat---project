import socket
import threading

def receive_messages(client_socket):
    while True:
        message = client_socket.recv(1024).decode('utf-8')
        if message:
            print(message)
        else:
            client_socket.close()
            break

def send_message(client_socket):
    while True:
        message = input("> ")
        if message:
            client_socket.send(message.encode('utf-8'))
        else:
            print("type a message!")


def connect_to_server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 1111))
    return client_socket

def start_receiving(client_socket):
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

def start_sending(client_socket):
    send_message(client_socket)

def close_connection(client_socket):
    client_socket.close()

if __name__ == "__main__":
    client_socket = connect_to_server()
    start_receiving(client_socket)
    start_sending(client_socket)
