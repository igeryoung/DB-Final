from ..Action import Action
from DB_utils import check_artist_exists, delete_artist_by_id

class DeleteArtist(Action):
    def exec(self, conn, admin_user):
        # Read the artist's user_id input from the admin
        user_id = self.read_input(conn, "Artist User ID to delete")
        
        # Verify if the artist exists in the database
        if not check_artist_exists(user_id):
            conn.send(f'''Artist with ID {user_id} does not exist.'''.encode('utf-8'))
            return
        
        # Delete the artist and associated data
        delete_artist_by_id(user_id)
        conn.send(f'''----------------------------------------\nSuccessfully deleted artist with ID: {user_id}'''.encode('utf-8'))

        return