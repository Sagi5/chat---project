import socket
import threading
import sqlite3

clients = []

def handle_client(client_socket, addr):
    print(f"New connection from {addr}")
    while True:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"received message from {addr}: {message}")
                broadcast_message(client_socket, message)
                save_message(addr, message)



def broadcast_message(sender_socket, message):
    for client in clients:
        if client != sender_socket:
            client.send(message.encode('utf-8'))


def save_message(addr, message):
        conn = sqlite3.connect('chat.db')
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS messages (address TEXT, message TEXT)')
        c.execute('INSERT INTO messages (address, message) VALUES (?, ?)', (str(addr), message))
        conn.commit()
        conn.close()


def remove_client(client_socket):
    if client_socket in clients:
        clients.remove(client_socket)
        client_socket.close()
        

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 1111))
    server.listen()
    print("Server listening")

    while True:
        client_socket, addr = server.accept()
        clients.append(client_socket)
        client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_handler.start()

if __name__ == "__main__":
    start_server()
