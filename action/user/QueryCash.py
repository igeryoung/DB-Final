from ..Action import Action
from DB_utils_ping import query_cash
## Tested 
class QueryCash(Action):
    def exec(self, conn, user):
        value = query_cash(user.get_userid())
        conn.send(f'''your current cash : {value}\n'''.encode('utf-8'))

        return 