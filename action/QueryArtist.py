from .Action import Action
from DB_utils_hcy import query_artist
## Tested 
class QueryArtist(Action):
    def exec(self, conn, user):
        print("Query Artist By Name")
        artist_name = self.read_input(conn, "Artist name")
        print(f'Looking for | {artist_name}')
        
        table = query_artist(artist_name)
        self.send_table(conn, table)
    
        return 