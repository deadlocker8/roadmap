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
		lines[i].style.height = (height-15) + "px";
		smallLines[i].style.height = (height-2) + "px";
	}
}