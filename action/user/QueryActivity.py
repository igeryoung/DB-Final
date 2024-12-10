from ..Action import Action
from datetime import datetime, timedelta
from DB_utils import user_query_activity

class QueryRecentActivity(Action):
    def exec(self, conn, user):
        query_date = datetime.now() + timedelta(days=60)
        table = user_query_activity(query_date)
        self.send_table(conn, table)