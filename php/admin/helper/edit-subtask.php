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

	if(!isset($_POST['task-ID']))
	{
		echo "error-edit";
		exit;
	}


	if(!isset($_POST['title']))
	{
		echo "error-edit";
		exit;
	}

	if(!isset($_POST['description']))
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
		if($db->updateSubtask($_POST['ID'], $_POST['task-ID'], $_POST['title'], $_POST['description'], $_POST['done']) == false)
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
		if($db->insertSubtask($_POST['task-ID'], $_POST['title'], $_POST['description'], $_POST['done']) == false)
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