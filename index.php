<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>Parking</title>
</head>

<body>
    <?php

	$hostname = "localhost";
	$username = "pi";
	$password = "raspberry";
	$db = "ParkingDB";

	$dbconnect=mysqli_connect($hostname,$username,$password,$db);

	if ($dbconnect->connect_error) {
		die("Database connection failed: " . $dbconnect->connect_error);
	}

	$query = mysqli_query($dbconnect, "SELECT bezet FROM `ParkingLot`")
		or die (mysqli_error($dbconnect));
	while ($row = mysqli_fetch_array($query)) {
		$bezet[] = $row[0];
	}
	$rood = '#E16950';
	$groen = '#91F160';
	?>
    <h1>
        Parking webinterface
    </h1>
    <svg width="150" height="360">
        <rect id="parking1" x="0" y="0" width="150" height="360" style="fill:
		<?php
            if($bezet[0] == 0){
                echo $groen;
            }
            else{
                echo $rood;
            }
        ?>
		;stroke:black;stroke-width:5;" />
    </svg>    
	<svg width="150" height="360">
        <rect id="parking1" x="0" y="0" width="150" height="360" style="fill:
		<?php
            if($bezet[1] == 0){
                echo $groen;
            }
            else{
                echo $rood;
            }
        ?>
		;stroke:black;stroke-width:5;" />
    </svg>    
	<svg width="150" height="360">
        <rect id="parking1" x="0" y="0" width="150" height="360" style="fill:
		<?php
            if($bezet[2] == 0){
                echo $groen;
            }
            else{
                echo $rood;
            }
        ?>
		;stroke:black;stroke-width:5;" />
    </svg>    
	<svg width="150" height="360">
        <rect id="parking1" x="0" y="0" width="150" height="360" style="fill:
		<?php
            if($bezet[3] == 0){
                echo $groen;
            }
            else{
                echo $rood;
            }
        ?>
		;stroke:black;stroke-width:5;" />
    </svg>
	<div> Aantal vrije plaatsen: <span style="font-weight:bold">
	<?php
	$counts = array_count_values($bezet);
	echo  $counts['0'] 
	?></span>
	</div>
	<?php
	$counts = array_count_values($bezet);
	if ($counts['0'] == 0){
		curl_setopt_array($ch = curl_init(), array(
		CURLOPT_URL => "https://api.pushover.net/1/messages.json",
		CURLOPT_POSTFIELDS => array(
			"token" => "adcxfe2q99fibaupf4arwf3cdi7sa4",
			"user" => "uabtbvyuxaudjddqp86o5rh5xordta",
			"message" => "Youre parking is full! 🚗",
		),
		CURLOPT_SAFE_UPLOAD => true,
		CURLOPT_RETURNTRANSFER => true,
		));
		curl_exec($ch);
		curl_close($ch);
		
		$servername = "localhost";
		$username = "pi";
		$password = "raspberry";
		$dbname = "ParkingDB";

		// Create connection
		$conn = new mysqli($servername, $username, $password, $dbname);
		// Check connection
		if ($conn->connect_error) {
			die("Connection failed: " . $conn->connect_error);
		}

		$sql = "UPDATE ParkingLot SET bezet=0 WHERE id=5";

		if ($conn->query($sql) === TRUE) {
			echo "";
		} 
		else {
			echo "";
		}
	}	
	if ($bezet['0'] == 0 or $bezet['1'] == 0 or $bezet['2'] == 0 or $bezet['3'] == 0 and $bezet[4] == 0){
		
		$servername = "localhost";
		$username = "pi";
		$password = "raspberry";
		$dbname = "ParkingDB";

		// Create connection
		$conn = new mysqli($servername, $username, $password, $dbname);
		// Check connection
		if ($conn->connect_error) {
			die("Connection failed: " . $conn->connect_error);
		}

		$sql = "UPDATE ParkingLot SET bezet=1 WHERE id=5";

		if ($conn->query($sql) === TRUE) {
			echo "";
		} 
		else {
			echo "";
		}
	}
	
	header("refresh: 3");
	?>
</body>
</html>
