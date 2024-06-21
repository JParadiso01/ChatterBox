import socket
import os 
import threading

ENCODING = 'utf-8'
#messages = [{addr}: {data}]
messages = []

def client_receive_message(addr, data):
    data = str(data, encoding=ENCODING)
    messages.append(data)


def client_send_message(conn,data):
    conn.sendall(bytes(data,ENCODING))

def print_message(msg):
   split_msg = msg.split(':')
   f_msg = f'\033[38;5;47m{split_msg[0]}\033[38;5;15m: {split_msg[1]}'
   print(f_msg)


def setup_screen(name):
    size = os.get_terminal_size()
    #clears screen
    print('\033[2J\033[H\033[1B')
    print(f'\033[1m\033[38;5;87m{str(name, encoding=ENCODING)}: \033[38;5;15m\033[22m')
    for msg in messages:
        print_message(msg)
    #brings cursor down and creates prompt
    print(f'\033[{size.lines-3}B')
    print('-'*size.columns)
    print('> ', end="")

def client(host='127.0.0.1', port=65432):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((host, port))
        except ConnectionRefusedError:
            print(f'Could not connect to {host} on port {port}.')
            exit(1)
        chatroom_name = s.recv(1024)
        data_thread = threading.Thread(target=send_data, args=[s])
        data_thread.start()
        while True:
            setup_screen(chatroom_name)
            data = s.recv(1024)
            client_receive_message(host, data)


def send_data(conn):
    
    while True:
        msg = input()
        client_send_message(conn, msg)


def main():
    '''
    host = input("Please enter the host that you want to connect to: ")
    port = None
    while port == None:
        try:
            port = int(input("Please enter the port that you would like to connect to: "))
        except:
            print(f'Please enter a valid port number')
    client(host, port)
    '''
    client()

if __name__ == '__main__':
    main()