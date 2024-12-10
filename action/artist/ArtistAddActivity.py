from ..Action import Action
from DB_utils import artist_activity_exist, db_register_activity
from datetime import datetime

class AddActivity(Action):
    def exec(self, conn, user):
        # Read activity title
        activity_title = self.read_input(conn, "activity title")
        print(f'Read activity title: {activity_title}')

        # Check if activity already exists
        while artist_activity_exist(user.userid, activity_title):
            conn.send("Activity title exists, please enter another one.\n".encode('utf-8'))
            activity_title = self.read_input(conn, "another activity title")

        # Read additional activity details
        activity_description = self.read_input(conn, "activity description")
        print(f'Read activity description: {activity_description}')

        activity_location = self.read_input(conn, "activity location")
        print(f'Read activity location: {activity_location}')

        # Read and format activity date
        activity_date_str = self.read_input(conn, "activity date (YYYY-MM-DD HH)")
        print(f'Read activity date: {activity_date_str}')

        try:
            # Convert the input to datetime format
            activity_date = datetime.strptime(activity_date_str, "%Y-%m-%d %H")
            print(f'Formatted activity date: {activity_date}')
        except ValueError:
            conn.send("Invalid date format. Please use YYYY-MM-DD HH.\n".encode('utf-8'))
            return -1

        # Register the activity in the database
        status = db_register_activity(
            user.userid, 
            activity_title, 
            activity_description, 
            activity_location, 
            activity_date
        )

        if status:
            conn.send(f'''\n----------------------------------------\n\nSuccessfully created activity!\nTitle: {activity_title}\n'''.encode('utf-8'))
            return
        else:
            return -1
