import re
from typing import List

class BlockDescriptor():
    def __init__(self,block_start,block_end,block_name,block_indent):
        self.block_start=block_start
        self.block_end=block_end
        self.block_name=block_name
        self.block_indent=block_indent
        self.block_translation:str
        #self.block_translated=False
        
    def get_line_count(self):
        return len(self.block_translation.split("\n"))


class BlockTranslator():
    def __init__(self,block:List[str],block_name):
        self.supported_blocks = {
            "VARIABLES":self.translateVariables,
            "SI":self.translateSi,
            "CASO":self.translateCaso,
            "MIENTRAS":self.translateMientras,
            "DESDE":self.translateDesde,
            }
        self.block=block
        self.block_name :str =block_name
        assert self.block[0].split(" ")[0]== self.block_name


    def translate(self):
        if  self.block_name not in self.supported_blocks:
            print(f"bloque {self.block_name} no soportado, se marcará con un asterisco en el output, no será ejecutable directamente")
            return self.defaultHandler()
        return self.supported_blocks[self.block_name]()

    #marks unsupported blocks with an asterisk in their first word, so they won't be detected again and cause an infinite loop
    def defaultHandler(self):
        first_line = self.block[0].split(" ")
        first_line[0]+="*"
        self.block[0] = " ".join(first_line).lstrip()
        x="\n".join(self.block)+"\n"
        return x
    
    #doesn't support struct and other complex variables for now
    def translateVariables(self):
        result=""
        lines = self.block
        assert lines[0].strip() == "VARIABLES"
        assert lines[-1].strip() =="INICIO"
        result+="#BLOQUE VARIABLES\n"
        for line in lines[1:-1]:
            assert len(line.split(":")) == 2
            expr = line.split(":")
            line =f"{expr[0]} = 0 #tipo:{expr[1]}"
            result+=line+"\n"
        result+="#FIN BLOQUE VARIABLES, INICIO PROGRAMA\n"
        return result
    
    def translateSi(self):
        result=""
        lines=self.block
        assert lines[0].strip().split(" ")[0]== "SI"
        assert lines[-1].strip() =="FIN_SI"

        for line in lines:
            words =line.split(" ")
            if words[0] == "SI":
                words[0]="if"
                result+=" ".join(words)+":\n"
            elif words[0] == "SI_NO":
                words[0] = "else"
                result+=" ".join(words)+":\n"
            elif words[0] =="FIN_SI":
                result+="#fin bloque SI"
                continue
            else:
                result+="\t"+line+"\n"
        return result
    
    """
    CASO <expresión> SEA
        <valor1>: < INSTRUCIÓNS 1>
        <valor2>: < INSTRUCIÓNS 2>
        ..........
        [SI_NO]: < INSTRUCIÓNS SI_NO>
    FIN_CASO
    """
    def translateCaso(self):
        result=""
        lines=self.block
        expr=0
        first__expr_found=False # first expression uses if, next use elif
        assert lines[0].split(" ")[0]== "CASO"
        assert lines[-1].strip() =="FIN_CASO"

        for line in lines:
            words=line.split(" ")
            if words[0] == "CASO":
                expr = line[line.index("CASO")+len("CASO"):line.index("SEA")]
            elif words[0] =="FIN_CASO":
                result+=f"#{line}"
            elif words[0] =="SI_NO":
                words[0]=words[0].lstrip()
                result+="else:\n"
            elif ":" in line:
                if first__expr_found:
                    result+=f"elif {expr} == {words[0]}:"
                else:
                    result+=f"if {expr} == {words[0]}:"
                    first__expr_found=True
                result+=" ".join(words[2:])+"\n"
            else:
                result+="\t"+line+"\n"
        return result
    
    def translateMientras(self):
        result=""
        lines=self.block

        assert lines[0].split(" ")[0]== "MIENTRAS"
        assert lines[-1].strip() =="FIN_MIENTRAS"

        for line in lines:
            words=line.split(" ")
            if words[0] == "MIENTRAS":
                expr = line[line.index("MIENTRAS")+len("MIENTRAS"):line.index("HACER")]
                result+=f"while {expr}:\n"
            elif words[0] == "FIN_MIENTRAS":
                result+="#FIN_MIENTRAS\n"
            else:
                result+="\t"+line+"\n"
        return result
    
    def translateDesde(self):
        result=""
        lines=self.block

        assert lines[0].split(" ")[0]== "DESDE"
        assert lines[-1].strip() =="FIN_DESDE"

        for line in lines:
            words=line.split(" ")
            if words[0]=="DESDE":
                var = line[line.index("DESDE")+len("DESDE"):line.index("HASTA")]
                var_name = var.split("=")[0]
                start = var.split("=")[1]
                if "PASO" in line:
                    end = line[line.index("HASTA")+len("HASTA"):line.index("PASO")]
                    step = line[line.index("PASO")+len("PASO"):line.index("HACER")]
                else:
                    end = words[-1]
                    paso = 1
                
                result+=f"for {var_name} in range({start},{end},{step}):\n"
            elif words[0] == "FIN_DESDE":
                result+="#FIN DESDE\n"
            else:
                result+="\t"+line+"\n"
        return result
