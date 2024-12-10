from ..Action import Action
from DB_utils import list_artist


class ListArtist(Action):
    def exec(self, conn, user):
        user_id = self.read_input(conn, "Artist ID/All")
        
        table = list_artist(user_id)
        self.send_table(conn, table)
    
        return
