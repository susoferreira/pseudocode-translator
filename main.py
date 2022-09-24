#!/usr/bin/python3
import os

from block import BlockDescriptor, BlockTranslator

"""
sustituciones:
declaración de variables

empieza con VARIABLES
nome_variable2 : tipo_variable2 --> nome_variable2=0 (no hace falta especificar tipo en python)
constantes: no existe ningún método para crear constantes en python
subrango: --> (?)
enumerado --> diccionario con valores numericos
asignacion : <- --> =

traducciones de operadores:
 y --> and
 o --> or
 MOD --> %
 DIV --> //
 ^ --> **
 = --> ==
 no --> not
 <> --> !=


control de flujo:
    CONTINUAR --> continue
    INTERRUMPIR --> break



 funciones:
 ESCRIBIR(texto) = print(texto)
 LEER(var) -> var =input()

 estructuras condicionales

 SI (LOGICA) ENTONCES
    X
 SI_NO
    Y
 ===========
 if condicion:
    X
 else:
    Y


 SI (LOGICA) ENTONCES
    X
 SI_NO (LOGICA) ENTONCES
    Y
 =========================
 if(logica):
    x
 elif:
    y

CASO <expresión> SEA
    <valor1>: < INSTRUCIÓNS 1>
    <valor2>: < INSTRUCIÓNS 2>
    ..........
    [SI_NO]: < INSTRUCIÓNS SI_NO>
FIN_CASO

======================

 var = expresión
 if var==valor1:
    instruccions 1
 elif var==valor2:
    instruccions 2
 else:
    instruccions_si_no



 DESDE <variable><-<inicio> HASTA <FINAL> PASO <paso> HACER 
    INSTRUCCIONES
 FIN_DESDE
 ======================
    for <variable> in range(<inicio>,<final>,<paso>)

 MIENTRAS <expresión_lóxica> HACER
    <INSTRUCIÓNS>
FIN_MIENTRAS
    while(<expresion_loxiga>):
"""

def __init__():
   text=open("test.txt","r").read()
   parser = Parser(text)
   result=parser.syntax_pass_output()

   with open("result.py","w") as r:
      r.write(result)
   print("el resultado se ha guardado en result.py")
   print("intentando ejecutar automáticamente")
   print("si no se ejecuta automáticamente puedes revisar el archivo result.py manualmente e intentar ejecutarlo")
   print("\n"*3)
   os.system("python ./result.py")

class Parser():


   def __init__(self,code):
      self.code: str=self._remove_empty_lines(code.expandtabs(4))
      self.first_pass_result=""
      self.syntax_pass_result=""
      self.indent_length=0
      self.max_indent_level=0
      self.syntax_pass_count=0
      self.blocks_found=[]
      self.substitutions = {
         "y" : "and",
         "o" : "or",
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
      self._first_pass()
      self._get_max_indent_level()
      for i in range(int(self.max_indent_level)-1):
         self._syntax_pass()

   def _remove_empty_lines(self,t:str):
      return "".join([s for s in t.strip().splitlines(True) if s.strip()])

   #saves the indentation level of each line in a list
   def _get_indents(self):
      indents=[]
      for line in self.code.split("\n"):
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
            s+="# nombre del algoritmo:"+new_line.split(" ")[0]+"\n"
            continue
         for word in self.substitutions:
            if word in new_line:
               new_line=new_line.replace(word,self.substitutions[word])
         s+=new_line+"\n"
      self.first_pass_result=s

   #used for debugging only
   def fist_pass_output(self):
      for line,indents in zip(self.first_pass_result.split("\n"),self._get_indents()):
         print(" "*indents+line)
         
   def _discover_blocks(self,lines,last_block_end):
      block_start=0
      block_end=0
      block_name=""
      block_indent=0
      block_found=False
      syntax_blocks={
         "VARIABLES":"INICIO",
         "SI":"FIN_SI",
         "CASO":"FIN_CASO",
         "MIENTRAS":"FIN_MIENTRAS",
         "DESDE":"FIN_DESDE"
         }
   
      for indent,enumeration in zip(self._get_indents()[last_block_end:],enumerate(lines[last_block_end:])):
         i=enumeration[0]+last_block_end
         line = enumeration[1]
         for block in syntax_blocks:
            if line.split(" ")[0] == block: # first word
               block_indent = indent
               block_start = i
               block_name = block
               print(f"inicio de bloque: {block_name} encontrado en la línea {block_start}")
               block_found=True
               break
         if block_found:
            break
      if not block_found:
         return
      
      for i in range(block_start,len(self._get_indents())):
         indent = self._get_indents()[i]
         line=lines[i]
         if indent != block_indent:
            continue

         #print("encontrada siguiente linea con la misma indentación:",i)
         #print("Este debería ser el final del bloque")

         if line.split(" ")[0] == syntax_blocks[block_name]:
            #print(f"{syntax_blocks[block_name]} encontrado en la línea esperada, bloque encontrado sin errores")
            block_end=i
            return BlockDescriptor(block_start, block_end, block_name, block_indent)
        
         
      raise Exception("ERROR: se esperaba {} pero se encontró {} en la línea {}".format(syntax_blocks[block_name],line.split(" ")[0],i))

   def _syntax_pass_get_lines(self):
       if not self.syntax_pass_result:
          tmp=self.first_pass_result.split("\n")
       else:
          #get results from last pass
          tmp=self.syntax_pass_result.split("\n")
       return tmp

   def _syntax_pass_build_result(self, lines):
      result=""
      last_block_end=-1
      for block in self.blocks_found:
         result+="\n".join(lines[last_block_end+1:block.block_start])+"\n"
         result+=(block.block_translation)
         last_block_end=block.block_end
      result+="\n".join(lines[block.block_end+1:]).expandtabs(4)
       
      return result

   #translates different syntaxes, not recursive, so we have to do a pass for every level of nesting
   def _syntax_pass(self):
      self.syntax_pass_count+=1
      print(f"pase de sintáxis número {self.syntax_pass_count}, se realiza un pase por cada nivel de indentación\n en esta ejecución se esperan {self.syntax_pass_count} pases",)
      result=""
      last_block_end = 0
      while True:
         if not result:
            # deletes the lines that have already been searched in this pass
            lines = self._syntax_pass_get_lines()
         else:
            lines = result.split("\n")
         block_data:BlockDescriptor|None = self._discover_blocks(lines,last_block_end)
         if not block_data:
            break
         block_data.block_translation=BlockTranslator(lines[block_data.block_start:block_data.block_end+1], block_data.block_name).translate()
         self.blocks_found.append(block_data)
         last_block_end=block_data.block_end
   
      result = self._syntax_pass_build_result(lines)
      self.syntax_pass_result =result

   def find_block_indent(self,line_index):
      block_list =self.blocks_found.copy()
      block_list.sort(key=lambda x: x.block_indent,reverse=True) # blocks with more indent have more priority
      result = 0
      indent_list=[] # when multiple blocks are nested their indents are added to get the total indent
      for block in block_list:

         if line_index in range(block.block_start,block.block_start+block.get_line_count()): # if we use block.block_start blocks HAVE to be the same length translated as in the pseudocode
            indent_list.append(block.block_indent)
      result = sum(indent_list)
      if result>3:
         return result
      return 3

   def syntax_pass_output(self):
      result="def main():"

      for i,line in enumerate(self.syntax_pass_result.split("\n")):
         result+=" "*self.find_block_indent(i)+line+"\n"
      result+= "main()"
      return result

__init__()
