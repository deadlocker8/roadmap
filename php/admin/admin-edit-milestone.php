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

if(!isset($_GET['roadmapID']))
{
	header('Location: ../error.php?message=error_param_missing');
	exit;
}

$roadmapID = $_GET['roadmapID'];
if(!is_numeric($roadmapID) || $roadmapID < 1)
{
	header('Location: ../error.php?message=error_param_invalid');
	exit;
}


if(!isset($_GET['edit']))
{
	$_GET['edit'] = "false";

	$_GET['id'] = 0;

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

	$milestone = $db->getMilestone($ID);
	if($milestone == false)
	{
		header('Location: ../error.php?message=error_milestone_not_existing');
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
			echo '<title>New Milestone</title>';
		}
		else
		{
			echo '<title>Edit Milestone</title>';
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
					echo '<h2 class="center-align" id="headline">New Milestone</h2>';
				}
				else
				{
					echo '<h2 class="center-align" id="headline">Edit Milestone</h2>';
				}
				?>

				<div class="row center-align">
					<div class="col s6 m4 offset-m2 l3 offset-l3">
						<div class="input-field col s12">
							<input id="version-code" name="version-code" type="text" value="<?php if(isset($milestone)){echo $milestone["VersionCode"];}?>">
							<label for="version-code">Version Code</label>
						</div>
					</div>
					<div class="col s6 m4 l3">
						<div class="input-field col s12">
							<input id="version-name" name="version-name" type="text" value="<?php if(isset($milestone)){ echo $milestone['VersionName'];}?>">
							<label for="version-name">Version Name</label>
						</div>
					</div>
				</div>
				<div class="row center-align">
					<div class="col s12 m8 offset-m2 l6 offset-l3">
						<div class="input-field col s12">
							<input id="title" name="title" type="text" value="<?php if(isset($milestone)){echo $milestone['Title'];}?>">
							<label for="title">Title</label>
						</div>
					</div>
				</div>
				<div class="row center-align">
					<div class="col s12 m8 offset-m2 l6 offset-l3">
						<div class="col s12 left-align">
							<label for="due-date" style="font-size: 1rem;">Due Date</label>
							<?php
								if(isset($milestone))
								{
									$dueDate = $milestone['DueDate'];
									$dueDate = date('d.m.Y', strtotime($dueDate));
									if($dueDate == "01.01.2000")
									{
										$dueDate = "";
									}
								}
								else
								{
									$dueDate = "";
								}
							?>
							<input type="date" class="datepicker" id="due-date" value="<?php echo $dueDate;?>">
						</div>
					</div>
				</div>
				<div class="row center-align">
					<div class="col s12 m8 offset-m2 l6 offset-l3">
						<div class="col s12 left-align">
							<input type="checkbox" id="checkbox-done"
							<?php
								if(isset($milestone))
								{
									if($milestone['Status'] == "1")
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

				<div class="row center-align
				<?php
				if(isset($milestone))
				{
					if($milestone['Status'] != "1")
					{
						echo "hide";
					}
				}
				else
				{
					echo "hide";
				}
				?>
				" id="row-done-date">
					<div class="col s12 m8 offset-m2 l6 offset-l3">
						<div class="col s12 left-align">
							<label for="done-date" style="font-size: 1rem;">Completion Date</label>
							<?php
							if(isset($milestone))
							{
								$doneDate = $milestone['CompletionDate'];
								$doneDate = date('d.m.Y', strtotime($doneDate));
								if($doneDate == "01.01.2000")
								{
									$doneDate = "";
								}
							}
							else
							{
								$doneDate = "";
							}
							?>
							<input type="date" class="datepicker" id="done-date" value="<?php echo $doneDate;?>">
						</div>
					</div>
				</div>

				<div class="row center-align margin-top">
					<div class="col s12 m8 offset-m2 l6 offset-l3">
						<a class="waves-effect waves-light btn blue darken-3" href="admin-milestones.php?id=<?php echo $roadmapID ;?>"><i class="material-icons left">arrow_back</i>Back</a>
						<a class="waves-effect waves-light btn blue darken-3 margin-left button-save-milestone" data-id="<?php echo $ID;?>" data-roadmapid="<?php echo $roadmapID;?>"><i class="material-icons left">save</i>Save</a>
					</div>
				</div>
			</div>
		</div>
	</body>
</html>