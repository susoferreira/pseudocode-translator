from typing import List
from .settings import settings

indent_size=settings["indent_size"]

class BlockDescriptor():
    def __init__(self,block_start,block_end,block_name,block_indent,block_pass):
        self.block_start=block_start
        self.block_end=block_end
        self.block_name=block_name
        self.block_indent=block_indent
        self.block_translation:str
        self.block_pass:int = block_pass #nesting level, used to build result, also probably equivalent to block_indent
        self.block_uid_start = "{" +f" {block_name}-{block_start}-{block_end}_START" +"}"
        self.block_uid_end = "{" +f" {block_name}-{block_start}-{block_end}_END" +"}"
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
        self.stripped_block = self.remove_indents(block)
        self.block_name :str =block_name
        assert self.block[0].lstrip().split(" ")[0]== self.block_name

    #return text found between 2 bigger substrings in a bigger string, meant for use on single lines but should work on any string
    def find_text_between(self,str1,str2,line):
        return line[line.index(str1)+len(str1):line.index(str2)]
    

    # used for easier code parsing, indents are removed and stored, then readded
    def store_indents(self,lines): 
        indents=[]
        for line in lines:
            leading_spaces = len(line) - len(line.lstrip())
            indents.append(leading_spaces)
        return indents
    def remove_indents(self,lines):
        new_lines=[]
        for line in lines:
            new_lines.append(line.lstrip())
        return new_lines
    def re_add_indents(self,indents,text):
        result=""
        lines = text.split("\n")
        for line,indentation in zip(lines,indents):
            result+=" "*indentation+line+"\n"
        return result

    def translate(self):
        if  self.block_name not in self.supported_blocks:
            print(f"bloque {self.block_name} no soportado, se marcará con un asterisco en el output, no será ejecutable directamente")
            return self.defaultHandler()

        indents = self.store_indents(self.block)
        translation = self.supported_blocks[self.block_name]().expandtabs(indent_size)
        return self.re_add_indents(indents, translation)

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
        lines = self.stripped_block
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
        lines=self.stripped_block
        assert lines[0].strip().split(" ")[0]== "SI"
        assert lines[-1].strip() =="FIN_SI"

        
        # we have to make sure to translate the first and last lines of each block only once,
        # because else we might mess with nested blocks translation
        # other keywords dont really matter (it might be possible to add them to first_pass substitution)

        expr = self.find_text_between("SI", "ENTONCES", lines[0])
        result+=f"if {expr}:\n"

        for line in lines[1:-1]: # skip first and last lines as those are handled differently
            words =line.split(" ")                
            if words[0] == "SI_NO":
                words[0] = "else"
                result+="else:\n"
            else:
                result+="\t"+line+"\n"

        result+="#"+lines[-1]+"\n"
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
        lines=self.stripped_block
        expr=0
        first__expr_found=False # first expression uses if, next use elif
        assert lines[0].split(" ")[0]== "CASO"
        assert lines[-1].strip() =="FIN_CASO"
    
        # we have to make sure to translate the first and last lines of each block only once,
        # because else we might mess with nested blocks translation
        # other keywords dont really matter (it might be possible to add them to first_pass substitution)
        expr = self.find_text_between("CASO", "SEA", lines[0])

        for line in lines[1:-1]:  # skip first and last lines as those are handled differently
            words=line.split(" ")

            if words[0] =="SI_NO":
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
                result+="#"+lines[-1]+"\n"
        return result
    
    def translateMientras(self):
        result=""
        lines=self.stripped_block

        assert lines[0].split(" ")[0]== "MIENTRAS"
        assert lines[-1].strip() =="FIN_MIENTRAS"

        # we have to make sure to translate the first and last lines of each block only once,
        # because else we might mess with nested blocks translation
        # other keywords dont really matter (it might be possible to add them to first_pass substitution)
        expr =self.find_text_between("MIENTRAS", "HACER", lines[0])
        result+=f"while {expr}:\n"

        for line in lines[1:-1]:
            words=line.split(" ")
            result+="\t"+line+"\n"

        result+="#FIN_MIENTRAS\n"
        return result
    
    def translateDesde(self):
        result=""
        lines=self.stripped_block

        assert lines[0].split(" ")[0] == "DESDE"
        assert lines[-1].strip() == "FIN_DESDE"

         # we have to make sure to translate the first and last lines of each block only once,
        # because else we might mess with nested blocks translation
        # other keywords dont really matter (it might be possible to add them to first_pass substitution)
        var = self.find_text_between("DESDE", "HASTA", lines[0])
        var_name = var.split("=")[0]
        start = var.split("=")[1]
        if "PASO" in lines[0]:
            end = self.find_text_between("HASTA", "PASO", lines[0])
            step =self.find_text_between("PASO", "HACER", lines[0])
        else:
            end = lines[0].split(" ")[-2]
            step = 1
        
        if settings["range_inclusive"]:
            end+="+1"

        result+=f"for {var_name} in range({start},{end},{step}):\n"


        for line in lines[1:-1]:
            words=line.split(" ")
            result+="\t"+line+"\n"
        result+=f"{var_name.lstrip()}+=1\n "
        result+="#FIN DESDE\n"
        return result
