from ..Action import Action
from DB_utils import play_song, query_song_id_by_song_title, like_song_by_song_id
import time
## Tested 
class PlaySong(Action):
    def exec(self, conn, user):
        song_name = self.read_input(conn, "Song name")

        song_id = query_song_id_by_song_title(song_name)

        if song_id == -1:
            conn.send(f"There's no song named {song_name}".encode('utf-8'))
            return
        
        play_song(user.get_userid(), song_id)
        
        conn.send(f"\n----------------------------------------\n".encode('utf-8'))
        conn.send(f"You are now listening : {song_name}, enjoy!\n".encode('utf-8'))
        conn.send(f"Do you like it?\n".encode('utf-8'))

        like = self.read_input(conn, "(Y/N)")
        if like == 'Y' or like  == 'y':
            like_song_by_song_id(song_id)

        conn.send(f"\n----------------------------------------\n".encode('utf-8'))
        conn.send(f"Thanks for your feedback! \n".encode('utf-8'))
    
        return 