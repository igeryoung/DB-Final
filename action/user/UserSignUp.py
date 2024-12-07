from ..Action import Action
from role.User import User
from DB_utils_ping import db_register_user, user_name_exist, user_email_exist
import re

def is_valid_email(email):
    # Basic email pattern: checks for ...@...
    email_pattern = r'^[^@]+@[^@]+\.[^@]+$'
    return re.match(email_pattern, email) is not None

class UserSignUp(Action):
    def exec(self, conn, user = None):
        # print(f'Enter SignUp Action')

        email = self.read_input(conn, "email")
        while not is_valid_email(email):
            conn.send("email format incorrect".encode('utf-8'))
            email = self.read_input(conn, "correct email")
        
        while user_email_exist(email):
            conn.send("Email exist, ".encode('utf-8'))
            email = self.read_input(conn, "another email")

        # Read Username
        username = self.read_input(conn, "username")
        while user_name_exist(username):
            conn.send("Username exist, ".encode('utf-8'))
            username = self.read_input(conn, "another username")
        
        # Read Password
        pwd = self.read_input(conn, "password")
        # Add to DB
        userid = db_register_user(username, pwd, email)
        conn.send(f'----------------------------------------\nSuccessfully create account! Userid = {userid}\n'.encode('utf-8'))

        return User(userid, username, pwd, email)

