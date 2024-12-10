from ..Action import Action
from DB_utils import list_artist_song

class ListSong(Action):
    def exec(self, conn, user):
        table = list_artist_song(user.get_userid())
        self.send_table(conn, table)
        return