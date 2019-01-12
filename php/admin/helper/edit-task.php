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

	if(!isset($_POST['milestone-ID']))
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
		if($db->updateTask($_POST['ID'], $_POST['milestone-ID'], $_POST['title'], $_POST['description'], $_POST['done']) == false)
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
		if($db->insertTask($_POST['milestone-ID'], $_POST['title'], $_POST['description'], $_POST['done']) == false)
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