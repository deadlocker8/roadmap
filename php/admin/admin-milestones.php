<!DOCTYPE html>

<?php
if(!isset($_SESSION))
{
	session_start();
}
if(!isset($_SESSION['loggedIn']))
{
	header('Location: login.php');
}

include_once('../getLanguageJSON.php');
include_once('../mysql.php');

if(!isset($_GET['id']))
{
	header('Location: ../error.php?message=error_param_missing');
	exit;
}

$ID = $_GET['id'];
if(!is_numeric($ID) || $ID < 1)
{
	header('Location: ../error.php?message=error_param_invalid');
	exit;
}

$db = new DB();
$db->createTables();

$projectName = $db->getRoadmap($ID);
if($projectName == false)
{
	header('Location: ../error.php?message=error_roadmap_not_existing');
	exit;
}
$projectName = $projectName["Projectname"];

?>
<html xmlns="http://www.w3.org/1999/html">
<head>
	<meta charset="UTF-8"/>
	<title>Milestones - Adminarea</title>
	<!--Import Google Icon Font-->
	<link href="http://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
	<!--Import materialize.css-->
	<link type="text/css" rel="stylesheet" href="../../materialize/css/materialize.min.css" media="screen,projection"/>
	<link type="text/css" rel="stylesheet" href="../../css/style.css"/>

	<!--Import jQuery before materialize.js-->
	<script type="text/javascript" src="../../js/jquery-2.2.4.min.js"></script>
	<script type="text/javascript" src="../../materialize/js/materialize.min.js"></script>
	<script type="text/javascript" src="../../js/main.js"></script>
	<script type="text/javascript" src="../../js/ResizeSensor.js"></script>
	<script type="text/javascript" src="../../js/ElementQueries.js"></script>

	<!--Let browser know website is optimized for mobile-->
	<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
</head>

<body class="grey lighten-3">
<a class="waves-effect waves-light btn blue darken-3" href="admin-roadmaps.php"><i class="material-icons left">arrow_back</i>Back</a>
<a class="waves-effect waves-light btn blue darken-3 right" href="logout.php"><i class="material-icons left">lock</i>Logout</a>
<div id="main">
	<div class="container">
		<h2 class="center-align" id="headline"><?php echo $projectName;?></h2>
		<h4 class="center-align" id="headline">Milestones</h4>

		<div class="row">
			<div class="col s12 m8 offset-m2 l6 offset-l3 center-align">
				<a class="waves-effect waves-light btn blue darken-3" href="admin-edit-milestone.php?roadmapID=<?php echo $ID;?>"><i
						class="material-icons left">add</i>New</a>
			</div>
		</div>
		<div class="row">
			<div class="col s12 m12 l12">
				<table class="bordered">
					<thead>
					<tr>
						<th data-field="id">Version Code</th>
						<th data-field="project-name">Version Name</th>
						<th data-field="project-name">Title</th>
						<th data-field="project-name">Due Date</th>
						<th data-field="project-name">Completion Date</th>
						<th data-field="project-name">Status</th>
					</tr>
					</thead>

					<tbody>
					<?php
					$milestones = $db->getMilestones($ID);

					if($milestones == false)
					{
						echo '<td colspan="6" class="center-align">No Milestones</td>';
						exit;
					}
					else
					{
						for($i = 0; $i < sizeof($milestones); $i++)
						{
							$status = $milestones[$i]['Status'];
							$dueDate = $milestones[$i]['DueDate'];
							$dueDate = date('d.m.Y', strtotime($dueDate));
							if($dueDate == "01.01.2001")
							{
								$dueDate = "";
							}

							$doneDate = $milestones[$i]['CompletionDate'];
							$doneDate = date('d.m.Y', strtotime($doneDate));
							if($doneDate == "01.01.2001")
							{
								$doneDate = "";
							}

							echo '<tr>' .
								'<td>' . $milestones[$i]['VersionCode'] . '</td>' .
								'<td>' . $milestones[$i]['VersionName'] . '</td>' .
								'<td>' . $milestones[$i]['Title'] . '</td>' .
								'<td>' . $dueDate . '</td>' .
								'<td>' . $doneDate . '</td>';

							if($status == "0")
							{
								echo '<td><i class="material-icons red-text">build</i></td>';
							}
							else
							{
								echo '<td><i class="material-icons green-text">check</i></td>';
							}

							echo '<td class="right-align">' .
								'<a class="btn-flat no-padding tooltipped" href="admin-edit-milestone.php?id=' . $milestones[$i]['ID'] . '&roadmapID='. $ID .'&edit=true" data-position="bottom" data-delay="50" data-tooltip="Edit"><i class="material-icons left">edit</i></a><br>' .
								'<a class="btn-flat button-delete-milestone no-padding tooltipped" data-id="' . $milestones[$i]['ID'] . '" data-roadmapid="' . $ID . '" data-position="bottom" data-delay="50" data-tooltip="Delete"><i class="material-icons left">delete</i></a><br>' .
								'<a class="btn-flat no-padding tooltipped" href="admin-tasks.php?id=' . $milestones[$i]['ID'] . '" data-position="bottom" data-delay="50" data-tooltip="Edit Tasks"><i class="material-icons left">assignment</i></a>' .
								'</td>' .
								'</tr>';
						}
					}
					?>
					</tbody>
				</table>
			</div>
		</div>
	</div>
</div>
</body>
</html>