from .Action import Action
from DB_utils_hcy import list_song_from_playlist
## Tested
class ListSongFromPlaylist(Action):
    def exec(self, conn, user):
        print("List songs from your playlist")
        playlist_name = self.read_input(conn, "playlist name")
        print(f'Looking for | {playlist_name}')
        
        table = list_song_from_playlist(playlist_name)
        self.send_table(conn, table)
    
        return 