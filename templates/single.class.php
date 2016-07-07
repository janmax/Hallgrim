<?php

	class autoILIASscript{
	
		function autoILIASscript(){
		
			$this->qType = "SINGLE";
			$this->qTitle = "Auswahl Frage";
			$this->qAuthor = "Vorname Name";
			$this->qNumber = 100;
			$this->qPoints = 10;
		
		}
		
		function exe(){

			$question = "Fragentext...";
			
			$answer = array(array("A", false), array("B", false), array("C", true));
			
			$ml = "Musterl&ouml;sung...";
		
			return array("q" => $question, "a" => $answer, "m" => $ml);
		
		}
	
	}

?>