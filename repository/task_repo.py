class TaskRepo:

    def __init__(self, cluster):
        self.cluster = cluster
        self.session = self.cluster.connect('task_manager')

    def create_task(self, task_id, title, description, status, due_date, assigned_user):
        self.session.execute(
            """
            INSERT INTO tasks (task_id, title, description, status, due_date, assigned_user)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (task_id, title, description, status, due_date, assigned_user)
        )

    def get_task_by_id(self, task_id):
        result = self.session.execute(
            """
            SELECT * FROM tasks WHERE task_id = %s
            """,
            (task_id,)
        )
        return result.one()

    def update_task(self, task_id, title=None, description=None, status=None, due_date=None, assigned_user=None):
        update_fields = []
        update_values = []

        if title:
            update_fields.append("title = %s")
            update_values.append(title)
        if description:
            update_fields.append("description = %s")
            update_values.append(description)
        if status:
            update_fields.append("status = %s")
            update_values.append(status)
        if due_date:
            update_fields.append("due_date = %s")
            update_values.append(due_date)
        if assigned_user:
            update_fields.append("assigned_user = %s")
            update_values.append(assigned_user)

        if update_fields:
            update_query = "UPDATE tasks SET " + ", ".join(update_fields) + " WHERE task_id = %s"
            self.session.execute(update_query, update_values + [task_id])
        else:
            raise Exception('No matching fields to operate on')

    def delete_task(self, task_id):
        self.session.execute(
            """
            DELETE FROM tasks WHERE task_id = %s
            """,
            (task_id,)
        )

    def get_all_tasks(self):
        result = self.session.execute(
        """
        select * from tasks
        """
        )
        return result
    
    def get_tasks_by_assigned_userid(self, userid):
        result = self.session.execute(
            """
            select * from tasks where user_id = %s
            """,
            (userid,)
        )
        return result

    def filter_tasks(self, status=None, due_date=None, assigned_user=None):
        cql = "SELECT * FROM tasks WHERE "
        filters = []

        if status:
            filters.append(f"status = '{status}'")
        if due_date:
            filters.append(f"due_date >= '{due_date}'")
        if assigned_user:
            filters.append(f"assigned_user = '{assigned_user}'")
        if not filters:
            raise Exception("no matching filters")

        cql += " AND ".join(filters)
        result = self.session.execute(cql)
        return result.all()

    def close_session(self):
        self.session.shutdown()