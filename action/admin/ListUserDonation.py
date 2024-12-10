from ..Action import Action
from DB_utils import list_user_donation


class ListUserDonation(Action):
    def exec(self, conn, user):
        print("List History")
        user_id = self.read_input(conn, "User ID/All")
        print(user_id)
        table = list_user_donation(user_id)
        self.send_table(conn, table)
    
        return
    
