from ..Action import Action
from DB_utils_ping import delete_song_from_playlist, query_song_id_by_artist_id_and_title
## Tested 
class DeleteSong(Action):
    def exec(self, conn, user):

        song_title = self.read_input(conn, "Song title")

        song_id = query_song_id_by_artist_id_and_title(user.get_userid(), song_title)

        if song_id == -1:
            conn.send(f'''you have no song name {song_title}'''.encode('utf-8'))
            return
        
        delete_song_from_playlist(song_id)
        conn.send(f'''successful delete song : {song_title}'''.encode('utf-8'))
    
        return 