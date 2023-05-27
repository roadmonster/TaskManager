from cassandra.cluster import Cluster

class UserRepo:

    def __init__(self, cluster) -> None:
        self.cluster = cluster
        self.session = self.cluster.connect('task_manager')

    def create_user(self, user_id, username, password, email, additional_info=None):
        self.session.execute(
            """
            INSERT INTO users (user_id, username, password, email, additional_info)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (user_id, username, password, email, additional_info)
        )

    def get_user_by_userid(self, userid):
        result = self.session.execute(
            """
            SELECT * FROM users WHERE user_id = %s
            """,
            (userid,)
        )
        return result.one()

    def get_user_by_email(self, email):
        result = self.session.execute(
            """
            SELECT * FROM users WHERE email = %s
            """,
            (email,)
        )
        return result.one()
    
    def close_session(self):
        self.session.shutdown()

    def get_all_users(self):
        return self.session.execute(
            """
            select * from users
            """
        )
