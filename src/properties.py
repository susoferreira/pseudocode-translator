settings = {
    "indent_size" : 4, # probably modified at runtime depending on the file
    "range_inclusive": True
}

substitutions = {
            #"y" : "and", 
            #"o" : "or",
            "MOD" : "%",
            "DIV" : "//",
            "^" : "**",
            "=" : "==",
            "no" : "not",
            "<>" : "!=",
            "<-" :"=",
            "CONTINUAR" : "continue",
            "INTERRUMPIR": "break",
            "ESCRIBIR":"print",
            "//":"#",
            "/*":"\"\"\"",
            "*/":"\"\"\""
        }

syntax_blocks ={
            "HACER":"MIENTRAS",
            "VARIABLES":"INICIO",
            "SI":"FIN_SI",
            "CASO":"FIN_CASO",
            "MIENTRAS":"FIN_MIENTRAS",
            "DESDE":"FIN_DESDE"
            }