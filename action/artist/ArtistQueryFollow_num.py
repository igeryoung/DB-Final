from ..Action import Action
from DB_utils_ping import artist_query_follow_num
## Tested 
class ArtistQueryFollow_num(Action):
    def exec(self, conn, user):
        value = artist_query_follow_num(user.get_userid())
        conn.send(f'''Your current follow number : {value}\n'''.encode('utf-8'))

        return 