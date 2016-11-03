<!DOCTYPE html>

<?php
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

$milestone = $db->getMilestone($ID);
if($milestone == false)
{
	header('Location: ../error.php?message=error_task_not_existing');
	exit;
}

?>
<html xmlns="http://www.w3.org/1999/html">
<head>
	<meta charset="UTF-8"/>
	<title>Tasks - Adminarea</title>
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
<a class="waves-effect waves-light btn blue darken-3" href="admin-milestones.php?id=<?php echo $milestone['RoadmapID'];?>"><i class="material-icons left">arrow_back</i>Back</a>
<div id="main">
	<div class="container">
		<h2 class="center-align" id="headline"><?php echo $milestone['Title'];?></h2>
		<h4 class="center-align" id="headline">Tasks</h4>

		<div class="row">
			<div class="col s12 m8 offset-m2 l6 offset-l3 center-align">
				<a class="waves-effect waves-light btn blue darken-3" href="admin-edit-task.php?milestoneID=<?php echo $ID;?>"><i
						class="material-icons left">add</i>New</a>
			</div>
		</div>
		<div class="row">
			<div class="col s12 m10 offset-m1 l8 offset-l2">
				<table class="bordered">
					<thead>
					<tr>
						<th data-field="id">ID</th>
						<th data-field="project-name">Title</th>
						<th data-field="project-name">Status</th>
					</tr>
					</thead>

					<tbody>
					<?php
					$tasks = $db->getTasks($ID);

					if($tasks == false)
					{
						echo '<td colspan="6" class="center-align">No Tasks</td>';
						exit;
					}
					else
					{
						for($i = 0; $i < sizeof($tasks); $i++)
						{
							$status = $tasks[$i]['Status'];
							echo '<tr>' .
								'<td>' . $tasks[$i]['ID'] . '</td>' .
								'<td>' . $tasks[$i]['Title'] . '</td>';

							if($status == "0")
							{
								echo '<td><i class="material-icons red-text">build</i></td>';
							}
							else
							{
								echo '<td><i class="material-icons green-text">check</i></td>';
							}

							echo '<td class="right-align">' .
								'<a class="btn-flat no-padding tooltipped" href="admin-edit-task.php?id=' . $tasks[$i]['ID'] . '&milestoneID='. $ID .'&edit=true" data-position="bottom" data-delay="50" data-tooltip="Edit"><i class="material-icons left">edit</i></a>' .
								'<a class="btn-flat button-delete-task no-padding tooltipped" data-id="' . $tasks[$i]['ID'] . '" data-milestoneid="' . $ID . '" data-position="bottom" data-delay="50" data-tooltip="Delete"><i class="material-icons left">delete</i></a>' .
								'<a class="btn-flat no-padding tooltipped" href="admin-subtasks.php?id=' . $tasks[$i]['ID'] . '" data-position="bottom" data-delay="50" data-tooltip="Edit Subtasks"><i class="material-icons left">assignment</i></a>' .
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