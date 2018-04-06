<?php

class WhileConstruct{
  public function whileConstruct() {
    $some_array = [];
    $counter = 0;
    while($counter < 100) {
      $some_array[] = $counter;
      $counter++;
    }
    echo("Done with while");
  }
}