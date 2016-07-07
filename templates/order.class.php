<?php

	class autoILIASscript{
	
		function autoILIASscript(){
		
			$this->qType = "ORDER";
			$this->qTitle = "Anordnungs Frage";
			$this->qAuthor = "Vorname Name";
			$this->qNumber = 100;
			$this->qPoints = 10;
		
		}
		
		function exe(){

			// <span style=\"font-size: x-small;\"><b>Hinweis: </b>GgF. m&uuml;ssen die Terme in der richtigen Reihenfolge durchnummeriert werden.</span>
			$question = "Fragentext...";
			
			$answer = array("A", "B", "C", "D");
			
			$ml = "Musterl&ouml;sung...";
		
			return array("q" => $question, "a" => $answer, "m" => $ml);
		
		}
	
	}

?>