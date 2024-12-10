from ..Action import Action
from DB_utils import delete_activity_by_id, query_activity_id_by_artist_id_and_title

class DeleteActivity(Action):
    def exec(self, conn, user):
        # Read activity title from the user
        activity_title = self.read_input(conn, "Activity title")

        # Query activity ID
        activity_id = query_activity_id_by_artist_id_and_title(user.get_userid(), activity_title)

        if activity_id == -1:
            conn.send(f'''You have no activity named {activity_title}\n'''.encode('utf-8'))
            return

        # Delete the activity
        delete_activity_by_id(activity_id)
        conn.send(f'''----------------------------------------\nSuccessfully deleted activity: {activity_title}\n'''.encode('utf-8'))
        return
