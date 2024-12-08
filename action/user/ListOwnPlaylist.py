from ..Action import Action
from DB_utils_hcy import list_playlist
## Tested
class ListOwnPlaylist(Action):
    def exec(self, conn, user):
        print("List Own Playlist")
        table = list_playlist(user.get_userid())
        self.send_table(conn, table)
    
        return