<?php
class BasicClass {

	public function hello() {
		echo ("printing hello");
	}

	public function helloConditional() {
		if (1 == 1) {
			echo ("printing hello");
		} else {
			echo ("HI");
		}
	}

	public function switch_test () {
	    switch (contenttype) {
            case 'news':
                echo "News flash!";
                 break;
            case 'interview':
                echo "Interview with Mr. B";
                break;
            case 'presentation':
                echo "An awesome Presentation";
                break;
        }
    }

    public function for_test() {
        for (x = 0; x < 10; x++) {
            y[x] = z+x;
            z = z+1;
        }
    }
}