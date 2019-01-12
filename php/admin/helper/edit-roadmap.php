<?php
include_once('../../database.php');

if($_SERVER['REQUEST_METHOD'] == 'POST')
{
	if(!isset($_POST['edit']))
	{
		echo "error";
		exit;
	}

	if($_POST['edit'] == "true")
	{
		if(!isset($_POST['ID']))
		{
			echo "error-edit";
			exit;
		}

		if(!isset($_POST['project-name']))
		{
			echo "error-edit";
			exit;
		}

		$db = new DB();
		$db->createTables();

		if($db->updateRoadmap($_POST['ID'], $_POST['project-name']) == false)
		{
			echo "error-edit";
			exit;
		}
		else
		{
			echo "success";
			exit;
		}
	}
	else
	{
		if(!isset($_POST['project-name']))
		{
			echo "error-insert";
			exit;
		}

		$db = new DB();
		$db->createTables();

		if($db->insertRoadmap($_POST['project-name']) == false)
		{
			echo "error-insert";
			exit;
		}
		else
		{
			echo "success";
			exit;
		}
	}
}
else
{
	echo "error";
	exit;
}