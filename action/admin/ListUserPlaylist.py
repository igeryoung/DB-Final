from ..Action import Action
from DB_utils import list_user_playlist


class ListUserPlaylist(Action):
    def exec(self, conn, user):
        print("List Playlist")
        user_id = self.read_input(conn, "User ID/All")
        print(user_id)
        table = list_user_playlist(user_id)
        self.send_table(conn, table)
    
        return
    
    

# All
#if(user_id == "All"):
    # SELECT * FROM public.playlist
    # ORDER BY playlist_id ASC 


# SELECT * FROM public.playlist
# WHERE listener_id = user_id
# ORDER BY playlist_id ASC 