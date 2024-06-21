import socket
import threading

EXIT_MSG = 'exit'
CHATROOM_NAME = b'Test'
ENCODING = 'utf-8'
messages = []
connections = []

def print_message(msg):
   split_msg = msg.split(':')
   f_msg = f'\033[38;5;47m{split_msg[1]}\033[38;5;15m: {split_msg[2]}'
   print(f_msg)
    
def server_receive_message(addr, data):
    msg = f'{addr}: {str(data, encoding=ENCODING)}'
    print(msg)
    messages.append(msg)
    return msg


def server_send_message(data):
    for conn in connections:
        conn[0].sendall(bytes(data,ENCODING))

def server(host='127.0.0.1', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f'Server listening on {host}:{port}')
        while True:
            conn, addr = s.accept()
            connections.append((conn, addr))
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()

def handle_client(conn, addr):
    connected = True
    print(f'Connected by {addr[0]} on port {addr[1]}')
    conn.send(CHATROOM_NAME)
    server_send_message(f"SERVER: {addr[0]} has joined the chat room!")
    while connected:
        conn_msg = conn.recv(1024)
        if str(conn_msg, encoding=ENCODING) == EXIT_MSG:
            connected = False
            connections.remove((conn, addr))
        formatted_msg = server_receive_message(addr[0], conn_msg)
        server_send_message(formatted_msg)
    conn.close()

if __name__ == '__main__':
    '''
    host = input("Please enter the host that you want to bind to: ")
    port = None
    while port == None:
        try:
            port = int(input("Please enter the port that you would like to bind to: "))
        except:
            print(f'Please enter a valid port number')
    server(host, port)
    '''
    server()