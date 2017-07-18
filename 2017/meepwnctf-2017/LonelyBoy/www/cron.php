link: '.$link;

//phantomjs here
if (!empty($link))
{
	$cmd="phantomjs something.js ".$link;
	system($cmd);
}

//then delete
mysqli_query($conn,"DELETE FROM saved_link WHERE id=$id");

/*
CREATE TABLE saved_link (
    id int NOT NULL AUTO_INCREMENT,
    link varchar(500) NOT NULL,
    PRIMARY KEY (id)
);
*/
?>