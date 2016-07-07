<?php
	class autoILIASscript{{
		function autoILIASscript(){{
			$this->qType   = "{type}";
			$this->qTitle  = "{title}";
			$this->qAuthor = "{author}";
			$this->qNumber = {number};
			$this->qPoints = {points};
			{gapComment}$this->gapLength = {gapLength};
		}}

		function exe(){{
			$question = "{question}";
			$ml = "{solution}";
			return array("q" => $question, "m" => $ml);
		}}
	}}
?>
