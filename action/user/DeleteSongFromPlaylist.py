from ..Action import Action
from DB_utils import delete_song_from_playlist
## Tested 
class DeleteSongFromPlaylist(Action):
    def exec(self, conn, user):
        print("Delete Song From Playlist")
        user_id = user.get_userid()
        playlist_id = self.read_input(conn, "Playlist id")
        song_id = self.read_input(conn, "Song id")
        print(f'Deleting')
        
        _ = delete_song_from_playlist(user_id, playlist_id, song_id)
        conn.send(f'''----------------------------------------\nSuccessfully deleted song from playlist!'''.encode('utf-8'))
    
        return 