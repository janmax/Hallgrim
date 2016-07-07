<?php

	class autoILIASscript{
	
		function autoILIASscript(){
		
			$this->qType = "NUMERIC";
			$this->qTitle = "Numerische Frage";
			$this->qAuthor = "Vorname Name";
			$this->qNumber = 100;
			$this->qPoints = 10;
			//$this->numericFormatstring = "";
		
		}
		
		function exe(){

			$question = "Fragentext...";
			
			$answer = 42;
			
			$ml = "Musterl&ouml;sung...";
		
			return array("q" => $question, "a" => $answer, "m" => $ml);
		
		}
	
	}

?>