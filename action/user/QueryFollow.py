from ..Action import Action
from DB_utils import list_all_follow_artist
## Tested 
class QueryFollow(Action):
    def exec(self, conn, user):
        
        table = list_all_follow_artist(user.get_userid())
        self.send_table(conn, table)
    
        return 