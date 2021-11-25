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
	$db = "IoT-Advanced-Project";

	$dbconnect=mysqli_connect($hostname,$username,$password,$db);

	if ($dbconnect->connect_error) {
		die("Database connection failed: " . $dbconnect->connect_error);
	}
	?>
	<?php

	$query = mysqli_query($dbconnect, "SELECT StatusParkingLot FROM `parkingLots`")
		or die (mysqli_error($dbconnect));
	while ($row = mysqli_fetch_array($query)) {
		$StatusParkingLot[] = $row[0];   
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
            if($StatusParkingLot[0] == 0){
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
            if($StatusParkingLot[1] == 0){
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
            if($StatusParkingLot[2] == 0){
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
            if($StatusParkingLot[3] == 0){
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
	header("refresh: 3");
	$counts = array_count_values($StatusParkingLot);
    if($counts['0'] == 0){
        echo '0';
    } else{
	    echo  $counts['0'];
    }
	?></span>
	</div>
</body>
</html>
