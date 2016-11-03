$(document).ready(function()
{
	$('.collapsible').collapsible({
		accordion: false // A setting that changes the collapsible behavior to expandable instead of the default accordion style
	});

	$('.milestone-title').click(function()
	{
		var $header = $(this);

		//getting the next element
		var $content = $header.next();

		//open up the content needed - toggle the slide- if visible, slide up, if not slidedown.
		$content.slideToggle(200);
	});

	//expand specific milestones on first load
	var initialExpandedMilestones = document.getElementsByClassName('init-as-expanded');
	for(var i = 0; i < initialExpandedMilestones.length; i++)
	{
		$(initialExpandedMilestones[i]).slideToggle(200);
	}

	//reacts to resize event of card and calls createTrainMap to adjust circles
	//https://github.com/marcj/css-element-queries
	var entries = document.getElementsByClassName('milestone');
	for(var i = 0; i < entries.length - 1; i++)
	{
		new ResizeSensor(entries[i], function()
		{
			createTrainMap();
		});
	}

	$('.button-save-roadmap').click(function()
	{
		editRoadmap(this.dataset.id, $('#project-name').val());
	});

	$('.button-save-milestone').click(function()
	{
		editMilestone(this.dataset.id, this.dataset.roadmapid);
	});

	$('.button-save-task').click(function()
	{
		editTask(this.dataset.id, this.dataset.milestoneid);
	});

	$('.button-save-subtask').click(function()
	{
		editSubtask(this.dataset.id, this.dataset.taskid);
	});

	$('.button-delete-roadmap').click(function()
	{
		var r = confirm("Do you really want to delete this roadmap?");
		if(r == true)
		{
			deleteRoadmap(this.dataset.id);
		}
	});

	$('.button-delete-milestone').click(function()
	{
		var r = confirm("Do you really want to delete this milestone?");
		if(r == true)
		{
			deleteMilestone(this.dataset.id, this.dataset.roadmapid);
		}
	});

	$('.button-delete-task').click(function()
	{
		var r = confirm("Do you really want to delete this task?");
		if(r == true)
		{
			deleteTask(this.dataset.id, this.dataset.milestoneid);
		}
	});

	$('.button-delete-subtask').click(function()
	{
		var r = confirm("Do you really want to delete this subtask?");
		if(r == true)
		{
			deleteSubtask(this.dataset.id, this.dataset.taskid);
		}
	});

	$('#checkbox-done').click(function()
	{
		var checked = document.getElementById("checkbox-done").checked;
		if(checked)
		{
			hideElement(document.getElementById("row-done-date"), false);

			var $input = $('#done-date').pickadate();
			var picker = $input.pickadate('picker');
			picker.set('select', new Date());
		}
		else
		{
			hideElement(document.getElementById("row-done-date"), true);
		}
	});

	$('.datepicker').pickadate({
		selectMonths: true, // Creates a dropdown to control month
		selectYears: 15, // Creates a dropdown of 15 years to control year
		format: 'dd.mm.yyyy',
		formatSubmit: 'yyyy-mm-dd'
	});

	$('.button-login').click(function()
	{
		login();
	});

	$('#password').keyup(function(e)
	{
		if(e.keyCode === 13)    //Enter
		{
			login();
		}
	});

	createTrainMap();
});

function isNull(object)
{
	if(object != "" && object != undefined)
	{
		return false;
	}
	else
	{
		return true;
	}
}

function hideElement(element, value)
{
	if(value == true)
	{
		element.classList.add("hide");
	}
	else
	{
		if(element.classList.contains("hide"))
		{
			element.classList.remove("hide");
		}
	}
}

function createTrainMap()
{
	var entries = document.getElementsByClassName('milestone');
	var lines = document.getElementsByClassName('train-line');
	var smallLines = document.getElementsByClassName('train-line-small');

	for(var i = 0; i < entries.length - 1; i++)
	{
		var height = entries[i].offsetHeight;
		lines[i].style.height = (height - 15) + "px";
		smallLines[i].style.height = (height - 2) + "px";
	}
}

