<?php

class DB
{
	private static $db;

	function __construct()
	{
		try
		{
			self::$db = new PDO(
				"mysql:host=localhost;dbname=roadmap",
				"root",
				"",
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
		$statement = self::$db->prepare("CREATE TABLE IF NOT EXISTS `roadmaps` ( `ID` int(10) unsigned NOT NULL AUTO_INCREMENT, `Projectname` text COLLATE utf8_general_ci NOT NULL, PRIMARY KEY (`ID`))ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci AUTO_INCREMENT=1;");
		$statement->execute();

		$statement = self::$db->prepare("CREATE TABLE IF NOT EXISTS `milestones` (".
			"`ID` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,".
			"`RoadmapID` int(10) UNSIGNED NOT NULL,".
			"`VersionCode` int(10) UNSIGNED NOT NULL,".
			"`VersionName` text COLLATE utf8_general_ci NOT NULL,".
			"`Title` text COLLATE utf8_general_ci NOT NULL,".
			"`DueDate` date NOT NULL,".
			"`CompletionDate` date NOT NULL,".
			"`Status` int(11) NOT NULL,".
			"PRIMARY KEY (`ID`)".
			") ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci AUTO_INCREMENT=1;");
		$statement->execute();

		$statement = self::$db->prepare("CREATE TABLE IF NOT EXISTS `tasks` (".
			"`ID` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,".
			"`MilestoneID` int(10) UNSIGNED NOT NULL,".
			"`Title` text CHARACTER SET utf8 NOT NULL,".
			"`Description` text CHARACTER SET utf8 NOT NULL,".
			"`Status` int(11) NOT NULL,".
			"PRIMARY KEY (`ID`)".
			") ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci AUTO_INCREMENT=1;");
		$statement->execute();

		$statement = self::$db->prepare("CREATE TABLE IF NOT EXISTS `subtasks` (".
			"`ID` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,".
			"`TaskID` int(10) UNSIGNED NOT NULL,".
			"`Title` text CHARACTER SET utf8 NOT NULL,".
			"`Description` text CHARACTER SET utf8 NOT NULL,".
			"`Status` int(11) NOT NULL,".
			"PRIMARY KEY (`ID`)".
			") ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci AUTO_INCREMENT=1;");
		$statement->execute();
	}

	//========================================
	//---------------- insert ----------------
	//========================================

	function insertRoadmap($projectName)
	{
		$statement = self::$db->prepare("INSERT INTO roadmaps VALUES('', :projectName);");
		$statement->bindParam("projectName", $projectName);

		return $statement->execute();
	}

	function insertMilestone($roadmapID, $versionCode, $versionName, $title, $dueDate)
	{
		$completionDate = "2000-01-01";
		$status = "0";
		$statement = self::$db->prepare("INSERT INTO milestones VALUES('', :roadmapID, :versionCode, :versionName, :title, :dueDate, :completionDate, :status);");
		$statement->bindParam("roadmapID", $roadmapID);
		$statement->bindParam("versionCode", $versionCode);
		$statement->bindParam("versionName", $versionName);
		$statement->bindParam("title", $title);
		$statement->bindParam("dueDate", $dueDate);
		$statement->bindParam("completionDate", $completionDate);
		$statement->bindParam("status", $status);

		return $statement->execute();
	}

	function insertTask($milestoneID, $title, $description)
	{
		$status = "0";
		$statement = self::$db->prepare("INSERT INTO tasks VALUES('', :milestoneID, :title, :description, :status);");
		$statement->bindParam("milestoneID", $milestoneID);
		$statement->bindParam("title", $title);
		$statement->bindParam("description", $description);
		$statement->bindParam("status", $status);

		return $statement->execute();
	}

	function insertSubtask($taskID, $title, $description)
	{
		$status = "0";
		$statement = self::$db->prepare("INSERT INTO subtasks VALUES('', :taskID, :title, :description, :status);");
		$statement->bindParam("taskID", $taskID);
		$statement->bindParam("title", $title);
		$statement->bindParam("description", $description);
		$statement->bindParam("status", $status);

		return $statement->execute();
	}

	//========================================
	//---------------- finish ----------------
	//========================================

	function finishMilestone($milestoneID)
	{
		$statement = self::$db->prepare("UPDATE milestones SET status='1' WHERE ID = :milestoneID;");
		$statement->bindParam("milestoneID", $milestoneID);

		return $statement->execute();
	}

	function finishTask($taskID)
	{
		$statement = self::$db->prepare("UPDATE tasks SET status='1' WHERE ID = :taskID;");
		$statement->bindParam("taskID", $taskID);

		return $statement->execute();
	}

	function finishSubTask($subtaskID)
	{
		$statement = self::$db->prepare("UPDATE subtasks SET status='1' WHERE ID = :subtaskID;");
		$statement->bindParam("subtaskID", $subtaskID);

		return $statement->execute();
	}

	//========================================
	//---------------- update ----------------
	//========================================

	function updateRoadmap($roadmapID, $projectName)
	{
		$statement = self::$db->prepare("UPDATE roadmaps SET Projectname = :projectName WHERE ID = :roadmapID;");
		$statement->bindParam("roadmapID", $roadmapID);
		$statement->bindParam("projectName", $projectName);

		return $statement->execute();
	}

	function updateMilestone($milestoneID, $roadmapID, $versionCode, $versionName, $title, $dueDate, $completionDate, $status)
	{
		$statement = self::$db->prepare("UPDATE milestones SET RoadmapID = :roadmapID, VersionCode = :versionCode, VersionName = :versionName, Title = :title, DueDate = :dueDate, CompletionDate = :completionDate, Status = :status WHERE ID = :milestoneID;");
		$statement->bindParam("milestoneID", $milestoneID);
		$statement->bindParam("roadmapID", $roadmapID);
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
		$statement = self::$db->prepare("UPDATE tasks SET MilestoneID = :milestoneID, Title = :title, Description = :description, Status = :status WHERE ID = :taskID;");
		$statement->bindParam("taskID", $taskID);
		$statement->bindParam("milestoneID", $milestoneID);
		$statement->bindParam("title", $title);
		$statement->bindParam("description", $description);
		$statement->bindParam("status", $status);

		return $statement->execute();
	}

	function updateSubtask($subtaskID, $taskID, $title, $description, $status)
	{
		$statement = self::$db->prepare("UPDATE subtasks SET TaskID = :taskID, Title = :title, Description = :description, Status = :status WHERE ID = :subtaskID;");
		$statement->bindParam("subtaskID", $subtaskID);
		$statement->bindParam("taskID", $taskID);
		$statement->bindParam("milestoneID", $milestoneID);
		$statement->bindParam("title", $title);
		$statement->bindParam("description", $description);
		$statement->bindParam("status", $status);

		return $statement->execute();
	}

	//========================================
	//----------------- get ------------------
	//========================================

	function getRoadmap($roadmapID)
	{
		$statement = self::$db->prepare("SELECT Projectname FROM roadmaps WHERE roadmaps.ID=:roadmapID;");
		$statement->bindParam("roadmapID", $roadmapID);
		$statement->execute();

		return $statement->fetch();
	}

	function getRoadmaps()
	{
		$statement = self::$db->prepare("SELECT * FROM roadmaps ORDER BY ID;");
		$statement->bindParam("roadmapID", $roadmapID);
		$statement->execute();

		return $statement->fetchAll();
	}

	function getMilestones($roadmapID)
	{
		$statement = self::$db->prepare("SELECT * FROM milestones WHERE milestones.roadmapID=:roadmapID ORDER BY VersionCode DESC;");
		$statement->bindParam("roadmapID", $roadmapID);
		$statement->execute();

		return $statement->fetchAll();
	}

	function getNumberOfOpenMilestones($roadmapID)
	{
		$statement = self::$db->prepare("SELECT COUNT(*) AS 'count' FROM milestones WHERE milestones.roadmapID=:roadmapID AND status = '0';");
		$statement->bindParam("roadmapID", $roadmapID);
		$statement->execute();

		return $statement->fetch();
	}

	function getTasks($milestoneID)
	{
		$statement = self::$db->prepare("SELECT * FROM tasks WHERE tasks.milestoneID=:milestoneID;");
		$statement->bindParam("milestoneID", $milestoneID);
		$statement->execute();

		return $statement->fetchAll();
	}

	function getNumberOfOpenTasks($milestoneID)
	{
		$statement = self::$db->prepare("SELECT COUNT(*) AS 'count' FROM tasks WHERE tasks.MilestoneID=:milestoneID AND status = '0';");
		$statement->bindParam("milestoneID", $milestoneID);
		$statement->execute();

		return $statement->fetch();
	}

	function getSubtasks($taskID)
	{
		$statement = self::$db->prepare("SELECT * FROM subtasks WHERE subtasks.taskID=:taskID;");
		$statement->bindParam("taskID", $taskID);
		$statement->execute();

		return $statement->fetchAll();
	}

	function getNumberOfOpenSubtasks($taskID)
	{
		$statement = self::$db->prepare("SELECT COUNT(*) AS 'count' FROM subtasks WHERE subtasks.TaskID=:taskID AND status = '0';");
		$statement->bindParam("taskID", $taskID);
		$statement->execute();

		return $statement->fetch();
	}

	//========================================
	//--------------- delete -----------------
	//========================================

	function deleteRoadmap($roadmapID)
	{
		$statement = self::$db->prepare("DELETE FROM roadmaps WHERE roadmaps.ID=:roadmapID;");
		$statement->bindParam("roadmapID", $roadmapID);
		$statement->execute();

		return $statement->execute();
	}

	function deleteMilestone($milestoneID)
	{
		$statement = self::$db->prepare("DELETE FROM milestones WHERE milestones.ID=:milestoneID;");
		$statement->bindParam("milestoneID", $milestoneID);
		$statement->execute();

		return $statement->execute();
	}

	function deleteTask($taskID)
	{
		$statement = self::$db->prepare("DELETE FROM tasks WHERE tasks.ID=:taskID;");
		$statement->bindParam("taskID", $taskID);
		$statement->execute();

		return $statement->execute();
	}

	function deleteSubtask($subtaskID)
	{
		$statement = self::$db->prepare("DELETE FROM subtasks WHERE subtasks.ID=:subtaskID;");
		$statement->bindParam("subtaskID", $subtaskID);
		$statement->execute();

		return $statement->execute();
	}
}