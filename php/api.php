<?php
include_once('database.php');

$result = new stdClass();;
if(!isset($_GET['id']))
{
    $result->response = "Invalid Parameters";
	echo json_encode($result);
	exit;
}

$ID = $_GET['id'];
if(!is_numeric($ID) || $ID < 1)
{
    $result->response = "Invalid Parameters";
    echo json_encode($result);
    exit;
}

$db = new DB();
$db->createTables();

$milestone = $db->getLatestFinishedMilestone($ID)[0];
if($milestone == false)
{
    $result->response = "Request Error";
    echo json_encode($result);
    exit;
}
else
{
    $params = array('versionName' => $milestone['VersionName'], 'date' => $milestone['CompletionDate']);
    $result->response = $params;
    echo json_encode($result);
    exit;
}