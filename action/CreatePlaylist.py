from .Action import Action
from DB_utils_hcy import create_playlist
## Tested 
class CreatePlaylist(Action):
    def exec(self, conn, user):
        print("Create Playlist")
        user_id = 1
        playlist_title = self.read_input(conn, "Playlist title")
        playlist_description = self.read_input(conn, "Playlist description")
        public_or_not = self.read_input(conn, "Public or not (Y/N)")
        print(f'Creating | {playlist_title}')
        
        table = create_playlist(user_id, playlist_title, playlist_description, public_or_not)
        self.send_table(conn, table)
    
        return 