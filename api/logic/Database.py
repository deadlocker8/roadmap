from enum import Enum
from sqlite3.dbapi2 import Date

import psycopg2
from psycopg2.extras import RealDictCursor

from blueprints.RoadmapAPI import RoadmapParameters
from blueprints.MilestoneAPI import MilestoneParameters
from blueprints.TaskAPI import TaskParameters
from blueprints.SubTaskAPI import SubTaskParameters


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

        self.__create_tables()

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

    def __create_tables(self):
        self.__create_table_roadmaps()
        self.__create_table_milestones()
        self.__create_table_tasks()
        self.__create_table_subtasks()

    def __create_table_roadmaps(self):
        query = 'CREATE SEQUENCE IF NOT EXISTS "roadmaps_ID_seq"'
        self.__query(query, fetch_type=FetchType.NONE)

        queryTable = f'CREATE TABLE IF NOT EXISTS "public"."roadmaps" ' \
                     f'("{RoadmapParameters.ID.value}" int4 NOT NULL DEFAULT ' \
                     f'nextval(\'"roadmaps_ID_seq"\'::regclass),' \
                     f'"{RoadmapParameters.PROJECT_NAME.value}" text NOT NULL, ' \
                     f'PRIMARY KEY ("{RoadmapParameters.ID.value}"));'
        self.__query(queryTable, fetch_type=FetchType.NONE)

    def __create_table_milestones(self):
        query = 'CREATE SEQUENCE IF NOT EXISTS "milestones_ID_seq"'
        self.__query(query, fetch_type=FetchType.NONE)

        queryTable = f'CREATE TABLE IF NOT EXISTS "public"."milestones" ' \
                     f'("{MilestoneParameters.ID.value}" int4 NOT NULL DEFAULT ' \
                     f'nextval(\'"milestones_ID_seq"\'::regclass),' \
                     f'"{MilestoneParameters.ROADMAP_ID.value}" int4 NOT NULL, ' \
                     f'"{MilestoneParameters.VERSION_CODE.value}" int4 NOT NULL, ' \
                     f'"{MilestoneParameters.VERSION_NAME.value}" text NOT NULL, ' \
                     f'"{MilestoneParameters.TITLE.value}" text NOT NULL, ' \
                     f'"{MilestoneParameters.DUE_DATE.value}" date NOT NULL, ' \
                     f'"{MilestoneParameters.COMPLETION_DATE.value}" date NOT NULL, ' \
                     f'"{MilestoneParameters.STATUS.value}" int4 NOT NULL, ' \
                     f'PRIMARY KEY ("{MilestoneParameters.ID.value}"));'
        self.__query(queryTable, fetch_type=FetchType.NONE)

    def __create_table_tasks(self):
        query = 'CREATE SEQUENCE IF NOT EXISTS "tasks_ID_seq"'
        self.__query(query, fetch_type=FetchType.NONE)

        queryTable = f'CREATE TABLE IF NOT EXISTS "public"."tasks" ' \
                     f'("{TaskParameters.ID.value}" int4 NOT NULL DEFAULT ' \
                     f'nextval(\'"tasks_ID_seq"\'::regclass),' \
                     f'"{TaskParameters.MILESTONE_ID.value}" int4 NOT NULL, ' \
                     f'"{TaskParameters.TITLE.value}" text NOT NULL, ' \
                     f'"{TaskParameters.DESCRIPTION.value}" text NOT NULL, ' \
                     f'"{TaskParameters.STATUS.value}" int4 NOT NULL, ' \
                     f'PRIMARY KEY ("{TaskParameters.ID.value}"));'
        self.__query(queryTable, fetch_type=FetchType.NONE)

    def __create_table_subtasks(self):
        query = 'CREATE SEQUENCE IF NOT EXISTS "subtasks_ID_seq"'
        self.__query(query, fetch_type=FetchType.NONE)

        queryTable = f'CREATE TABLE IF NOT EXISTS "public"."subtasks" ' \
                     f'("{SubTaskParameters.ID.value}" int4 NOT NULL DEFAULT ' \
                     f'nextval(\'"subtasks_ID_seq"\'::regclass),' \
                     f'"{SubTaskParameters.TASK_ID.value}" int4 NOT NULL, ' \
                     f'"{SubTaskParameters.TITLE.value}" text NOT NULL, ' \
                     f'"{SubTaskParameters.DESCRIPTION.value}" text NOT NULL, ' \
                     f'"{SubTaskParameters.STATUS.value}" int4 NOT NULL, ' \
                     f'PRIMARY KEY ("{SubTaskParameters.ID.value}"));'
        self.__query(queryTable, fetch_type=FetchType.NONE)

