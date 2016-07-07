<?php
	class autoILIASscript{
		function autoILIASscript(){
			$this->qType = "FREE";
			$this->qTitle = "Freitext Frage";
			$this->qAuthor = "Vorname Name";
			$this->qNumber = 100;
			$this->qPoints = 10;
		}

		function exe(){
			$question = "Fragentext...";
			$ml = "Musterl&ouml;sung...";
			return array("q" => $question, "m" => $ml);
		}
	}
?>
