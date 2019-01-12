<!DOCTYPE html>

<?php
include_once('../getLanguageJSON.php');
include_once('../database.php');
?>
<html xmlns="http://www.w3.org/1999/html">
	<head>
		<meta charset="UTF-8"/>
		<title>Login</title>

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
		<div id="main">
			<div class="container">
				<h2 class="center-align" id="headline">Login</h2>

				<div class="row center-align">
					<div class="col s10 offset-s1 m6 offset-m3 l4 offset-l4">
						<div class="input-field col s12">
							<input id="password" name="password" type="password">
							<label for="password">Password</label>
						</div>
					</div>
				</div>
				<div class="row center-align margin-top">
					<div class="col s12 m8 offset-m2 l6 offset-l3">
						<a class="waves-effect waves-light btn blue darken-3" href="../index.php"><i class="material-icons left">home</i>Home</a>
						<a class="waves-effect waves-light btn blue darken-3 margin-left button-login"><i class="material-icons left">exit_to_app</i>Login</a>
					</div>
				</div>
			</div>
		</div>
	</body>
</html>