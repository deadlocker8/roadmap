<?php
include_once('../../database.php');

if($_SERVER['REQUEST_METHOD'] == 'POST')
{
	if(!isset($_POST['edit']))
	{
		echo "error";
		exit;
	}

	if(!isset($_POST['ID']))
	{
		echo "error-edit";
		exit;
	}

	if(!isset($_POST['roadmap-ID']))
	{
		echo "error-edit";
		exit;
	}

	if(!isset($_POST['version-name']))
	{
		echo "error-edit";
		exit;
	}

	if(!isset($_POST['version-code']))
	{
		echo "error-edit";
		exit;
	}

	if(!isset($_POST['title']))
	{
		echo "error-edit";
		exit;
	}

	if(!isset($_POST['due-date']))
	{
		echo "error-edit";
		exit;
	}

	if(!isset($_POST['done-date']))
	{
		echo "error-edit";
		exit;
	}

	if(!isset($_POST['done']))
	{
		echo "error-edit";
		exit;
	}

	$db = new DB();
	$db->createTables();

	if($_POST['edit'] == "true")
	{		
		if($db->updateMilestone($_POST['ID'], $_POST['version-code'], $_POST['version-name'], $_POST['title'], $_POST['due-date'], $_POST['done-date'], $_POST['done']) == false)
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
		if($db->insertMilestone($_POST['roadmap-ID'], $_POST['version-code'], $_POST['version-name'], $_POST['title'], $_POST['due-date'], $_POST['done-date'], $_POST['done']) == false)
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