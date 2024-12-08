from ..Action import Action
from DB_utils_hcy import list_playlist

class ListOtherPlaylist(Action):
    def exec(self, conn, user):
        print("List Other's Playlist")
        user_id = self.read_input(conn, "User ID/All")
        table = list_playlist(user_id)
        self.send_table(conn, table)
    
        return
    
    
    
    
# All
# SELECT * FROM public.playlist
# AND is_public = 'Y' 
# ORDER BY playlist_id ASC 

#ELSE 
# SELECT * FROM public.playlist
# WHERE listener_id = {user_id}
# AND is_public = 'Y' 
# ORDER BY playlist_id ASC 