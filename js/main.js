$(document).ready(function(){
	$('.collapsible').collapsible({
		accordion : false // A setting that changes the collapsible behavior to expandable instead of the default accordion style
	});

	$('#button-previousVersions1').click(function()
	{
		togglePreviousVersions();
	});

	$('#button-previousVersions2').click(function()
	{
		togglePreviousVersions();
	});
});

var hidden = true;
var buttonPreviousVersionShow = "Show Previous Versions";
var buttonPreviousVersionHide = "Hide Previous Versions";

function togglePreviousVersions()
{
	var element = document.getElementById('previousVersions');

	if(hidden)
	{
		hideElement(element, false);
		document.getElementById('button-previousVersions1').innerHTML = buttonPreviousVersionHide;
		document.getElementById('button-previousVersions2').innerHTML = buttonPreviousVersionHide;
		hidden = false;
	}
	else
	{
		hideElement(element, true);
		document.getElementById('button-previousVersions1').innerHTML = buttonPreviousVersionShow;
		document.getElementById('button-previousVersions2').innerHTML = buttonPreviousVersionShow;
		hidden = true;
	}
}

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
	var timer = setInterval(function ()
	{
		if (op >= 0.9){
			clearInterval(timer);
			element.style.opacity = 1.0;
		}
		element.style.opacity = op;
		op += 0.1;
	}, 50);
}