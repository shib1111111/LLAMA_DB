non_dml_keywords_list = [
            r"\bcreate\b", r"\balter\b", r"\bdrop\b", r"\btruncate\b", r"\brename\b", r"\bgrant\b", r"\brevoke\b",
            r"\bcommit\b", r"\brollback\b", r"\bsavepoint\b", r"\bset\b", r"\bshow\b", r"\buse\b", r"\block\b", r"\bunlock\b", r"\bmerge\b"
        ]

        
restricted_phrases_list= [
            r"\bshow me\b", r"\bgraph\b", r"\bvisualize\b", r"\bpivot table\b", r"\bcrosstab\b"
        ]


non_query_words_list =  [
            r"\bthank you\b", r"\bthanks\b", r"\bsorry\b", r"\bbye\b",
            r"\bgood\b", r"\bhello\b", r"\bhi\b", r"\bhey\b", r"\bexcuse\b",
            r"\bthank\b", r"\bok\b", r"\bokay\b", r"\bsure\b", r"\bno problem\b", r"\bgreat\b",
            r"\bawesome\b", r"\bcool\b", r"\bcheers\b", r"\bcare\b",
            r"\bwelcome\b", r"\bappreciate\b"
        ]
    
abusive_words_list = [
            r"\bfuck\b", r"\bshit\b", r"\basshole\b", r"\bbitch\b", r"\bdamn\b",
            r"\bcunt\b", r"\bdick\b", r"\bpussy\b", r"\bmotherfucker\b", r"\bcocksucker\b",
            r"\bwhore\b", r"\bslut\b", r"\bbastard\b", r"\bprick\b", r"\bdouche\b",
            r"\btwat\b", r"\bwanker\b", r"\bjerk\b", r"\bfaggot\b", r"\bqueer\b",
            r"\bdyke\b", r"\bcock\b", r"\bcrap\b", r"\bbugger\b", r"\bshithead\b",
            r"\bfuckhead\b", r"\bshitface\b", r"\bfuckface\b", r"\bcockface\b",
            r"\bcockhead\b", r"\bbuttfuck\b", r"\bjackass\b", r"\bpiss\b", r"\bpiss off\b",
            r"\bwank\b", r"\bwank off\b", r"\bhell\b", r"\bshite\b", r"\btit\b",
            r"\btits\b", r"\bfuckwit\b", r"\bknobhead\b", r"\bpisshead\b", r"\bshitbag\b",
            r"\bshit-for-brains\b", r"\basswipe\b", r"\bassclown\b", r"\basshat\b",
            r"\bdickweed\b", r"\bdickwad\b", r"\bshitstorm\b", r"\bshitshow\b",
            r"\bfucktard\b", r"\bfuckwit\b", r"\bshitbag\b", r"\bshitheel\b",
            r"\bjerkoff\b", r"\bshitstain\b", r"\bscumbag\b", r"\bscumbucket\b"
        ]
