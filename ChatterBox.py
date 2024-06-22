#TODO: Add names instead of IPs (would need preprocessing step before adding them to chat room)
#TODO: Add encryption to the messages! maybe start out with a simple XOR or something, and then go to like AES/ actual algorithms
#TODO: Fix exiting from the sever so that error messages do not appear


import socket
import threading

EXIT_MSG = 'exit'
CHATROOM_NAME = b'Test'
ENCODING = 'utf-8'
#messages = [{addr}: {data}]
messages = []
#client_info = {(connection_socket,(addr, port)): name}  
client_info = { }

def print_message(msg):
   split_msg = msg.split(':')
   f_msg = f'\033[38;5;47m{split_msg[1]}\033[38;5;15m:{split_msg[2]}'
   print(f_msg)
    
def server_receive_message(addr, data):
    msg = f'{addr}: {str(data, encoding=ENCODING)}'
    print(msg)
    messages.append(msg)
    return msg

def server_send_message(data):
    for conn in client_info:
        conn[0].sendall(bytes(data,ENCODING))

def server(host='127.0.0.1', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f'Server listening on {host}:{port}')
        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()

def handle_client(conn, addr):
    global client_info

    #get client info
    connected = True
    print(f'[INFO]: {addr[0]} has connected on port {addr[1]}')
    conn.send(CHATROOM_NAME)
    conn.sendall(b"SERVER:Please enter a username")
    username = conn.recv(1024)
    username = str(username, encoding=ENCODING)
    client_info[(conn, addr)] = username
    server_send_message(f"SERVER:{username} has joined the chat room!")

    #generic client loop
    while connected:
        conn_msg = conn.recv(1024)
        if str(conn_msg, encoding=ENCODING) == EXIT_MSG:
            connected = False
            client_info.pop((conn, addr))
            print(f'[INFO]: {addr} has exitted the chat room')
            break
        formatted_msg = server_receive_message(client_info[(conn, addr)], conn_msg)
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