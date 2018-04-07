<?php

class ComplicatedIfElse {

	public function complicatedIfElse() {
		echo ("Life is complicated fren ;)");
		if (1 == 2 && $x <= 2 && 3 >= 3 || empty($x)) {
			$x = 2;
			nestedIfEvaluation(1, "Hell", $xx);
		}
		elseif (3==2)
		{
			echo ("Arithmatic :(");
		}
		elseif (2==2)
		{
			$x[0] = 3;
			$x[] = 3;
			$x = 3;
		}
		else
		{
			echo ("Socrates");
		}
		echo "Afterwards";
		$date_obj = new Carbon('29-10-2018');
		$abc = nestedIfEvaluation($date_obj);
		$hello = $date_obj->date(1,2,3);
		$date_obj->is_object(1,2,4,5);
		hello(1,2,3);
		Carbon::helloworld(1,3,4);
	}

}
