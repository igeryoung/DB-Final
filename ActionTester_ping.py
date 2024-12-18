import socket
from threading import Thread
from global_db import db_connect
from utils import *
from action.user.Donate import Donate


if __name__ == '__main__':

    db = db_connect()
    cur = db.cursor()

    bind_ip = "127.0.0.1"
    bind_port = 8800

    test_action = Donate('', 'test')
    data = {
        "artist name": 'Ping',
        "donate value" : '20',
        "Confirm? (Y/N) ": "Y",
    }
    test_action.set_test_input(data)
    test_action.exec(None, None)