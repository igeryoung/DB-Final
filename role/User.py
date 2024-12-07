from .Role import Role
# from action.Exit import Exit
from action.user.AddSongToPlaylist import AddSongToPlaylist
from action.user.CreatePlaylist import CreatePlaylist
from action.user.DeleteSongFromPlaylist import DeleteSongFromPlaylist
from action.user.ListPlaylist import ListPlaylist
from action.user.ListSongFromPlaylist import ListSongFromPlaylist
from action.user.QueryAlbum import QueryAlbum
from action.user.QueryArtist import QueryArtist
from action.user.QuerySong import QuerySong


class User(Role):
    def __init__(self, userid, username, pwd, email):
        super().__init__(userid, username, pwd, email)

        self.user_action =  [
                                ListPlaylist("List All Playlists"),
                                CreatePlaylist("Create Playlist"),
                                AddSongToPlaylist("Add Song To Playlist"),
                                DeleteSongFromPlaylist("Delete Song From Playlist"),
                                ListSongFromPlaylist("List Song From Playlist"),
                                QueryAlbum("Query Album"),
                                QueryArtist("Query Artist"),
                                QuerySong("Query Song")
                            ]
        

