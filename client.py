import socket
import os 
import threading

exiting = False
ENCODING = 'utf-8'
#messages = [{addr}: {data}]
messages = []

def client_receive_message(addr, data):
    global messages
    data = str(data, encoding=ENCODING)
    messages.append(data)

def client_send_message(conn,data):
    conn.sendall(bytes(data,ENCODING))

def print_messages():
    global exiting
    for msg in messages:
        split_msg = msg.split(':')

        #connection closed
        if split_msg == ['']:
            exiting = True
            print('\033[2J\033[H')
            exit(0)
            break
        
        f_msg = f'\033[38;5;47m{split_msg[0]}\033[38;5;15m:{split_msg[1]}'
        print(f_msg)

def setup_screen(name):
    size = os.get_terminal_size()
    #clears screen
    print('\033[2J\033[H\033[1B')
    print(f'\033[1m\033[38;5;87m{name}: \033[38;5;15m\033[22m')
    print_messages()
    #brings cursor down and creates prompt
    print(f'\033[H\033[{size.lines-2}E'+'-'*size.columns + '> ', end='', flush=True)

def send_data(conn, name):
    global exiting
    while True:
        msg = input()
        if exiting:
            print(f'Exiting {name}')
            exit(0)
        client_send_message(conn, msg)

def client(host='127.0.0.1', port=65432):
    global exiting
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
            if exiting:
                print(f'Exiting {chatroom_name}')
                exit(0)
            try:
                setup_screen(chatroom_name)
                data = s.recv(1024)
                client_receive_message(host, data)
            except ConnectionResetError:
                print(f'Server has closed the connection to {chatroom_name}')
                exiting = True
                exit(0)


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