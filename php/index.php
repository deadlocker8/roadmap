<!DOCTYPE html>

<?php
include_once('getLanguageJSON.php');
include_once('mysql.php');

if(!isset($_GET['id']))
{
	//TODO
	die("get param missing");
}

$ID = $_GET['id'];
if(!is_numeric($ID) || $ID < 1)
{
	//TODO
	die("param is not numeric or less than 1");
}

$db = new DB();
$db->createTables();

$projectName = $db->getRoadmap($ID);
if($projectName == false)
{
	//TODO
	die("no roadmap with this ID existing");
}
$projectName = $projectName["Projectname"];

$milestones = $db->getMilestones($ID);
if($milestones == false)
{
	//TODO
	die("no milestones for this roadmap");
}

$numberOfMilestones = sizeof($milestones);

$numberofOpenMilestones = $db->getNumberOfOpenMilestones($ID);
if($numberofOpenMilestones == false)
{
	//TODO
	die("error getting open milestones");
}

$numberofOpenMilestones = $numberofOpenMilestones['count'];
?>
<html xmlns="http://www.w3.org/1999/html">
	<head>
		<meta charset="UTF-8"/>
		<title>Roadmap - <?php echo $projectName;?></title>
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
				<h2 class="center-align" id="headline"><?php echo $projectName;?> Roadmap</h2>
				<div class="row">
					<div class="col s12">
						<div class="row">
							<div class="col s1 m2 l2 offset-m1 offset-l1 no-padding">
								<div class="hide-on-small-only trainmap">
									<?php
										for($i = 0; $i < $numberofOpenMilestones; $i++)
										{
											echo '<div class="train-circle train-circle-light"></div>';

											if($numberofOpenMilestones != $numberOfMilestones || $i != ($numberofOpenMilestones-1))
											{
												echo '<div class="train-line dotted"></div>';
											}
										}

										for($i = 0; $i < ($numberOfMilestones - $numberofOpenMilestones); $i++)
										{
											echo '<div class="train-circle blue"></div>';

											if($i !=  (($numberOfMilestones - $numberofOpenMilestones) - 1))
											{
												echo '<div class="train-line"></div>';
											}
										}
									?>
								</div>
								<div class="hide-on-med-and-up trainmap-small">
									<?php
										for($i = 0; $i < $numberofOpenMilestones; $i++)
										{
											echo '<div class="train-circle train-circle-light train-circle-small"></div>';

											if($numberofOpenMilestones != $numberOfMilestones || $i != ($numberofOpenMilestones-1))
											{
												echo '<div class="train-line dotted-small train-line-small"></div>';
											}
										}

										for($i = 0; $i < ($numberOfMilestones - $numberofOpenMilestones); $i++)
										{
											echo '<div class="train-circle blue train-circle-small"></div>';

											if($i !=  (($numberOfMilestones - $numberofOpenMilestones) - 1))
											{
												echo '<div class="train-line train-line-small"></div>';
											}
										}
									?>
								</div>
							</div>
						<div class="col s11 m7 l6">

							<?php
								$isFirstMilestone = true;
								for($i = 0; $i < $numberOfMilestones; $i++)
								{
									$currentMilestone = $milestones[$i];

									//Milestone is inDev
									if($currentMilestone['Status'] == 0)
									{
										$color = 'blue lighten-2';

										$dueDate = $currentMilestone['DueDate'];
										if($dueDate == "2000-01-01")
										{
											$dueDate = "-";
										}
										else
										{
											$dueDate = date_create($dueDate);
											$dueDate = date_format($dueDate, "d.m.Y");
										}

										$tasks = $db->getTasks($currentMilestone['ID']);
										if($tasks == false)
										{
											echo '<div class="card padding white milestone">' .
												'<div class="card-content">' .
												'<div class="'.$color.' center-align milestone-title">' .
												'<span class="card-title bold padding-left-and-right truncate">' . $currentMilestone['VersionName'] . ' - ' . $currentMilestone['Title'] . '</span>' .
												'</div>' .
												'<div class="milestone-content margin-top">' .
												'<div class="white progress-container">'.
												'<div class="progress grey lighten-2 high-progress margin-bottom">'.
												'<div class="determinate green" style="width: 0%"></div>'.
												'</div>'.
												'</div>'.
												'<div class="row">' .
												'<div class="col s6 valign-wrapper">' .
												'<i class="material-icons valign">event</i><span class="valign margin-left">' . $languageJSON->due_by . ' ' . $dueDate . '</span>' .
												'</div>' .
												'<div class="col s6 valign-wrapper">' .
												'<i class="material-icons valign">event</i><span class="valign margin-left">0% ' . $languageJSON->done . '</span>' .
												'</div>' .
												'</div>' .
												'</div>' .
												'</div>' .
												'</div>';
										}
										else
										{
											$dueDate = $currentMilestone['DueDate'];
											if($dueDate == "2000-01-01")
											{
												$dueDate = "-";
											}
											else
											{
												$dueDate = date_create($dueDate);
												$dueDate = date_format($dueDate, "d.m.Y");
											}

											$completionDate = $currentMilestone['CompletionDate'];
											$completionDate = date_create($completionDate);
											$completionDate = date_format($completionDate, "d.m.Y");

											$numberOfOpenTasks = $db->getNumberOfOpenTasks($currentMilestone['ID']);
											if($numberOfOpenTasks == false)
											{
												//TODO
											}
											else
											{
												$numberOfOpenTasks = $numberOfOpenTasks['count'];
												$percentage = ($numberOfOpenTasks / sizeof($tasks))*100;
												$percentage = round($percentage);

												echo '<div class="card padding white milestone">' .
													'<div class="card-content">' .
													'<div class="'.$color.' center-align milestone-title">' .
													'<span class="card-title bold padding-left-and-right truncate">' . $currentMilestone['VersionName'] . ' - ' . $currentMilestone['Title'] . '</span>' .
													'</div>' .
													'<div class="milestone-content margin-top">' .
													'<div class="white progress-container">'.
													'<div class="progress grey lighten-2 high-progress margin-bottom">'.
													'<div class="determinate green" style="width: '.$percentage.'%"></div>'.
													'</div>'.
													'</div>'.
													'<div class="row">' .
													'<div class="col s6 valign-wrapper">' .
													'<i class="material-icons valign">event</i><span class="valign margin-left">' . $languageJSON->due_by . ' ' . $dueDate . '</span>' .
													'</div>' .
													'<div class="col s6 valign-wrapper">' .
													'<i class="material-icons valign">event</i><span class="valign margin-left">'.$percentage.'% ' . $languageJSON->done .'</span>' .
													'</div>' .
													'</div>' .
													'<ul class="collapsible white" data-collapsible="accordion">';
												for($k = 0; $k < sizeof($tasks); $k++)
												{
													$currentTask = $tasks[$k];

													$subtasks = $db->getSubtasks($currentTask['ID']);
													if($subtasks == false)
													{
														//inDev
														if($currentTask['Status'] == 0)
														{
															echo '<li>' .
																'<div class="collapsible-header bold"><i class="material-icons red-text">build</i>' . $currentTask['Title'] . '</div>' .
																'<div class="collapsible-body"><p>' . $currentTask['Description'] . '</p></div>' .
																'</li>';
														}
														//done
														else
														{
															echo '<li>' .
																'<div class="collapsible-header bold"><i class="material-icons green-text">check</i>' . $currentTask['Title'] . '</div>' .
																'<div class="collapsible-body"><p>' . $currentTask['Description'] . '</p></div>' .
																'</li>';
														}
													}
													else
													{
														$numberOfOpenSubtasks = $db->getNumberOfOpenSubtasks($currentTask['ID']);
														if($numberOfOpenSubtasks == false)
														{
															//TODO
														}
														else
														{
															$numberOfOpenSubtasks = $numberOfOpenSubtasks['count'];
															if($numberOfOpenSubtasks == sizeof($subtasks))
															{
																echo '<li>' .
																	'<div class="collapsible-header bold"><i class="material-icons green-text">check</i>Layout<span class="right">' . $numberOfOpenSubtasks . '/' . sizeof($subtasks) . '</span></div>' .
																	'<div class="collapsible-body">' .
																	'<ul class="collapsible white margin-left-and-right no-shadow margin-top-and-bottom" data-collapsible="accordion">';
															}
															else
															{
																echo '<li>' .
																	'<div class="collapsible-header bold"><i class="material-icons red-text">build</i>Layout<span class="right">' . $numberOfOpenSubtasks . '/' . sizeof($subtasks) . '</span></div>' .
																	'<div class="collapsible-body">' .
																	'<ul class="collapsible white margin-left-and-right no-shadow margin-top-and-bottom" data-collapsible="accordion">';
															}

															for($m = 0; $m < sizeof($subtasks); $m++)
															{
																$currentSubTask = $subtasks[$m];
																//inDev
																if($currentSubTask['Status'] == 0)
																{
																	echo '<li>' .
																		'<div class="collapsible-header bold"><span class="left">' . ($m + 1) . '</span><i class="material-icons red-text margin-left">build</i>' . $currentSubTask['Title'] . '</div>' .
																		'<div class="collapsible-body"><p>' . $currentSubTask['Description'] . '</p></div>' .
																		'</li>';
																}
																//done
																else
																{
																	echo '<li>' .
																		'<div class="collapsible-header bold"><span class="left">' . ($m + 1) . '</span><i class="material-icons green-text margin-left">check</i>' . $currentSubTask['Title'] . '</div>' .
																		'<div class="collapsible-body"><p>' . $currentSubTask['Description'] . '</p></div>' .
																		'</li>';
																}
															}

															echo '</ul>' .
																'</div>' .
																'</li>';
														}
													}
												}

												echo '</ul>' .
													'</div>' .
													'</div>' .
													'</div>';
											}
										}
									}
									//Milestone is done
									else
									{
										if($isFirstMilestone)
										{
											$color = 'amber lighten-2';
										}
										else
										{
											$color = 'grey lighten-2';
										}

										$dueDate = $currentMilestone['DueDate'];
										if($dueDate == "2000-01-01")
										{
											$dueDate = "-";
										}
										else
										{
											$dueDate = date_create($dueDate);
											$dueDate = date_format($dueDate, "d.m.Y");
										}

										$completionDate = $currentMilestone['CompletionDate'];
										$completionDate = date_create($completionDate);
										$completionDate = date_format($completionDate, "d.m.Y");

										$tasks = $db->getTasks($currentMilestone['ID']);
										if($tasks == false)
										{
											echo '<div class="card padding white milestone">' .
												'<div class="card-content">' .
												'<div class="'.$color.' center-align milestone-title">' .
												'<span class="card-title bold padding-left-and-right truncate">' . $currentMilestone['VersionName'] . ' - ' . $currentMilestone['Title'] . '</span>' .
												'</div>';

												if($isFirstMilestone)
												{
													echo '<div class="milestone-content margin-top init-as-expanded">';
												}
												else
												{
													echo '<div class="milestone-content margin-top">';
												}

												echo '<div class="row">' .
												'<div class="col s6 valign-wrapper">' .
												'<i class="material-icons valign">event</i><span class="valign margin-left">' . $languageJSON->due_by . ' ' . $dueDate . '</span>' .
												'</div>' .
												'<div class="col s6 valign-wrapper">' .
												'<i class="material-icons valign">event</i><span class="valign margin-left">' . $languageJSON->done_at . ' ' . $completionDate . '</span>' .
												'</div>' .
												'</div>' .
												'</div>' .
												'</div>' .
												'</div>';
										}
										else
										{
											echo '<div class="card padding white milestone">' .
												'<div class="card-content">' .
												'<div class="'.$color.' center-align milestone-title">' .
												'<span class="card-title bold padding-left-and-right truncate">' . $currentMilestone['VersionName'] . ' - ' . $currentMilestone['Title'] . '</span>' .
												'</div>';

												if($isFirstMilestone)
												{
													echo '<div class="milestone-content margin-top init-as-expanded">';
												}
												else
												{
													echo '<div class="milestone-content margin-top">';
												}

											echo '<div class="row">' .
												'<div class="col s6 valign-wrapper">' .
												'<i class="material-icons valign">event</i><span class="valign margin-left">' . $languageJSON->due_by . ' ' . $dueDate . '</span>' .
												'</div>' .
												'<div class="col s6 valign-wrapper">' .
												'<i class="material-icons valign">event</i><span class="valign margin-left">' . $languageJSON->done_at . ' ' . $completionDate . '</span>' .
												'</div>' .
												'</div>' .
												'<ul class="collapsible white" data-collapsible="accordion">';
											for($k = 0; $k < sizeof($tasks); $k++)
											{
												$currentTask = $tasks[$k];

												$subtasks = $db->getSubtasks($currentTask['ID']);
												if($subtasks == false)
												{
													echo '<li>' .
														'<div class="collapsible-header bold"><i class="material-icons green-text">check</i>' . $currentTask['Title'] . '</div>' .
														'<div class="collapsible-body"><p>' . $currentTask['Description'] . '</p></div>' .
														'</li>';
												}
												else
												{
													$numberOfOpenSubtasks = $db->getNumberOfOpenSubtasks($currentTask['ID']);
													if($numberOfOpenSubtasks == false)
													{

													}
													else
													{
														$numberOfOpenSubtasks = $numberOfOpenSubtasks['count'];
														if($numberOfOpenSubtasks == sizeof($subtasks))
														{
															echo '<li>' .
																'<div class="collapsible-header bold"><i class="material-icons green-text">check</i>Layout<span class="right">' . $numberOfOpenSubtasks . '/' . sizeof($subtasks) . '</span></div>' .
																'<div class="collapsible-body">' .
																'<ul class="collapsible white margin-left-and-right no-shadow margin-top-and-bottom" data-collapsible="accordion">';
														}
														else
														{
															echo '<li>' .
																'<div class="collapsible-header bold"><i class="material-icons red-text">build</i>Layout<span class="right">' . $numberOfOpenSubtasks . '/' . sizeof($subtasks) . '</span></div>' .
																'<div class="collapsible-body">' .
																'<ul class="collapsible white margin-left-and-right no-shadow margin-top-and-bottom" data-collapsible="accordion">';
														}

														for($m = 0; $m < sizeof($subtasks); $m++)
														{
															$currentSubTask = $subtasks[$m];
															//inDev
															if($currentSubTask['Status'] == 0)
															{
																echo '<li>' .
																	'<div class="collapsible-header bold"><span class="left">' . ($m + 1) . '</span><i class="material-icons red-text margin-left">build</i>' . $currentSubTask['Title'] . '</div>' .
																	'<div class="collapsible-body"><p>' . $currentSubTask['Description'] . '</p></div>' .
																	'</li>';
															}
															//done
															else
															{
																echo '<li>' .
																	'<div class="collapsible-header bold"><span class="left">' . ($m + 1) . '</span><i class="material-icons green-text margin-left">check</i>' . $currentSubTask['Title'] . '</div>' .
																	'<div class="collapsible-body"><p>' . $currentSubTask['Description'] . '</p></div>' .
																	'</li>';
															}
														}

														echo '</ul>' .
															'</div>' .
															'</li>';
													}
												}
											}

											echo '</ul>' .
												'</div>' .
												'</div>' .
												'</div>';
										}

										if($isFirstMilestone)
										{
											$isFirstMilestone = false;
										}
									}
								}
							?>
						</div>
					</div>
				</div>
			</div>
		</div>
	</body>
</html>