import socket
import threading

HOST = '127.0.0.1'
PORT = 1234
active_clients = []


def listen_for_messages(client,username):
# YT: How To Create A Real Time Chat App In Python Using Socket Programming | Part 2
    while True:
        message = client.recv(2048).decode('utf-8')
        if message != '':
            final_msg = username + ":" + message
            send_msg_to_all(final_msg)
        else:
            print(f"Message from {username} is empty ")


def send_msg_to_client(client,message):
    client.sendall(message.encode())



def send_msg_to_all(message):
    for user in active_clients:
            send_msg_to_client(user[1],message) 


def client_handler(client):
    # server wil listen to client message that will contain the username
    while True:
        username = client.recv(2048).decode('utf-8')
        if username != '':
            active_clients.append((username,client))
            send_msg_to_all(f"[SERVER]: {username} has joined the chat")
            break
        else:
            print("Client username is empty")
    threading.Thread(target=listen_for_messages, args=(client,username,)).start()


def main():
    # creating the socket class object
    # AF_INET: uses IPV4 address
    # SOCK_STREAM: TCP , SOCK_DGRAM: UDP
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    try:
        server.bind((HOST,PORT))
        print(f"Running the server on {HOST} {PORT}")
    except:
        print(f"Unable to connect to host {HOST} and port {PORT}")

    # set the listener limit to 5 connections at the same time
    server.listen(5)

    # accept data from the client
    while True:
        client , address =  server.accept()
        print(f"Successfully connected to client {address[0]} {address[1]}")

        threading.Thread(target=client_handler, args=(client, )).start()

if __name__ == '__main__':
    main()
