from ..Action import Action
from DB_utils_hcy import delete_song_from_playlist
## Tested 
class DeleteSongFromPlaylist(Action):
    def exec(self, conn, user):
        print("Delete Song From Playlist")
        user_id = user.get_userid()
        playlist_id = self.read_input(conn, "Playlist id")
        song_id = self.read_input(conn, "Song id")
        print(f'Deleting')
        
        table = delete_song_from_playlist(user_id, playlist_id, song_id)
        self.send_table(conn, table)
    
        return 