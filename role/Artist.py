from .Role import Role
from action.artist import (AddAlbum, ListAlbum, AddSong, 
                           ListSong, DeleteSong, ListSongInAlbum, 
                           DeleteAlbum, QueryCash, ArtistQueryFollow_num)



class Artist(Role):
    def __init__(self, userid, username, pwd, email):
        super().__init__(userid, username, pwd, email)

        self.user_action =  [
                                AddAlbum("Upload a new Album"),
                                AddSong("Upload a new Song"),
                                ListSong("List all of my Song"),
                                ListAlbum("List all of my Albums"),
                                ListSongInAlbum("List Song in one Album"),
                                DeleteSong("Delete my Song"),
                                DeleteAlbum("Delete my Album"),
                                QueryCash("Query Cash"),
                                ArtistQueryFollow_num("Query Follow Number")

                            ]
    def get_info_msg(self):
        return f'Artist_id: {self.userid}, Artist_name: {self.username}, email: {self.email}, role: {type(self).__name__}'
        

