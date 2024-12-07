import socket
from threading import Thread
from DB_utils import db_connect
from utils import *
from actions import LogIn, SignUp


if __name__ == '__main__':

    db = db_connect()
    cur = db.cursor()

    bind_ip = "127.0.0.1"
    bind_port = 8800

    test_action = LogIn('user login', 'test')
    data = {
        "email": 'alice@example.com',
        "password": 'password123'
    }
    test_action.set_test_input()
    test_action.exec()