function editRoadmap(roadmap_ID, projectname)
{
	if(isNull(projectname))
	{
		alert("Project Name shouldn't be empty!");
		return;
	}

	if(roadmap_ID == "0")
	{
		//insert new roadmap

		$.post('../admin/helper/edit-roadmap.php',
			{
				"project-name": projectname,
				"edit": "false"

			}, function(data, error)
			{
				data = data.toString().trim();
				switch(data)
				{
					case "error":
						alert('An error occurred');
						break;
					case "error-edit":
						alert('An error occurred while editing the roadmap with the ID ' + roadmap_ID);
						break;
					case "error-insert":
						alert('An error occurred while inserting the new roadmap');
						break;
					default:
						window.location.href = "../admin/admin-roadmaps.php";
						break;
				}
			});
	}
	else
	{
		//edit existing roadmap

		$.post('../admin/helper/edit-roadmap.php',
			{
				"ID": roadmap_ID,
				"project-name": projectname,
				"edit": "true"

			}, function(data, error)
			{
				data = data.toString().trim();
				switch(data)
				{
					case "error":
						alert('An error occurred');
						break;
					case "error-edit":
						alert('An error occurred while editing the roadmap with the ID ' + roadmap_ID);
						break;
					case "error-insert":
						alert('An error occurred while inserting the new roadmap');
						break;
					default:
						window.location.href = "../admin/admin-roadmaps.php";
						break;
				}
			});
	}
}

function deleteRoadmap(roadmap_ID)
{
	$.post('../admin/helper/delete-roadmap.php',
		{
			"roadmap_ID": roadmap_ID,

		}, function(data, error)
		{
			data = data.toString().trim();

			if(data != "error")
			{
				window.location.href = "../admin/admin-roadmaps.php";
			}
			else
			{
				alert('An error occurred while deleting the roadmap with the ID ' + roadmap_ID);
			}
		});
}

function editMilestone(milestone_ID, roadmap_ID)
{
	var edit = document.getElementById('edit').innerHTML;
	var versionCode = $('#version-code').val();
	var versionName = $('#version-name').val();
	var title = $('#title').val();
	var dueDate = $('#due-date').val();
	var doneDate = $('#done-date').val();
	var done = document.getElementById("checkbox-done").checked;

	if(isNull(versionCode))
	{
		alert("Version Code shouldn't be empty!");
		return;
	}

	if(isNull(versionName))
	{
		alert("Version Name shouldn't be empty!");
		return;
	}

	if(isNull(title))
	{
		alert("Title shouldn't be empty!");
		return;
	}

	if(isNull(dueDate))
	{
		dueDate = "01.01.2000";
	}

	if(isNull(doneDate))
	{
		doneDate = "01.01.2000";
	}

	if(done)
	{
		done = 1;
	}
	else
	{
		done = 0;
		doneDate =  "01.01.2000";
	}

	$.post('../admin/helper/edit-milestone.php',
		{
			"version-code": versionCode,
			"version-name": versionName,
			"title": title,
			"due-date": dueDate,
			"done-date": doneDate,
			"done": done,
			"edit": edit,
			"ID": milestone_ID,
			"roadmap-ID": roadmap_ID

		}, function(data, error)
		{
			data = data.toString().trim();
			switch(data)
			{
				case "error":
					alert('An error occurred');
					break;
				case "error-edit":
					alert('An error occurred while editing the roadmap with the ID ' + roadmap_ID);
					break;
				case "error-insert":
					alert('An error occurred while inserting the new milestone');
					break;
				default:
					window.location.href = "../admin/admin-milestones.php?id=" + roadmap_ID;
					break;
			}
		});
}

