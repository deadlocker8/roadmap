<?php
include_once('../../mysql.php');

if($_SERVER['REQUEST_METHOD'] == 'POST')
{
	if(!isset($_POST['roadmap_ID']))
	{
		echo "error";
		exit;
	}

	$db = new DB();
	$db->createTables();

	if($db->deleteRoadmap($_POST['roadmap_ID']) == false)
	{
		echo "error2";
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