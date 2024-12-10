from ..Action import Action
from DB_utils import artist_query_activity
## Tested 
class QueryActivity(Action):
    def exec(self, conn, user):
        table = artist_query_activity(user.get_userid())
        self.send_table(conn, table)
        return 