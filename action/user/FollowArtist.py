from ..Action import Action
from DB_utils import query_artist_id_by_name, follow_artist
## Tested 
class FollowArtist(Action):
    def exec(self, conn, user):
        uid = user.get_userid()
        name = self.read_input(conn, "artist name")
        artist_id = query_artist_id_by_name(name)
        if artist_id == -1:
            conn.send(f'''No artist name {name}'''.encode('utf-8'))
            return
        
        msg = follow_artist(uid, artist_id, name)
        conn.send(msg.encode('utf-8'))

        return  