settings = {
    "indent_size" : 4, # probably modified at runtime depending on the file
    "range_inclusive": True
}

first_substitution = {
            #"y" : "and", 
            #"o" : "or",
            ">=":"{gt}",
            "<=":"{lt}",
            "MOD" : "{mod}",
            "DIV" : "{int_div}",
            "^" : "{pow}",
            "=" : "{eq_comp}",
            "no" : "{not}",
            "<>" : "{neq}",
            "<-" :"{asignation}",
            "CONTINUAR" : "{cont}",
            "INTERRUMPIR": "{break}",
            "ESCRIBIR":"print",
            "//":"#",
            "/*":"\"\"\"",
            "*/":"\"\"\""
        } # not every simbol needs an intermediary tag
second_substitution = {
            #"y" : "and", 
            #"o" : "or",
            "{gt}":">=",
            "{lt}":"<=",
            "{mod}" : "%",
            "{int_div}": "//",
            "{pow}" : "**",
            "{eq_comp}" : "==",
            "{not}" : "not",
            "{neq}" : "!=",
            "{asignation}" :"=",
            "{cont}" : "continue",
            "{break}": "break",

        }




syntax_blocks ={
            "HACER":"MIENTRAS",
            "VARIABLES":"INICIO",
            "SI":"FIN_SI",
            "CASO":"FIN_CASO",
            "MIENTRAS":"FIN_MIENTRAS",
            "DESDE":"FIN_DESDE"
            }