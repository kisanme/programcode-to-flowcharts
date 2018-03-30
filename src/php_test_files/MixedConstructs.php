<?php

$c = 1;
while ($c <= 10) {
	if ($c % 2 == 0) {
		echo "$c is an even number";
	} else {
		echo "$c is an odd number";
	}
	$c += 1;
}