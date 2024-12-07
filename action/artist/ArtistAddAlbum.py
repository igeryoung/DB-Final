from ..Action import Action
from DB_utils_ping import artist_album_exist, db_register_album

class AddAlbum(Action):
    def exec(self, conn, user):
        album_name = self.read_input(conn, "album name")
        print(f'Read album name: {album_name}')

        while artist_album_exist(user.userid , album_name):
            conn.send("Album name exist, ".encode('utf-8'))
            album_name = self.read_input(conn, "another album name")

        album_genre = self.read_input(conn, "album genre")
        print(f'Read album genre: {album_genre}')

        status = db_register_album(user.userid, album_name, album_genre)
        if status:
            conn.send(f'''----------------------------------------\n
                    Successfully create album! album_name = {album_name}\n'''.encode('utf-8'))
            return
        else:
            return -1