#TODO: Add encryption to the messages! maybe start out with a simple XOR or something, and then go to like AES/ actual algorithms
#TODO: Implement TLS/SSL support (which would handle encryption...)
#TODO: Make UI cooler (maybe use those big unicode blocks '█' or those continous lines from unicode)

import argparse
import socket
import threading

class Message:
    def __init__(self, addr, data):
        self.sender = addr
        self.data = str(data, encoding=ENCODING)
    def __str__(self):
        return f"{self.sender}: {self.data}"
    def message_to_bytes(self):
        return bytes(f"{self.sender}: {self.data}", ENCODING)
    
EXIT_MSG = 'exit'
DEFAULT_CHATROOM_NAME = b'Chat Room'
ENCODING = 'utf-8'
#messages = [Message, ...]
messages = []
#client_info = {(connection_socket,(addr, port)): name}  
client_info = { }

USRNAME_MSG = Message("SERVER", b"Please enter a username")
CONNECTED_MSG = Message("SERVER", b"")

def print_message(msg):
   print(msg)
    
def server_receive_message(name, data):
    msg = Message(name, data)
    print(msg)
    messages.append(msg)
    return msg

def server_send_message(msg):
    for conn in client_info:
        conn[0].sendall(bytes(msg.__str__(),ENCODING))

def server(host, port, name):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f'Server listening on {host}:{port}')
        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr, name))
            thread.start()


def handle_client(conn, addr, name):
    global client_info

    #get client info
    connected = True
    try:
        print(f'[INFO]: {addr} has connected')
        conn.send(bytes(name, ENCODING))
        conn.sendall(USRNAME_MSG.message_to_bytes())
        username = conn.recv(1024)
        username = str(username, encoding=ENCODING)
        client_info[(conn, addr)] = username
        CONNECTED_MSG.data = f"{username} has joined the chat room!"
        print(CONNECTED_MSG)
        server_send_message(CONNECTED_MSG)
    except ConnectionResetError:
        connected = False
        print(f'[INFO]: {addr} has disconnected')
        conn.close()

    #generic client loop
    while connected:
        try:
            msg_in_bytes = conn.recv(1024)
            if str(msg_in_bytes, encoding=ENCODING) == EXIT_MSG:
                connected = False
                client_info.pop((conn, addr))
                print(f'[INFO]: {addr}:{username} has exitted the chat room')
                print(f'SERVER: {username} has left the chat room')
                server_send_message(f'SERVER: {username} has left the chat room')
                break
            formatted_msg = server_receive_message(client_info[(conn, addr)], msg_in_bytes)
            server_send_message(formatted_msg)
        except ConnectionResetError:
            connected = False
            client_info.pop((conn, addr))
            print(f'[INFO]: {addr}:{username} has exitted the chat room')
            print(f'SERVER: {username} has left the chat room')
            server_send_message(f'SERVER: {username} has left the chat room')
            break
    conn.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=True, description='Sets up a messaging server')
    parser.add_argument('-t','--host', action='store',default='127.0.0.1', help='The IP you want the socket to bind to. The default IP is "127.0.0.1"',type=str)
    parser.add_argument('-p','--port', action='store',default=8080, help='The port you want the socket to bind to. The default port is "8080"',type=int)
    parser.add_argument('-n','--name', action='store',default='Chat Room', help='The name you want the chat room to be titled. The default name is "Chat Room"',type=str)
    
    args = parser.parse_args()
    server(args.host, args.port, args.name)