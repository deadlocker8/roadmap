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

	$('.button-delete-roadmap').click(function()
	{
		var r = confirm("Do you really want to delete this roadmap?");
		if(r == true)
		{
			deleteRoadmap(this.dataset.id);
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