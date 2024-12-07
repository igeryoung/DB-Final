from ..Action import Action
from DB_utils_hcy import query_song
## Tested 
class QuerySong(Action):
    def exec(self, conn, user):
        print("Query Song By Name")
        song_name = self.read_input(conn, "Song name")
        print(f'Looking for | {song_name}')
        
        table = query_song(song_name)
        self.send_table(conn, table)
    
        return 