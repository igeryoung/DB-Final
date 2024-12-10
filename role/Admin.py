from .Role import Role
from action.admin import ListUser, ListArtist, DeleteListener, DeleteArtist, ListUserHistory, ListUserDonation

class Admin(Role):
    def __init__(self, userid, username, pwd, email):
        super().__init__(userid, username, pwd, email)

        self.user_action =  [
                                ListUser("List Listener"),
                                ListArtist("List Artist"),
                                DeleteListener("Delete Listener"),
                                DeleteArtist("Delete Artist"),
                                ListUserHistory("List User History"),
                                ListUserDonation("List User Donation"),
                            ]
        

