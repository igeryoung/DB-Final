from ..Action import Action
from DB_utils import check_listener_exists, delete_listener_by_id

class DeleteListener(Action):
    def exec(self, conn, admin_user):
        # Read the user_id input from the admin
        user_id = self.read_input(conn, "Listener User ID to delete")
        
        # Verify if the user exists in the database
        if not check_listener_exists(user_id):
            conn.send(f'''Listener with ID {user_id} does not exist.'''.encode('utf-8'))
            return
        
        # Delete the listener
        delete_listener_by_id(user_id)
        conn.send(f'''----------------------------------------\nSuccessfully deleted listener with ID: {user_id}'''.encode('utf-8'))

        return