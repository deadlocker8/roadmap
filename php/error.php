<!DOCTYPE html>

<?php
include_once('getLanguageJSON.php');
?>
<html xmlns="http://www.w3.org/1999/html">
	<head>
		<meta charset="UTF-8"/>
		<title>Roadmap</title>
		<!--Import Google Icon Font-->
		<link href="http://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
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
		<main>
			<div class="container">
				<div class="row">
					<div class="s6 offset-s3 center-align margin-top-huge">
						<h5>
							<?php
								if(isset($_GET['message']))
								{
									if($languageJSON->{$_GET['message']})
									{
										echo $languageJSON->{$_GET['message']};
									}
									else
									{
										echo $languageJSON->error_general;
									}
								}
								else
								{
									echo $languageJSON->error_general;
								}
							?>
						</h5>
					</div>
				</div>
			</div>
		</main>
	</body>
</html>