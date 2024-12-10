from ..Action import Action
from DB_utils import add_song_to_playlist
## Tested 
class AddSongToPlaylist(Action):
    def exec(self, conn, user):
        print("Add Song To Playlist")
        user_id = user.get_userid()
        playlist_id = self.read_input(conn, "Playlist id")
        song_id = self.read_input(conn, "Song id")
        print(f'Adding')
        
        _ = add_song_to_playlist(user_id, playlist_id, song_id)
        conn.send(f'''----------------------------------------\nSuccessfully added song to playlist!'''.encode('utf-8'))
    
        return 