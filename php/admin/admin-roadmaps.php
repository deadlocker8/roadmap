<!DOCTYPE html>

<?php
include_once('../getLanguageJSON.php');
include_once('../mysql.php');

$db = new DB();
$db->createTables();
?>
<html xmlns="http://www.w3.org/1999/html">
	<head>
		<meta charset="UTF-8"/>
		<title>Roadmaps - Adminarea</title>
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
				<h2 class="center-align" id="headline">Roadmaps</h2>

				<div class="row">
					<div class="col s12 m8 offset-m2 l6 offset-l3 center-align">
						<a class="waves-effect waves-light btn blue darken-3" href="admin-edit-roadmap.php"><i class="material-icons left">add</i>New</a>
					</div>
				</div>
				<div class="row">
					<div class="col s12 m8 offset-m2 l6 offset-l3">
						<table class="bordered">
							<thead>
							<tr>
								<th data-field="id">ID</th>
								<th data-field="project-name">Project Name</th>
							</tr>
							</thead>

							<tbody>
							<?php
								$roadmaps = $db->getRoadmaps();

								if($roadmaps == false)
								{
									header('Location: error.php?message=error_database_connection');
									exit;
								}
								else
								{
									for($i = 0; $i < sizeof($roadmaps); $i++)
									{
										echo '<tr>'.
												'<td>'.$roadmaps[$i]['ID'].'</td>'.
												'<td>'.$roadmaps[$i]['Projectname'].'</td>'.
												'<td class="right-align">'.
													'<a class="btn-flat" href="admin-edit-roadmap.php?id='.$roadmaps[$i]['ID'].'&edit=true"><i class="material-icons left">edit</i></a>'.
													'<a class="btn-flat button-delete-roadmap" data-id="'.$roadmaps[$i]['ID'].'"><i class="material-icons left">delete</i></a>'.
												'</td>'.
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