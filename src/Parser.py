
from .block import BlockDescriptor, BlockTranslator
from .properties import settings
from typing import List
import src.properties as props


class Parser():


    def __init__(self,code):
        self.code: str=code.expandtabs(settings["indent_size"])
        self.first_pass_result="" #supposed to have same number of lines as self.code
        self.first_pass_with_identifiers ="" # supposed to have same number of lines as self.code
        self.indent_length=0
        self.max_indent_level=0
        self.syntax_pass_count=0
        self.result=""
        self.blocks_found:List[BlockDescriptor]=[]
        self.first_substitution = props.first_substitution
        self.second_substitution = props.second_substitution
        self._get_max_indent_level()

    def parse(self):
        self._first_pass()
        for i in range(int(self.max_indent_level)):
            self._find_all_blocks() #first we find ALL blocks and mark then with identifiers in the text so line number does not matter anymore
        
        self.blocks_found.sort(key=lambda block: block.block_indent, reverse=True) # sort from most indent to least indent

        self.result=self.first_pass_with_identifiers
        for block in self.blocks_found:
            #then we translate it and replace it in-text
            #one by one because nesting
            pass
            self._translate_block(block,self.result)
            self.result = self._build_result(self.result,block)
        



    def _remove_empty_lines(self,t:str):
        return "".join([s for s in t.strip().splitlines(True) if s.strip()])

    #saves the indentation level of each line in a list
    def _get_indents(self,lines=None):
        if not lines:
            lines =self.code.split("\n")
        indents=[]
        for line in lines:
            leading_spaces = len(line) - len(line.lstrip())
            indents.append(leading_spaces)
        return indents

    def _get_max_indent_level(self):
        tmp= self._get_indents()
        while 0 in tmp:
            tmp.remove(0)
        self.indent_length =  min(tmp)
        self.max_indent_level=max(tmp)/self.indent_length
        assert self.max_indent_level == int(self.max_indent_level)
        
    # substitutes the terms in self.substitutions with their python equivalents
    def _first_pass(self):
        s=""
        for line in self.code.split("\n"):
            new_line=line.lstrip()
            #special cases
            if new_line.split(" ")[0] == "ALGORITMO":
                s+="# nombre del algoritmo:"+new_line.split(" ")[-1]+"\n"
                continue
            for word in self.first_substitution:
                if word in new_line:
                    new_line=new_line.replace(word,self.first_substitution[word])
            s+=new_line+"\n"
        self.first_pass_result=s[:-1] # [:-1] to eliminate last newline

        s=""
        for line in self.first_pass_result.split("\n"):
            new_line=line.lstrip()
            for word in self.second_substitution:
                if word in new_line:
                    new_line=new_line.replace(word,self.second_substitution[word])
            s+=new_line+"\n"
        self.first_pass_result=s[:-1] # [:-1] to eliminate last newline
        assert len(self.first_pass_result.split("\n")) == len(self.code.split("\n"))


    #used for debugging only
    def fist_pass_output(self):
        for line,indents in zip(self.first_pass_result.split("\n"),self._get_indents()):
            print(" "*indents+line)
            
    def _discover_block(self,lines,last_block_end):
        block_start=0
        block_end=0
        block_name=""
        block_indent=0
        block_found=False
        block_already_found = False
        syntax_blocks=props.syntax_blocks
    
        for indent,enumeration in zip(self._get_indents()[last_block_end:],enumerate(lines[last_block_end:])):
            i=enumeration[0]+last_block_end
            line = enumeration[1]
            for block in syntax_blocks:
                if line.lstrip().split(" ")[0] == block: # first word
                    for found_block in self.blocks_found:
                        if i == found_block.block_start or i==found_block.block_end:
                            block_already_found=True # block has already been found in an earlier pass
                            break
                    if block_already_found:
                        #last_block_end=i-1
                        block_already_found = False
                        break
                    block_indent = indent
                    block_start = i
                    block_name = block
                    block_found=True
                    print(f"inicio de bloque: {block_name} encontrado en la línea {block_start}")
                    break
            if block_found:
                break
        if not block_found:
            return

      
        indents = self._get_indents()
        for i in range(block_start,len(indents)):
            indent = indents[i]
            line=lines[i]
            if indent != block_indent:
                  continue

            #print("encontrada siguiente linea con la misma indentación:",i)
            #print("Este debería ser el final del bloque")

            if line.lstrip().split(" ")[0] == syntax_blocks[block_name]:
                print(f"{syntax_blocks[block_name]} encontrado en la línea esperada, bloque encontrado sin errores")
                block_end=i
                return BlockDescriptor(block_start, block_end, block_name, block_indent,self.syntax_pass_count)
        raise Exception("Error: no se ha encontrado el final del bloque",block_name)

    def replace_text_between(self,originalText, delimeterA, delimterB, replacementText):
        leadingText = originalText.split(delimeterA)[0]
        trailingText = originalText.split(delimterB)[1]

        result= leadingText + replacementText + trailingText
        return result
    def _build_result(self, lines,block):
        result = self.replace_text_between(lines,block.block_uid_start,block.block_uid_end,block.block_translation)
        return result

    #translates different syntaxes, not recursive, so we have to do a pass for every level of nesting
    def _find_all_blocks(self):
        self.syntax_pass_count+=1
        print(f"pase de sintáxis número {self.syntax_pass_count}, se realiza un pase por cada nivel de indentación\n en esta ejecución se esperan {self.max_indent_level} pases",)
        last_block_end = 0
        while True:

            lines= lines = self.first_pass_result.split("\n")
            block_data:BlockDescriptor|None = self._discover_block(lines,last_block_end)
            if not block_data:
                break
            self._add_block_identifiers(block_data)
            self.blocks_found.append(block_data)
            last_block_end=block_data.block_end


    #adds identifiers to the start and end of blocks so they can be found later regardless of indentation changes while translatings
    # maybe not needed if translating all blocks starting from the inside works
    # WIP
    def _add_block_identifiers(self,block:BlockDescriptor):
        lines: list[str] = self.first_pass_with_identifiers.split("\n") if self.first_pass_with_identifiers else self.first_pass_result.split("\n")

        result = ""


        block_with_uuid ="\n"+block.block_uid_start+"\n".join(lines[block.block_start:block.block_end+1]).rstrip()+block.block_uid_end

        result+= "\n".join(lines[0:block.block_start])
        result+= block_with_uuid+"\n"
        result+= "\n".join(lines[block.block_end+1:])

        if result[-1] == "\n" and len(result.split("\n")) == (len(lines)+1): #remove trailing newline to pass assert
            result=result[:-1]
        assert len(result.split("\n")) == len(lines)

        self.first_pass_with_identifiers=result


    def _translate_block(self,block,text):
        block_text = self._find_block_by_identifier(block,text).split("\n")
        block.block_translation=BlockTranslator(block_text,block.block_name).translate()

    def _find_block_by_identifier(self,block:BlockDescriptor,text):
        return text[text.index(block.block_uid_start)+len(block.block_uid_start):text.index(block.block_uid_end)]


    def find_block_indent(self,line_index):
        block_list =self.blocks_found.copy()
        block_list.sort(key=lambda x: x.block_indent,reverse=True) # blocks with more indent have more priority
        result = 0
        for block in block_list:

            if line_index in range(block.block_start,block.block_start+block.get_line_count()): # if we use block.block_start blocks HAVE to be the same length translated as in the pseudocode
                result = block.block_indent
        if result>settings['indent_size']:
            return result
        return settings["indent_size"]

    def syntax_pass_output(self):
        result="def main():\n"

        for i,line in enumerate(self.result.split("\n")):
            result+=" "*self.find_block_indent(i)+line+"\n"
        result+= "main()"
        return result