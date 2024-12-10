from ..Action import Action
from DB_utils import list_listener


class ListUser(Action):
    def exec(self, conn, user):
        user_id = self.read_input(conn, "User ID/All")
        
        table = list_listener(user_id)
        self.send_table(conn, table)
    
        return
