from ..Action import Action
from DB_utils import query_album
## Tested 
class QueryAlbum(Action):
    def exec(self, conn, user):
        print("Query Album By Name")
        album_name = self.read_input(conn, "Album name")
        print(f'Looking for | {album_name}')
        
        table = query_album(album_name)
        self.send_table(conn, table)
    
        return 