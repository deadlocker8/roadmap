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

        //open up the content needed - toggle the slide- if visible, slide up, if not slide down.
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

    $('.button-delete-roadmap').click(function(event)
    {
        var response = confirm("Do you really want to delete this roadmap?");
        if(response === true)
        {
            header("location: " + this.href);
        }
    });

    $('.button-delete-milestone').click(function(event)
    {
        var response = confirm("Do you really want to delete this milestone?");
        if(response === true)
        {
            header("location: " + this.href);
        }
    });

    $('.button-delete-task').click(function(event)
    {
        var response = confirm("Do you really want to delete this task?");
        if(response === true)
        {
            header("location: " + this.href);
        }
    });

    $('.button-delete-subtask').click(function(event)
    {
        var response = confirm("Do you really want to delete this subtask?");
        if(response === true)
        {
            header("location: " + this.href);
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

    createTrainMap();
});

function isNull(object)
{
    return object === "" || object === undefined;
}

function hideElement(element, value)
{
    if(value === true)
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

function validateLoginForm()
{
    var password = $('#password').val();

    if(isNull(password))
    {
        alert("Please enter your password.");
        return false;
    }
}

function validateNewRoadmapForm()
{
    var projectName = $('#project-name').val();

    if(isNull(projectName))
    {
        alert("Please enter a project name.");
        return false;
    }
}

function validateNewMilestoneForm()
{
    var versionCode = $('#version-code').val();
    var versionName = $('#version-name').val();
    var title = $('#title').val();
    var dueDate = document.getElementById('due-date');
    var doneDate = document.getElementById('done-date');
    var done = document.getElementById('checkbox-done').checked;

    if(isNull(versionCode))
    {
        alert("Version Code shouldn't be empty!");
        return false;
    }

    if(isNull(versionName))
    {
        alert("Version Name shouldn't be empty!");
        return false;
    }

    if(isNull(title))
    {
        alert("Title shouldn't be empty!");
        return false;
    }

    if(isNull(dueDate.value))
    {
        dueDate.value = "01.01.2000";
    }

    if(isNull(doneDate.value))
    {
        doneDate.value = "01.01.2000";
    }

    if(!done)
    {
        doneDate.value = "01.01.2000";
    }

    return true;
}

function validateNewTaskForm()
{
    var title = $('#title').val();
    var description = document.getElementById('description');

    if(isNull(title))
    {
        alert("Title shouldn't be empty!");
        return false;
    }

    if(isNull(description))
    {
        alert("Description shouldn't be empty!");
        return false;
    }

    return true;
}
