import socket
import os 
import threading
import argparse

ENCODING = 'utf-8'
EXIT_MSG = 'exit'
#messages = [Message, ...]
messages = []

class Message:
    def __init__(self, data):
        split_data = str(data, encoding=ENCODING)
        split_data = split_data.split(":")
        self.sender = split_data[0]
        self.data = split_data[1]
    def __str__(self):
        return f"\033[38;5;47m{self.sender}\033[38;5;15m:{self.data}"
    

'''
def encode_message(data):
    encoded_data = ''
    for letter in data:
        encoded_data += chr(ord(letter) ^ 47)
    print(encoded_data)
    return encoded_data

def decode_message(data):
    decoded_data = ''
    for letter in data:
        decoded_data += chr(ord(letter) ^ 47)
    print(decoded_data)
    return decoded_data
'''

def client_receive_message(addr, data):
    global messages
    msg = Message(data)
    messages.append(msg)

def client_send_message(conn,data):
    conn.sendall(bytes(data,ENCODING))

def print_messages(size):
    global messages
    MISC_LINE_COIUNT = 4 
    msgs = messages
    if len(messages) >= size.lines-MISC_LINE_COIUNT:
        dif = len(messages) - (size.lines-MISC_LINE_COIUNT)
        msgs = messages[dif:]   
    for msg in msgs:

        print(msg)

def setup_screen(name):
    size = os.get_terminal_size()
    #clears screen
    print('\033[2J\033[H')
    print(f'\033[1m\033[38;5;87m{name}: \033[38;5;15m\033[22m')
    print_messages(size)
    #brings cursor down and creates prompt
    print(f'\033[H\033[{size.lines-2}E'+'-'*size.columns + '> ', end='', flush=True)

def send_data(conn, name):
    global exiting
    while True:
        msg = input()
        if msg == EXIT_MSG:
            client_send_message(conn, msg)
            conn.close()
            exit(0)
        client_send_message(conn, msg)

def client(host='127.0.0.1', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((host, port))
        except ConnectionRefusedError:
            print(f'Could not connect to {host} on port {port}.')
            exit(1)
        chatroom_name = s.recv(1024)
        chatroom_name = str(chatroom_name, encoding=ENCODING)
        input_thread = threading.Thread(target=send_data, args=(s, chatroom_name))
        input_thread.start()
        while True:
            try:
                setup_screen(chatroom_name)
                data = s.recv(1024)
                client_receive_message(host, data)
            except (ConnectionResetError, ConnectionAbortedError):
                print(f'Connection to {chatroom_name} has been closed')
                exit(0)


def main():
    parser = argparse.ArgumentParser(add_help=True, description='Sets up a messaging client')
    parser.add_argument('-t','--host', action='store',default='127.0.0.1', help='The IP you want the socket to bind to. The default IP is "127.0.0.1"',type=str)
    parser.add_argument('-p','--port', action='store',default=8080, help='The port you want the socket to bind to. The default port is "8080"',type=int)

    args = parser.parse_args()

    client(args.host, args.port)

if __name__ == '__main__':
    main()