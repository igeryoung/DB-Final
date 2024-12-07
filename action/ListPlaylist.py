from .Action import Action
from DB_utils import list_playlist
class ListPlaylist(Action):
    def exec(self, conn, user):
        print("List Playlist")
        table = list_playlist(user.get_userid())
        self.send_table(conn, table)
    
        return