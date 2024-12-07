from ..Action import Action
from DB_utils_ping import list_artist_album

class ListAlbum(Action):
    def exec(self, conn, user):
        table = list_artist_album(user.get_userid())
        self.send_table(conn, table)
        return