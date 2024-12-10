from ..Action import Action
from DB_utils_ping import query_song_in_album

class ListSongInAlbum(Action):
    def exec(self, conn, user):
        uid = user.get_userid()
        album_title = self.read_input(conn, "Album title")

        res = query_song_in_album(uid, album_title)
        
        if res == -1:
            conn.send(f'''You have no album name {album_title}'''.encode('utf-8'))

        self.send_table(conn, res)
        return