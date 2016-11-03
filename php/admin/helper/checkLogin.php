<?php

$PASSWORD = "123";

if(!isset($_SESSION))
{
	session_start();
}

if($_SERVER['REQUEST_METHOD'] == 'POST')
{
	if(isset($_POST['password']))
	{
		if($_POST['password'] == $PASSWORD)
		{
			$_SESSION['loggedIn'] = 'true';
			echo "success";
		}
		else
		{
			echo "bad_login";
		}
	}
	else
	{
		echo "error";
	}
}
else
{
	echo "error";
}