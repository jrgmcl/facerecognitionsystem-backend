<?php


$temp_path = $_FILES['fileToUpload']['tmp_name'];
$dataset = "/var/www/html/datasets/";
$target_file = $dataset.$_FILES["fileToUpload"]["name"];
$uploadOk = 1;
$imageFileType = strtolower(pathinfo($target_file,PATHINFO_EXTENSION));

// Check if image file is a actual image or fake image
if(isset($_POST["submit"])) {
	$check = getimagesize($_FILES["fileToUpload"]["tmp_name"]);
	if($check !== false) {
		echo "File is an image - " . $check["mime"] . ".</br>";
		echo $temp_path."</br>";
		$uploadOk = 1;
	} else {
		echo "File is not an image.";
		$uploadOk = 0;
	}
}

// Check if file already exists


// Check file size
if ($_FILES["fileToUpload"]["size"] > 500000) {
	echo "Sorry, your file is too large.";
	$uploadOk = 0;
}

// Allow certain file formats
if($imageFileType != "jpg" && $imageFileType != "png" && $imageFileType != "jpeg"
&& $imageFileType != "gif" ) {
	echo "Sorry, only JPG, JPEG, PNG & GIF files are allowed.";
	$uploadOk = 0;
}

// Check if $uploadOk is set to 0 by an error
if ($uploadOk == 0) {
	echo "Sorry, your file was not uploaded.";
	// if everything is ok, try to upload file
} else {
	if(mkdir($dataset."Jorge", 0777, true)){
		echo "Folder created";
	}
	else {
		echo "Error on creating the folder";
	}
	
	$new_target_file = $dataset."Jorge/".$_FILES["fileToUpload"]["name"];
	echo $new_target_file;
	if (file_exists($new_target_file)) {
		echo "Sorry, file already exists.";
		$uploadOk = 0;
	}
	if (move_uploaded_file($temp_path, $new_target_file)) {
		echo "The file ". htmlspecialchars( basename( $_FILES["fileToUpload"]["name"])). " has been uploaded.";
	} else {
		echo (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file))."</br>";
		#echo "test";
		echo "Sorry, there was an error uploading your file.";
	}
}

?>