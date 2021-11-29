<?php
/*
  Rui Santos
  Complete project details at https://RandomNerdTutorials.com/esp32-esp8266-mysql-database-php/
  
  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files.
  
  The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software.
*/

$servername = "db.sinners.be";

// REPLACE with your Database name
$dbname = "vincentsomers_plantdata";
// REPLACE with Database user
$username = "vincentsomers";
// REPLACE with Database user password
$password = "cKWtZSjfterq";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
} 

$sql = "SELECT id FROM display where status = 1";

if ($result = $conn->query($sql)) {
    while ($row = $result->fetch_assoc()) {
        $row_id = $row["id"];
        $row_status = $row["status"];
      
        echo ''. $row_id .'';
    }
    $result->free();
}

$conn->close();
?> 