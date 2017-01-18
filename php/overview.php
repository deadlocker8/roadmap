<!DOCTYPE html>

<?php
include_once('getLanguageJSON.php');
include_once('mysql.php');

$db = new DB();
$db->createTables();
?>
<html xmlns="http://www.w3.org/1999/html">
	<head>
		<meta charset="UTF-8"/>
		<title>Roadmaps</title>
		<!--Import Google Icon Font-->
		<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
		<!--Import materialize.css-->
		<link type="text/css" rel="stylesheet" href="../materialize/css/materialize.min.css" media="screen,projection"/>
		<link type="text/css" rel="stylesheet" href="../css/style.css"/>

		<!--Import jQuery before materialize.js-->
		<script type="text/javascript" src="../js/jquery-2.2.4.min.js"></script>
		<script type="text/javascript" src="../materialize/js/materialize.min.js"></script>
		<script type="text/javascript" src="../js/main.js"></script>
		<script type="text/javascript" src="../js/ResizeSensor.js"></script>
		<script type="text/javascript" src="../js/ElementQueries.js"></script>

		<!--Let browser know website is optimized for mobile-->
		<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
	</head>

	<body class="grey lighten-3">
		<a class="btn-flat right" href="admin/login.php">Login</a>
		<div style="clear: both;"></div>
		<div id="main">
			<div class="container">
				<h2 class="center-align" id="headline">All Roadmaps</h2>

				<div class="row">
					<div class="col s12 m10 offset-m1 l6 offset-l3">
						<?php
							$roadmaps = $db->getRoadmaps();

							if($roadmaps == false)
							{
								echo '<h5 class="center-align">no roadmaps available</h5>';
							}
							else
							{
								echo '<div class="collection center-align">';
								for($i = 0; $i < sizeof($roadmaps); $i++)
								{
									echo '<a class="collection-item blue-text" href="index.php?id='.$roadmaps[$i]['ID'].'">'.$roadmaps[$i]['Projectname'].'</a>';
								}
								echo '</div>';
							}
							?>
					 </div>
				</div>
			</div>
		</div>
	</body>
</html>