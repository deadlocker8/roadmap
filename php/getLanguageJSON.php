<?php
$file = realpath(dirname(__FILE__) . '/language.json');
if(file_exists($file))
{
	$languageJSON = json_decode(file_get_contents($file));
}
else
{
	$languageJSON = json_decode('{
		"due_by": "Due by",
		"done": "Done",
		"done_at": "Done at"
	}');
}