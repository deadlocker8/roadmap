from enum import Enum

import psycopg2
from psycopg2.extras import RealDictCursor


class FetchType(Enum):
    NONE = 1
    ONE = 2
    ALL = 3


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
        self.__connection.autocommit = True
        self.__cursor = self.__connection.cursor(cursor_factory=RealDictCursor)

    def __disconnect(self):
        if self.__connection is not None:
            self.__connection.close()

    def __query(self, query, *args, fetch_type=FetchType.ALL):
        try:
            self.__cursor.execute(query, args)
        except psycopg2.InterfaceError:
            self.__disconnect()
            self.__connect()
            self.__cursor.execute(query, args)

        if fetch_type == FetchType.ONE:
            return self.__cursor.fetchone()
        if fetch_type == FetchType.ALL:
            return self.__cursor.fetchall()

    # ROADMAPS
    def get_roadmaps(self):
        query = 'SELECT * FROM roadmaps ORDER BY "ID";'
        return self.__query(query)

    def get_roadmap(self, roadmapID):
        query = 'SELECT "Projectname" FROM roadmaps WHERE "ID"=%s;'
        return self.__query(query, roadmapID, fetch_type=FetchType.ONE)

    def add_roadmap(self, name):
        query = 'INSERT INTO roadmaps ("Projectname") VALUES (%s);'
        self.__query(query, name, fetch_type=FetchType.NONE)

    def update_roadmap(self, roadmapID, name):
        query = 'UPDATE roadmaps SET "Projectname"=%s WHERE "ID"=%s;'
        self.__query(query, name, roadmapID, fetch_type=FetchType.NONE)

    def delete_roadmap(self, roadmapID):
        query = 'DELETE FROM roadmaps WHERE "ID"=%s;'
        self.__query(query, roadmapID, fetch_type=FetchType.NONE)

    # MILESTONES
    def get_all_milestones(self):
        query = 'SELECT * FROM milestones ORDER BY "VersionCode" DESC;'
        return self.__query(query)

    def get_milestones(self, roadmapID):
        query = 'SELECT * FROM milestones WHERE "RoadmapID"=%s ORDER BY "VersionCode" DESC;'
        return self.__query(query, roadmapID)

    def get_open_milestones(self, roadmapID):
        query = 'SELECT * FROM milestones WHERE "RoadmapID"=%s AND "Status"=0 ORDER BY "VersionCode" DESC;'
        return self.__query(query, roadmapID)

    def get_milestone(self, milestoneID):
        query = 'SELECT * FROM milestones WHERE "ID"=%s;'
        return self.__query(query, milestoneID, fetch_type=FetchType.ONE)

    def get_latest_milestone(self, roadmapID):
        query = 'SELECT * FROM milestones WHERE "RoadmapID"=%s AND "Status" = 1 ORDER BY "VersionCode" DESC;'
        return self.__query(query, roadmapID, fetch_type=FetchType.ONE)

    def add_milestone(self, roadmapID, versionCode, versionName, title, dueDate, completionDate):
        query = 'INSERT INTO milestones ("RoadmapID", "VersionCode", "VersionName", "Title", "DueDate", "CompletionDate", "Status") VALUES (%s, %s, %s, %s, %s, %s, %s);'
        self.__query(query, roadmapID, versionCode, versionName, title, dueDate, completionDate, 1, fetch_type=FetchType.NONE)

    def update_milestone(self, milestoneID, roadmapID, versionCode, versionName, title, dueDate, completionDate, status):
        query = 'UPDATE milestones SET "RoadmapID"=%s, "VersionCode"=%s, "VersionName"=%s, "Title"=%s, "DueDate"=%s, "CompletionDate"=%s, "Status"=%s WHERE "ID"=%s;'
        self.__query(query, roadmapID, versionCode, versionName, title, dueDate, completionDate, status, milestoneID, fetch_type=FetchType.NONE)

    def delete_milestone(self, milestoneID):
        query = 'DELETE FROM milestones WHERE "ID"=%s;'
        self.__query(query, milestoneID, fetch_type=FetchType.NONE)

    # TASKS
    def get_all_tasks(self):
        query = 'SELECT * FROM tasks;'
        return self.__query(query)

    def get_tasks(self, milestoneID):
        query = 'SELECT * FROM tasks WHERE "MilestoneID"=%s;'
        return self.__query(query, milestoneID)

    def get_open_tasks(self, milestoneID):
        query = 'SELECT * FROM tasks WHERE "MilestoneID"=%s AND "Status"=0;'
        return self.__query(query, milestoneID)

    def get_task(self, taskID):
        query = 'SELECT * FROM tasks WHERE "ID"=%s;'
        return self.__query(query, taskID, fetch_type=FetchType.ONE)

    def add_task(self, milestoneID, title, description):
        query = 'INSERT INTO tasks ("MilestoneID", "Title", "Description", "Status") VALUES (%s, %s, %s, %s);'
        self.__query(query, milestoneID, title, description, 1, fetch_type=FetchType.NONE)

    def update_task(self, taskID, milestoneID, title, description, status):
        query = 'UPDATE tasks SET "MilestoneID"=%s, "Title"=%s, "Description"=%s, "Status"=%s WHERE "ID"=%s;'
        self.__query(query, milestoneID, title, description, status, taskID, fetch_type=FetchType.NONE)

    def delete_task(self, taskID):
        query = 'DELETE FROM tasks WHERE "ID"=%s;'
        self.__query(query, taskID, fetch_type=FetchType.NONE)

    # SUBTASKS
    def get_all_sub_tasks(self):
        query = 'SELECT * FROM subtasks;'
        return self.__query(query)

    def get_sub_tasks(self, taskID):
        query = 'SELECT * FROM subtasks WHERE "TaskID"=%s;'
        return self.__query(query, taskID)

    def get_open_sub_tasks(self, taskID):
        query = 'SELECT * FROM subtasks WHERE "TaskID"=%s AND "Status"=0;'
        return self.__query(query, taskID)

    def get_sub_task(self, subTaskID):
        query = 'SELECT * FROM subtasks WHERE "ID"=%s;'
        return self.__query(query, subTaskID, fetch_type=FetchType.ONE)

    def add_sub_task(self, taskID, title, description):
        query = 'INSERT INTO subtasks ("TaskID", "Title", "Description", "Status") VALUES (%s, %s, %s, %s);'
        self.__query(query, taskID, title, description, 1, fetch_type=FetchType.NONE)

    def update_sub_task(self, subTaskID, taskID, title, description, status):
        query = 'UPDATE subtasks SET "TaskID"=%s, "Title"=%s, "Description"=%s, "Status"=%s WHERE "ID"=%s;'
        self.__query(query, taskID, title, description, status, subTaskID, fetch_type=FetchType.NONE)

    def delete_sub_task(self, subTaskID):
        query = 'DELETE FROM subtasks WHERE "ID"=%s;'
        self.__query(query, subTaskID, fetch_type=FetchType.NONE)
