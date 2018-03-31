<?php

class BasicClass {

	public function helloConditional() {
//		if (1 == 2) {
        // // Both the following may look same, but they are different - the left-associativity
//		if (1 == 2 && (2 == 2 || 3 == 3)) {
		echo('hello world is a nice text');
		if (1 == 2 && $x <= 2 && 3 >= 3 || 4 == 4 && $x == 2 || empty($x)) {
		    $x = 2;
//		    if ($x == 2) {
//		        echo ("HINDRANCE");
//		    }
			echo ("printing hello");
			echo ("jinthu");
			nestedIfEvaluation(1, "Hell", $xx);
		}
		elseif (2==2)
		{
			echo ("Hello");
			$x = 3;
		}
		else
        {
			echo ("HI");
		}
		echo "Afterwards";
		$hi = new Carbon('29-10-2018');
		// $abc = isset($hi);
		$abc = nestedIfEvaluation($hi);
		$hello = $hi->date(1,2,3);
		$hi->is_object(1,2,4,5);
		hello(1,2,3);
		Carbon::helloworld(1,3,4);
	}

//	public function nestedIfEvaluation() {
//	    $x = 2;
//		if ($x < 2) {
//		    if ($x == 0) {
//                echo ("Zero test");
//		    }
//			echo ("1 or negative number");
//		} else {
//			echo ("positive numbers greater than 2");
//		}
//		echo ("Outro");
//	}


//    public function whileEvaluation() {
//      $counter = 0;
//      while ($counter < 100) {
//        $some_array[] = $counter;
//        $counter ++;
//      }
//    }

//	public function switch_test () {
//	    switch (contenttype) {
//            case 'news':
//                echo "News flash!";
//                 break;
//            case 'interview':
//                echo "Interview with Mr. B";
//                break;
//            case 'presentation':
//                echo "An awesome Presentation";
//                break;
//        }
//    }

//    public function for_test() {
//        $y = 20;
//        $z = 10;
//        for ($x = 0; $x < 10; $x++) {
//            $y[$x] = $z+$x;
//            $z = $z+1;
//        }
//    }

//	public function hello() {
//		echo ("printing hello");
//	}
}
