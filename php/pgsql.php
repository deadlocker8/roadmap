<?php /** @noinspection SqlNoDataSourceInspection */

class DB
{
    private static $db;

    function __construct()
    {
        try
        {
            include(dirname(__FILE__)."/admin/helper/settings.php");
            self::$db = new PDO(
                "pgsql:host=localhost;dbname=" . $database_name,
                $database_user,
                $database_password,
                array(PDO::MYSQL_ATTR_INIT_COMMAND => "SET NAMES 'utf8'"));

            self::createTables();
        }
        catch(PDOException $e)
        {
            die($e);
        }
    }

    function createTables()
    {
        $statement = self::$db->prepare('CREATE TABLE IF NOT EXISTS "roadmaps" ('.
            '"ID" serial NOT NULL PRIMARY KEY,'.
            '"Projectname" text NOT NULL);');
        $statement->execute();

        $statement = self::$db->prepare('CREATE TABLE IF NOT EXISTS "milestones" ('.
            '"ID" serial NOT NULL PRIMARY KEY,'.
            '"RoadmapID" integer NOT NULL,'.
            '"VersionCode"integer NOT NULL,'.
            '"VersionName" text NOT NULL,'.
            '"Title" text NOT NULL,'.
            '"DueDate" date NOT NULL,'.
            '"CompletionDate" date NOT NULL,'.
            '"Status" integer NOT NULL);');
        $statement->execute();

        $statement = self::$db->prepare('CREATE TABLE IF NOT EXISTS "tasks" ('.
            '"ID" serial NOT NULL PRIMARY KEY,'.
            '"MilestoneID" integer NOT NULL,'.
            '"Title" text NOT NULL,'.
            '"Description" text NOT NULL,'.
            '"Status" integer NOT NULL);');
        $statement->execute();

        $statement = self::$db->prepare('CREATE TABLE IF NOT EXISTS "subtasks" ('.
            '"ID" serial NOT NULL PRIMARY KEY,'.
            '"TaskID" integer NOT NULL,'.
            '"Title" text NOT NULL,'.
            '"Description" text NOT NULL,'.
            '"Status" integer NOT NULL);');
        $statement->execute();
    }

    //========================================
    //---------------- insert ----------------
    //========================================

    function insertRoadmap($projectName)
    {
        $statement = self::$db->prepare('INSERT INTO roadmaps ("Projectname") VALUES(:projectName);');
        $statement->bindParam("projectName", $projectName);

        return $statement->execute();
    }

    function insertMilestone($roadmapID, $versionCode, $versionName, $title, $dueDate, $completionDate, $status)
    {
        $statement = self::$db->prepare('INSERT INTO milestones ("RoadmapID", "VersionCode", "VersionName", "Title", "DueDate", "CompletionDate", "Status") VALUES(:roadmapID, :versionCode, :versionName, :title, to_date(:dueDate, \'DD.MM.YY\'), to_date(:completionDate, \'DD.MM.YY\'), :status);');
        $statement->bindParam("roadmapID", $roadmapID);
        $statement->bindParam("versionCode", $versionCode);
        $statement->bindParam("versionName", $versionName);
        $statement->bindParam("title", $title);
        $statement->bindParam("dueDate", $dueDate);
        $statement->bindParam("completionDate", $completionDate);
        $statement->bindParam("status", $status);

        return $statement->execute();
    }

    function insertTask($milestoneID, $title, $description, $status)
    {
        $statement = self::$db->prepare('INSERT INTO tasks ("MilestoneID", "Title", "Description", "Status") VALUES(:milestoneID, :title, :description, :status);');
        $statement->bindParam("milestoneID", $milestoneID);
        $statement->bindParam("title", $title);
        $statement->bindParam("description", $description);
        $statement->bindParam("status", $status);

        return $statement->execute();
    }

    function insertSubtask($taskID, $title, $description, $status)
    {
        $statement = self::$db->prepare('INSERT INTO subtasks ("TaskID", "Title", "Description", "Status") VALUES(:taskID, :title, :description, :status);');
        $statement->bindParam("taskID", $taskID);
        $statement->bindParam("title", $title);
        $statement->bindParam("description", $description);
        $statement->bindParam("status", $status);
        $success = $statement->execute();

        $this->checkParentTask($taskID);

        return $success;
    }

    //========================================
    //---------------- finish ----------------
    //========================================

    function finishMilestone($milestoneID)
    {
        $statement = self::$db->prepare('UPDATE milestones SET "Status"=1 WHERE "ID" = :milestoneID;');
        $statement->bindParam("milestoneID", $milestoneID);

        return $statement->execute();
    }

