<?php

class MixedConstruct{
  public function mixedConstruct()
  {
    $c = 1;
    while ($c <= 10) {
      if ($c % 2 == 0) {
        echo ("While and True");
        echo ("$c is an even number");
      } else {
        echo ("While and False");
        echo ("$c is an odd number");
      }
      $c++;
    }
    echo("Out of the loop");
  }
}