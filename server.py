import socket
from threading import Thread
from global_db import db_connect
from utils import *
from action import UserLogIn, UserSignUp, ArtistSignUp, ArtistLogIn


welcome_action = [
    UserLogIn("Log in as an [User]"), 
    ArtistLogIn("Log in as an [Artist]"),
    UserSignUp("Sign up as an [User]"), 
    ArtistSignUp("Sign up as an [Artist]")
]


def handle_connection(conn, client_addr):
    try:
        
        while True: # Welcome Page
            conn.send("----------------------------------------\nWelcome to Study Group System! Please select your option:\n".encode('utf-8'))
            conn.send(f'[INPUT]Please select your option:\n{list_option(welcome_action)}---> '.encode('utf-8'))
                
            action = get_selection(conn, welcome_action)
            print("action", action)
            user = action.exec(conn)
            # print(user)
            if user == -1:
                raise Exception("End connection")
            
            send_msg =  f'\n----------------------------------------\n\nHi {user.get_username()}!\n' + \
                        f'[ Info ] {user.get_info_msg_no_pwd()}\n'
            conn.send(send_msg.encode('utf-8'))

            while True: # Function Page
                
                conn.send(f'\n----------------------------------------\n\n'.encode('utf-8'))
                actions = user.get_available_action()
                conn.send(f'[INPUT]Please select your option:\n{list_option(actions)}---> '.encode('utf-8'))
                action = get_selection(conn, actions)
                conn.send(f'\n----------------------------------------\n\n'.encode('utf-8'))
                
                ret = action.exec(conn, user)
                if ret == -1:
                    break

    except Exception:
        print(f"Connection with {client_addr} close.")
        conn.close()
    finally:
        print(f"Connection with {client_addr} close.")
        conn.close()


if __name__ == '__main__':

    db = db_connect()
    cur = db.cursor()
    print("db", db)
    print("cur", cur)
    bind_ip = "127.0.0.1"
    bind_port = 8800

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP
    server_socket.bind((bind_ip, bind_port))
    server_socket.listen(5)

    print(f'Server listening on {bind_ip}:{bind_port} ...')


    try:
        while True:
            (conn, client_addr) = server_socket.accept()
            print("Connect to client:", client_addr)

            thread = Thread(target=handle_connection, args=(conn, client_addr,))
            thread.start()
    finally:
        db.close()
        server_socket.close()