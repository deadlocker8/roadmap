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

if(!isset($_GET['milestoneID']))
{
	header('Location: ../error.php?message=error_param_missing');
	exit;
}

$milestoneID = $_GET['milestoneID'];
if(!is_numeric($milestoneID) || $milestoneID < 1)
{
	header('Location: ../error.php?message=error_param_invalid');
	exit;
}


if(!isset($_GET['edit']))
{
	$_GET['edit'] = "false";

	$ID = 0;

	$db = new DB();
	$db->createTables();
}
else
{
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

	$task = $db->getTask($ID);
	if($task == false)
	{
		header('Location: ../error.php?message=error_task_not_existing');
		exit;
	}
}
?>
<html xmlns="http://www.w3.org/1999/html">
	<head>
		<meta charset="UTF-8"/>
		<?php
		if($_GET['edit'] == "false")
		{
			echo '<title>New Task</title>';
		}
		else
		{
			echo '<title>Edit Task</title>';
		}
		?>
		<!--Import Google Icon Font-->
		<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
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
		<div class="hide" id="edit"><?php echo $_GET['edit'];?></div>
		<div id="main">
			<div class="container">
				<?php
				if($_GET['edit'] == "false")
				{
					echo '<h2 class="center-align" id="headline">New Task</h2>';
				}
				else
				{
					echo '<h2 class="center-align" id="headline">Edit Task</h2>';
				}
				?>

				<div class="row center-align">
					<div class="col s6 m8 offset-m2 l6 offset-l3">
						<div class="input-field col s12">
							<input id="title" name="title" type="text" value="<?php if(isset($task)){echo $task['Title'];}?>">
							<label for="title">Title</label>
						</div>
					</div>
				</div>
				<div class="row center-align">
					<div class="col s6 m8 offset-m2 l6 offset-l3">
						<div class="input-field col s12">
							<input id="description" name="description" type="text" value="<?php if(isset($task)){echo $task['Description'];}?>">
							<label for="description">Description</label>
						</div>
					</div>
				</div>
				<div class="row center-align">
					<div class="col s6 m8 offset-m2 l6 offset-l3">
						<div class="col s12 left-align">
							<input type="checkbox" id="checkbox-done"
							<?php
								if(isset($task))
								{
									if($task['Status'] == "1")
									{
										echo "checked";
									}
								}
							?>
							/>
							<label for="checkbox-done">Done</label>
						</div>
					</div>
				</div>

				<div class="row center-align margin-top">
					<div class="col s12 m8 offset-m2 l6 offset-l3">
						<a class="waves-effect waves-light btn blue darken-3" href="admin-tasks.php?id=<?php echo $milestoneID;?>"><i class="material-icons left">arrow_back</i>Back</a>
						<a class="waves-effect waves-light btn blue darken-3 margin-left button-save-task" data-id="<?php echo $ID;?>" data-milestoneid="<?php echo $milestoneID;?>"><i class="material-icons left">save</i>Save</a>
					</div>
				</div>
			</div>
		</div>
	</body>
</html>