# ROADMAPS
    def get_roadmaps(self):
        query = f'SELECT * FROM roadmaps ORDER BY "{RoadmapParameters.ID.value}";'
        return self.__query(query)

    def get_roadmap(self, roadmapID):
        query = f'SELECT * FROM roadmaps WHERE "{RoadmapParameters.ID.value}"=%s;'
        return self.__query(query, roadmapID, fetch_type=FetchType.ONE)

    def add_roadmap(self, name):
        query = f'INSERT INTO roadmaps ("{RoadmapParameters.PROJECT_NAME.value}") VALUES (%s);'
        self.__query(query, name, fetch_type=FetchType.NONE)

    def update_roadmap(self, roadmapID, name):
        query = f'UPDATE roadmaps SET "{RoadmapParameters.PROJECT_NAME.value}"=%s WHERE "{RoadmapParameters.ID.value}"=%s;'
        self.__query(query, name, roadmapID, fetch_type=FetchType.NONE)

    def delete_roadmap(self, roadmapID):
        query = f'DELETE FROM roadmaps WHERE "{RoadmapParameters.ID.value}"=%s;'
        self.__query(query, roadmapID, fetch_type=FetchType.NONE)

    # MILESTONES
    def get_all_milestones(self):
        query = f'SELECT * FROM milestones ORDER BY "{MilestoneParameters.VERSION_CODE.value}" DESC;'
        return self.__query(query)

    def get_milestones(self, roadmapID):
        query = f'SELECT * FROM milestones WHERE "{MilestoneParameters.ROADMAP_ID.value}"=%s ORDER BY "{MilestoneParameters.VERSION_CODE.value}" DESC;'
        return self.__query(query, roadmapID)

    def get_open_milestones(self, roadmapID):
        query = f'SELECT * FROM milestones WHERE "{MilestoneParameters.ROADMAP_ID.value}"=%s AND "Status"=0 ORDER BY "{MilestoneParameters.VERSION_CODE.value}" DESC;'
        return self.__query(query, roadmapID)

    def get_milestone(self, milestoneID):
        query = f'SELECT * FROM milestones WHERE "{MilestoneParameters.ID.value}"=%s;'
        return self.__query(query, milestoneID, fetch_type=FetchType.ONE)

    def get_latest_milestone(self, roadmapID):
        query = f'SELECT * FROM milestones WHERE "{MilestoneParameters.ROADMAP_ID.value}"=%s AND "{MilestoneParameters.STATUS.value}" = 1 ORDER BY "{MilestoneParameters.VERSION_CODE.value}" DESC;'
        return self.__query(query, roadmapID, fetch_type=FetchType.ONE)

    def add_milestone(self, roadmapID, versionCode, versionName, title, dueDate, completionDate, status):
        query = f'INSERT INTO milestones ("{MilestoneParameters.ROADMAP_ID.value}", "{MilestoneParameters.VERSION_CODE.value}", "{MilestoneParameters.VERSION_NAME.value}", "{MilestoneParameters.TITLE.value}", "{MilestoneParameters.DUE_DATE.value}", "{MilestoneParameters.COMPLETION_DATE.value}", "{MilestoneParameters.STATUS.value}") VALUES (%s, %s, %s, %s, %s, %s, %s);'
        self.__query(query, roadmapID, versionCode, versionName, title, dueDate, completionDate, status,
                     fetch_type=FetchType.NONE)

    def update_milestone(self, milestoneID, roadmapID, versionCode, versionName, title, dueDate, completionDate,
                         status):
        query = f'UPDATE milestones SET "{MilestoneParameters.ROADMAP_ID.value}"=%s, "{MilestoneParameters.VERSION_CODE.value}"=%s, "{MilestoneParameters.VERSION_NAME.value}"=%s, "{MilestoneParameters.TITLE.value}"=%s, "{MilestoneParameters.DUE_DATE.value}"=%s, "{MilestoneParameters.COMPLETION_DATE.value}"=%s, "{MilestoneParameters.STATUS.value}"=%s WHERE "{MilestoneParameters.ID.value}"=%s;'
        self.__query(query, roadmapID, versionCode, versionName, title, dueDate, completionDate, status, milestoneID,
                     fetch_type=FetchType.NONE)

    def finish_milestone(self, milestoneID):
        query = f'UPDATE milestones SET "{MilestoneParameters.COMPLETION_DATE.value}"=%s, "{MilestoneParameters.STATUS.value}"=%s WHERE "{MilestoneParameters.ID.value}"=%s;'
        self.__query(query, Date.today(), 1, milestoneID, fetch_type=FetchType.NONE)

    def delete_milestone(self, milestoneID):
        query = f'DELETE FROM milestones WHERE "{MilestoneParameters.ID.value}"=%s;'
        self.__query(query, milestoneID, fetch_type=FetchType.NONE)

    # TASKS
    def get_all_tasks(self):
        query = f'SELECT * FROM tasks ORDER BY "{TaskParameters.ID.value}";'
        return self.__query(query)

    def get_tasks(self, milestoneID):
        query = f'SELECT * FROM tasks WHERE "{TaskParameters.MILESTONE_ID.value}"=%s ORDER BY "{TaskParameters.ID.value}";'
        return self.__query(query, milestoneID)

    def get_open_tasks(self, milestoneID):
        query = f'SELECT * FROM tasks WHERE "{TaskParameters.MILESTONE_ID.value}"=%s AND "{TaskParameters.STATUS.value}"=0 ORDER BY "{TaskParameters.ID.value}";'
        return self.__query(query, milestoneID)

    def get_task(self, taskID):
        query = f'SELECT * FROM tasks WHERE "{TaskParameters.ID.value}"=%s;'
        return self.__query(query, taskID, fetch_type=FetchType.ONE)

    def add_task(self, milestoneID, title, description, status):
        query = f'INSERT INTO tasks ("{TaskParameters.MILESTONE_ID.value}", "{TaskParameters.TITLE.value}", "{TaskParameters.DESCRIPTION.value}", "{TaskParameters.STATUS.value}") VALUES (%s, %s, %s, %s);'
        self.__query(query, milestoneID, title, description, status, fetch_type=FetchType.NONE)

    def update_task(self, taskID, milestoneID, title, description, status):
        query = f'UPDATE tasks SET "{TaskParameters.MILESTONE_ID.value}"=%s, "{TaskParameters.TITLE.value}"=%s, "{TaskParameters.DESCRIPTION.value}"=%s, "{TaskParameters.STATUS.value}"=%s WHERE "{TaskParameters.ID.value}"=%s;'
        self.__query(query, milestoneID, title, description, status, taskID, fetch_type=FetchType.NONE)

    def finish_task(self, taskID):
        query = f'UPDATE tasks SET "{TaskParameters.STATUS.value}"=%s WHERE "{TaskParameters.ID.value}"=%s;'
        self.__query(query, 1, taskID, fetch_type=FetchType.NONE)

    def delete_task(self, taskID):
        query = f'DELETE FROM tasks WHERE "{TaskParameters.ID.value}"=%s;'
        self.__query(query, taskID, fetch_type=FetchType.NONE)

    # SUBTASKS
    def get_all_sub_tasks(self):
        query = f'SELECT * FROM subtasks ORDER BY "{SubTaskParameters.ID.value}";'
        return self.__query(query)

    def get_sub_tasks(self, taskID):
        query = f'SELECT * FROM subtasks WHERE "{SubTaskParameters.TASK_ID.value}"=%s ORDER BY "{SubTaskParameters.ID.value}";'
        return self.__query(query, taskID)

    def get_open_sub_tasks(self, taskID):
        query = f'SELECT * FROM subtasks WHERE "{SubTaskParameters.TASK_ID.value}"=%s AND "{SubTaskParameters.STATUS.value}"=0 ORDER BY "{SubTaskParameters.ID.value}";'
        return self.__query(query, taskID)

    def get_sub_task(self, subTaskID):
        query = f'SELECT * FROM subtasks WHERE "{SubTaskParameters.ID.value}"=%s;'
        return self.__query(query, subTaskID, fetch_type=FetchType.ONE)

    def add_sub_task(self, taskID, title, description, status):
        query = f'INSERT INTO subtasks ("{SubTaskParameters.TASK_ID.value}", "{SubTaskParameters.TITLE.value}", "{SubTaskParameters.DESCRIPTION.value}", "{SubTaskParameters.STATUS.value}") VALUES (%s, %s, %s, %s);'
        self.__query(query, taskID, title, description, status, fetch_type=FetchType.NONE)

    def update_sub_task(self, subTaskID, taskID, title, description, status):
        query = f'UPDATE subtasks SET "{SubTaskParameters.TASK_ID.value}"=%s, "{SubTaskParameters.TITLE.value}"=%s, "{SubTaskParameters.DESCRIPTION.value}"=%s, "{SubTaskParameters.STATUS.value}"=%s WHERE "{SubTaskParameters.ID.value}"=%s;'
        self.__query(query, taskID, title, description, status, subTaskID, fetch_type=FetchType.NONE)

    def finish_sub_task(self, subTaskID):
        query = f'UPDATE subtasks SET "{SubTaskParameters.STATUS.value}"=%s WHERE "{SubTaskParameters.ID.value}"=%s;'
        self.__query(query, 1, subTaskID, fetch_type=FetchType.NONE)

    def delete_sub_task(self, subTaskID):
        query = f'DELETE FROM subtasks WHERE "{SubTaskParameters.ID.value}"=%s;'
        self.__query(query, subTaskID, fetch_type=FetchType.NONE)
