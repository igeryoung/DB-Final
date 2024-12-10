from .Role import Role
from action.ListPlaylist import ListPlaylist

class Admin(Role):
    def __init__(self, userid, username, pwd, email):
        super().__init__(userid, username, pwd, email)

        self.user_action =  [
                                ListPlaylist("List All Playlists"),
                            ]
        

