from ..Action import Action
from DB_utils import artist_query_cash
## Tested 
class QueryCash(Action):
    def exec(self, conn, user):
        value = artist_query_cash(user.get_userid())
        conn.send(f'''Your current cash : {value}\n'''.encode('utf-8'))

        return 