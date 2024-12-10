from ..Action import Action
from DB_utils_ping import query_artist_id_by_name, query_cash, donate_cash
## Tested 
class Donate(Action):
    def exec(self, conn, user):
        uid = user.get_userid()
        name = self.read_input(conn, "artist name")
        artist_id = query_artist_id_by_name(name)
        if artist_id == -1:
            conn.send(f'''No artist name {name}'''.encode('utf-8'))
            return
        dot_value = self.read_input(conn, "donate value")
        print(dot_value)
        cur_value = query_cash(uid)
        
        if not dot_value.isdigit():
            conn.send(f'''Please input a number\n'''.encode('utf-8'))
            return
        elif int(dot_value) <= 0:
            conn.send(f'''Please input a number greater than 0\n'''.encode('utf-8'))
            return
        elif cur_value < int(dot_value):
            conn.send(f'''No sufficent found, you only have {cur_value}\n'''.encode('utf-8'))
        else:
            conn.send(f'''Ready donate $ [{dot_value}] to [{name}] \n'''.encode('utf-8'))
            confirm = self.read_input(conn, "Confirm? (Y/N) ")
            if confirm == "Y" or confirm == "y":
                donate_cash(uid, artist_id, int(dot_value))
                conn.send(f"Successfully donated [{dot_value}] to Artist: [{name}].".encode('utf-8'))
            else:
                conn.send(f"Donate cancel.".encode('utf-8'))

        return  