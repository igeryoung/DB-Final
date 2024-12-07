from .Action import Action
from role.User import User
# from role.Admin import Admin
from DB_utils_ping import fetch_user_by_email
import re

def is_valid_email(email):
    # Basic email pattern: checks for ...@...
    email_pattern = r'^[^@]+@[^@]+\.[^@]+$'
    return re.match(email_pattern, email) is not None

class LogIn(Action):
    def exec(self, conn, user=None):
        count = 3
        email = self.read_input(conn, "email")
        print(f'Read email: {email}')

        while not is_valid_email(email):
            conn.send("email format incorrect".encode('utf-8'))
            email = self.read_input(conn, "correct email")

        userid, username, pwd, is_admin = fetch_user_by_email(email)
        # print(f'--After fetch')

        while username is None:
            conn.send("Userid not exist, ".encode('utf-8'))
            userid = self.read_input(conn, "correct userid")
            userid, username, pwd, is_admin = fetch_user_by_email(userid)

        pwd_input = self.read_input(conn, "password")
        
        while count > 0 and pwd_input != pwd:
            conn.send(f'[INPUT]Password incorrect, please enter password (remaining try: {count}): '.encode('utf-8'))
            pwd_input = conn.recv(100).decode("utf-8")
            count -= 1
        if count == 0:
            conn.send(f'[EXIT]Connection close. Reason: Password incorrect.'.encode('utf-8'))
            return -1
        
        else:
            print(f'welcome! {username}')
            return User(userid, username, pwd, email)