import socket
from threading import Thread
from DB_utils import db_connect
from utils import *
from action.user.ListSongFromPlaylist import ListSongFromPlaylist
from action.user.AddSongToPlaylist import AddSongToPlaylist
from action.user.DeleteSongFromPlaylist import DeleteSongFromPlaylist
if __name__ == '__main__':

    db = db_connect()
    cur = db.cursor()

    bind_ip = "127.0.0.1"
    bind_port = 8800

    test_action = DeleteSongFromPlaylist('user login', 'test')
    data = {
        "Playlist id": 1,
        "Song id": 3
    }
    test_action.set_test_input(data)
    test_action.exec(None, None)