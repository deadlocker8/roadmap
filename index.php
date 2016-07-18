<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/html">
	<head>
		<meta charset="UTF-8"/>
		<title>Roadmap</title>
		<!--Import Google Icon Font-->
		<link href="http://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
		<!--Import materialize.css-->
		<link type="text/css" rel="stylesheet" href="materialize/css/materialize.min.css"  media="screen,projection"/>
		<link type="text/css" rel="stylesheet" href="css/style.css"/>

		<!--Import jQuery before materialize.js-->
		<script type="text/javascript" src="js/jquery-2.2.4.min.js"></script>
		<script type="text/javascript" src="materialize/js/materialize.min.js"></script>
		<script type="text/javascript" src="js/main.js"></script>

		<!--Let browser know website is optimized for mobile-->
		<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
	</head>

	<body class="grey lighten-3">
		<div id="main">
			<div class="container">
				<h2 class="center-align" id="headline">PlayWall Roadmap</h2>
				<div class="row">
					<div class="col s12 m6">
						<div class="card padding white">
							<div class="card-content">
								<div class="amber lighten-2 center-align margin-bottom">
									<span class="card-title bold">Current Version (v1.5.7)</span>
								</div>
								<div class="white progress-container">
									<div class="progress grey lighten-2 high-progress margin-bottom">
										<div class="determinate green" style="width: 66%"></div>
									</div>
								</div>
								<div class="row">
									<div class="col s6 valign-wrapper">
										<i class="material-icons valign">event</i><span class="valign margin-left">Due by 25.06.16</span>
									</div>
									<div class="col s6 valign-wrapper">
										<i class="material-icons valign">settings</i><span class="valign margin-left">66% Done</span>
									</div>
								</div>
								<ul class="collapsible white" data-collapsible="accordion">
									<li>
										<div class="collapsible-header bold"><i class="material-icons green-text">check</i>Layout</div>
										<div class="collapsible-body"><p>In dieser Version, besteht die Möglichkeit zwischen einem neuen Layout und dem alten Layout für die Kacheln zu wählen.</p></div>
									</li>
									<li>
										<div class="collapsible-header bold"><i class="material-icons green-text">check</i>Play in Background</div>
										<div class="collapsible-body"><p>PlayWall ermöglicht es nun Audio und andere Medien im Hintergrund wiederzugeben, während eine andere Seite offen ist.</p></div>
									</li>
									<li>
										<div class="collapsible-header bold"><i class="material-icons red-text">build</i>Live Mode</div>
										<div class="collapsible-body"><p>Mit dem neuen Livemode ist ein noch einfach die Kontrolle während Veranstaltungen zu behalten.</p></div>
									</li>
								</ul>
							</div>
						</div>
					</div>
					<div class="col s12 m6">
						<div class="card padding white">
							<div class="card-content">
								<div class="grey lighten-2 center-align margin-bottom">
									<span class="card-title bold">Next Version (v1.6.0)</span>
								</div>
								<div class="white progress-container">
									<div class="progress grey lighten-2 high-progress margin-bottom">
										<div class="determinate green" style="width: 0%"></div>
									</div>
								</div>
								<div class="row">
									<div class="col s6 valign-wrapper">
										<i class="material-icons valign">event</i><span class="valign margin-left">&lt;No Due Date&gt;</span>
									</div>
									<div class="col s6 valign-wrapper">
										<i class="material-icons valign">settings</i><span class="valign margin-left">0% Done</span>
									</div>
								</div>
								<ul class="collapsible white" data-collapsible="accordion">
									<li>
										<div class="collapsible-header bold"><i class="material-icons red-text">build</i>Trigger</div>
										<div class="collapsible-body"><p>PlayWall bietet nur die Möglichkeit Kacheln und anderen Einstellungen eventbasiert zu steuern. </p></div>
									</li>
									<li>
										<div class="collapsible-header bold"><i class="material-icons red-text">build</i>Updates</div>
										<div class="collapsible-body"><p>Noch nie war es so einfach Updates zu erhalten. Mit dem neuen Updater können Plugins und das Programm im handumdrehen aktualisiert werden. </p></div>
									</li>
									<li>
										<div class="collapsible-header bold"><i class="material-icons red-text">build</i>Lock</div>
										<div class="collapsible-body"><p>Sichere deine Einstellungen ganz einfach mit nur einem Klick.</p></div>
									</li>
									<li>
										<div class="collapsible-header bold"><i class="material-icons red-text">build</i>Beta Update Kanal</div>
										<div class="collapsible-body"><p>Es ist jetzt möglich, direkt Beta Versionen zu installieren und zu aktualisieren.</p></div>
									</li>
									<li>
										<div class="collapsible-header bold"><i class="material-icons red-text">build</i>Neues Logo</div>
										<div class="collapsible-body"><p>Das Programm hat ein neues Logo erhalten.</p></div>
									</li>
								</ul>
							</div>
						</div>
					</div>
				</div>

				<div class="hide-on-med-and-up center-align">
					<a class="btn-flat no-transform blue-text margin-bottom" id="button-previousVersions1">Show Previous Versions</a>
				</div>

				<div class="hide-on-small-only">
					<a class="btn-flat no-transform blue-text margin-bottom" id="button-previousVersions2">Show Previous Versions</a>
				</div>

				<div class="hide" id="previousVersions">
					<?php include('history.php'); ?>
				</div>

			</div>
		</div>
	</body>
</html>