    function finishTask($taskID)
    {
        $statement = self::$db->prepare('UPDATE tasks SET "Status"=1 WHERE "ID" = :taskID;');
        $statement->bindParam("taskID", $taskID);

        return $statement->execute();
    }

    function reopenTask($taskID)
    {
        $statement = self::$db->prepare('UPDATE tasks SET "Status"=0 WHERE "ID" = :taskID;');
        $statement->bindParam("taskID", $taskID);

        return $statement->execute();
    }

    function finishSubTask($subtaskID)
    {
        $statement = self::$db->prepare('UPDATE subtasks SET "Status"=1 WHERE "ID" = :subtaskID;');
        $statement->bindParam("subtaskID", $subtaskID);

        return $statement->execute();
    }

    //========================================
    //---------------- update ----------------
    //========================================

    function updateRoadmap($roadmapID, $projectName)
    {
        $statement = self::$db->prepare('UPDATE roadmaps SET "Projectname" = :projectName WHERE "ID"= :roadmapID;');
        $statement->bindParam("roadmapID", $roadmapID);
        $statement->bindParam("projectName", $projectName);

        return $statement->execute();
    }

    function updateMilestone($milestoneID, $versionCode, $versionName, $title, $dueDate, $completionDate, $status)
    {
        $statement = self::$db->prepare('UPDATE milestones SET "VersionCode" = :versionCode, "VersionName" = :versionName, "Title" = :title, "DueDate"=to_date(:dueDate, \'DD.MM.YY\'), "CompletionDate"=to_date(:completionDate, \'DD.MM.YY\'), "Status" = :status WHERE "ID" = :milestoneID;');
        $statement->bindParam("milestoneID", $milestoneID);
        $statement->bindParam("versionCode", $versionCode);
        $statement->bindParam("versionName", $versionName);
        $statement->bindParam("title", $title);
        $statement->bindParam("dueDate", $dueDate);
        $statement->bindParam("completionDate", $completionDate);
        $statement->bindParam("status", $status);

        return $statement->execute();
    }

    function updateTask($taskID, $milestoneID, $title, $description, $status)
    {
        $statement = self::$db->prepare('UPDATE tasks SET "MilestoneID" = :milestoneID, "Title" = :title, "Description" = :description, "Status" = :status WHERE "ID" = :taskID;');
        $statement->bindParam("taskID", $taskID);
        $statement->bindParam("milestoneID", $milestoneID);
        $statement->bindParam("title", $title);
        $statement->bindParam("description", $description);
        $statement->bindParam("status", $status);

        return $statement->execute();
    }

    function updateSubtask($subtaskID, $taskID, $title, $description, $status)
    {
        $statement = self::$db->prepare('UPDATE subtasks SET "TaskID" = :taskID, "Title" = :title, "Description" = :description, "Status" = :status WHERE "ID" = :subtaskID;');
        $statement->bindParam("subtaskID", $subtaskID);
        $statement->bindParam("taskID", $taskID);
        $statement->bindParam("title", $title);
        $statement->bindParam("description", $description);
        $statement->bindParam("status", $status);

        $success = $statement->execute();
        $this->checkParentTask($taskID);

        return $success;
    }

    function checkParentTask($taskID)
    {
        $subTasks = $this->getSubtasks($taskID);
        $counter = 0;
        for($m = 0; $m < sizeof($subTasks); $m++)
        {
            $currentSubTask = $subTasks[$m];
            if ($currentSubTask['Status'] == 1)
            {
                $counter = $counter + 1;
            }
        }

        if($counter == sizeof($subTasks))
        {
            $this->finishTask($taskID);
        }
        else
        {
            $this->reopenTask($taskID);
        }
    }

    function markAllTasksAsDone($milestoneID)
    {
        $tasks = $this->getTasks($milestoneID);
        for($m = 0; $m < sizeof($tasks); $m++)
        {
            $subTasks = $this->getSubtasks($tasks[$m]['ID']);
            for($i = 0; $i < sizeof($subTasks); $i++)
            {
                if($this->finishSubTask($subTasks[$i]["ID"]) == false)
                {
                    return false;
                }
            }

            if($this->finishTask($tasks[$m]['ID']) == false)
            {
                return false;
            }
        }

        return true;
    }

    //========================================
    //----------------- get ------------------
    //========================================

    function getRoadmap($roadmapID)
    {
        $statement = self::$db->prepare('SELECT "Projectname" FROM roadmaps WHERE "ID"=:roadmapID;');
        $statement->bindParam("roadmapID", $roadmapID);
        $statement->execute();

        return $statement->fetch();
    }

