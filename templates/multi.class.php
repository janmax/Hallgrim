<?php

	class autoILIASscript{
	
		function autoILIASscript(){
		
			$this->qType = "MULTI";
			$this->qTitle = "Mehrfach Auswahl Frage";
			$this->qAuthor = "Vorname Name";
			$this->qNumber = 100;
			$this->qPoints = 10;																	// Gesamtpunktzahl = |Antwortmoeglichkeiten| * $this->qPoints
		
		}
		
		function exe(){

			$question = "Fragentext...";
			
			$answer = array(array("A", true), array("B", false), array("C", true));
			
			$ml = "Musterl&ouml;sung...";
		
			return array("q" => $question, "a" => $answer, "m" => $ml);
		
		}
	
	}

?>