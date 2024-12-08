from ..Action import Action
from DB_utils_hcy import list_playlist


class ListUserPlaylist(Action):
    def exec(self, conn, user):
        print("List Playlist")
        user_id = self.read_input(conn, "User ID/All")
        table = list_playlist(user.get_userid())
        self.send_table(conn, table)
    
        return
    
    

# All
#if(user_id == "All"):
    # SELECT * FROM public.playlist
    # ORDER BY playlist_id ASC 


# SELECT * FROM public.playlist
# WHERE listener_id = user_id
# ORDER BY playlist_id ASC 