    function getRoadmaps()
    {
        $statement = self::$db->prepare('SELECT * FROM roadmaps ORDER BY "ID";');
        $statement->bindParam("roadmapID", $roadmapID);
        $statement->execute();

        return $statement->fetchAll();
    }

    function getMilestones($roadmapID)
    {
        $statement = self::$db->prepare('SELECT * FROM milestones WHERE "RoadmapID"=:roadmapID ORDER BY "VersionCode" DESC;');
        $statement->bindParam("roadmapID", $roadmapID);
        $statement->execute();

        return $statement->fetchAll();
    }

    function getMilestone($milestoneID)
    {
        $statement = self::$db->prepare('SELECT * FROM milestones WHERE "ID"=:milestoneID;');
        $statement->bindParam("milestoneID", $milestoneID);
        $statement->execute();

        return $statement->fetch();
    }

    function getNumberOfOpenMilestones($roadmapID)
    {
        $statement = self::$db->prepare('SELECT COUNT(*) AS "count" FROM milestones WHERE "RoadmapID"=:roadmapID AND "Status" = 0;');
        $statement->bindParam("roadmapID", $roadmapID);
        $statement->execute();

        return $statement->fetch();
    }

    function getTasks($milestoneID)
    {
        $statement = self::$db->prepare('SELECT * FROM tasks WHERE "MilestoneID"=:milestoneID;');
        $statement->bindParam("milestoneID", $milestoneID);
        $statement->execute();

        return $statement->fetchAll();
    }

    function getTask($taskID)
    {
        $statement = self::$db->prepare('SELECT * FROM tasks WHERE "ID"=:taskID;');
        $statement->bindParam("taskID", $taskID);
        $statement->execute();

        return $statement->fetch();
    }

    function getNumberOfOpenTasks($milestoneID)
    {
        $statement = self::$db->prepare('SELECT COUNT(*) AS "count" FROM tasks WHERE "MilestoneID"=:milestoneID AND "Status" = 0;');
        $statement->bindParam("milestoneID", $milestoneID);
        $statement->execute();

        return $statement->fetch();
    }

    function getSubtasks($taskID)
    {
        $statement = self::$db->prepare('SELECT * FROM subtasks WHERE "TaskID"=:taskID;');
        $statement->bindParam("taskID", $taskID);
        $statement->execute();

        return $statement->fetchAll();
    }

    function getSubtask($taskID)
    {
        $statement = self::$db->prepare('SELECT * FROM subtasks WHERE "ID"=:taskID;');
        $statement->bindParam("taskID", $taskID);
        $statement->execute();

        return $statement->fetch();
    }

    function getNumberOfOpenSubtasks($taskID)
    {
        $statement = self::$db->prepare('SELECT COUNT(*) AS "count" FROM subtasks WHERE "TaskID"=:taskID AND "Status" = 0;');
        $statement->bindParam("taskID", $taskID);
        $statement->execute();

        return $statement->fetch();
    }

    function getLatestFinishedMilestone($roadmapID)
    {
        $statement = self::$db->prepare('SELECT * FROM milestones WHERE "RoadmapID"=:roadmapID AND "Status" = 1 ORDER BY "VersionCode" DESC;');
        $statement->bindParam("roadmapID", $roadmapID);
        $statement->execute();

        return $statement->fetchAll();
    }

    //========================================
    //--------------- delete -----------------
    //========================================

    function deleteRoadmap($roadmapID)
    {
        $statement = self::$db->prepare('DELETE FROM roadmaps WHERE "ID"=:roadmapID;');
        $statement->bindParam("roadmapID", $roadmapID);
        $statement->execute();

        return $statement->execute();
    }

    function deleteMilestone($milestoneID)
    {
        $statement = self::$db->prepare('DELETE FROM milestones WHERE "ID"=:milestoneID;');
        $statement->bindParam("milestoneID", $milestoneID);
        $statement->execute();

        return $statement->execute();
    }

    function deleteTask($taskID)
    {
        $statement = self::$db->prepare('DELETE FROM tasks WHERE "ID"=:taskID;');
        $statement->bindParam("taskID", $taskID);
        $statement->execute();

        return $statement->execute();
    }

    function deleteSubtask($subtaskID, $taskID)
    {
        $statement = self::$db->prepare('DELETE FROM subtasks WHERE "ID"=:subtaskID;');
        $statement->bindParam("subtaskID", $subtaskID);
        $success = $statement->execute();

        $this->checkParentTask($taskID);

        return $success;
    }
}