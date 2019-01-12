<?php
include_once('../../database.php');

if($_SERVER['REQUEST_METHOD'] == 'POST')
{
	if(!isset($_POST['milestoneID']))
	{
		echo "error";
		exit;
	}

	$db = new DB();
	$db->createTables();

    if($db->markAllTasksAsDone($_POST['milestoneID']) == false)
    {
        echo "error";
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
	echo "error";
	exit;
}