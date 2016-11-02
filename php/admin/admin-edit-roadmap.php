<!DOCTYPE html>

<?php
include_once('../getLanguageJSON.php');
include_once('../mysql.php');

if(!isset($_GET['edit']))
{
	$_GET['edit'] = "false";

	$_GET['id'] = 0;

	$db = new DB();
	$db->createTables();

	$projectName = '';
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

	$projectName = $db->getRoadmap($ID);
	if($projectName == false)
	{
		header('Location: ../error.php?message=error_roadmap_not_existing');
		exit;
	}
	$projectName = $projectName["Projectname"];
}
?>
<html xmlns="http://www.w3.org/1999/html">
	<head>
		<meta charset="UTF-8"/>
		<?php
		if($_GET['edit'] == "false")
		{
			echo '<title>New Roadmap</title>';
		}
		else
		{
			echo '<title>Edit Roadmap</title>';
		}
		?>
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
		<div id="main">
			<div class="container">
				<?php
				if($_GET['edit'] == "false")
				{
					echo '<h2 class="center-align" id="headline">New Roadmap</h2>';
				}
				else
				{
					echo '<h2 class="center-align" id="headline">Edit Roadmap</h2>';
				}
				?>

				<div class="row center-align">
					<div class="col s12 m8 offset-m2 l6 offset-l3">
						<div class="input-field col s12">
							<input id="project-name" name="project-name" type="text" value="<?php echo $projectName;?>">
							<label for="project-name">Project Name</label>
						</div>
					</div>
				</div>
				<div class="row center-align margin-top">
					<div class="col s12 m8 offset-m2 l6 offset-l3">
						<a class="waves-effect waves-light btn blue darken-3" href="admin-roadmaps.php"><i class="material-icons left">arrow_back</i>Back</a>
						<a class="waves-effect waves-light btn blue darken-3 margin-left button-save-roadmap" data-id="<?php echo $_GET['id'];?>"><i class="material-icons left">save</i>Save</a>
					</div>
				</div>
			</div>
		</div>
	</body>
</html>