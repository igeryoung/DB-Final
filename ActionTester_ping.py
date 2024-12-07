import socket
from threading import Thread
from DB_utils_ping import db_connect
from utils import *
from action.SignUp import SignUp


if __name__ == '__main__':

    db = db_connect()
    cur = db.cursor()

    bind_ip = "127.0.0.1"
    bind_port = 8800

    test_action = SignUp('user sign up', 'test')
    data = {
        "email": 'ping@example.com',
        "username": 'kent',
        "password": 'password1333',
    }
    test_action.set_test_input(data)
    test_action.exec(None, None)