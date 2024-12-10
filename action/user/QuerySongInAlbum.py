from ..Action import Action
from DB_utils import query_song_in_album
## Tested 
class QuerySongInAlbum(Action):
    def exec(self, conn, user):
        uid = "All"
        album_title = self.read_input(conn, "Album title")

        res = query_song_in_album(uid, album_title)
        
        if res == -1:
            conn.send(f'''No album name {album_title}'''.encode('utf-8'))

        self.send_table(conn, res)
        return