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
		<div id="main">
			<div class="container">
				<h2 class="center-align" id="headline">PlayWall Roadmap</h2>
				<div class="row">
					<div class="col s12">
						<div class="row">
							<div class="col s1 m2 l2 offset-m1 offset-l1 no-padding">
								<div class="hide-on-small-only trainmap">
									<div class="train-circle train-circle-light"></div>
									<div class="train-line dotted"></div>
									<div class="train-circle blue"></div>
									<div class="train-line"></div>
									<div class="train-circle blue"></div>
									<div class="train-line"></div>
									<div class="train-circle blue"></div>
									<div class="train-line"></div>
									<div class="train-circle blue"></div>
								</div>
								<div class="hide-on-med-and-up trainmap-small">
									<div class="train-circle train-circle-light train-circle-small"></div>
									<div class="train-line dotted-small train-line-small"></div>
									<div class="train-circle blue train-circle-small"></div>
									<div class="train-line train-line-small"></div>
									<div class="train-circle blue train-circle-small"></div>
									<div class="train-line train-line-small"></div>
									<div class="train-circle blue train-circle-small"></div>
									<div class="train-line train-line-small"></div>
									<div class="train-circle blue train-circle-small"></div>
								</div>
							</div>
						<div class="col s11 m7 l6">
							<div class="card padding white milestone">
								<div class="card-content">
									<div class="blue lighten-2 center-align milestone-title">
										<span class="card-title bold padding-left-and-right truncate">v1.6.0 - Next Version</span>
									</div>
									<div class="milestone-content margin-top init-as-expanded">
										<div class="white progress-container">
											<div class="progress grey lighten-2 high-progress margin-bottom">
												<div class="determinate green" style="width: 40%"></div>
											</div>
										</div>
										<div class="row">
											<div class="col s6 valign-wrapper">
												<i class="material-icons valign">event</i><span class="valign margin-left"><?php echo $languageJSON->due_by?> 25.06.16</span>
											</div>
											<div class="col s6 valign-wrapper">
												<i class="material-icons valign">settings</i><span class="valign margin-left">40% <?php echo $languageJSON->done?></span>
											</div>
										</div>
										<ul class="collapsible white" data-collapsible="accordion">
											<li>
												<div class="collapsible-header bold"><i class="material-icons red-text">build</i>Layout<span class="right">1/3</span></div>
												<div class="collapsible-body">

													<ul class="collapsible white margin-left-and-right no-shadow margin-top-and-bottom" data-collapsible="accordion">
														<li>
															<div class="collapsible-header bold"><span class="left">1</span><i class="material-icons green-text margin-left">check</i>Layout Einstellungen</div>
															<div class="collapsible-body"><p>PlayWall ermöglicht es nun Audio und andere Medien im Hintergrund wiederzugeben, während eine andere Seite offen ist.</p></div>
														</li>
														<li>
															<div class="collapsible-header bold"><span class="left">2</span><i class="material-icons red-text margin-left">build</i>Layout Cards</div>
															<div class="collapsible-body"><p>PlayWall ermöglicht es nun Audio und andere Medien im Hintergrund wiederzugeben, während eine andere Seite offen ist.</p></div>
														</li>
														<li>
															<div class="collapsible-header bold"><span class="left">3</span><i class="material-icons red-text margin-left">build</i>Layout Equalizer</div>
															<div class="collapsible-body"><p>PlayWall ermöglicht es nun Audio und andere Medien im Hintergrund wiederzugeben, während eine andere Seite offen ist.</p></div>
														</li>
													</ul>

												</div>
											</li>
											<li>
												<div class="collapsible-header bold"><i class="material-icons green-text">check</i>Live Mode</div>
												<div class="collapsible-body"><p>Mit dem neuen Livemode ist ein noch einfach die Kontrolle während Veranstaltungen zu behalten.</p></div>
											</li>
											<li>
												<div class="collapsible-header bold"><i class="material-icons red-text">build</i>Trigger</div>
												<div class="collapsible-body"><p>Mit dem neuen Livemode ist ein noch einfach die Kontrolle während Veranstaltungen zu behalten.</p></div>
											</li>
										</ul>
									</div>
								</div>
							</div>


							<div class="card padding white milestone">
								<div class="card-content">
									<div class="amber lighten-2 center-align milestone-title">
										<span class="card-title bold padding-left-and-right truncate">v1.5.7 - Current Version</span>
									</div>
									<div class="milestone-content margin-top init-as-expanded">
										<div class="row">
											<div class="col s6 valign-wrapper">
												<i class="material-icons valign">event</i><span class="valign margin-left"><?php echo $languageJSON->due_by?> 25.06.16</span>
											</div>
											<div class="col s6 valign-wrapper">
												<i class="material-icons valign">event</i><span class="valign margin-left"><?php echo $languageJSON->done_at?> 25.06.16</span>
											</div>
										</div>
										<ul class="collapsible white" data-collapsible="accordion">
											<li>
												<div class="collapsible-header bold"><i class="material-icons green-text">check</i>Play in Background</div>
												<div class="collapsible-body"><p>PlayWall ermöglicht es nun Audio und andere Medien im Hintergrund wiederzugeben, während eine andere Seite offen ist.</p></div>
											</li>
											<li>
												<div class="collapsible-header bold"><i class="material-icons green-text">check</i>Live Mode</div>
												<div class="collapsible-body"><p>Mit dem neuen Livemode ist ein noch einfach die Kontrolle während Veranstaltungen zu behalten.</p></div>
											</li>
										</ul>
									</div>
								</div>
							</div>

							<div class="card padding white milestone">
								<div class="card-content">
									<div class="grey lighten-2 center-align milestone-title">
										<span class="card-title bold padding-left-and-right truncate">v1.3.0 - Third Version</span>
									</div>
									<div class="milestone-content margin-top">
										<div class="row">
											<div class="col s6 valign-wrapper">
												<i class="material-icons valign">event</i><span class="valign margin-left"><?php echo $languageJSON->due_by?> 25.06.16</span>
											</div>
											<div class="col s6 valign-wrapper">
												<i class="material-icons valign">event</i><span class="valign margin-left"><?php echo $languageJSON->done_at?> 25.06.16</span>
											</div>
										</div>
										<ul class="collapsible white" data-collapsible="accordion">
											<li>
												<div class="collapsible-header bold"><i class="material-icons green-text">check</i>Play in Background</div>
												<div class="collapsible-body"><p>PlayWall ermöglicht es nun Audio und andere Medien im Hintergrund wiederzugeben, während eine andere Seite offen ist.</p></div>
											</li>
											<li>
												<div class="collapsible-header bold"><i class="material-icons green-text">check</i>Live Mode</div>
												<div class="collapsible-body"><p>Mit dem neuen Livemode ist ein noch einfach die Kontrolle während Veranstaltungen zu behalten.</p></div>
											</li>
											<li>
												<div class="collapsible-header bold"><i class="material-icons green-text">check</i>Live Mode</div>
												<div class="collapsible-body"><p>Mit dem neuen Livemode ist ein noch einfach die Kontrolle während Veranstaltungen zu behalten.</p></div>
											</li>
											<li>
												<div class="collapsible-header bold"><i class="material-icons green-text">check</i>Live Mode</div>
												<div class="collapsible-body"><p>Mit dem neuen Livemode ist ein noch einfach die Kontrolle während Veranstaltungen zu behalten.</p></div>
											</li>
											<li>
												<div class="collapsible-header bold"><i class="material-icons green-text">check</i>Live Mode</div>
												<div class="collapsible-body"><p>Mit dem neuen Livemode ist ein noch einfach die Kontrolle während Veranstaltungen zu behalten.</p></div>
											</li>
											<li>
												<div class="collapsible-header bold"><i class="material-icons green-text">check</i>Live Mode</div>
												<div class="collapsible-body"><p>Mit dem neuen Livemode ist ein noch einfach die Kontrolle während Veranstaltungen zu behalten.</p></div>
											</li>

										</ul>
									</div>
								</div>
							</div>

							<div class="card padding white milestone">
								<div class="card-content">
									<div class="grey lighten-2 center-align milestone-title">
										<span class="card-title bold padding-left-and-right truncate">v1.1.0 - Second Version</span>
									</div>
									<div class="milestone-content margin-top">
										<div class="row">
											<div class="col s6 valign-wrapper">
												<i class="material-icons valign">event</i><span class="valign margin-left"><?php echo $languageJSON->due_by?> 25.06.16</span>
											</div>
											<div class="col s6 valign-wrapper">
												<i class="material-icons valign">event</i><span class="valign margin-left"><?php echo $languageJSON->done_at?> 25.06.16</span>
											</div>
										</div>
										<ul class="collapsible white" data-collapsible="accordion">
											<li>
												<div class="collapsible-header bold"><i class="material-icons green-text">check</i>Play in Background</div>
												<div class="collapsible-body"><p>PlayWall ermöglicht es nun Audio und andere Medien im Hintergrund wiederzugeben, während eine andere Seite offen ist.</p></div>
											</li>
											<li>
												<div class="collapsible-header bold"><i class="material-icons green-text">check</i>Live Mode</div>
												<div class="collapsible-body"><p>Mit dem neuen Livemode ist ein noch einfach die Kontrolle während Veranstaltungen zu behalten.</p></div>
											</li>
											<li>
												<div class="collapsible-header bold"><i class="material-icons green-text">check</i>Live Mode</div>
												<div class="collapsible-body"><p>Mit dem neuen Livemode ist ein noch einfach die Kontrolle während Veranstaltungen zu behalten.</p></div>
											</li>
											<li>
												<div class="collapsible-header bold"><i class="material-icons green-text">check</i>Live Mode</div>
												<div class="collapsible-body"><p>Mit dem neuen Livemode ist ein noch einfach die Kontrolle während Veranstaltungen zu behalten.</p></div>
											</li>
											<li>
												<div class="collapsible-header bold"><i class="material-icons green-text">check</i>Live Mode</div>
												<div class="collapsible-body"><p>Mit dem neuen Livemode ist ein noch einfach die Kontrolle während Veranstaltungen zu behalten.</p></div>
											</li>
											<li>
												<div class="collapsible-header bold"><i class="material-icons green-text">check</i>Live Mode</div>
												<div class="collapsible-body"><p>Mit dem neuen Livemode ist ein noch einfach die Kontrolle während Veranstaltungen zu behalten.</p></div>
											</li>

										</ul>
									</div>
								</div>
							</div>

							<div class="card padding white milestone">
								<div class="card-content">
									<div class="grey lighten-2 center-align milestone-title">
										<span class="card-title bold padding-left-and-right truncate">v1.0.0 - First Version</span>
									</div>
									<div class="milestone-content margin-top">
										<div class="row">
											<div class="col s6 valign-wrapper">
												<i class="material-icons valign">event</i><span class="valign margin-left"><?php echo $languageJSON->due_by?> 25.06.16</span>
											</div>
											<div class="col s6 valign-wrapper">
												<i class="material-icons valign">event</i><span class="valign margin-left"><?php echo $languageJSON->done_at?> 25.06.16</span>
											</div>
										</div>
										<ul class="collapsible white" data-collapsible="accordion">
											<li>
												<div class="collapsible-header bold"><i class="material-icons green-text">check</i>Play in Background</div>
												<div class="collapsible-body"><p>PlayWall ermöglicht es nun Audio und andere Medien im Hintergrund wiederzugeben, während eine andere Seite offen ist.</p></div>
											</li>
											<li>
												<div class="collapsible-header bold"><i class="material-icons green-text">check</i>Live Mode</div>
												<div class="collapsible-body"><p>Mit dem neuen Livemode ist ein noch einfach die Kontrolle während Veranstaltungen zu behalten.</p></div>
											</li>
											<li>
												<div class="collapsible-header bold"><i class="material-icons green-text">check</i>Live Mode</div>
												<div class="collapsible-body"><p>Mit dem neuen Livemode ist ein noch einfach die Kontrolle während Veranstaltungen zu behalten.</p></div>
											</li>
											<li>
												<div class="collapsible-header bold"><i class="material-icons green-text">check</i>Live Mode</div>
												<div class="collapsible-body"><p>Mit dem neuen Livemode ist ein noch einfach die Kontrolle während Veranstaltungen zu behalten.</p></div>
											</li>
											<li>
												<div class="collapsible-header bold"><i class="material-icons green-text">check</i>Live Mode</div>
												<div class="collapsible-body"><p>Mit dem neuen Livemode ist ein noch einfach die Kontrolle während Veranstaltungen zu behalten.</p></div>
											</li>
											<li>
												<div class="collapsible-header bold"><i class="material-icons green-text">check</i>Live Mode</div>
												<div class="collapsible-body"><p>Mit dem neuen Livemode ist ein noch einfach die Kontrolle während Veranstaltungen zu behalten.</p></div>
											</li>
										</ul>
									</div>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</body>
</html>