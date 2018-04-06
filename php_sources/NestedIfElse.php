<?php

class NestedIfElse{
  public function NestedIfElse()
  {
    $x = 1;
    if ($x==0) {
      echo($x . ' is zero');
      if ($y == 0) {
        echo("$y is zero too");
        $y = 20 ;
      }
      $y = 30;
    } else {
      $z = 10;
      $y = 10;
    }
    echo ("Value of y is: $y");
  }
}