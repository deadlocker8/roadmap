import psycopg2
from psycopg2.extras import RealDictCursor


class Database:
    def __init__(self, database_settings):
        self.__host = database_settings["host"]
        self.__port = database_settings["port"]
        self.__database = database_settings["databaseName"]
        self.__user = database_settings["user"]
        self.__password = database_settings["password"]

        self.__connection = None
        self.__cursor = None

        self.__connect()

    def __connect(self):
        self.__connection = psycopg2.connect(user=self.__user,
                                             password=self.__password,
                                             host=self.__host,
                                             port=self.__port,
                                             database=self.__database)
        self.__cursor = self.__connection.cursor(cursor_factory=RealDictCursor)

    def __disconnect(self):
        if self.__connection is not None:
            self.__connection.close()

    def __query(self, query, *args, fetch_one=False):
        try:
            self.__cursor.execute(query, args)
        except psycopg2.InterfaceError:
            self.__disconnect()
            self.__connect()

        self.__cursor.execute(query, args)
        if fetch_one:
            return self.__cursor.fetchone()
        return self.__cursor.fetchall()

    def get_roadmaps(self):
        query = 'SELECT * FROM roadmaps ORDER BY "ID";'
        return self.__query(query)

    def get_roadmap(self, roadmapID):
        query = 'SELECT "Projectname" FROM roadmaps WHERE "ID"=%s;'
        return self.__query(query, roadmapID, fetch_one=True)

    def get_milestones(self, roadmapID):
        query = 'SELECT * FROM milestones WHERE "RoadmapID"=%s ORDER BY "VersionCode" DESC;'
        return self.__query(query, roadmapID)

    def get_open_milestones(self, roadmapID):
        query = 'SELECT * FROM milestones WHERE "RoadmapID"=%s AND "Status"=0 ORDER BY "VersionCode" DESC;'
        return self.__query(query, roadmapID)

    def get_milestone(self, milestoneID):
        query = 'SELECT * FROM milestones WHERE "ID"=%s;'
        return self.__query(query, milestoneID, fetch_one=True)

    def get_latest_milestone(self, roadmapID):
        query = 'SELECT * FROM milestones WHERE "RoadmapID"=%s AND "Status" = 1 ORDER BY "VersionCode" DESC;'
        return self.__query(query, roadmapID, fetch_one=True)

    def get_tasks(self, milestoneID):
        query = 'SELECT * FROM tasks WHERE "MilestoneID"=%s;'
        return self.__query(query, milestoneID)

    def get_open_tasks(self, milestoneID):
        query = 'SELECT * FROM tasks WHERE "MilestoneID"=%s AND "Status"=0;'
        return self.__query(query, milestoneID)

    def get_task(self, taskID):
        query = 'SELECT * FROM tasks WHERE "ID"=%s;'
        return self.__query(query, taskID, fetch_one=True)

    def get_sub_tasks(self, taskID):
        query = 'SELECT * FROM subtasks WHERE "TaskID"=%s;'
        return self.__query(query, taskID)

    def get_open_sub_tasks(self, taskID):
        query = 'SELECT * FROM subtasks WHERE "TaskID"=%s AND "Status"=0;'
        return self.__query(query, taskID)

    def get_sub_task(self, subTaskID):
        query = 'SELECT * FROM subtasks WHERE "ID"=%s;'
        return self.__query(query, subTaskID, fetch_one=True)
