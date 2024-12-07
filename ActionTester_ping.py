import socket
from threading import Thread
from DB_utils_hcy import db_connect
from utils import *
from action.QuerySong import QuerySong


if __name__ == '__main__':

    db = db_connect()
    cur = db.cursor()

    bind_ip = "127.0.0.1"
    bind_port = 8800

    test_action = QuerySong('user login', 'test')
    data = {
        "Song name": 'Love',
    }
    test_action.set_test_input(data)
    test_action.exec(None, None)