<?php

	class autoILIASscript{
	
		function autoILIASscript(){
		
			$this->qType = "SELECT";
			$this->qTitle = "Auswahll&uuml;cken Frage";
			$this->qAuthor = "Vorname Name";
			$this->qNumber = 100;
			$this->qPoints = 10;
		
		}
		
		function exe(){

			$question = "Fragentext mit L&uuml;cken zum Ausw&auml;hlen [select][i(2P)]richtig[/i][i(0P)]falsch[/i][/select]...";
			
			$ml = "Musterl&ouml;sung...";
			
			return array("q" => $question, "m" => $ml);
		
		}
	
	}

?>