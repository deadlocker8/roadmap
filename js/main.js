$(document).ready(function()
{
	$('.collapsible').collapsible({
		accordion: false // A setting that changes the collapsible behavior to expandable instead of the default accordion style
	});

	$('.version-entry-title').click(function()
	{
		toggleDetail($(this).get(0));
		createTrainMap();
	});

	$('.collapsible-header').click(function()
	{
		setTimeout(function()
		{
			createTrainMap();
		}, 300);

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

function fadeIn(element)
{
	element.style.opacity = 0;
	var op = 0;
	var timer = setInterval(function()
	{
		if(op >= 0.9)
		{
			clearInterval(timer);
			element.style.opacity = 1.0;
		}
		element.style.opacity = op;
		op += 0.1;
	}, 50);
}

function createTrainMap()
{
	var entries = document.getElementsByClassName('version-entry');
	var lines = document.getElementsByClassName('train-line');

	for(var i = 0; i < entries.length - 1; i++)
	{
		var height = entries[i].offsetHeight - 16;
		lines[i].style.height = height + "px";
	}
}

function toggleDetail(element)
{
	var container = element.parentElement.parentElement.childNodes[3];
	var cardHeader = element.parentElement;

	if(container.classList.contains("hide"))
	{
		hideElement(container, false);

		fadeIn(container);

		if(!cardHeader.classList.contains("margin-bottom"))
		{
			cardHeader.classList.add("margin-bottom");
		}
	}
	else
	{
		hideElement(container, true);

		if(cardHeader.classList.contains("margin-bottom"))
		{
			cardHeader.classList.remove("margin-bottom");
		}
	}
}