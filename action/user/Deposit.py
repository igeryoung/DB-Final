from ..Action import Action
from DB_utils_ping import deposit_cash

class Deposit(Action):
    def exec(self, conn, user):
        value = self.read_input(conn, "Deposit Value")

        if not value.isdigit():
            conn.send(f'''Please input a number\n'''.encode('utf-8'))
            return
        elif int(value) <= 0:
            conn.send(f'''Please input a number greater than 0\n'''.encode('utf-8'))
            return
        else:
            deposit_cash(user.get_userid(), value)
            conn.send(f'''----------------------------------------\nsuccessful deposit : {value}'''.encode('utf-8'))

        return