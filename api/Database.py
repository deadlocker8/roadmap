from DatabaseConnection import DatabaseConnection


class Database:
    def __init__(self, host, port, database, user, password):
        self.__host = host
        self.__port = port
        self.__database = database
        self.__user = user
        self.__password = password

    def get_roadmaps(self):
        query = 'SELECT * FROM roadmaps ORDER BY "ID";'
        with DatabaseConnection(self.__host, self.__port, self.__database, self.__user, self.__password) as conn:
            conn.execute(query)
            return conn.fetchall()

    def get_roadmap_name(self, roadmapID):
        query = 'SELECT "Projectname" FROM roadmaps WHERE "ID"=%s;'

        with DatabaseConnection(self.__host, self.__port, self.__database, self.__user, self.__password) as conn:
            conn.execute(query, (roadmapID,))
            return conn.fetchone()

    def get_milestones(self, roadmapID):
        query = 'SELECT * FROM milestones WHERE "RoadmapID"=%s ORDER BY "VersionCode" DESC;'

        with DatabaseConnection(self.__host, self.__port, self.__database, self.__user, self.__password) as conn:
            conn.execute(query, (roadmapID,))
            return conn.fetchall()

    def get_milestone(self, milestoneID):
        query = 'SELECT * FROM milestones WHERE "ID"=%s;'

        with DatabaseConnection(self.__host, self.__port, self.__database, self.__user, self.__password) as conn:
            conn.execute(query, (milestoneID,))
            return conn.fetchone()

    def get_tasks(self, milestoneID):
        query = 'SELECT * FROM tasks WHERE "MilestoneID"=%s;'

        with DatabaseConnection(self.__host, self.__port, self.__database, self.__user, self.__password) as conn:
            conn.execute(query, (milestoneID,))
            return conn.fetchall()

    def get_task(self, taskID):
        query = 'SELECT * FROM tasks WHERE "ID"=%s;'

        with DatabaseConnection(self.__host, self.__port, self.__database, self.__user, self.__password) as conn:
            conn.execute(query, (taskID,))
            return conn.fetchone()

    def get_sub_tasks(self, milestoneID):
        query = 'SELECT * FROM subtasks WHERE "TaskID"=%s;'

        with DatabaseConnection(self.__host, self.__port, self.__database, self.__user, self.__password) as conn:
            conn.execute(query, (milestoneID,))
            return conn.fetchall()

    def get_sub_task(self, taskID):
        query = 'SELECT * FROM subtasks WHERE "ID"=%s;'

        with DatabaseConnection(self.__host, self.__port, self.__database, self.__user, self.__password) as conn:
            conn.execute(query, (taskID,))
        return conn.fetchone()
