(function(){

	$(document).ready(function(){

        // Enable functionality for nice looking multi-select.
        
		$("#search-tool select").chosen();

		// todo: This needs to be made better!
		var $main_search_input = $("#id_q");
		var $near_prompt_wrap = $("#near-prompt-wrap");
		function check_near_prompt() {
			var text = $main_search_input.val();
			if (text && text.toLowerCase().search(/\snear\s/) > -1) {
                $near_prompt_wrap.html($("#near-prompt-wrap-template").html());
        		var $near_prompt = $("#id_nearprompt");
				$near_prompt_wrap.fadeIn(500);
				if ($near_prompt.val() == "") {
					$near_prompt.val("5");
				}
			} else {
				$near_prompt_wrap.fadeOut(500);
				$near_prompt_wrap.html("");
                
			}
		}
		check_near_prompt();			
		$main_search_input.keyup(check_near_prompt);

        // Enable search help link functionality

        var $search_help = $("#search-help-link");
        var $search_instructions = $(".search-instructions-wrap")
        $search_help.click(function(e) {
            e.preventDefault();
            $search_help.hide();
            $search_instructions.slideDown(1000);
        });
        
        // Limit search input to valid characters

        var $search_entry_fields = $(".search-entry-field");
        $search_entry_fields.keypress(function(e) {
            var code = (e.keyCode ? e.keyCode : e.which);
            var key = String.fromCharCode(code);
            var regex_invalid = /[^A-Za-z0-9\s\*]/;
            if (key.match(regex_invalid)) {
                e.preventDefault();
            }
        });

    });

})();