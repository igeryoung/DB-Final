from ..Action import Action
from DB_utils import delete_album, query_album_id_by_title_and_artist

class DeleteAlbum(Action):
    def exec(self, conn, user):

        album_title = self.read_input(conn, "Album title")
        del_recur = self.read_input(conn, "also delete song belong to that Album?(Y/N)")

        album_id = query_album_id_by_title_and_artist(user.get_userid(), album_title)

        if album_id == -1:
            conn.send(f'''you have no album name {album_title}'''.encode('utf-8'))
            return
        
        if del_recur == "Y" or del_recur == 'y':
            del_recur = "Y"
        else:
            del_recur = 'N'
        delete_album(album_id, del_recur)
        conn.send(f'''----------------------------------------\nsuccessful delete album : {album_title}'''.encode('utf-8'))
    
        return 