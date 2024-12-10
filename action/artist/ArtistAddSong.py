from ..Action import Action
from DB_utils import db_register_song

class AddSong(Action):
    def exec(self, conn, user):
        song_name = self.read_input(conn, "song name")
        print(f'Read song name: {song_name}')

        # while artist_song_exist(user.userid , song_name):
        #     conn.send("Song name exist, ".encode('utf-8'))
        #     song_name = self.read_input(conn, "another song name")

        song_genre = self.read_input(conn, "song genre")
        print(f'Read song genre: {song_genre}')
        song_language = self.read_input(conn, "song language")
        print(f'Read song language: {song_language}')

        song_album = self.read_input(conn, "song album")
        print(f'Read song album: {song_album}')

        if song_album == 'no':
            song_album = None

        status = db_register_song(
            user.get_userid(), 
            song_name, 
            song_genre, 
            song_language, 
            album=song_album
        )
        
        if status:
            conn.send(f'''----------------------------------------\n
                    Successfully create song! song_name = {song_name}\n'''.encode('utf-8'))
            return
        else:
            return -1