function deleteMilestone(milestone_ID, roadmap_ID)
{
	$.post('../admin/helper/delete-milestone.php',
		{
			"milestone_ID": milestone_ID,

		}, function(data, error)
		{
			data = data.toString().trim();

			if(data != "error")
			{
				window.location.href = "../admin/admin-milestones.php?id=" + roadmap_ID;
			}
			else
			{
				alert('An error occurred while deleting the milestone with the ID ' + milestone_ID);
			}
		});
}

function editTask(task_ID, milestone_ID)
{
	var edit = document.getElementById('edit').innerHTML;
	var title = $('#title').val();
	var description = $('#description').val();;
	var done = document.getElementById("checkbox-done").checked;

	if(isNull(title))
	{
		alert("Title shouldn't be empty!");
		return;
	}

	if(done)
	{
		done = 1;
	}
	else
	{
		done = 0;
	}

	$.post('../admin/helper/edit-task.php',
		{
			"title": title,
			"description": description,
			"done": done,
			"edit": edit,
			"ID": task_ID,
			"milestone-ID": milestone_ID

		}, function(data, error)
		{
			data = data.toString().trim();
			switch(data)
			{
				case "error":
					alert('An error occurred');
					break;
				case "error-edit":
					alert('An error occurred while editing the task with the ID ' + task_ID);
					break;
				case "error-insert":
					alert('An error occurred while inserting the new task');
					break;
				default:
					window.location.href = "../admin/admin-tasks.php?id=" + milestone_ID;
					break;
			}
		});
}

function deleteTask(task_ID, milestone_ID)
{
	$.post('../admin/helper/delete-task.php',
		{
			"task_ID": task_ID,

		}, function(data, error)
		{
			data = data.toString().trim();

			if(data != "error")
			{
				window.location.href = "../admin/admin-tasks.php?id=" + milestone_ID;
			}
			else
			{
				alert('An error occurred while deleting the task with the ID ' + task_ID);
			}
		});
}

function editSubtask(subtask_ID, task_ID)
{
	var edit = document.getElementById('edit').innerHTML;
	var title = $('#title').val();
	var description = $('#description').val();;
	var done = document.getElementById("checkbox-done").checked;

	if(isNull(title))
	{
		alert("Title shouldn't be empty!");
		return;
	}

	if(done)
	{
		done = 1;
	}
	else
	{
		done = 0;
	}

	$.post('../admin/helper/edit-subtask.php',
		{
			"title": title,
			"de6scription": description,
			"done": done,
			"edit": edit,
			"ID": subtask_ID,
			"task-ID": task_ID

		}, function(data, error)
		{
			data = data.toString().trim();
			switch(data)
			{
				case "error":
					alert('An error occurred');
					break;
				case "error-edit":
					alert('An error occurred while editing the subtask with the ID ' + subtask_ID);
					break;
				case "error-insert":
					alert('An error occurred while inserting the new task');
					break;
				default:
					window.location.href = "../admin/admin-subtasks.php?id=" + task_ID;
					break;
			}
		});
}


function deleteSubtask(subtask_ID, task_ID)
{
	$.post('../admin/helper/delete-subtask.php',
		{
			"subtask_ID": subtask_ID,

		}, function(data, error)
		{
			data = data.toString().trim();

			if(data != "error")
			{
				window.location.href = "../admin/admin-subtasks.php?id=" + task_ID;
			}
			else
			{
				alert('An error occurred while deleting the subtask with the ID ' + subtask_ID);
			}
		});
}

function login()
{
	var password = $('#password').val();

	if(isNull(password))
	{
		alert("Please enter your password.");
		return;
	}

	$.post('../admin/helper/checkLogin.php',
		{
			"password": password,

		}, function(data, error)
		{
			data = data.toString().trim();

			if(data != "error" && data != "bad_login")
			{
				window.location.href = "../admin/admin-roadmaps.php";
			}
			else
			{
				alert('Wrong password!');
			}
		});
}