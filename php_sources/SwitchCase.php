<?php

class SwitchCase{
  public function switchCase()
  {
    $content_type = "news";
    switch ($content_type) {
      case "news":
        echo "News flash!";
        break;
      case "interview":
        echo "Interview with Mr. B";
        break;
      case "presentation":
        echo "An awesome presentation";
        break;
    }
  }
}