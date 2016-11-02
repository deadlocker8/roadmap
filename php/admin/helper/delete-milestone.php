<?php
include_once('../../mysql.php');

if($_SERVER['REQUEST_METHOD'] == 'POST')
{
	if(!isset($_POST['milestone_ID']))
	{
		echo "error";
		exit;
	}

	$db = new DB();
	$db->createTables();

	if($db->deleteMilestone($_POST['milestone_ID']) == false)
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