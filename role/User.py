from .Role import Role

# from action.Exit import Exit
from action.user.AddSongToPlaylist import AddSongToPlaylist
from action.user.CreatePlaylist import CreatePlaylist
from action.user.DeleteSongFromPlaylist import DeleteSongFromPlaylist
from action.user.ListOwnPlaylist import ListOwnPlaylist
from action.user.ListOtherPlaylist import ListOtherPlaylist
from action.user.ListSongFromPlaylist import ListSongFromPlaylist
from action.user.QueryAlbum import QueryAlbum
from action.user.QueryArtist import QueryArtist
from action.user.QuerySong import QuerySong
from action.user.QuerySongInAlbum import QuerySongInAlbum
from action.user.PlaySong import PlaySong
from action.user.Deposit import Deposit
from action.user.QueryCash import QueryCash
from action.user.Donate import Donate
from action.user.FollowArtist import FollowArtist
from action.user.CancelFollowArtist import CancelFollowArtist
from action.user.QueryFollow import QueryFollow


class User(Role):
    def __init__(self, userid, username, pwd, email):
        super().__init__(userid, username, pwd, email)

        self.user_action = [
            QueryAlbum("Query Album"),
            QueryArtist("Query Artist"),
            QuerySong("Query Song"),
            QuerySongInAlbum("Query Song in Album"),
            ListOwnPlaylist("List Your Playlists"),
            ListOtherPlaylist("List Other's Playlists"),
            CreatePlaylist("Create Playlist"),
            AddSongToPlaylist("Add Song To Playlist"),
            DeleteSongFromPlaylist("Delete Song From Playlist"),
            ListSongFromPlaylist("List Song From Playlist"),
            PlaySong("Play certain Song"),
            QueryCash("Query Cash"),
            Deposit("Deposit Cash"),
            Donate("Donate to Artist"),
            FollowArtist("Follow Artist"),
            CancelFollowArtist("Cancel Follow Artist"),
            QueryFollow("List all my following Artist"),

            
        ]
