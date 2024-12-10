from ..Action import Action
from role.Artist import Artist
from DB_utils import db_register_artist, artist_email_exist, artist_name_exist
import re

def is_valid_email(email):
    # Basic email pattern: checks for ...@...
    email_pattern = r'^[^@]+@[^@]+\.[^@]+$'
    return re.match(email_pattern, email) is not None

class CreateArtist(Action):
    def exec(self, conn, artist = None):
        # print(f'Enter SignUp Action')

        email = self.read_input(conn, "email")
        while not is_valid_email(email):
            conn.send("email format incorrect".encode('utf-8'))
            email = self.read_input(conn, "correct email")
        
        while artist_email_exist(email):
            conn.send("Email exist, ".encode('utf-8'))
            email = self.read_input(conn, "another email")

        # Read artistname
        artistname = self.read_input(conn, "artistname")
        while artist_name_exist(artistname):
            conn.send("artistname exist, ".encode('utf-8'))
            artistname = self.read_input(conn, "another artistname")
        
        # Read Password
        pwd = self.read_input(conn, "password")
        # Add to DB
        artistid = db_register_artist(artistname, pwd, email)
        conn.send(f'----------------------------------------\nSuccessfully create account! artistid = {artistid}\n'.encode('utf-8'))

        return Artist(artistid, artistname, pwd, email)

