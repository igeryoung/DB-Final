import socket
from threading import Thread
from DB_utils_hcy import db_connect
from utils import *
from action.ListSongFromPlaylist import ListSongFromPlaylist


if __name__ == '__main__':

    db = db_connect()
    cur = db.cursor()

    bind_ip = "127.0.0.1"
    bind_port = 8800

    test_action = ListSongFromPlaylist('user login', 'test')
    data = {
        "playlist name": "Test"
    }
    test_action.set_test_input(data)
    test_action.exec(None, None)