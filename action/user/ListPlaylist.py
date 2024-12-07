from ..Action import Action
from DB_utils_hcy import list_playlist
## Tested
class ListPlaylist(Action):
    def exec(self, conn, user):
        print("List Playlist")
        table = list_playlist(user.get_userid())
        self.send_table(conn, table)
    
        return